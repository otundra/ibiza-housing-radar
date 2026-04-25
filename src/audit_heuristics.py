"""Heurísticas deterministas del auditor (capa 3a/3b).

Tres comprobaciones sin IA, sin coste de API:

- ``check_cross_source``  — cuántas fuentes independientes documentan el
  mismo binomio actor + palanca. Cuenta dominios distintos en
  ``data/classified.json`` de la semana.
- ``check_verbatim_match`` — ratio de coincidencia entre el
  ``statement_verbatim`` extraído por Haiku y el cuerpo de la URL fuente
  (con caché HTTP local de 30 días en ``.cache/http/``).
- ``check_whitelist``     — encaje del dominio fuente con el actor declarado
  contra ``data/actor_domains.yml`` (refuerza / neutro / debilita).

Estas heurísticas alimentan el bloque ``signals`` del registro de auditoría
(plano §3.2). En el MVP se calculan y almacenan, pero ``compute_tier()``
real (PI10) decide más adelante cómo combinarlas en el badge público; aquí
solo se generan datos.

Plano: DISENO-AUDITOR-MVP.md §4.
"""
from __future__ import annotations

import hashlib
import logging
import re
import time
from difflib import SequenceMatcher
from html.parser import HTMLParser
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

import httpx
import yaml

ROOT = Path(__file__).resolve().parent.parent
CACHE_DIR = ROOT / ".cache" / "http"
CACHE_TTL_DAYS = 30
HTTP_TIMEOUT = 15.0
HTTP_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "es-ES,es;q=0.9,ca;q=0.8,en;q=0.7",
}

VERBATIM_THRESHOLD_BLOCKING = 0.60
VERBATIM_THRESHOLD_GREEN = 0.80
VERBATIM_QUOTE_THRESHOLD = 0.95

log = logging.getLogger("audit_heuristics")


# ---------------------------------------------------------------------------
# Utilidades
# ---------------------------------------------------------------------------

def _root_domain(url: str) -> str:
    """Hostname normalizado: minúsculas, sin ``www.`` ni ``m.``.

    No se acorta a 2 segmentos: ``ibavi.caib.es`` queda intacto para no
    colisionar con ``caib.es``. El refinamiento de subdominios se hace en
    la revisión de la whitelist post-backfill ([D3](DECISIONES.md)).
    """
    parsed = urlparse(url)
    host = (parsed.hostname or "").lower()
    if not host:
        return ""
    for prefix in ("www.", "m."):
        if host.startswith(prefix):
            host = host[len(prefix):]
            break
    return host


def _norm_text(s: Any) -> str:
    return str(s or "").strip().lower()


def load_actor_domains(path: Path | str) -> dict:
    """Carga el YAML de la whitelist V1."""
    return yaml.safe_load(Path(path).read_text(encoding="utf-8")) or {}


# ---------------------------------------------------------------------------
# 1. Cruce de fuentes
# ---------------------------------------------------------------------------

def _actors_match(propuesta_actor: str, news_hint: str) -> bool:
    """Match flexible para nombres de actor.

    Devuelve True si una de las cadenas está contenida en la otra (ignorando
    mayúsculas y espacios extra). Captura variantes como ``Marí`` ⇆
    ``Marí (Vox)``, o ``patronales, sindicatos`` ⇆ ``Consell, patronales,
    sindicatos`` cuando comparten núcleo.
    """
    a = _norm_text(propuesta_actor)
    b = _norm_text(news_hint)
    if not a or not b:
        return False
    return a in b or b in a


def check_cross_source(proposal: dict, news_week: list[dict]) -> dict:
    """Cuántas fuentes independientes documentan la propuesta.

    Filtra ``news_week`` (clasificadas de la semana) por ``is_housing=True``
    y misma ``palanca`` (campo ``lever`` en la clasificación). De esas, las
    que tengan ``proposal_actor_hint`` que case con el actor de la propuesta
    cuentan. Agrupa los resultados por dominio raíz y devuelve el número de
    dominios distintos.

    El dominio de ``url_source`` siempre cuenta (mínimo 1).

    Plano: §4.1.
    """
    palanca = _norm_text(proposal.get("palanca"))
    actor = (proposal.get("actor") or "").strip()
    url_source = proposal.get("url_source") or ""

    matching_urls: list[str] = []
    domains: set[str] = set()

    for n in news_week:
        if not n.get("is_housing"):
            continue
        if _norm_text(n.get("lever")) != palanca:
            continue
        hint = n.get("proposal_actor_hint") or ""
        if not _actors_match(actor, hint):
            continue
        url = n.get("url") or ""
        if not url:
            continue
        d = _root_domain(url)
        if not d:
            continue
        matching_urls.append(url)
        domains.add(d)

    if url_source:
        d = _root_domain(url_source)
        if d:
            domains.add(d)
            if url_source not in matching_urls:
                matching_urls.append(url_source)

    return {
        "n_fuentes_independientes": len(domains),
        "urls": matching_urls,
        "dominios": sorted(domains),
    }


