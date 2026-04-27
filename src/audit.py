"""Auditor MVP — orquestador completo + registro JSON append-only.

Tres bloques principales:

- ``run_blind_audit`` (capa 2). Segunda lectura ciega con Sonnet 4.6 sobre
  el mismo prompt y payload que pasa por capa 1 (Haiku) en
  ``src/extract.py``. Alimenta el comparador determinista de
  ``src/audit_compare.py``.
- ``build_signals`` + ``compute_tier``. Bloque ``signals`` (11 señales del
  registro de auditoría, plano §3.2) y stub de ``compute_tier`` que en el
  MVP siempre devuelve ``value=None`` con ``reason='pendiente_estudio'``.
- ``audit_proposals`` + ``write_audit_log``. Orquestador del MVP completo:
  capa 2 ciega (un único batch Sonnet) + comparador + heurísticas
  (``src/audit_heuristics.py``) + signals + escritura del JSON por
  propuesta en ``data/audit/{edition}/{proposal_id}.json`` (append-only;
  si el archivo existe, error sin sobreescribir).

Invocación independiente como paso del pipeline::

    ANTHROPIC_API_KEY=... python -m src.audit             # con API
    python -m src.audit --dry-run                         # sin API

Plano: DISENO-AUDITOR-MVP.md §2.1 + §3.1 + §6.
"""
from __future__ import annotations

import argparse
import json
import logging
import os
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from src.audit_compare import compare_extractions
from src.audit_heuristics import load_actor_domains, run_heuristics
from src.costs import assert_budget_available, record_call
from src.extract import EXTRACT_SYSTEM, MODEL_BASE, MODEL_VALIDATOR, _call, _try_json

log = logging.getLogger("audit")

ROOT = Path(__file__).resolve().parent.parent
EXTRACTED_FILE = ROOT / "data" / "extracted.json"
CLASSIFIED_FILE = ROOT / "data" / "classified.json"
ACTOR_DOMAINS_FILE = ROOT / "data" / "actor_domains.yml"
AUDIT_DIR = ROOT / "data" / "audit"

SEVERITY_TO_CONSENSO = {
    "none": "completo",
    "minor": "parcial",
    "critical": "disputa",
}


# ---------------------------------------------------------------------------
# Capa 2 — segunda lectura ciega (Sonnet)
# ---------------------------------------------------------------------------

def run_blind_audit(client, items: list[dict], edition: str) -> dict[str, list[dict]]:
    """Capa 2: lectura ciega con Sonnet sobre el mismo envío que Haiku.

    El payload se construye igual que extract_with_haiku() para que la
    comparación posterior sea limpia. Devuelve mapping news_id ->
    list[proposals]. Si el modelo no devuelve lista válida, devuelve
    dict vacío y registra el fallo en logs.
    """
    if not items:
        return {}

    payload = json.dumps(
        [
            {
                "id": it.get("id", it["url"]),
                "title": it["title"],
                "summary": it["summary"][:500],
                "url": it["url"],
                "proposal_actor_hint": it.get("proposal_actor_hint"),
            }
            for it in items
        ],
        ensure_ascii=False,
        indent=2,
    )

    assert_budget_available(planned_cost=0.2)
    log.info("Auditoría ciega con %s sobre %d items", MODEL_VALIDATOR, len(items))
    text, usage = _call(client, MODEL_VALIDATOR, EXTRACT_SYSTEM, payload, max_tokens=8192)
    record_call(edition=edition, stage="audit_blind", model=MODEL_VALIDATOR, usage=usage)

    parsed = _try_json(text)
    if not isinstance(parsed, list):
        log.error("Auditor ciego no devolvió lista. Respuesta truncada: %s", text[:500])
        return {}

    out: dict[str, list[dict]] = {}
    for record in parsed:
        if not isinstance(record, dict):
            continue
        nid = record.get("news_id") or record.get("id")
        if not nid:
            continue
        out[nid] = record.get("proposals", []) or []
    return out


# ---------------------------------------------------------------------------
# Bloque signals + stub de tier
# ---------------------------------------------------------------------------

