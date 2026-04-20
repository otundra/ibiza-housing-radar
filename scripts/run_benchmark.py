"""Benchmark de los 3 modelos de Anthropic (Haiku 4.5, Sonnet 4.6, Opus 4.7)
sobre las tareas del pipeline del observatorio documental.

Ejecución:
    export ANTHROPIC_API_KEY=sk-ant-...
    python -m scripts.run_benchmark

Opciones:
    --dry-run     No llama a la API; solo valida estructura y muestra prompts.
    --tasks T1,T2 Solo ejecuta las tareas indicadas (por defecto: todas).
    --models M1,M2 Solo ejecuta los modelos indicados (por defecto: todos).
    --out FILE    Ruta del JSON de resultados (por defecto: data/bench/results_v1.json).

Coste estimado por ejecución completa (3 modelos × 3 tareas × 20 noticias):
- Haiku:  ~0,05 € + ~0,10 € + ~0,15 € = ~0,30 €
- Sonnet: ~0,15 € + ~0,30 € + ~0,50 € = ~0,95 €
- Opus:   ~0,80 € + ~1,50 € + ~2,50 € = ~4,80 €
TOTAL estimado: ~6 € una vez.

Registra cada llamada en data/costs.csv con stage="bench_{task}" para trazabilidad.
"""
from __future__ import annotations

import argparse
import json
import logging
import os
import re
import sys
import time
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

log = logging.getLogger("bench")

ROOT = Path(__file__).resolve().parent.parent
DATASET_PATH = ROOT / "data" / "bench" / "dataset_v1.json"
GOLD_PATH = ROOT / "data" / "bench" / "gold_standard_v1.json"
DEFAULT_OUT = ROOT / "data" / "bench" / "results_v1.json"
REPORT_PATH = ROOT / "REPORTE-BENCHMARK.md"

MODELS = {
    "haiku":  "claude-haiku-4-5-20251001",
    "sonnet": "claude-sonnet-4-6",
    "opus":   "claude-opus-4-7",
}

TASKS = ["classify", "detect", "extract"]

# -----------------------------------------------------------------------------
# Prompts
# -----------------------------------------------------------------------------

CLASSIFY_SYSTEM = """Eres un analista de prensa local de Ibiza especializado en vivienda y mercado laboral de temporada.

Recibirás una lista JSON de noticias (título + resumen). Devuelves un JSON con la misma longitud, en el mismo orden, donde cada elemento es un objeto con estos campos:

- "is_housing" (bool): true solo si la noticia trata de vivienda en Ibiza/Formentera con ángulo relevante para trabajadores de temporada, asentamientos, alquileres, precios, normativa de habitatge o vivienda turística.
- "actor" (string): uno de "consell", "ayuntamiento", "govern_balear", "patronal", "sindicato", "propietarios", "trabajadores", "judicial", "policial", "tercer_sector", "otro".
- "lever" (string): uno de "normativa", "fiscal", "oferta_vivienda", "intermediacion", "enforcement", "denuncia_social", "precio", "otro".

Responde EXCLUSIVAMENTE con el JSON, sin texto previo ni posterior, empezando por `["""

DETECT_SYSTEM = """Eres un analista que identifica propuestas en noticias de vivienda en Ibiza.

Para cada noticia, clasifica en uno de TRES valores:

- "formal": actor con nombre propone medida CONCRETA y ejecutable. Ejemplo: "Cáritas reclama moratoria del desalojo hasta acreditar realojo". Aparece en /propuestas/.

- "en_movimiento": actor con nombre declara intención pero SIN medida concreta todavía. Ejemplo: "El Consell encarga estudio sobre vivienda vacía para diseñar políticas". Es intención registrada, pero la medida queda por concretar. Aparece en /radar/.

- "ninguna": cobertura de hecho, testimonio personal, dato descriptivo, sentencia judicial, acción ya ejecutada. Ejemplo: "Se ofrecen habitaciones a 3.500 €/mes"; "TSJIB avala denegación de licencia"; "La Cifra: 2 M€ recaudados en multas".

Devuelve JSON en el mismo orden de las noticias, cada elemento con:
- "proposal_type" ("formal" | "en_movimiento" | "ninguna")
- "proposal_actor_hint" (string | null): nombre del actor, si proposal_type ≠ ninguna.

Responde EXCLUSIVAMENTE con el JSON empezando por `["""

