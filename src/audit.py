"""Auditor — capa 2 ciega + bloque ``signals`` para tiers.

- Capa 2 (``run_blind_audit``): segunda lectura independiente con Sonnet 4.6
  sobre el mismo prompt y payload que pasa por capa 1 (Haiku) en
  ``src/extract.py``. Alimenta el comparador campo a campo de
  ``src/audit_compare.py``.
- Bloque ``signals`` (``build_signals``): combina comparador + heurísticas
  (``src/audit_heuristics.py``) + verify (cuando esté disponible) en las 11
  señales del registro de auditoría (plano §3.2).
- Stub ``compute_tier``: en el MVP siempre devuelve ``value=None`` con
  ``reason='pendiente_estudio'`` y deja ``signals`` listo para que la
  fórmula real (PI10) lea el bloque cuando el estudio de tiers se
  conecte.

Plano: DISENO-AUDITOR-MVP.md §2.1 + §9 (fases 1-2).
Capas restantes (registro JSON, integración con ``report.py``, prueba
empírica W10) llegan en fases 3-4.
"""
from __future__ import annotations

import json
import logging
import re
from typing import Any

from src.costs import assert_budget_available, record_call
from src.extract import EXTRACT_SYSTEM, MODEL_VALIDATOR, _call, _try_json

log = logging.getLogger("audit")

SEVERITY_TO_CONSENSO = {
    "none": "completo",
    "minor": "parcial",
    "critical": "disputa",
}


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
