"""Extractor de propuestas estructuradas.

Lee data/classified.json (items con is_housing=True). Para cada item con
proposal_type != "ninguna", extrae ficha estructurada.

Arquitectura de confianza (decisión editor 2026-04-20, opción C):

    Haiku extrae → Sonnet valida → si Sonnet marca invalid → Opus reextrae

Principios:
- CERO INFERENCIA: actor, URL, cifras, citas → literales del texto.
- URL OBLIGATORIA: si el item no tiene URL, la propuesta no se registra.
- ACTOR CON NOMBRE OBLIGATORIO: si el actor no es nombrable, no se registra.
- Coaliciones se expresan con todos los firmantes literales en el campo actor.

Output: data/extracted.json con propuestas estructuradas + metadata de qué
modelo produjo cada una + flags de disputas.
"""
from __future__ import annotations

import json
import logging
import os
import sys
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Any

import anthropic

from src.costs import record_call, assert_budget_available

log = logging.getLogger("extract")

ROOT = Path(__file__).resolve().parent.parent
IN_FILE = ROOT / "data" / "classified.json"
OUT_FILE = ROOT / "data" / "extracted.json"

MODEL_BASE = "claude-haiku-4-5-20251001"
MODEL_VALIDATOR = "claude-sonnet-4-6"
MODEL_FALLBACK = "claude-opus-4-7"

EXTRACT_SYSTEM = """Eres un analista que extrae propuestas de vivienda hechas por actores con nombre, en noticias de prensa local de Ibiza.

Recibes una lista de noticias, cada una con: id, title, summary, url, proposal_actor_hint (opcional).

Para cada noticia devuelves un objeto con:
- "news_id": el id recibido.
- "proposals": lista de propuestas extraídas (puede ser vacía).

Cada propuesta:
{
  "actor": "<nombre(s) literal(es) del firmante(s), coma separada si es coalición>",
  "actor_type": "partido|sindicato|patronal|tercer_sector|academico|judicial|institucional_publico|colectivo_ciudadano|coalicion_intersectorial|coalicion_institucional|otro",
  "statement_summary": "<1-2 frases FIELES al texto; nunca añadas interpretación>",
  "statement_verbatim": "<fragmento literal de la noticia que soporta la propuesta, entrecomillado si aparece textual>",
  "url_source": "<URL literal del input, nunca modificada>",
  "palanca": "normativa|fiscal|oferta_vivienda|intermediacion|enforcement|laboral|judicial|denuncia_social|otro",
  "target_actor": "<actor que ejecutaría; cadena vacía si no se menciona>",
  "horizon": "inmediato|corto_plazo|temporada_2026|temporada_2027|estructural",
  "state": "propuesta|en_movimiento|en_debate|aprobada|en_ejecucion|implementada|descartada|pendiente_resolucion_judicial",
  "viability_legal": "alta|media|baja|no_evaluada",
  "viability_legal_reason": "",
  "viability_economic": "alta|media|baja|sin_cifra_publica_disponible|no_evaluada",
  "viability_economic_reason": "",
  "supporters_cited": [],
  "opponents_cited": [],
  "precedents": []
}

REGLAS DURAS:
- Si la noticia no contiene propuesta atribuible a actor con nombre, devuelve lista vacía. NUNCA inventes actores.
- url_source debe ser la URL EXACTA del input.
- NUNCA inventes cifras, precedentes ni nombres no presentes en el texto.
- COALICIONES: si firman varios actores juntos, incluye los nombres literales separados por coma. actor_type = coalicion_intersectorial (privado+sindicato) o coalicion_institucional (con administración).
- EN_MOVIMIENTO: si la propuesta es intención sin medida concreta, state = "en_movimiento".
- Viabilidad: solo la declaras si el propio texto de la noticia la argumenta. Si no, "no_evaluada" con reason vacío.

CLASIFICACIÓN DE ACTOR_TYPE — reglas específicas para instituciones públicas:
- Si el actor aparece vinculado a "Consell d'Eivissa", "Consell Insular", "Govern Balear", "Govern", "IBAVI", "Ayuntamiento de [municipio]", "Ministerio", "Delegación del Gobierno", "Síndic", "Defensor", o cualquier cargo institucional ("conseller/a", "consejero/a", "regidor/a", "alcalde/sa", "director/a general", "secretari/a d'Estat"): **actor_type = "institucional_publico"**. NO uses "otro" en estos casos aunque el nombre del cargo sea corto o poco familiar.
- Si el actor es PARTIDO POLÍTICO en oposición o como siglas (PP, PSOE, Vox, Més, Sumar, Sa Unió, Unides Podem, PI), actor_type = "partido".
- Si estás cubriendo un actor que habla DESDE un partido pero ostenta un cargo institucional (p.ej. "conseller de Vivienda" que es de PSOE), prima el cargo institucional: actor_type = "institucional_publico". El partido puede anotarse en supporters_cited si aparece explícito.
- "otro" solo para actores genuinamente fuera de las categorías.

Responde EXCLUSIVAMENTE con el JSON empezando por `[`."""