EXTRACT_SYSTEM = """Eres un analista que extrae propuestas con estructura completa.

Para cada noticia, identifica las propuestas de actores con nombre (formales o en_movimiento) y devuelve ficha estructurada.

REGLAS DURAS:
- Si la noticia NO contiene propuesta (formal ni en_movimiento), devuelve lista vacía.
- url_source debe ser la URL EXACTA del input, no inventada.
- statement_summary: resumen fiel 1-2 frases; nunca añadir interpretación no textual.
- Si no se puede evaluar viabilidad desde el input, "no_evaluada" con reason vacío.
- Si no hay dato, lista vacía (no inventes).
- COALICIONES: si varios actores firman juntos, actor = nombres literales separados por coma ("CAEB, PIMEEF, CCOO y UGT"). actor_type = coalicion_intersectorial (privado+sindicato) o coalicion_institucional (con administración o sociedad civil).
- EN MOVIMIENTO: si la propuesta es intención sin medida concreta (ej. estudio encargado, anuncio sin plan), state = "en_movimiento".

Devuelve JSON: lista del mismo tamaño que las noticias. Cada elemento:
- "news_id" (str)
- "proposals" (array de objetos):
  {
    "actor": "<nombre(s) literal(es), coma si coalición>",
    "actor_type": "partido|sindicato|patronal|tercer_sector|academico|judicial|institucional_publico|colectivo_ciudadano|coalicion_intersectorial|coalicion_institucional|otro",
    "statement_summary": "<resumen fiel 1-2 frases>",
    "url_source": "<URL literal del input>",
    "palanca": "normativa|fiscal|oferta_vivienda|intermediacion|enforcement|laboral|judicial|denuncia_social|otro",
    "target_actor": "<actor que ejecutaría o cadena vacía>",
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

Responde EXCLUSIVAMENTE con el JSON empezando por `["""


# -----------------------------------------------------------------------------
# Dataclasses
# -----------------------------------------------------------------------------

@dataclass
class CallResult:
    model: str
    task: str
    news_id: str
    output: Any
    input_tokens: int
    output_tokens: int
    cache_read_tokens: int
    cache_write_tokens: int
    cost_usd: float
    latency_s: float
    error: str = ""


@dataclass
class BenchmarkResults:
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    dataset_version: str = "v1"
    calls: list[CallResult] = field(default_factory=list)


# -----------------------------------------------------------------------------
# Runner
# -----------------------------------------------------------------------------

def load_dataset() -> list[dict]:
    return json.loads(DATASET_PATH.read_text())


def load_gold() -> dict:
    return json.loads(GOLD_PATH.read_text())


def build_user_message(task: str, items: list[dict]) -> str:
    """Construye el prompt de usuario agregando todos los items en un único payload."""
    slim = [
        {
            "id": it["id"],
            "title": it["title"],
            "summary": it["summary"][:500],
            "url": it.get("url", ""),
        }
        for it in items
    ]
    return json.dumps(slim, ensure_ascii=False, indent=2)


def get_system_prompt(task: str) -> str:
    return {
        "classify": CLASSIFY_SYSTEM,
        "detect":   DETECT_SYSTEM,
        "extract":  EXTRACT_SYSTEM,
    }[task]


def call_model(
    client,
    model_id: str,
    system: str,
    user: str,
    max_tokens: int = 4096,
) -> tuple[str, dict, float]:
    """Llama al modelo y devuelve (texto, usage_dict, latencia_s)."""
    t0 = time.time()
    resp = client.messages.create(
        model=model_id,
        max_tokens=max_tokens,
        system=[{"type": "text", "text": system, "cache_control": {"type": "ephemeral"}}],
        messages=[{"role": "user", "content": user}],
    )
    dt = time.time() - t0
    text = "".join(b.text for b in resp.content if b.type == "text").strip()
    if text.startswith("```"):
        text = text.split("```", 2)[1]
        if text.startswith("json"):
            text = text[4:]
        text = text.strip("` \n")
    usage = resp.usage.model_dump() if hasattr(resp.usage, "model_dump") else dict(resp.usage)
    return text, usage, dt


