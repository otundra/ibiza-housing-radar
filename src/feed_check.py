"""Monitor diario de salud de fuentes RSS + búsqueda automática de URL nueva.

Complementa `src/sources_health.py`, que opera dentro del ciclo semanal del
pipeline y detecta tarde. Este módulo se ejecuta en un workflow separado
(diario) y solo hace dos cosas:

1. Para cada feed de `sources.yaml`, comprobar disponibilidad técnica:
   HTTP 2xx + XML parseable + ≥1 entrada + última entrada reciente (≤60 días).
2. Para cada feed nativo caído, intentar descubrir una URL alternativa
   inspeccionando el sitio (link rel=alternate, rutas comunes, página índice).

Nunca reemplaza URLs por su cuenta: si descubre candidatos válidos los
propone por Telegram para revisión manual. La regla 5 del proyecto
("una mirada antes de añadir") y `feedback_esperar_ok_antes_de_editar`
exigen OK explícito del editor antes de tocar `sources.yaml`.

Sin coste IA: usa httpx + feedparser + heurísticas locales. Coste por
ejecución: cero euros (ancho de banda despreciable).

Uso:
    python -m src.feed_check          # ejecución diaria desde Actions
    python -m src.feed_check --dry    # local, no manda Telegram aunque haya secrets
"""
from __future__ import annotations

import argparse
import logging
import os
import re
import sys
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from pathlib import Path
from time import mktime
from typing import Any, Final
from urllib.parse import urljoin, urlparse

import feedparser
import httpx
import yaml

log = logging.getLogger("feed_check")

ROOT = Path(__file__).resolve().parent.parent
SOURCES_FILE = ROOT / "src" / "sources.yaml"

HTTP_TIMEOUT_S: Final[float] = 15.0
USER_AGENT: Final[str] = (
    "Mozilla/5.0 (compatible; IbizaHousingRadarBot/1.0; +https://otundra.github.io/ibiza-housing-radar/)"
)
STALE_DAYS: Final[int] = 60

# Rutas comunes de feed que probamos cuando el sitio no declara link rel=alternate
COMMON_FEED_PATHS: Final[tuple[str, ...]] = (
    "/feed/", "/feed", "/rss/", "/rss",
    "/feed.rss", "/rss.xml", "/feed.xml",
    "/index.xml", "/atom.xml",
)

# Páginas índice donde el sitio suele listar todos sus feeds
COMMON_INDEX_PAGES: Final[tuple[str, ...]] = (
    "/feed.html", "/rss.html", "/feeds.html", "/feeds/",
)

# Cuántos candidatos como máximo proponemos por feed caído (más es ruido)
MAX_CANDIDATES_PER_FEED: Final[int] = 3

# Cuántos enlaces de una página índice validamos como máximo. Las páginas
# índice de Prensa Ibérica tienen ~250 feeds; validarlos todos sería 250
# requests HTTP por feed caído. Validamos solo los top N tras ordenar por
# match de nombre.
MAX_INDEX_LINKS_TO_VALIDATE: Final[int] = 12


@dataclass
class CheckResult:
    """Resultado del chequeo técnico de un feed."""

    name: str
    url: str
    kind: str
    status: str  # ok | stale | empty | malformed | http_error | network_error
    http_code: int | None = None
    entries: int = 0
    last_entry_age_days: int | None = None
    detail: str = ""

    @property
    def is_down(self) -> bool:
        return self.status in {"empty", "malformed", "http_error", "network_error"}

    @property
    def needs_attention(self) -> bool:
        return self.status != "ok"


@dataclass
class Candidate:
    """URL candidata descubierta automáticamente, ya validada."""

    url: str
    title: str
    entries: int
    last_entry_age_days: int | None
    discovered_via: str  # link_alternate | common_path | index_page

    def matches_original_name(self, original_name: str) -> bool:
        """Heurística simple: comparte palabras significativas con el nombre original."""
        normalized = re.sub(r"[^a-z0-9 ]", " ", self.title.lower()).split()
        original_words = re.sub(r"[^a-z0-9 ]", " ", original_name.lower()).split()
        # Palabras de >3 letras que sean del nombre original
        significant = {w for w in original_words if len(w) > 3}
        return any(w in normalized for w in significant)