VALIDATOR_SYSTEM = """Eres un validador estricto. Recibes:
1. Una noticia (title, summary, url).
2. Una extracción propuesta (lista de propuestas con actor, url, statement, etc.).

Tu trabajo: verificar que la extracción es fiel al texto. NO añades ni corriges; solo validas.

Devuelve JSON: {"valid": true|false, "reason": "<motivo corto si false, ≤1 frase>"}

Criterios OBLIGATORIOS para valid=true:
- Cada actor nombrado aparece LITERALMENTE en el texto (o es inferencia trivial: p.ej. "Cáritas" cuando la noticia dice "Cáritas Ibiza").
- url_source coincide con la URL dada en el input.
- Las cifras citadas aparecen en el texto.
- statement_summary no añade afirmaciones que el texto no soporta.
- Si es coalición, los firmantes nombrados aparecen en el texto (no hay inferencia de miembros no mencionados).
- Si la noticia menciona "patronales y sindicatos" genéricamente, la extracción NO puede nombrar entidades concretas (CAEB, CCOO, etc.) a menos que aparezcan literalmente.

Sé estricto. Si tienes duda razonable, valid=false."""


@dataclass
class ExtractionResult:
    news_id: str
    proposals: list[dict]
    produced_by: str = MODEL_BASE  # modelo que produjo esta extracción final
    validator_verdict: str = ""     # "valid" | "invalid" | "skipped"
    validator_reason: str = ""
    was_disputed: bool = False


def _call(client, model: str, system: str, user: str, max_tokens: int = 8192) -> tuple[str, dict]:
    resp = client.messages.create(
        model=model,
        max_tokens=max_tokens,
        system=[{"type": "text", "text": system, "cache_control": {"type": "ephemeral"}}],
        messages=[{"role": "user", "content": user}],
    )
    text = "".join(b.text for b in resp.content if b.type == "text").strip()
    if text.startswith("```"):
        text = text.split("```", 2)[1]
        if text.startswith("json"):
            text = text[4:]
        text = text.strip("` \n")
    usage = resp.usage.model_dump() if hasattr(resp.usage, "model_dump") else dict(resp.usage)
    return text, usage


def _try_json(text: str):
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return None


def extract_with_haiku(client, items: list[dict], edition: str) -> dict[str, list[dict]]:
    """Extracción base con Haiku sobre todos los items en un batch."""
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

    assert_budget_available(planned_cost=0.1)
    log.info("Extracción base con %s sobre %d items", MODEL_BASE, len(items))
    text, usage = _call(client, MODEL_BASE, EXTRACT_SYSTEM, payload, max_tokens=8192)
    record_call(edition=edition, stage="extract_base", model=MODEL_BASE, usage=usage)

    parsed = _try_json(text)
    if not isinstance(parsed, list):
        log.error("Haiku extract no devolvió lista. Respuesta truncada: %s", text[:500])
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


def validate_extraction(
    client, news: dict, proposals: list[dict], edition: str
) -> tuple[bool, str]:
    """Sonnet valida una extracción concreta. Devuelve (valid, reason)."""
    if not proposals:
        return True, "extracción vacía, sin validación necesaria"

    payload = json.dumps(
        {
            "noticia": {
                "title": news["title"],
                "summary": news["summary"],
                "url": news["url"],
            },
            "extraccion_propuesta": {"proposals": proposals},
        },
        ensure_ascii=False,
        indent=2,
    )

    assert_budget_available(planned_cost=0.05)
    text, usage = _call(client, MODEL_VALIDATOR, VALIDATOR_SYSTEM, payload, max_tokens=512)
    record_call(edition=edition, stage="extract_validate", model=MODEL_VALIDATOR, usage=usage)

    parsed = _try_json(text)
    if not isinstance(parsed, dict):
        log.warning("Validador no devolvió dict para news=%s. Asumiendo invalid.", news.get("id"))
        return False, "validador_respuesta_no_parseable"

    valid = bool(parsed.get("valid", False))
    reason = str(parsed.get("reason", ""))
    return valid, reason