def build_signals(
    proposal: dict,
    compare_result: dict,
    heuristics_result: dict,
    verify_result: dict | None = None,
) -> dict[str, Any]:
    """Construye el bloque ``signals`` con las 11 señales del registro.

    Plano §3.2. En el MVP varias señales (``fecha_coherente``,
    ``wayback_snapshot``) sólo se rellenan si el caller pasa
    ``verify_result``; sin él quedan ``None`` para que la fórmula real las
    detecte como pendientes. ``url_ok`` se intenta rellenar primero desde
    verify y, si no, desde el ``url_ok`` que devuelve la heurística de
    verbatim al hacer fetch.
    """
    severity = (compare_result or {}).get("severity")
    cross = (heuristics_result or {}).get("cross_source") or {}
    verbatim = (heuristics_result or {}).get("verbatim_match") or {}
    whitelist = (heuristics_result or {}).get("whitelist") or {}
    verify = verify_result or {}

    url_ok: bool | None = verify.get("url_ok")
    if url_ok is None:
        url_ok = verbatim.get("url_ok")

    viability_econ = str(proposal.get("viability_economic") or "")
    viability_con_cifra = bool(re.search(r"\d", viability_econ))

    whitelist_match = whitelist.get("match")
    traza_dominio_actor: bool | None = None
    if whitelist_match in ("refuerza", "neutro"):
        traza_dominio_actor = True
    elif whitelist_match == "debilita":
        traza_dominio_actor = False

    statement_type = (proposal.get("statement_type") or "reported")

    return {
        "ia_consenso": SEVERITY_TO_CONSENSO.get(severity, "desconocido"),
        "arbitraje": "no_hubo",
        "url_ok": url_ok,
        "traza_dominio_actor": traza_dominio_actor,
        "fecha_coherente": verify.get("fecha_coherente"),
        "verbatim_match_ratio": verbatim.get("ratio"),
        "wayback_snapshot": verify.get("wayback_snapshot"),
        "n_fuentes_independientes": cross.get("n_fuentes_independientes", 1),
        "whitelist_match": whitelist_match,
        "viability_con_cifra": viability_con_cifra,
        "statement_type": statement_type,
    }


def compute_tier(signals: dict) -> dict:
    """Hueco reservado en el MVP — siempre devuelve ``value=None``.

    En la iteración posterior ([D9](DECISIONES.md), PI10), esta función
    leerá el bloque ``signals`` y devolverá un color real (🟢🟡🟠🔴). El
    estudio de tiers (`ESTUDIO-TIERS.md`) ya cierra el árbol de decisión;
    sólo falta conectarlo al ``compute_tier()`` real.

    Plano: §2.1.
    """
    return {
        "value": None,
        "reason": "pendiente_estudio",
        "signals": dict(signals or {}),
    }


# ---------------------------------------------------------------------------
# Registro JSON append-only
# ---------------------------------------------------------------------------