@dataclass
class DiscoveryResult:
    """Resultado del proceso de descubrimiento para un feed caído."""

    feed_name: str
    original_url: str
    candidates: list[Candidate] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)


def load_sources() -> dict[str, Any]:
    return yaml.safe_load(SOURCES_FILE.read_text())


def _http_get(client: httpx.Client, url: str) -> httpx.Response | None:
    """GET con timeout y headers humanos. Devuelve None si red falla."""
    try:
        return client.get(url, follow_redirects=True, timeout=HTTP_TIMEOUT_S)
    except (httpx.RequestError, httpx.TimeoutException) as exc:
        log.warning("HTTP error %s: %s", url, exc)
        return None


def _parse_entry_age_days(parsed: feedparser.FeedParserDict) -> int | None:
    """Edad en días de la entrada más reciente, o None si no se puede calcular."""
    if not parsed.entries:
        return None
    most_recent_ts: float | None = None
    for entry in parsed.entries:
        for field_name in ("published_parsed", "updated_parsed"):
            ts = entry.get(field_name)
            if ts:
                try:
                    epoch = mktime(ts)
                except (TypeError, OverflowError, ValueError):
                    continue
                if most_recent_ts is None or epoch > most_recent_ts:
                    most_recent_ts = epoch
                break
    if most_recent_ts is None:
        return None
    age = datetime.now(timezone.utc) - datetime.fromtimestamp(most_recent_ts, tz=timezone.utc)
    return age.days


def check_feed(client: httpx.Client, feed_cfg: dict[str, str]) -> CheckResult:
    """Devuelve el estado técnico de un feed."""
    name = feed_cfg["name"]
    url = feed_cfg["url"]
    kind = feed_cfg.get("kind", "native")
    result = CheckResult(name=name, url=url, kind=kind, status="ok")

    resp = _http_get(client, url)
    if resp is None:
        result.status = "network_error"
        result.detail = "timeout o error de red"
        return result

    result.http_code = resp.status_code
    if resp.status_code >= 400:
        result.status = "http_error"
        result.detail = f"HTTP {resp.status_code}"
        return result

    parsed = feedparser.parse(resp.content)
    if parsed.bozo and not parsed.entries:
        result.status = "malformed"
        exc = getattr(parsed, "bozo_exception", "bozo")
        result.detail = str(exc)[:200]
        return result

    result.entries = len(parsed.entries)
    if result.entries == 0:
        result.status = "empty"
        result.detail = "feed parsea pero sin entradas"
        return result

    age = _parse_entry_age_days(parsed)
    result.last_entry_age_days = age
    if age is not None and age > STALE_DAYS:
        result.status = "stale"
        result.detail = f"última entrada hace {age} días (umbral {STALE_DAYS})"

    return result


def _extract_alternate_feeds(html: str, base_url: str) -> list[str]:
    """Extrae URLs de <link rel="alternate" type="application/(rss|atom)+xml">."""
    pattern = re.compile(
        r'<link[^>]*rel=["\']alternate["\'][^>]*type=["\']application/(?:rss|atom)\+xml["\'][^>]*href=["\']([^"\']+)["\']',
        re.IGNORECASE,
    )
    pattern_swapped = re.compile(
        r'<link[^>]*type=["\']application/(?:rss|atom)\+xml["\'][^>]*href=["\']([^"\']+)["\']',
        re.IGNORECASE,
    )
    urls: list[str] = []
    for m in pattern.finditer(html):
        urls.append(urljoin(base_url, m.group(1)))
    for m in pattern_swapped.finditer(html):
        u = urljoin(base_url, m.group(1))
        if u not in urls:
            urls.append(u)
    return urls