def run_task_for_model(client, task: str, model_key: str, dataset: list[dict]) -> list[CallResult]:
    """Ejecuta una tarea sobre todo el dataset para un modelo. Batching: una sola llamada."""
    from src.costs import compute_cost, record_call  # noqa: E402

    model_id = MODELS[model_key]
    system = get_system_prompt(task)
    user = build_user_message(task, dataset)

    max_tokens = {"classify": 4096, "detect": 4096, "extract": 8192}[task]

    log.info("Calling %s for task=%s on %d items...", model_id, task, len(dataset))
    try:
        text, usage, latency = call_model(client, model_id, system, user, max_tokens=max_tokens)
        parsed = try_parse_json(text)
        error = "" if parsed is not None else "JSON malformado"
        cost = compute_cost(model_id, usage)
        record_call(
            edition=f"bench-{task}",
            stage=f"bench_{task}",
            model=model_id,
            usage=usage,
        )
        results = split_per_item(task, parsed, dataset, model_key, cost, usage, latency, error)
    except Exception as exc:  # noqa: BLE001
        log.error("Fallo en %s/%s: %s", model_key, task, exc)
        results = [
            CallResult(
                model=model_key, task=task, news_id=it["id"],
                output=None, input_tokens=0, output_tokens=0,
                cache_read_tokens=0, cache_write_tokens=0,
                cost_usd=0.0, latency_s=0.0, error=str(exc),
            )
            for it in dataset
        ]
    return results


def try_parse_json(text: str):
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return None


def split_per_item(
    task: str, parsed, dataset: list[dict], model_key: str,
    total_cost: float, usage: dict, latency: float, error: str,
) -> list[CallResult]:
    """Convierte un batch parseado en resultados por item."""
    # El coste y la latencia son compartidos por todo el batch; los repartimos
    # por item para que cada fila tenga valor informativo agregable.
    n = max(len(dataset), 1)
    per_cost = total_cost / n
    per_in = (usage.get("input_tokens", 0) or 0) // n
    per_out = (usage.get("output_tokens", 0) or 0) // n
    per_cr = (usage.get("cache_read_input_tokens", 0) or 0) // n
    per_cw = (usage.get("cache_creation_input_tokens", 0) or 0) // n

    items_by_id = {it["id"]: it for it in dataset}
    by_id = {}

    if isinstance(parsed, list):
        for i, record in enumerate(parsed):
            # El id puede venir explícito (extract) o por orden (classify, detect)
            nid = None
            if isinstance(record, dict):
                nid = record.get("news_id") or record.get("id")
            if not nid and i < len(dataset):
                nid = dataset[i]["id"]
            if nid:
                by_id[nid] = record

    results = []
    for it in dataset:
        nid = it["id"]
        out = by_id.get(nid)
        err = error if out is None and error else ""
        results.append(CallResult(
            model=model_key, task=task, news_id=nid, output=out,
            input_tokens=per_in, output_tokens=per_out,
            cache_read_tokens=per_cr, cache_write_tokens=per_cw,
            cost_usd=per_cost, latency_s=latency / n, error=err,
        ))
    return results


# -----------------------------------------------------------------------------
# Evaluación contra gold standard
# -----------------------------------------------------------------------------

def evaluate_classify(output: dict | None, gold: dict) -> dict:
    if not isinstance(output, dict):
        return {"ok": False, "score": 0.0, "details": "output no es dict"}
    gold_c = gold["task_1_classify"]
    match_housing = output.get("is_housing") == gold_c["is_housing"]
    match_actor = output.get("actor") == gold_c["actor"]
    match_lever = output.get("lever") == gold_c["lever"]
    total = sum([match_housing, match_actor, match_lever])
    return {
        "ok": total == 3,
        "score": total / 3.0,
        "housing_ok": match_housing,
        "actor_ok": match_actor,
        "lever_ok": match_lever,
    }


