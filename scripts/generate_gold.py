"""Genera el gold standard automáticamente.

Proceso:
1. Opus 4.7 con extended thinking responde cada tarea sobre cada noticia.
2. Sonnet 4.6 actúa como validador revisando cada respuesta de Opus.
3. Items donde Opus y Sonnet coinciden 100% → entran en gold_auto.
4. Items donde discrepan → van a gold_discrepancies con razón.
5. Telegram alerta con resumen al terminar.

Output:
- data/bench/gold_auto_v1.json
- data/bench/gold_discrepancies.json
- private/bench-log.md (append de la ejecución)

Coste estimado una vez: ~3 €.

Uso:
    export ANTHROPIC_API_KEY=sk-ant-...
    python -m scripts.generate_gold
"""
from __future__ import annotations

import argparse
import json
import logging
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

log = logging.getLogger("gen-gold")

ROOT = Path(__file__).resolve().parent.parent
DATASET_PATH = ROOT / "data" / "bench" / "dataset_v1.json"
OUT_AUTO = ROOT / "data" / "bench" / "gold_auto_v1.json"
OUT_DISCREP = ROOT / "data" / "bench" / "gold_discrepancies.json"
LOG_PATH = ROOT / "private" / "bench-log.md"

OPUS = "claude-opus-4-7"
SONNET = "claude-sonnet-4-6"

# Prompts — mismos que run_benchmark.py, sincronizados manualmente cuando cambien.

CLASSIFY_SYSTEM = """Eres un analista de prensa local de Ibiza especializado en vivienda y mercado laboral de temporada.

Para cada noticia que te pase (título + resumen), devuelve un objeto JSON con:
- "is_housing" (bool)
- "actor" (string): consell | ayuntamiento | govern_balear | patronal | sindicato | propietarios | trabajadores | judicial | policial | tercer_sector | otro
- "lever" (string): normativa | fiscal | oferta_vivienda | intermediacion | enforcement | denuncia_social | precio | otro

Devuelve JSON array en el mismo orden de las noticias."""

DETECT_SYSTEM = """Eres un analista que identifica propuestas en noticias de vivienda en Ibiza.

Para cada noticia, devuelve `proposal_type` con uno de tres valores:
- "formal": actor con nombre propone medida CONCRETA y ejecutable.
- "en_movimiento": actor con nombre declara intención pero sin medida concreta aún (estudio encargado, debate, anuncio sin plan).
- "ninguna": cobertura de hecho, testimonio, dato, sentencia, acción ya ejecutada.

También devuelve `proposal_actor_hint` (nombre del actor o null).

Devuelve JSON array en el mismo orden."""

EXTRACT_SYSTEM = """Eres un analista que extrae propuestas con estructura completa.

Para cada noticia, devuelve lista de propuestas (puede ser vacía). Cada propuesta:
{
  "actor": "<nombre(s) literal(es) del firmante(s), separados por coma si es coalición>",
  "actor_type": "partido|sindicato|patronal|tercer_sector|academico|judicial|institucional_publico|colectivo_ciudadano|coalicion_intersectorial|coalicion_institucional|otro",
  "statement_summary": "<1-2 frases fieles al input, sin añadir interpretación>",
  "url_source": "<URL literal del input>",
  "palanca": "normativa|fiscal|oferta_vivienda|intermediacion|enforcement|laboral|judicial|denuncia_social|otro",
  "target_actor": "<ejecutor esperado o cadena vacía>",
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
- Si propuesta es "en_movimiento" (intención sin medida concreta), state = "en_movimiento".
- Si firman varios actores juntos: actor = nombres literales separados por coma ("CAEB, PIMEEF, CCOO y UGT"), actor_type = coalicion_intersectorial (privado+sindicato) o coalicion_institucional (con administración).
- NUNCA inventes URLs, cifras ni actores.
- Si no puedes evaluar viabilidad desde el input, "no_evaluada" con reason vacío.
- url_source debe ser EXACTAMENTE la URL proporcionada en el input.

Devuelve JSON array en el mismo orden de las noticias; cada elemento es {"news_id": "nXX", "proposals": [...]}."""


VALIDATOR_SYSTEM = """Eres un validador crítico. Recibes:
1. Una noticia (título + resumen + URL).
2. Una respuesta propuesta sobre ella.

Tu trabajo: decidir si la respuesta es razonablemente correcta según el contenido literal de la noticia y las reglas indicadas.

Devuelve JSON:
{
  "valid": true|false,
  "reason": "breve motivo si false (máx 1 frase)"
}

Criterios de validación:
- Los hechos citados en la respuesta están en la noticia.
- Las URLs citadas coinciden con la del input.
- Si es coalición, se nombran todos los firmantes.
- No hay inferencias no soportadas por el texto.

Sé estricto: si hay duda, false."""