def retry_with_opus(client, news: dict, edition: str) -> list[dict]:
    """Opus reextrae la propuesta. Solo se invoca cuando Sonnet disputa a Haiku."""
    payload = json.dumps(
        [
            {
                "id": news.get("id", news["url"]),
                "title": news["title"],
                "summary": news["summary"][:500],
                "url": news["url"],
                "proposal_actor_hint": news.get("proposal_actor_hint"),
            }
        ],
        ensure_ascii=False,
        indent=2,
    )

    assert_budget_available(planned_cost=0.5)
    log.info("Opus fallback para news=%s (disputa Haiku↔Sonnet)", news.get("id"))
    text, usage = _call(client, MODEL_FALLBACK, EXTRACT_SYSTEM, payload, max_tokens=8192)
    record_call(edition=edition, stage="extract_fallback", model=MODEL_FALLBACK, usage=usage)

    parsed = _try_json(text)
    if not isinstance(parsed, list) or not parsed:
        log.error("Opus fallback no parseable para news=%s", news.get("id"))
        return []
    first = parsed[0]
    return first.get("proposals", []) or []


def run(items_with_proposals: list[dict], edition: str) -> list[ExtractionResult]:
    """Pipeline completo: Haiku base + Sonnet validación + Opus fallback.

    items_with_proposals: items ya clasificados con proposal_type != 'ninguna'.
    """
    if not items_with_proposals:
        return []

    # Asignar ids estables si no los tienen
    for i, it in enumerate(items_with_proposals):
        if "id" not in it:
            it["id"] = f"item-{i:03d}"

    # max_retries=5: reintentos automáticos ante errores transitorios de la API
    # (408/409/429/5xx, conexión). Cubre picos de saturación sin perder edición.
    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"], max_retries=5)

    # Paso 1: Haiku extrae todos en un batch
    haiku_extractions = extract_with_haiku(client, items_with_proposals, edition)

    # Paso 2: Sonnet valida cada extracción no vacía; Paso 3: Opus reextrae si disputa
    results: list[ExtractionResult] = []
    news_by_id = {it["id"]: it for it in items_with_proposals}

    for nid, item in news_by_id.items():
        haiku_props = haiku_extractions.get(nid, [])
        if not haiku_props:
            results.append(ExtractionResult(
                news_id=nid, proposals=[],
                produced_by=MODEL_BASE,
                validator_verdict="skipped",
            ))
            continue

        valid, reason = validate_extraction(client, item, haiku_props, edition)
        if valid:
            results.append(ExtractionResult(
                news_id=nid, proposals=haiku_props,
                produced_by=MODEL_BASE,
                validator_verdict="valid",
                validator_reason=reason,
            ))
            continue

        # Disputa: Opus reextrae
        opus_props = retry_with_opus(client, item, edition)
        results.append(ExtractionResult(
            news_id=nid,
            proposals=opus_props,
            produced_by=MODEL_FALLBACK,
            validator_verdict="invalid",
            validator_reason=reason,
            was_disputed=True,
        ))

    return results


def main() -> int:
    logging.basicConfig(level=logging.INFO, format="[%(levelname)s %(name)s] %(message)s")
    edition = os.environ.get("EDITION", "adhoc")

    if not IN_FILE.exists():
        log.error("Falta %s. Ejecuta `python -m src.classify` antes.", IN_FILE)
        return 2

    classified = json.loads(IN_FILE.read_text())
    # Solo items con propuesta declarada (formal o en_movimiento)
    candidates = [
        c for c in classified
        if c.get("is_housing") and c.get("proposal_type") in ("formal", "en_movimiento")
    ]
    log.info("Candidatos a extracción: %d de %d", len(candidates), len(classified))

    if not candidates:
        OUT_FILE.write_text(json.dumps([], ensure_ascii=False, indent=2))
        log.info("Sin candidatos; escribo lista vacía en %s", OUT_FILE)
        return 0

    results = run(candidates, edition=edition)

    # Serializar
    serializable = []
    for r in results:
        serializable.append({
            "news_id": r.news_id,
            "proposals": r.proposals,
            "produced_by": r.produced_by,
            "validator_verdict": r.validator_verdict,
            "validator_reason": r.validator_reason,
            "was_disputed": r.was_disputed,
        })
    OUT_FILE.write_text(json.dumps(serializable, ensure_ascii=False, indent=2))

    disputed = sum(1 for r in results if r.was_disputed)
    total_props = sum(len(r.proposals) for r in results)
    log.info(
        "Extracción completada: %d items procesados, %d propuestas totales, %d disputas Opus.",
        len(results), total_props, disputed,
    )
    if disputed / max(len(results), 1) > 0.2:
        log.warning(
            "Ratio de disputas > 20%% (%d/%d). Señal de alerta: Haiku puede no estar llegando.",
            disputed, len(results),
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