def evaluate_detect(output: dict | None, gold: dict) -> dict:
    if not isinstance(output, dict):
        return {"ok": False, "score": 0.0, "details": "output no es dict"}
    gold_d = gold["task_2_proposal_detect"]
    gold_type = gold_d.get("proposal_type", "ninguna")
    out_type = output.get("proposal_type", "ninguna")

    # Match exacto da 1.0; match parcial (formal vs en_movimiento vs ninguna)
    # con algún acierto parcial da 0.5 solo si el modelo distingue "algo vs nada".
    if out_type == gold_type:
        return {"ok": True, "score": 1.0, "match_exact": True}
    # Si gold es "ninguna" y output no, es falso positivo pleno (score 0).
    # Si gold es "formal" y output "en_movimiento", error parcial (score 0.5).
    if {out_type, gold_type} == {"formal", "en_movimiento"}:
        return {"ok": False, "score": 0.5, "match_exact": False, "note": "confusión formal↔en_movimiento"}
    return {"ok": False, "score": 0.0, "match_exact": False}


def evaluate_extract(output: dict | None, gold: dict) -> dict:
    if not isinstance(output, dict):
        return {"ok": False, "score": 0.0, "details": "output no es dict"}
    gold_e = gold.get("task_3_extract", [])
    out_props = output.get("proposals", [])

    if not gold_e and not out_props:
        return {"ok": True, "score": 1.0, "match_count": True, "details": "ambos vacíos"}
    if bool(gold_e) != bool(out_props):
        return {
            "ok": False, "score": 0.0, "match_count": False,
            "details": f"gold={len(gold_e)} props, output={len(out_props)} props",
        }

    # Comparación por campos clave (actor, url_source, palanca)
    matches = 0
    for gp in gold_e:
        for op in out_props:
            same_url = gp.get("url_source") == op.get("url_source")
            same_actor_family = (gp.get("actor_type") == op.get("actor_type"))
            if same_url and same_actor_family:
                matches += 1
                break
    score = matches / max(len(gold_e), 1)
    return {
        "ok": score >= 0.75,
        "score": score,
        "match_count": len(gold_e) == len(out_props),
        "matches": matches,
        "gold_count": len(gold_e),
        "output_count": len(out_props),
    }


EVAL_FUNCS = {
    "classify": evaluate_classify,
    "detect": evaluate_detect,
    "extract": evaluate_extract,
}


# -----------------------------------------------------------------------------
# Informe
# -----------------------------------------------------------------------------