def call(client, model: str, system: str, user: str, max_tokens: int = 8192,
         thinking: bool = False) -> tuple[str, dict]:
    kwargs = {
        "model": model,
        "max_tokens": max_tokens,
        "system": [{"type": "text", "text": system, "cache_control": {"type": "ephemeral"}}],
        "messages": [{"role": "user", "content": user}],
    }
    if thinking:
        # Opus con razonamiento extendido (API actualizada 2026)
        kwargs["thinking"] = {"type": "adaptive"}
        kwargs["output_config"] = {"effort": "high"}
        kwargs["max_tokens"] = max(kwargs["max_tokens"], 8000)
    resp = client.messages.create(**kwargs)
    text = "".join(b.text for b in resp.content if b.type == "text").strip()
    if text.startswith("```"):
        text = text.split("```", 2)[1]
        if text.startswith("json"):
            text = text[4:]
        text = text.strip("` \n")
    usage = resp.usage.model_dump() if hasattr(resp.usage, "model_dump") else dict(resp.usage)
    return text, usage


def try_json(text: str):
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return None


def generate_opus_gold(client, dataset: list[dict]) -> dict[str, dict]:
    """Opus con thinking responde cada tarea para todas las noticias."""
    from src.costs import record_call

    payload = json.dumps([{"id": it["id"], "title": it["title"], "summary": it["summary"], "url": it["url"]} for it in dataset], ensure_ascii=False, indent=2)

    result: dict[str, dict] = {it["id"]: {} for it in dataset}

    for task_name, system_prompt, field in [
        ("classify", CLASSIFY_SYSTEM, "task_1_classify"),
        ("detect", DETECT_SYSTEM, "task_2_proposal_detect"),
        ("extract", EXTRACT_SYSTEM, "task_3_extract"),
    ]:
        log.info("Opus thinking | task=%s | items=%d", task_name, len(dataset))
        text, usage = call(client, OPUS, system_prompt, payload, max_tokens=16000, thinking=True)
        record_call(edition="gold-gen", stage=f"gold_{task_name}_opus", model=OPUS, usage=usage)

        parsed = try_json(text)
        if not isinstance(parsed, list):
            log.error("Opus respuesta no parseable en %s: %s", task_name, text[:200])
            continue

        for i, record in enumerate(parsed):
            # id explícito o por orden
            nid = None
            if isinstance(record, dict):
                nid = record.get("news_id") or record.get("id")
            if not nid and i < len(dataset):
                nid = dataset[i]["id"]
            if not nid:
                continue

            if task_name == "extract":
                # record = {"news_id": "nXX", "proposals": [...]}
                props = record.get("proposals", []) if isinstance(record, dict) else []
                result[nid][field] = props
            else:
                result[nid][field] = record

    return result


def validate_with_sonnet(client, dataset: list[dict], gold: dict[str, dict]) -> dict[str, dict]:
    """Sonnet revisa cada respuesta. Devuelve dict con {id: {task: {valid, reason}}}."""
    from src.costs import record_call

    items_by_id = {it["id"]: it for it in dataset}
    validation: dict[str, dict] = {}

    for nid, tasks in gold.items():
        validation[nid] = {}
        noticia = items_by_id.get(nid)
        if not noticia:
            continue

        for task_field, response in tasks.items():
            user_payload = {
                "noticia": {
                    "title": noticia["title"],
                    "summary": noticia["summary"],
                    "url": noticia["url"],
                },
                "task": task_field,
                "response": response,
            }
            text, usage = call(
                client, SONNET, VALIDATOR_SYSTEM,
                json.dumps(user_payload, ensure_ascii=False, indent=2),
                max_tokens=512,
            )
            record_call(edition="gold-gen", stage=f"gold_validate_{task_field}", model=SONNET, usage=usage)
            parsed = try_json(text)
            if not isinstance(parsed, dict):
                validation[nid][task_field] = {"valid": False, "reason": "Validador respuesta no parseable"}
            else:
                validation[nid][task_field] = {
                    "valid": bool(parsed.get("valid")),
                    "reason": parsed.get("reason", ""),
                }

    return validation