def _extract_feed_links_from_html(html: str, base_url: str) -> list[tuple[str, str]]:
    """Saca (texto, url) de enlaces a posibles feeds dentro de un HTML índice.

    Útil para parsear páginas tipo /feed.html, /rss.html...

    Cubre tres patrones reales encontrados en sitios de prensa española:
    - Enlaces directos con href acabado en .rss/.xml (Periódico de Ibiza).
    - Tabla con título en celda separada (rss_body_title) + enlace con icono
      (Prensa Ibérica: Diario de Ibiza, Diari de Girona, etc.).
    - URLs tipo /rss/section/N o /rss/microsite/N sin extensión explícita.
    """
    out: list[tuple[str, str]] = []

    # 1. Enlaces directos con extensión .rss/.xml en href + texto en el anchor
    pattern_ext = re.compile(
        r'<a[^>]*href=["\']([^"\']*\.(?:rss|xml))["\'][^>]*>(.*?)</a>',
        re.DOTALL | re.IGNORECASE,
    )
    for m in pattern_ext.finditer(html):
        href = urljoin(base_url, m.group(1))
        text = re.sub(r"<[^>]+>", "", m.group(2)).strip()
        text = re.sub(r"\s+", " ", text)
        out.append((text, href))

    # 2. Patrón tabla Prensa Ibérica: una celda con clase que contiene
    # "title" y luego, en celdas hermanas, un <a href="..."> con icono.
    # El doble guion bajo (rss__body__title) es habitual en este sitio.
    pattern_table = re.compile(
        r'class=["\'][^"\']*rss[_-]+body[_-]+title[^"\']*["\'][^>]*>'
        r'(?:\s*<[^>]+>)*\s*([^<]+?)\s*</td>'
        r'(.{0,1500}?)'  # Misma fila, lo siguiente está cerca
        r'href=["\']([^"\']+(?:\.(?:rss|xml)|/section/\d+|/microsite/\d+)[^"\']*)["\']',
        re.DOTALL | re.IGNORECASE,
    )
    for m in pattern_table.finditer(html):
        text = m.group(1).strip()
        href = urljoin(base_url, m.group(3))
        out.append((text, href))

    # 3. Cualquier enlace cuyo href contenga /section/N o /microsite/N (Prensa
    # Ibérica de fallback) — texto sacado del anchor aunque sea solo un icono.
    pattern_section = re.compile(
        r'<a[^>]*href=["\']([^"\']*(?:/section/\d+|/microsite/\d+)[^"\']*)["\'][^>]*>(.*?)</a>',
        re.DOTALL | re.IGNORECASE,
    )
    for m in pattern_section.finditer(html):
        href = urljoin(base_url, m.group(1))
        text = re.sub(r"<[^>]+>", "", m.group(2)).strip()
        text = re.sub(r"\s+", " ", text)
        out.append((text, href))

    return out


def _validate_candidate(client: httpx.Client, url: str, via: str) -> Candidate | None:
    """Comprueba que la URL devuelve un feed válido con al menos 1 entrada."""
    resp = _http_get(client, url)
    if resp is None or resp.status_code >= 400:
        return None
    parsed = feedparser.parse(resp.content)
    if parsed.bozo and not parsed.entries:
        return None
    if not parsed.entries:
        return None
    title = (parsed.feed.get("title") or "").strip() or url
    age = _parse_entry_age_days(parsed)
    return Candidate(
        url=url,
        title=title,
        entries=len(parsed.entries),
        last_entry_age_days=age,
        discovered_via=via,
    )


def _section_keywords(feed_name: str) -> set[str]:
    """Saca las palabras significativas de la *sección* del feed.

    Convención en sources.yaml: "Medio · Sección" (o "Medio · Sección Subsección").
    La sección (lo que va tras el "·") es lo distintivo. Si no hay "·", usamos
    todo el nombre. Devuelve palabras de >3 letras normalizadas.
    """
    if "·" in feed_name:
        section = feed_name.split("·", 1)[1]
    else:
        section = feed_name
    words = re.sub(r"[^a-z0-9 ]", " ", section.lower()).split()
    return {w for w in words if len(w) > 3}


_SEPARATOR_RE: Final[re.Pattern[str]] = re.compile(r"\s*[:·—–\-]\s+")


def _title_section_part(title: str) -> str:
    """Devuelve la parte 'sección' del título de un feed.

    Convención común en feeds: `"Medio: Sección"` o `"Medio — Sección"`.
    Si hay separador, lo que va después es la sección y suele ser lo
    distintivo. Si no hay separador, el título entero se considera "general"
    (feed raíz del medio).
    """
    parts = _SEPARATOR_RE.split(title, maxsplit=1)
    if len(parts) == 2 and parts[1].strip():
        return parts[1]
    return ""