def write_audit_log(record: dict, edition: str) -> Path:
    """Escribe un registro JSON en ``data/audit/{edition}/{proposal_id}.json``.

    Append-only: si el archivo existe, lanza ``FileExistsError`` sin
    sobreescribir. La intención es que el archivo histórico del auditor
    nunca se corrompa; las correcciones se añaden al bloque
    ``corrections`` del propio JSON, no al archivo desde fuera.

    Plano §3.1.
    """
    proposal_id = record.get("proposal_id")
    if not proposal_id:
        raise ValueError("record sin proposal_id; no se puede escribir el log.")
    week_dir = AUDIT_DIR / edition
    week_dir.mkdir(parents=True, exist_ok=True)
    path = week_dir / f"{proposal_id}.json"
    if path.exists():
        raise FileExistsError(f"audit log ya existe (no se sobreescribe): {path}")
    path.write_text(
        json.dumps(record, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    return path


# ---------------------------------------------------------------------------
# Orquestador
# ---------------------------------------------------------------------------

def _items_for_blind(
    extracted: list[dict],
    classified: list[dict],
) -> list[dict]:
    """Reconstruye el formato (id/title/summary/url/hint) de los items que
    hay que volver a leer ciegamente con Sonnet.

    El cruce extracted ↔ classified se hace por URL (cada propuesta lleva
    ``url_source`` que coincide con la ``url`` del clasificado). Así
    evitamos asumir que los índices ``item-NNN`` empatan con la posición
    en classified.json (que no siempre lo hacen porque ``extract.py``
    enumera tras filtrar).
    """
    by_url = {n.get("url"): n for n in classified if n.get("url")}
    items: list[dict] = []
    for it in extracted:
        proposals = it.get("proposals") or []
        if not proposals:
            continue
        nid = it.get("news_id")
        url = (proposals[0].get("url_source") or "").strip()
        n = by_url.get(url)
        if n is None:
            log.warning(
                "news_id %s (url=%s) sin entrada en classified — se omite de capa 2.",
                nid, url,
            )
            continue
        items.append({
            "id": nid,
            "title": n.get("title", ""),
            "summary": n.get("summary", "") or "",
            "url": n.get("url", ""),
            "proposal_actor_hint": n.get("proposal_actor_hint"),
        })
    return items


def _build_audit_record(
    *,
    proposal_id: str,
    edition: str,
    proposal_haiku: dict,
    proposal_blind: dict | None,
    compare_result: dict,
    heuristics_result: dict,
    timings: dict,
) -> dict:
    """Construye el dict JSON del registro de auditoría según §3.1.

    El bloque ``verify`` queda mínimo en el MVP: ``verify.py`` corre sobre
    la edición markdown completa, no por propuesta, así que aquí sólo
    rellenamos lo que ya saben las heurísticas (``url_ok`` desde el fetch
    de ``check_verbatim_match`` y ``traza_dominio_actor`` desde la
    whitelist). ``wayback_snapshot``, ``fecha_coherente`` y verbos
    prohibidos quedan vacíos hasta que se conecte una capa de verify por
    propuesta (iteración posterior, plano §8).
    """
    now = datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")

    signals = build_signals(
        proposal_haiku, compare_result, heuristics_result, verify_result=None,
    )
    tier = compute_tier(signals)

    verbatim = (heuristics_result or {}).get("verbatim_match") or {}

    verify_block = {
        "url_ok": verbatim.get("url_ok"),
        "http_status": None,
        "checked_at": now,
        "wayback_snapshot": None,
        "traza_dominio_actor": signals.get("traza_dominio_actor"),
        "fecha_coherente": None,
        "verbos_prohibidos_detectados": [],
    }

    return {
        "proposal_id": proposal_id,
        "week": edition,
        "created_at": now,
        "tier": tier,
        "corrections": [],
        "layers": {
            "haiku": {
                "model": MODEL_BASE,
                "extracted_at": now,
                "proposal": proposal_haiku,
            },
            "sonnet_blind": {
                "model": MODEL_VALIDATOR,
                "extracted_at": now,
                "proposal": proposal_blind,
            },
            "compare": compare_result,
            "heuristics": heuristics_result,
        },
        "verify": verify_block,
        "timestamps": timings,
    }


def audit_proposals(
    client,
    extracted: list[dict],
    classified: list[dict],
    actor_domains: dict,
    edition: str,
    *,
    dry_run: bool = False,
) -> list[dict]:
    """Auditor MVP de extremo a extremo sobre las propuestas extraídas.

    Pasos por cada propuesta:

    1. Capa 2 ciega (un único batch Sonnet sobre todos los news_items con
       propuestas). En ``--dry-run`` se reusa la ficha de Haiku como
       lectura ciega: el comparador siempre devuelve ``severity=none``.
    2. ``compare_extractions`` (Haiku vs blind).
    3. ``run_heuristics`` (cross_source + verbatim_match + whitelist).
    4. ``build_signals`` + ``compute_tier`` (stub).
    5. ``write_audit_log`` (append-only en ``data/audit/{edition}/``).

    Devuelve la lista de registros (mismos que se escriben a disco). Si
    un archivo ya existía y no se pudo escribir, se loguea aviso y el
    registro queda en memoria pero no se persiste (sin tocar el JSON
    histórico).
    """
    items_with_props = [it for it in extracted if it.get("proposals")]
    if not items_with_props:
        log.info("Auditor: no hay propuestas extraídas — nada que auditar.")
        return []

    sonnet_ms_total = 0
    if dry_run:
        log.info("dry-run: capa 2 reusa fichas Haiku como blind, severity=none.")
        blind_by_id: dict[str, list[dict]] = {
            it.get("news_id"): list(it.get("proposals") or [])
            for it in items_with_props
        }
    else:
        items_blind = _items_for_blind(extracted, classified)
        if items_blind:
            t0 = time.perf_counter()
            blind_by_id = run_blind_audit(client, items_blind, edition)
            sonnet_ms_total = int((time.perf_counter() - t0) * 1000)
        else:
            blind_by_id = {}

    total_props = sum(len(it.get("proposals") or []) for it in items_with_props)
    sonnet_share = sonnet_ms_total // max(1, total_props)

    records: list[dict] = []
    counter = 0
    for it in items_with_props:
        nid = it.get("news_id")
        proposals_haiku = it.get("proposals") or []
        proposals_blind = blind_by_id.get(nid, [])

        for i, proposal_haiku in enumerate(proposals_haiku):
            counter += 1
            proposal_id = f"{edition}-{counter:03d}"

            proposal_blind = proposals_blind[i] if i < len(proposals_blind) else None

            t0 = time.perf_counter()
            compare_result = compare_extractions(proposal_haiku, proposal_blind or {})
            heuristics_result = run_heuristics(proposal_haiku, classified, actor_domains)
            heuristics_ms = int((time.perf_counter() - t0) * 1000)

            timings = {
                "haiku_ms": None,
                "sonnet_blind_ms": sonnet_share,
                "heuristics_ms": heuristics_ms,
                "verify_ms": 0,
                "total_ms": sonnet_share + heuristics_ms,
            }

            record = _build_audit_record(
                proposal_id=proposal_id,
                edition=edition,
                proposal_haiku=proposal_haiku,
                proposal_blind=proposal_blind,
                compare_result=compare_result,
                heuristics_result=heuristics_result,
                timings=timings,
            )

            try:
                path = write_audit_log(record, edition)
                log.info("auditoría: %s", path.relative_to(ROOT))
            except FileExistsError as exc:
                log.warning("salto sin sobreescribir: %s", exc)

            records.append(record)

    return records


# ---------------------------------------------------------------------------
# Entry point como paso del pipeline
# ---------------------------------------------------------------------------

def _default_edition() -> str:
    iso = datetime.now(timezone.utc).isocalendar()
    return f"{iso.year}-w{iso.week:02d}"


def main() -> int:
    logging.basicConfig(level=logging.INFO, format="[%(levelname)s %(name)s] %(message)s")

    parser = argparse.ArgumentParser(
        description="Auditor MVP — capas 2-3 + bloque signals + log JSON.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Salta capa 2 Sonnet (no consume API); usa Haiku como blind.",
    )
    parser.add_argument(
        "--edition",
        default=None,
        help="Etiqueta de la edición (formato YYYY-wWW). Por defecto, semana actual UTC.",
    )
    args = parser.parse_args()

    if not EXTRACTED_FILE.exists():
        log.error("falta %s — corre extract antes.", EXTRACTED_FILE)
        return 1
    if not CLASSIFIED_FILE.exists():
        log.error("falta %s — corre classify antes.", CLASSIFIED_FILE)
        return 1
    if not ACTOR_DOMAINS_FILE.exists():
        log.error("falta %s — necesario para la heurística whitelist.", ACTOR_DOMAINS_FILE)
        return 1

    extracted = json.loads(EXTRACTED_FILE.read_text(encoding="utf-8"))
    classified = json.loads(CLASSIFIED_FILE.read_text(encoding="utf-8"))
    actor_domains = load_actor_domains(ACTOR_DOMAINS_FILE)

    edition = args.edition or _default_edition()

    client = None
    if not args.dry_run:
        try:
            import anthropic
            # max_retries=5: reintentos automáticos ante errores transitorios de
            # la API (408/409/429/5xx, conexión). Cubre saturación sin perder edición.
            client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"], max_retries=5)
        except KeyError:
            log.error("ANTHROPIC_API_KEY no definida — usa --dry-run para correr sin API.")
            return 1

    records = audit_proposals(
        client, extracted, classified, actor_domains, edition,
        dry_run=args.dry_run,
    )

    n_critical = sum(
        1 for r in records if (r["layers"]["compare"] or {}).get("severity") == "critical"
    )
    n_minor = sum(
        1 for r in records if (r["layers"]["compare"] or {}).get("severity") == "minor"
    )
    log.info(
        "Auditor: %d propuestas auditadas (críticas=%d, menores=%d).",
        len(records), n_critical, n_minor,
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
