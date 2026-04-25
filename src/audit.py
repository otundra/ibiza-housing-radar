"""Auditor — capa 2 ciega.

Segunda lectura independiente del mismo material que pasa por la capa 1
(Haiku) en src/extract.py. La capa 2 usa Sonnet 4.6 con el mismo prompt
EXTRACT_SYSTEM, sin ver la salida de Haiku. Sirve de doble-ojo automático
para alimentar el comparador campo a campo (src/audit_compare.py).

Plano: DISENO-AUDITOR-MVP.md §2.1 + §9 (fase 1).
Capas restantes (heurísticas, lista blanca, registro JSON, integración con
report.py, hueco para tiers) llegan en fases 2 y 3 del plano.
"""
from __future__ import annotations

import json
import logging

from src.costs import assert_budget_available, record_call
from src.extract import EXTRACT_SYSTEM, MODEL_VALIDATOR, _call, _try_json

log = logging.getLogger("audit")


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