def _name_match_score(text: str, feed_name: str) -> int:
    """Score por coincidencia de palabras de la sección original con el título.

    Mejora la calidad del ranking de candidatos: prioriza títulos que
    contengan la palabra de la sección en su parte específica (tras un
    separador), no solo en el prefijo del medio.
    """
    section_kw = _section_keywords(feed_name)
    full_text_words = set(re.sub(r"[^a-z0-9 ]", " ", text.lower()).split())
    base = sum(1 for w in section_kw if w in full_text_words)

    section_part = _title_section_part(text)
    if not section_part:
        # Penalización suave a feeds "generales" (sin separador en el título).
        # No es descalificación: a veces el feed general es la única alternativa.
        return base - 1

    section_text_words = set(re.sub(r"[^a-z0-9 ]", " ", section_part.lower()).split())
    bonus = sum(2 for w in section_kw if w in section_text_words)
    return base + bonus


def _rank_candidates(candidates: list[Candidate], feed_name: str) -> list[Candidate]:
    """Ordena candidatos: primero por match de nombre, luego por frescura, luego por entradas."""
    def key(c: Candidate) -> tuple[int, int, int]:
        match = _name_match_score(c.title, feed_name)
        # Frescura invertida: menos días = mejor; None va al final
        freshness = -c.last_entry_age_days if c.last_entry_age_days is not None else -10_000
        return (match, freshness, c.entries)
    return sorted(candidates, key=key, reverse=True)


def discover_alternative(
    client: httpx.Client, feed_name: str, original_url: str
) -> DiscoveryResult:
    """Intenta encontrar una URL alternativa para un feed caído.

    Tres estrategias acumulativas (no en cascada): recogemos candidatos
    validados de todas y al final los ordenamos por coincidencia con el
    nombre original, frescura y volumen. Devolvemos los mejores. La
    responsabilidad final de aceptar un candidato es del editor.
    """
    result = DiscoveryResult(feed_name=feed_name, original_url=original_url)
    parsed_url = urlparse(original_url)
    if not parsed_url.netloc:
        result.notes.append("URL original sin host; no hay dónde buscar.")
        return result
    home_url = f"{parsed_url.scheme}://{parsed_url.netloc}/"

    seen_urls: set[str] = {original_url}
    all_candidates: list[Candidate] = []

    # 1. Home + <link rel="alternate">
    home_resp = _http_get(client, home_url)
    if home_resp is not None and home_resp.status_code < 400:
        for candidate_url in _extract_alternate_feeds(home_resp.text, home_url):
            if candidate_url in seen_urls:
                continue
            seen_urls.add(candidate_url)
            cand = _validate_candidate(client, candidate_url, via="link_alternate")
            if cand:
                all_candidates.append(cand)
    else:
        result.notes.append(f"No se pudo leer la home ({home_url}).")

    # 2. Rutas comunes
    for path in COMMON_FEED_PATHS:
        candidate_url = urljoin(home_url, path)
        if candidate_url in seen_urls:
            continue
        seen_urls.add(candidate_url)
        cand = _validate_candidate(client, candidate_url, via="common_path")
        if cand:
            all_candidates.append(cand)

    # 3. Páginas índice (/feed.html, /rss.html, etc.)
    # Validamos solo los enlaces que mejor coincidan con el nombre original,
    # para no hacer cientos de HTTP requests cuando el sitio tiene muchas
    # secciones (Prensa Ibérica publica ~250 feeds por diario).
    for index_path in COMMON_INDEX_PAGES:
        index_url = urljoin(home_url, index_path)
        index_resp = _http_get(client, index_url)
        if index_resp is None or index_resp.status_code >= 400:
            continue
        links = _extract_feed_links_from_html(index_resp.text, index_url)
        if not links:
            continue

        # Orden descendente por match con el nombre original
        ranked = sorted(
            links,
            key=lambda item: _name_match_score(item[0], feed_name),
            reverse=True,
        )
        for text, candidate_url in ranked[:MAX_INDEX_LINKS_TO_VALIDATE]:
            if candidate_url in seen_urls:
                continue
            seen_urls.add(candidate_url)
            cand = _validate_candidate(client, candidate_url, via="index_page")
            if cand:
                cand.title = cand.title or text
                all_candidates.append(cand)

    result.candidates = _rank_candidates(all_candidates, feed_name)[:MAX_CANDIDATES_PER_FEED]

    if not result.candidates:
        result.notes.append(
            "Ninguna estrategia automática encontró un feed alternativo válido."
        )
    return result


