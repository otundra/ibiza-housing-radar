"""Clasificador y detector de propuestas con Claude Haiku 4.5.

Para cada noticia del ingest, determina:
- is_housing: si trata realmente de vivienda/temporeros en Ibiza/Formentera.
- actor principal (consell, ayuntamiento, govern_balear, patronal, sindicato,
  propietarios, trabajadores, judicial, policial, tercer_sector, otro).
- lever: palanca de política (normativa, fiscal, oferta_vivienda, intermediacion,
  enforcement, denuncia_social, precio, otro).
- headline_es: resumen 1 línea en español.
- proposal_type: "formal" | "en_movimiento" | "ninguna".
- proposal_actor_hint: nombre del actor que propone (si aplica).

Envía todos los items en UNA sola llamada para minimizar coste y aprovechar
prompt caching. Resiliente ante respuestas malformadas o cortas.

Modelo: Haiku 4.5. Decisión 2026-04-20 post benchmark.
"""
from __future__ import annotations

import json
import logging
import os
import sys
from pathlib import Path
from typing import Any

import anthropic

from src.costs import record_call, assert_budget_available

log = logging.getLogger("classify")

ROOT = Path(__file__).resolve().parent.parent
IN_FILE = ROOT / "data" / "ingested.json"
OUT_FILE = ROOT / "data" / "classified.json"

MODEL = "claude-haiku-4-5-20251001"

SYSTEM = """Eres un analista de prensa local de Ibiza especializado en vivienda y mercado laboral de temporada.

Recibirás una lista JSON de noticias (título + resumen). Devuelves un JSON con la misma longitud, en el mismo orden, donde cada elemento tiene los siguientes campos:

- "is_housing" (bool): true solo si la noticia trata de vivienda en Ibiza/Formentera con ángulo relevante para trabajadores de temporada, asentamientos, alquileres, precios, normativa de habitatge o vivienda turística. Falso si es turismo general, política sin aterrizaje concreto, o ruido.

- "actor" (string): uno de "consell", "ayuntamiento", "govern_balear", "patronal", "sindicato", "propietarios", "trabajadores", "judicial", "policial", "tercer_sector", "otro".

- "lever" (string): uno de "normativa", "fiscal", "oferta_vivienda", "intermediacion", "enforcement", "denuncia_social", "precio", "otro".

- "headline_es" (string): 1 línea (máx 110 caracteres), directa, sin adornos, en español neutro.

- "proposal_type" (string): uno de "formal", "en_movimiento", "ninguna".
   - "formal": actor con nombre propone medida CONCRETA y ejecutable. Ej: "Cáritas reclama moratoria del desalojo hasta acreditar realojo"; "CAEB, PIMEEF, CCOO y UGT piden residencias para temporeros".
   - "en_movimiento": actor con nombre declara intención pero SIN medida concreta todavía. Ej: "Consell encarga estudio sobre vivienda vacía para diseñar políticas"; "patronal anuncia que trabajará en propuesta".
   - "ninguna": cobertura de hecho, testimonio personal, dato descriptivo, sentencia judicial, acción ya ejecutada, mera crónica.

- "proposal_actor_hint" (string | null): si proposal_type ≠ "ninguna", nombre literal del actor que propone (o de todos los firmantes separados por coma si es coalición). Si "ninguna", null.

Responde EXCLUSIVAMENTE con el JSON, sin texto previo ni posterior, empezando por `[`."""


def classify(items: list[dict[str, Any]], edition: str) -> list[dict[str, Any]]:
    if not items:
        return []

    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

    # Payload ligero para ahorrar tokens
    payload = [
        {"i": i, "title": it["title"], "summary": it["summary"][:400]}
        for i, it in enumerate(items)
    ]

    assert_budget_available(planned_cost=0.05)

    log.info("Classifying %d items with %s", len(items), MODEL)
    resp = client.messages.create(
        model=MODEL,
        max_tokens=4096,
        system=[{"type": "text", "text": SYSTEM, "cache_control": {"type": "ephemeral"}}],
        messages=[{
            "role": "user",
            "content": json.dumps(payload, ensure_ascii=False),
        }],
    )
    record_call(
        edition=edition,
        stage="classify",
        model=MODEL,
        usage=resp.usage.model_dump() if hasattr(resp.usage, "model_dump") else dict(resp.usage),
    )

    text = "".join(block.text for block in resp.content if block.type == "text").strip()
    if text.startswith("```"):
        text = text.split("```", 2)[1]
        if text.startswith("json"):
            text = text[4:]
        text = text.strip("` \n")

    try:
        labels = json.loads(text)
    except json.JSONDecodeError as e:
        log.error("Respuesta no era JSON:\n%s", text[:500])
        raise

    if not isinstance(labels, list):
        raise ValueError(f"Clasificador devolvió no-lista: {type(labels).__name__}")

    # Resiliencia: si devuelve menos items que el input, loguea y sigue con los
    # válidos. Nunca abortamos el pipeline por respuesta incompleta de Haiku.
    if len(labels) != len(items):
        log.warning(
            "Clasificador devolvió %d items, esperados %d. Continuando con los válidos.",
            len(labels), len(items),
        )

    out = []
    for i, item in enumerate(items):
        if i < len(labels) and isinstance(labels[i], dict):
            merged = {**item, **labels[i]}
        else:
            # Fallback conservador: si el clasificador no respondió para este
            # item, lo marcamos como no-housing para que no entre en el resto
            # del pipeline. Mejor perder señal que colar ruido.
            merged = {
                **item,
                "is_housing": False,
                "actor": "otro",
                "lever": "otro",
                "headline_es": item["title"][:110],
                "proposal_type": "ninguna",
                "proposal_actor_hint": None,
                "_classify_fallback": True,
            }
            log.warning("Item %d sin clasificación; fallback conservador.", i)
        out.append(merged)
    return out


def main() -> int:
    logging.basicConfig(level=logging.INFO, format="[%(levelname)s %(name)s] %(message)s")
    edition = os.environ.get("EDITION", "adhoc")
    items = json.loads(IN_FILE.read_text())
    classified = classify(items, edition=edition)
    housing = [c for c in classified if c.get("is_housing")]
    OUT_FILE.write_text(json.dumps(housing, ensure_ascii=False, indent=2))

    # Resumen útil para logs
    formal = sum(1 for c in housing if c.get("proposal_type") == "formal")
    en_mov = sum(1 for c in housing if c.get("proposal_type") == "en_movimiento")
    ninguna = sum(1 for c in housing if c.get("proposal_type") == "ninguna")
    log.info(
        "Clasificados: %d total → %d housing → formal=%d, en_movimiento=%d, ninguna=%d → %s",
        len(classified), len(housing), formal, en_mov, ninguna, OUT_FILE,
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