def split_consensus(
    opus_gold: dict[str, dict],
    validation: dict[str, dict],
) -> tuple[dict, dict]:
    """Separa en items validados vs discrepancias."""
    auto_gold: dict[str, dict] = {}
    discrepancies: dict[str, dict] = {}

    for nid, tasks in opus_gold.items():
        item_valid = True
        item_errors = {}
        for task_field in tasks:
            v = validation.get(nid, {}).get(task_field, {})
            if not v.get("valid"):
                item_valid = False
                item_errors[task_field] = v.get("reason", "no validado")

        if item_valid:
            auto_gold[nid] = tasks
        else:
            discrepancies[nid] = {
                "opus_response": tasks,
                "validator_notes": item_errors,
            }

    return auto_gold, discrepancies


def append_log(summary: dict) -> None:
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    line = (
        f"\n## {summary['timestamp']}\n"
        f"- Dataset: {summary['dataset_version']} ({summary['total_items']} items)\n"
        f"- Validados (gold_auto): **{summary['valid']}** / {summary['total_items']}\n"
        f"- Discrepancias: **{summary['discrep']}**\n"
        f"- Coste total: **{summary['cost_eur']:.4f} €**\n"
    )
    existing = LOG_PATH.read_text() if LOG_PATH.exists() else "# Log de ejecuciones del benchmark\n\nRegistro automático de cada `generate_gold.py` y `run_benchmark.py`.\n"
    LOG_PATH.write_text(existing + line)


def notify_summary(summary: dict) -> None:
    try:
        from src.notify import notify
        msg = (
            f"✅ Gold auto generado\n"
            f"Validados: {summary['valid']}/{summary['total_items']}\n"
            f"Discrepancias: {summary['discrep']}\n"
            f"Coste: {summary['cost_eur']:.2f} €"
        )
        level = "ok" if summary["discrep"] == 0 else "info"
        notify(msg, level=level)
    except Exception as exc:  # noqa: BLE001
        log.warning("No se pudo notificar por Telegram: %s", exc)


def main() -> int:
    logging.basicConfig(level=logging.INFO, format="[%(levelname)s %(name)s] %(message)s")
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    dataset = json.loads(DATASET_PATH.read_text())
    log.info("Dataset cargado: %d noticias", len(dataset))

    if args.dry_run:
        log.info("=== DRY RUN === No se llama a la API.")
        log.info("Prompts: CLASSIFY(%d) DETECT(%d) EXTRACT(%d) VALIDATOR(%d)",
                 len(CLASSIFY_SYSTEM), len(DETECT_SYSTEM), len(EXTRACT_SYSTEM), len(VALIDATOR_SYSTEM))
        return 0

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        log.error("Falta ANTHROPIC_API_KEY")
        return 2

    import anthropic
    client = anthropic.Anthropic(api_key=api_key)

    from src.costs import current_month_spend_usd, usd_to_eur

    cost_before = current_month_spend_usd()

    log.info("Fase 1/2: Opus thinking genera gold candidato...")
    opus_gold = generate_opus_gold(client, dataset)

    log.info("Fase 2/2: Sonnet valida respuestas...")
    validation = validate_with_sonnet(client, dataset, opus_gold)

    auto_gold, discrepancies = split_consensus(opus_gold, validation)

    OUT_AUTO.parent.mkdir(parents=True, exist_ok=True)
    meta = {
        "_metadata": {
            "version": "auto_v1",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "method": "Opus 4.7 extended thinking + Sonnet 4.6 validator",
            "dataset": "dataset_v1.json",
        }
    }
    OUT_AUTO.write_text(json.dumps({**meta, **auto_gold}, ensure_ascii=False, indent=2))
    OUT_DISCREP.write_text(json.dumps({**meta, **discrepancies}, ensure_ascii=False, indent=2))
    log.info("gold_auto → %s", OUT_AUTO)
    log.info("discrepancias → %s", OUT_DISCREP)

    cost_after = current_month_spend_usd()
    cost_eur = usd_to_eur(cost_after - cost_before)

    summary = {
        "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
        "dataset_version": "v1",
        "total_items": len(dataset),
        "valid": len(auto_gold),
        "discrep": len(discrepancies),
        "cost_eur": cost_eur,
    }
    append_log(summary)
    notify_summary(summary)

    log.info("RESUMEN: %d validados, %d discrepancias, %.4f €", summary["valid"], summary["discrep"], cost_eur)
    return 0


if __name__ == "__main__":
    sys.exit(main())