def format_telegram_report(
    checks: list[CheckResult],
    discoveries: list[DiscoveryResult],
) -> str | None:
    """Construye el cuerpo del mensaje de Telegram. None si no hay nada que reportar."""
    problems = [c for c in checks if c.needs_attention]
    if not problems:
        return None

    lines: list[str] = ["Salud diaria de fuentes RSS — incidencias:"]
    for c in problems:
        icon = "❌" if c.is_down else "⏸"
        detail = c.detail or "(sin detalle)"
        lines.append(f"{icon} {c.name}")
        lines.append(f"    estado: {c.status} · {detail}")

    if discoveries:
        lines.append("")
        lines.append("URLs alternativas encontradas automáticamente:")
        for d in discoveries:
            if d.candidates:
                lines.append(f"\n→ {d.feed_name}")
                for i, cand in enumerate(d.candidates, 1):
                    age = (
                        f"última entrada hace {cand.last_entry_age_days}d"
                        if cand.last_entry_age_days is not None
                        else "sin fecha"
                    )
                    lines.append(
                        f"  {i}. {cand.url}\n"
                        f"     título: {cand.title[:60]}\n"
                        f"     {cand.entries} entradas · {age} · vía {cand.discovered_via}"
                    )
            else:
                lines.append(f"\n→ {d.feed_name}: sin alternativa automática.")
                for note in d.notes:
                    lines.append(f"     {note}")

    lines.append("")
    lines.append(
        "Decide a mano qué hacer: edita `src/sources.yaml` con la URL que prefieras "
        "(o ignora si el sitio está caído puntualmente). Sin acción, este aviso vuelve mañana."
    )
    return "\n".join(lines)


def run() -> int:
    cfg = load_sources()
    feeds = cfg["feeds"]
    log.info("Comprobando %d feeds...", len(feeds))

    checks: list[CheckResult] = []
    headers = {"User-Agent": USER_AGENT, "Accept": "application/rss+xml, application/atom+xml, application/xml, text/xml, */*"}
    with httpx.Client(headers=headers) as client:
        for feed_cfg in feeds:
            r = check_feed(client, feed_cfg)
            checks.append(r)
            log.info(
                "%-50s status=%s code=%s entries=%d age=%s",
                r.name, r.status, r.http_code, r.entries, r.last_entry_age_days,
            )

        # Descubrimiento solo para nativos que están caídos (no stale)
        discoveries: list[DiscoveryResult] = []
        for r in checks:
            if r.kind != "native" or not r.is_down:
                continue
            log.info("→ buscando alternativa para %s...", r.name)
            d = discover_alternative(client, r.name, r.url)
            discoveries.append(d)
            for c in d.candidates:
                log.info("   candidato: %s (vía %s, %d entradas)",
                         c.url, c.discovered_via, c.entries)
            if not d.candidates:
                for note in d.notes:
                    log.info("   %s", note)

    report = format_telegram_report(checks, discoveries)
    if report is None:
        log.info("Todos los feeds OK. Sin alertas.")
        return 0

    log.warning("Hay incidencias:\n%s", report)
    return _send_or_skip(report)


def _send_or_skip(message: str) -> int:
    """Manda por Telegram si hay secrets configurados. Si no, solo loguea."""
    if os.environ.get("FEED_CHECK_DRY", "").lower() in {"1", "true", "yes"}:
        log.info("DRY mode: no envío Telegram.")
        return 0
    try:
        from src.notify import notify
    except Exception as exc:  # noqa: BLE001
        log.warning("No pude importar notify (%s); skip Telegram.", exc)
        return 0
    delivered = notify(message, level="warning")
    return 0 if delivered else 0  # nunca rompemos el workflow


def main() -> int:
    ap = argparse.ArgumentParser(description="Monitor diario de salud de feeds RSS.")
    ap.add_argument("--dry", action="store_true",
                    help="No manda Telegram aunque haya secrets (test local).")
    args = ap.parse_args()
    if args.dry:
        os.environ["FEED_CHECK_DRY"] = "1"
    logging.basicConfig(level=logging.INFO, format="[%(levelname)s %(name)s] %(message)s")
    return run()


if __name__ == "__main__":
    sys.exit(main())
