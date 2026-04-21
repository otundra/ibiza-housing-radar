"""Verificación pre-publicación.

Comprobaciones (bloqueantes salvo que se indique):
1. URLs del markdown devuelven HTTP 200.
2. Actores citados en la edición aparecen en extracted.json (trazabilidad).
3. Verbos prohibidos no aparecen en el cuerpo editorial (cero inferencia).
4. Frontmatter mínimo correcto.

Si hay fallo bloqueante: `main()` devuelve exit 1, notifica por Telegram/issue,
y el orquestador NO publica.
"""
from __future__ import annotations

import argparse
import json
import logging
import os
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import httpx

log = logging.getLogger("verify")

ROOT = Path(__file__).resolve().parent.parent
EXTRACTED_FILE = ROOT / "data" / "extracted.json"

# Verbos prohibidos — cualquier coincidencia en el cuerpo editorial bloquea.
# Separamos por espacios para evitar falsos positivos dentro de palabras.
VERBOS_PROHIBIDOS = [
    "debería", "deberían",
    "convendría", "convendrían",
    "sería oportuno",
    "hace falta",
    "urge ",
    "proponemos",
    "habría que",
    "toca ",
    "corresponde ",
    "es necesario",
    "se debe ",
    "hay que ",
]

# Regex para extraer URLs de markdown (enlaces [texto](url) y autolinks <url>)
URL_PATTERN = re.compile(r"\[[^\]]*\]\((https?://[^\s)]+)\)|<(https?://[^\s>]+)>")
HTTP_TIMEOUT = 10.0

# User-Agent realista. Muchos medios (Cadena SER, El País, La Vanguardia…)
# rechazan HEAD/GET desde agentes minimalistas o "python-httpx" con 403.
# No intentamos engañar: la URL es pública y solo estamos comprobando que
# existe. Un UA de navegador estándar es lo que pasa por cualquier proxy.
HTTP_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "es-ES,es;q=0.9,ca;q=0.8,en;q=0.7",
}

# Códigos que consideramos "URL viva pero inaccesible para bots". No bloquean;
# solo generan soft_warning. El editor sabe que la URL es válida y el lector
# humano la abrirá sin problema.
SOFT_FAIL_CODES = {401, 403, 405, 429}
BLOCKING_FAIL_CODES = {404, 410}


@dataclass
class VerificationReport:
    urls_checked: int = 0
    urls_failed: list[dict] = field(default_factory=list)
    actors_checked: int = 0
    actors_untraceable: list[str] = field(default_factory=list)
    forbidden_verbs_found: list[dict] = field(default_factory=list)
    frontmatter_issues: list[str] = field(default_factory=list)
    blocking_failures: list[str] = field(default_factory=list)
    soft_warnings: list[str] = field(default_factory=list)

    def ok(self) -> bool:
        return not self.blocking_failures

    def summary(self) -> str:
        return (
            f"URLs: {self.urls_checked} chequeadas, {len(self.urls_failed)} fallos. "
            f"Actores: {self.actors_checked}, {len(self.actors_untraceable)} sin traza. "
            f"Verbos prohibidos: {len(self.forbidden_verbs_found)}. "
            f"Frontmatter: {len(self.frontmatter_issues)} incidencias. "
            f"Bloqueantes: {len(self.blocking_failures)}. "
            f"Avisos: {len(self.soft_warnings)}."
        )


# ---------------------------------------------------------------------------
# Parser del markdown de la edición
# ---------------------------------------------------------------------------

def split_frontmatter(md: str) -> tuple[dict, str]:
    """Separa el frontmatter YAML del cuerpo."""
    if not md.startswith("---"):
        return {}, md
    try:
        end = md.index("\n---", 3)
    except ValueError:
        return {}, md
    fm_raw = md[3:end].strip()
    body = md[end + 4:].lstrip("\n")
    # Parse YAML minimalista (clave: valor por línea)
    fm: dict = {}
    for line in fm_raw.splitlines():
        line = line.rstrip()
        if not line or line.startswith("#"):
            continue
        if ":" not in line:
            continue
        k, v = line.split(":", 1)
        k = k.strip()
        v = v.strip().strip('"').strip("'")
        fm[k] = v
    return fm, body


def extract_urls(body: str) -> list[str]:
    urls: list[str] = []
    for m in URL_PATTERN.finditer(body):
        url = m.group(1) or m.group(2)
        if url and url not in urls:
            urls.append(url)
    return urls


def extract_cited_actors(body: str) -> list[str]:
    """Heurística mínima: busca nombres en cabeceras de propuestas ('**Actor:**')."""
    pattern = re.compile(r"\*\*Actor(?:es)?(?: que la propone)?:\*\*\s*(.+)")
    names: list[str] = []
    for m in pattern.finditer(body):
        actor = m.group(1).strip()
        # Quitar enlaces markdown si los hay
        actor = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", actor)
        names.append(actor)
    return names


# ---------------------------------------------------------------------------
# Checks
# ---------------------------------------------------------------------------