# ---------------------------------------------------------------------------
# 2. Coincidencia textual verbatim
# ---------------------------------------------------------------------------

class _BodyExtractor(HTMLParser):
    """Acumulador mínimo de texto fuera de bloques de navegación.

    Quita ``<script>``, ``<style>``, ``<nav>``, ``<footer>``, ``<header>``,
    ``<aside>``, ``<noscript>``, ``<form>``. No intenta encontrar ``<main>``
    ni ``<article>``: con SequenceMatcher bastará con un cuerpo razonablemente
    limpio.
    """

    SKIP_TAGS = {
        "script", "style", "nav", "footer", "header",
        "aside", "noscript", "form", "iframe", "svg",
    }

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self._skip_depth = 0
        self._chunks: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:  # noqa: ARG002
        if tag in self.SKIP_TAGS:
            self._skip_depth += 1

    def handle_endtag(self, tag: str) -> None:
        if tag in self.SKIP_TAGS and self._skip_depth > 0:
            self._skip_depth -= 1

    def handle_data(self, data: str) -> None:
        if self._skip_depth > 0:
            return
        text = data.strip()
        if text:
            self._chunks.append(text)

    def text(self) -> str:
        return " ".join(self._chunks)


def _cache_path(url: str) -> Path:
    h = hashlib.sha256(url.encode("utf-8")).hexdigest()[:32]
    return CACHE_DIR / f"{h}.html"


def _fetch_with_cache(url: str) -> tuple[str | None, bool]:
    """Devuelve ``(html_text, cache_hit)``. ``html_text`` es ``None`` si falla.

    Caché en ``.cache/http/`` con TTL 30 días. Reintentos: 2 (5xx o red).
    """
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    path = _cache_path(url)
    now = time.time()
    if path.exists():
        age_days = (now - path.stat().st_mtime) / 86400.0
        if age_days < CACHE_TTL_DAYS:
            try:
                return path.read_text(encoding="utf-8", errors="ignore"), True
            except OSError:
                pass

    last_exc: Exception | None = None
    for _ in range(2):
        try:
            with httpx.Client(
                timeout=HTTP_TIMEOUT, follow_redirects=True, headers=HTTP_HEADERS,
            ) as client:
                r = client.get(url)
            if r.status_code >= 400:
                if r.status_code in (401, 403, 405, 429):
                    return None, False
                if 500 <= r.status_code < 600:
                    continue
                return None, False
            text = r.text
            try:
                path.write_text(text, encoding="utf-8")
            except OSError as exc:
                log.warning("no puedo escribir caché %s: %s", path, exc)
            return text, False
        except Exception as exc:  # noqa: BLE001
            last_exc = exc
            continue

    if last_exc is not None:
        log.warning("fetch %s falla tras 2 intentos: %s", url, last_exc)
    return None, False


def _verbatim_coverage(body_text: str, needle: str) -> float:
    """Fracción del verbatim que tiene contraparte en el cuerpo.

    Suma de los matching blocks dividido por longitud del verbatim. Mejor
    señal que ``SequenceMatcher.ratio()`` cuando ``body`` es mucho más
    largo que ``needle`` (que sesga ratio a la baja).
    """
    a = re.sub(r"\s+", " ", body_text.lower())
    b = re.sub(r"\s+", " ", needle.lower())
    if not b:
        return 0.0
    sm = SequenceMatcher(None, a, b, autojunk=False)
    total = sum(block.size for block in sm.get_matching_blocks())
    return min(1.0, total / len(b))