def generate_report(results: BenchmarkResults, gold: dict, out_path: Path) -> None:
    """Construye el ESTUDIO-3-MODELOS.md con resultados comparativos."""
    lines: list[str] = []
    lines.append("# Estudio comparativo de 3 modelos de Anthropic")
    lines.append("")
    lines.append(f"**Ejecución:** {results.timestamp}")
    lines.append(f"**Dataset:** {results.dataset_version} — 20 noticias reales curadas.")
    lines.append("**Modelos evaluados:** Haiku 4.5 (`claude-haiku-4-5`), Sonnet 4.6 (`claude-sonnet-4-6`), Opus 4.7 (`claude-opus-4-7`).")
    lines.append("**Tareas:** clasificación (`classify`), detección de propuesta (`detect`), extracción estructurada (`extract`).")
    lines.append("")

    # Tabla resumen por modelo × tarea
    by = {}
    for call in results.calls:
        by.setdefault((call.model, call.task), []).append(call)

    lines.append("## Resumen — precisión por modelo y tarea")
    lines.append("")
    lines.append("| Modelo | classify | detect | extract | ∑ score |")
    lines.append("|---|---|---|---|---|")
    for model_key in MODELS:
        row = [f"**{model_key}**"]
        total = 0.0
        for task in TASKS:
            calls = by.get((model_key, task), [])
            scores = []
            for c in calls:
                g = gold.get(c.news_id, {})
                ev = EVAL_FUNCS[task](c.output if isinstance(c.output, dict) else None, g)
                scores.append(ev["score"])
            avg = sum(scores) / len(scores) if scores else 0
            total += avg
            row.append(f"{avg*100:.1f}%")
        row.append(f"{total:.2f}")
        lines.append("| " + " | ".join(row) + " |")
    lines.append("")

    # Tabla coste y latencia
    lines.append("## Coste y latencia por ejecución completa")
    lines.append("")
    lines.append("| Modelo | Coste total (€) | Tokens in | Tokens out | Cache read | Latencia acum. (s) |")
    lines.append("|---|---|---|---|---|---|")
    for model_key in MODELS:
        total_cost = 0.0
        t_in = t_out = t_cr = 0
        t_lat = 0.0
        for task in TASKS:
            for c in by.get((model_key, task), []):
                total_cost += c.cost_usd
                t_in += c.input_tokens
                t_out += c.output_tokens
                t_cr += c.cache_read_tokens
                t_lat += c.latency_s
        from src.costs import usd_to_eur
        lines.append(
            f"| {model_key} | {usd_to_eur(total_cost):.4f} € | {t_in:,} | {t_out:,} | {t_cr:,} | {t_lat:.2f} |"
        )
    lines.append("")

    # Detalle de errores por modelo
    lines.append("## Errores detectados")
    lines.append("")
    any_error = False
    for model_key in MODELS:
        for task in TASKS:
            for c in by.get((model_key, task), []):
                if c.error:
                    lines.append(f"- `{model_key}` / `{task}` / `{c.news_id}`: {c.error}")
                    any_error = True
    if not any_error:
        lines.append("*Ninguno.*")
    lines.append("")

    # Detalle por item (primeros 5 para legibilidad, el resto en JSON completo)
    lines.append("## Detalle por noticia (primeros 5 items)")
    lines.append("")
    for news_id in sorted(gold.keys())[:5]:
        if news_id.startswith("_"):
            continue
        lines.append(f"### {news_id}")
        lines.append("")
        for task in TASKS:
            lines.append(f"**Tarea: {task}**")
            lines.append("")
            lines.append("| Modelo | Output | Score |")
            lines.append("|---|---|---|")
            for model_key in MODELS:
                calls = [c for c in results.calls if c.model == model_key and c.task == task and c.news_id == news_id]
                if calls:
                    c = calls[0]
                    ev = EVAL_FUNCS[task](c.output if isinstance(c.output, dict) else None, gold[news_id])
                    lines.append(f"| {model_key} | `{truncate(json.dumps(c.output, ensure_ascii=False), 120)}` | {ev['score']*100:.0f}% |")
            lines.append("")

    # Recomendación
    lines.append("## Recomendación de reparto")
    lines.append("")
    recommendation = derive_recommendation(results, gold)
    for task, reco in recommendation.items():
        lines.append(f"- **{task}** → `{reco['model']}` (score {reco['score']*100:.1f}%, coste/ejecución {reco['cost_eur']:.4f} €). {reco['reason']}")
    lines.append("")

    # Coste proyectado mensual con el reparto
    monthly_est = sum(reco["cost_eur"] for reco in recommendation.values()) * 4  # 4 ediciones/mes
    lines.append(f"**Coste mensual proyectado con el reparto recomendado (sin self-review ni auditorías):** ~{monthly_est:.2f} €/mes en las 3 tareas principales. Ampliable con el resto de fases del pipeline (rescue, verify, generate) que no entran en este benchmark.")
    lines.append("")

    out_path.write_text("\n".join(lines))
    log.info("Informe escrito en %s", out_path)


def truncate(s: str, n: int) -> str:
    return s if len(s) <= n else s[:n-3] + "..."