def check_urls(urls: list[str]) -> tuple[int, list[dict], list[dict]]:
    """Devuelve (total_checked, blocking_failures, soft_warnings).

    - 2xx/3xx: OK.
    - 401/403/405/429: URL viva pero bloquea bots. Soft warning.
    - 404/410: URL rota real. Bloqueante.
    - 5xx o excepción de red: Soft warning (no culpa nuestra).
    - Otros 4xx: Bloqueante por defecto (comportamiento raro que merece revisión).
    """
    blocking: list[dict] = []
    soft: list[dict] = []
    with httpx.Client(timeout=HTTP_TIMEOUT, follow_redirects=True, headers=HTTP_HEADERS) as client:
        for url in urls:
            status: int | None = None
            error: str | None = None
            try:
                r = client.head(url)
                status = r.status_code
                if status >= 400:
                    r = client.get(url)
                    status = r.status_code
            except Exception as exc:  # noqa: BLE001
                error = str(exc)

            if error:
                soft.append({"url": url, "error": error})
            elif status is None or status < 400:
                pass  # OK
            elif status in SOFT_FAIL_CODES:
                soft.append({"url": url, "status": status, "reason": "bot-blocked or rate-limited (URL viva)"})
            elif status in BLOCKING_FAIL_CODES:
                blocking.append({"url": url, "status": status})
            elif status >= 500:
                soft.append({"url": url, "status": status, "reason": "server error"})
            else:
                blocking.append({"url": url, "status": status})
    return len(urls), blocking, soft


def check_actor_traceability(actors: list[str], extracted: list[dict]) -> list[str]:
    """Devuelve los actores que NO aparecen en ningún extract de la edición."""
    known: set[str] = set()
    for item in extracted:
        for prop in item.get("proposals", []):
            actor = (prop.get("actor") or "").strip()
            if actor:
                known.add(actor)
                # Para coaliciones, añade también cada firmante suelto
                for part in re.split(r"[,\s]+y\s+|\s*,\s*", actor):
                    part = part.strip()
                    if part:
                        known.add(part)
            for sup in prop.get("supporters_cited", []) or []:
                known.add(sup.strip())

    untraceable: list[str] = []
    for a in actors:
        a = a.strip()
        if not a:
            continue
        # Match flexible: si "a" aparece contenido en algún actor conocido (o viceversa)
        matched = any(
            a.lower() in k.lower() or k.lower() in a.lower()
            for k in known
        )
        if not matched:
            untraceable.append(a)
    return untraceable


def check_forbidden_verbs(body: str) -> list[dict]:
    # Quitar el frontmatter y las URLs (para no levantar falsos positivos)
    clean = re.sub(r"https?://\S+", " ", body)
    findings: list[dict] = []
    lower = clean.lower()
    for verb in VERBOS_PROHIBIDOS:
        v = verb.lower()
        if v in lower:
            # Context extraction
            idx = lower.find(v)
            ctx_start = max(0, idx - 40)
            ctx_end = min(len(clean), idx + len(v) + 40)
            findings.append({
                "verb": verb.strip(),
                "context": clean[ctx_start:ctx_end].replace("\n", " "),
            })
    return findings


def check_frontmatter(fm: dict) -> list[str]:
    required = ["layout", "title", "week", "date", "permalink"]
    issues = [f"falta campo requerido: {k}" for k in required if k not in fm]
    return issues


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def verify(md_path: Path, extracted_path: Path = EXTRACTED_FILE) -> VerificationReport:
    rep = VerificationReport()

    if not md_path.exists():
        rep.blocking_failures.append(f"No existe el markdown: {md_path}")
        return rep

    md = md_path.read_text()
    fm, body = split_frontmatter(md)

    # 1. Frontmatter
    for issue in check_frontmatter(fm):
        rep.frontmatter_issues.append(issue)
        rep.blocking_failures.append(f"frontmatter: {issue}")

    # 2. URLs
    urls = extract_urls(body)
    n, blocking, soft = check_urls(urls)
    rep.urls_checked = n
    rep.urls_failed = blocking
    for f in blocking:
        rep.blocking_failures.append(f"URL rota (bloqueante): {f}")
    for s in soft:
        rep.soft_warnings.append(f"URL con aviso (no bloqueante): {s}")

    # 3. Trazabilidad de actores
    extracted = []
    if extracted_path.exists():
        extracted = json.loads(extracted_path.read_text())
    actors = extract_cited_actors(body)
    rep.actors_checked = len(actors)
    untraceable = check_actor_traceability(actors, extracted)
    rep.actors_untraceable = untraceable
    for a in untraceable:
        rep.blocking_failures.append(f"Actor sin traza en extracted.json: {a!r}")

    # 4. Verbos prohibidos
    verbs = check_forbidden_verbs(body)
    rep.forbidden_verbs_found = verbs
    for v in verbs:
        rep.blocking_failures.append(f"Verbo prohibido: {v['verb']!r} — contexto: {v['context']!r}")

    return rep


def main() -> int:
    logging.basicConfig(level=logging.INFO, format="[%(levelname)s %(name)s] %(message)s")
    parser = argparse.ArgumentParser()
    parser.add_argument("markdown", help="Ruta al markdown de la edición a verificar")
    parser.add_argument("--extracted", default=str(EXTRACTED_FILE))
    parser.add_argument("--report-out", default=str(ROOT / "data" / "verification_report.json"))
    args = parser.parse_args()

    rep = verify(Path(args.markdown), Path(args.extracted))

    # Serializar reporte
    Path(args.report_out).write_text(json.dumps({
        "urls_checked": rep.urls_checked,
        "urls_failed": rep.urls_failed,
        "actors_checked": rep.actors_checked,
        "actors_untraceable": rep.actors_untraceable,
        "forbidden_verbs_found": rep.forbidden_verbs_found,
        "frontmatter_issues": rep.frontmatter_issues,
        "blocking_failures": rep.blocking_failures,
        "soft_warnings": rep.soft_warnings,
    }, ensure_ascii=False, indent=2))

    log.info(rep.summary())
    if not rep.ok():
        log.error("Verificación BLOQUEANTE. No se publica.")
        try:
            from src.notify import notify
            notify(
                f"🚨 Verificación bloqueante:\n{rep.summary()}\n\nRevisar `data/verification_report.json` y logs.",
                level="critical",
            )
        except Exception:  # noqa: BLE001
            pass
        return 1

    log.info("Verificación OK. Listo para publicar.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