def check_verbatim_match(proposal: dict) -> dict:
    """Coincidencia textual entre ``statement_verbatim`` y la URL fuente.

    Plano: §4.2.
    """
    url = proposal.get("url_source") or ""
    verbatim = (proposal.get("statement_verbatim") or "").strip()
    statement_type = _norm_text(proposal.get("statement_type")) or "reported"

    out: dict[str, Any] = {
        "ratio": None,
        "statement_type": statement_type,
        "threshold_blocking": VERBATIM_THRESHOLD_BLOCKING,
        "threshold_green": VERBATIM_THRESHOLD_GREEN,
        "passed_blocking": None,
        "passed_green": None,
        "html_cache_hit": False,
        "url_ok": None,
        "error": None,
    }

    if not url or not verbatim:
        out["error"] = "missing_url_or_verbatim"
        return out

    html_text, cache_hit = _fetch_with_cache(url)
    out["html_cache_hit"] = cache_hit
    if html_text is None:
        out["error"] = "fetch_failed"
        out["url_ok"] = False
        return out

    out["url_ok"] = True
    parser = _BodyExtractor()
    try:
        parser.feed(html_text)
    except Exception as exc:  # noqa: BLE001
        out["error"] = f"parse_failed:{exc.__class__.__name__}"
        return out

    ratio = _verbatim_coverage(parser.text(), verbatim)
    out["ratio"] = round(ratio, 3)

    threshold_blocking = VERBATIM_THRESHOLD_BLOCKING
    if statement_type == "quote":
        threshold_blocking = VERBATIM_QUOTE_THRESHOLD
        out["threshold_blocking"] = VERBATIM_QUOTE_THRESHOLD
    out["passed_blocking"] = ratio >= threshold_blocking
    out["passed_green"] = ratio >= VERBATIM_THRESHOLD_GREEN

    return out


# ---------------------------------------------------------------------------
# 3. Encaje dominio-actor (whitelist)
# ---------------------------------------------------------------------------

def _domain_in_list(domain: str, listado: set[str] | list[str]) -> bool:
    """True si ``domain`` está en ``listado`` o es subdominio de alguno."""
    if not domain:
        return False
    for d in listado:
        if domain == d or domain.endswith("." + d):
            return True
    return False


def check_whitelist(proposal: dict, actor_domains: dict) -> dict:
    """Encaje del dominio de ``url_source`` con el actor declarado.

    Reglas (plano §4.3):

    - Dominio en ``actors[actor].oficial`` → ``refuerza``.
    - Dominio en ``actors[actor].cobertura_aceptada`` → ``neutro``.
    - Dominio en ``medios_cobertura_aceptada`` → ``neutro``.
    - Actor existe pero ningún caso anterior aplica → ``debilita``.
    - Actor NO existe en el YAML → ``debilita`` + ``whitelist_miss=True``.
    """
    actor = (proposal.get("actor") or "").strip()
    url = proposal.get("url_source") or ""
    domain = _root_domain(url)

    out = {
        "match": "debilita",
        "domain": domain,
        "known_actor": False,
        "whitelist_miss": True,
    }

    if not actor or not domain:
        return out

    actors = actor_domains.get("actors") or {}
    medios = set(actor_domains.get("medios_cobertura_aceptada") or [])

    actor_record = actors.get(actor)
    if actor_record is None:
        actor_lower = actor.lower()
        for k, v in actors.items():
            if k.strip().lower() == actor_lower:
                actor_record = v
                break

    if actor_record is None:
        if _domain_in_list(domain, medios):
            out["match"] = "neutro"
        return out

    out["known_actor"] = True
    out["whitelist_miss"] = False

    oficial = set(actor_record.get("oficial") or [])
    cobertura = set(actor_record.get("cobertura_aceptada") or [])

    if _domain_in_list(domain, oficial):
        out["match"] = "refuerza"
        return out
    if _domain_in_list(domain, cobertura):
        out["match"] = "neutro"
        return out
    if _domain_in_list(domain, medios):
        out["match"] = "neutro"
        return out

    return out


# ---------------------------------------------------------------------------
# Orquestador
# ---------------------------------------------------------------------------

def run_heuristics(
    proposal: dict,
    news_week: list[dict],
    actor_domains: dict,
) -> dict:
    """Lanza las 3 heurísticas. Devuelve el bloque ``layers.heuristics``."""
    return {
        "cross_source": check_cross_source(proposal, news_week),
        "verbatim_match": check_verbatim_match(proposal),
        "whitelist": check_whitelist(proposal, actor_domains),
    }