def derive_recommendation(results: BenchmarkResults, gold: dict) -> dict:
    """Por cada tarea, elige el modelo con mejor ratio score/coste."""
    from src.costs import usd_to_eur
    by = {}
    for call in results.calls:
        by.setdefault((call.model, call.task), []).append(call)

    reco = {}
    for task in TASKS:
        candidates = []
        for model_key in MODELS:
            calls = by.get((model_key, task), [])
            scores = []
            total_cost = 0.0
            for c in calls:
                g = gold.get(c.news_id, {})
                ev = EVAL_FUNCS[task](c.output if isinstance(c.output, dict) else None, g)
                scores.append(ev["score"])
                total_cost += c.cost_usd
            avg_score = sum(scores) / len(scores) if scores else 0
            candidates.append({
                "model": model_key,
                "score": avg_score,
                "cost_eur": usd_to_eur(total_cost),
            })

        if not candidates:
            continue

        # Regla de negocio:
        # - Si algún modelo tiene score >= 0.95 y es el más barato con ese umbral, gana.
        # - Si ningún modelo llega a 0.95, ganar el mejor score absoluto si la diferencia
        #   con el siguiente es > 10 puntos; si está en <10, gana el más barato.
        candidates.sort(key=lambda x: (-x["score"], x["cost_eur"]))
        best = candidates[0]
        cheap_and_good = [c for c in candidates if c["score"] >= 0.95]
        if cheap_and_good:
            winner = min(cheap_and_good, key=lambda x: x["cost_eur"])
            reason = f"≥95% de calidad y el más barato entre los que cumplen."
        else:
            # No hay excelencia absoluta; buscar trade-off
            top_score = candidates[0]["score"]
            close = [c for c in candidates if top_score - c["score"] <= 0.10]
            winner = min(close, key=lambda x: x["cost_eur"])
            if winner["model"] == candidates[0]["model"]:
                reason = "mejor puntuación y coste aceptable."
            else:
                reason = f"dentro de 10 puntos del mejor ({candidates[0]['model']}), {(candidates[0]['cost_eur']/max(winner['cost_eur'],0.0001)):.1f}× más barato."

        reco[task] = {
            "model": winner["model"],
            "score": winner["score"],
            "cost_eur": winner["cost_eur"],
            "reason": reason,
        }
    return reco


# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true", help="No llama a la API")
    parser.add_argument("--tasks", default=",".join(TASKS))
    parser.add_argument("--models", default=",".join(MODELS.keys()))
    parser.add_argument("--out", default=str(DEFAULT_OUT))
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO, format="[%(levelname)s %(name)s] %(message)s")

    dataset = load_dataset()
    gold = load_gold()
    log.info("Dataset: %d noticias. Gold standard: %d entradas.", len(dataset), sum(1 for k in gold if not k.startswith("_")))

    tasks = [t.strip() for t in args.tasks.split(",") if t.strip() in TASKS]
    models_selected = [m.strip() for m in args.models.split(",") if m.strip() in MODELS]

    if args.dry_run:
        log.info("=== DRY RUN === No se llama a la API.")
        for t in tasks:
            log.info("Task=%s | system prompt len=%d | items=%d", t, len(get_system_prompt(t)), len(dataset))
        return 0

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        log.error("Falta ANTHROPIC_API_KEY en el entorno.")
        return 2

    import anthropic
    client = anthropic.Anthropic(api_key=api_key)

    results = BenchmarkResults()
    for task in tasks:
        for model_key in models_selected:
            calls = run_task_for_model(client, task, model_key, dataset)
            results.calls.extend(calls)

    # Serializar resultados crudos
    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    raw = {
        "timestamp": results.timestamp,
        "dataset_version": results.dataset_version,
        "calls": [asdict(c) for c in results.calls],
    }
    out_path.write_text(json.dumps(raw, ensure_ascii=False, indent=2))
    log.info("Resultados crudos → %s", out_path)

    # Generar informe
    generate_report(results, gold, REPORT_PATH)
    log.info("Informe generado en %s", REPORT_PATH)
    return 0


if __name__ == "__main__":
    sys.exit(main())
