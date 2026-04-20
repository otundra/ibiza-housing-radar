"""Clasificador de noticias con Claude Haiku.

Para cada item determina:
- is_housing: si realmente trata de vivienda/trabajadores en Ibiza.
- actor principal (Consell, ayuntamiento, patronal, sindicato, propietarios,
  trabajadores, judicial, otro).
- palanca (fiscal, normativa, oferta-stock, intermediación, denuncia, otro).
- headline_es: resumen en 1 línea en español.

Envía todos los items en UNA sola llamada para minimizar coste.
"""
from __future__ import annotations

import json
import logging
import os
import sys
from pathlib import Path
from typing import Any

import anthropic

from costs import record_call, assert_budget_available

log = logging.getLogger("classify")

ROOT = Path(__file__).resolve().parent.parent
IN_FILE = ROOT / "data" / "ingested.json"
OUT_FILE = ROOT / "data" / "classified.json"

MODEL = "claude-haiku-4-5-20251001"

SYSTEM = """Eres un analista de prensa local de Ibiza especializado en vivienda y mercado laboral de temporada.

Recibirás una lista JSON de noticias (título + resumen). Devuelves un JSON con la misma longitud, en el mismo orden, donde cada elemento es un objeto con estos campos:

- "is_housing" (bool): true solo si la noticia trata de vivienda en Ibiza/Formentera con ángulo relevante para trabajadores de temporada, asentamientos, alquileres, precios, normativa de habitatge o vivienda turística. Falso si es turismo general, política sin aterrizaje concreto, o ruido.
- "actor" (string): uno de "consell", "ayuntamiento", "govern_balear", "patronal", "sindicato", "propietarios", "trabajadores", "judicial", "policial", "tercer_sector", "otro".
- "lever" (string): la palanca que toca la noticia. Uno de "normativa", "fiscal", "oferta_vivienda", "intermediacion", "enforcement", "denuncia_social", "precio", "otro".
- "headline_es" (string): 1 línea (máx 110 caracteres), directa, sin adornos, en español neutro.

Responde EXCLUSIVAMENTE con el JSON, sin texto previo ni posterior, empezando por `[`."""


def classify(items: list[dict[str, Any]], edition: str) -> list[dict[str, Any]]:
    if not items:
        return []

    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

    # Simplificamos el payload enviado para ahorrar tokens.
    payload = [
        {"i": i, "title": it["title"], "summary": it["summary"][:400]}
        for i, it in enumerate(items)
    ]

    assert_budget_available(planned_cost=0.05)

    log.info("Classifying %d items with %s", len(items), MODEL)
    resp = client.messages.create(
        model=MODEL,
        max_tokens=4096,
        system=SYSTEM,
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
    # Tolerancia a code fences
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

    if not isinstance(labels, list) or len(labels) != len(items):
        raise ValueError(
            f"Clasificador devolvió {len(labels) if isinstance(labels, list) else '?'} elementos, esperaba {len(items)}"
        )

    out = []
    for item, label in zip(items, labels):
        merged = {**item, **label}
        out.append(merged)
    return out


def main() -> int:
    logging.basicConfig(level=logging.INFO, format="[%(levelname)s %(name)s] %(message)s")
    edition = os.environ.get("EDITION", "adhoc")
    items = json.loads(IN_FILE.read_text())
    classified = classify(items, edition=edition)
    housing = [c for c in classified if c.get("is_housing")]
    OUT_FILE.write_text(json.dumps(housing, ensure_ascii=False, indent=2))
    log.info(
        "Clasificados: %d total → %d relevantes de vivienda → %s",
        len(classified), len(housing), OUT_FILE,
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
