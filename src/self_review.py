"""Autoevaluación semanal de la edición recién publicada.

Tras escribir la edición, Sonnet revisa la edición nueva + 3 anteriores
y puntúa 5 dimensiones. Si alguna <7, alerta Telegram con link al log.

Modelo: Sonnet 4.6. Coste: ~0,15 €/edición. Decisión 2026-04-20.

Desde Fase 3 del auditor MVP (DISENO-AUDITOR-MVP.md §6.4): además de la
edición, el revisor recibe un bloque ``auditor`` con el ratio de
disputas Haiku↔Sonnet de la semana. Si el ratio está fuera del rango
saludable [0.08, 0.25] (ESTUDIO-COSTES-AUDITOR.md §12.1), Sonnet lo
anota como aviso y el editor lo ve en la alerta del lunes.
"""
from __future__ import annotations

import json
import logging
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import anthropic

from src.costs import record_call, assert_budget_available

log = logging.getLogger("self-review")

ROOT = Path(__file__).resolve().parent.parent
EDITIONS_DIR = ROOT / "docs" / "_editions"
OUT_DIR = ROOT / "private" / "self-review"
LOG_PATH = ROOT / "private" / "self-review-log.md"
AUDIT_DIR = ROOT / "data" / "audit"

MODEL = "claude-sonnet-4-6"

# Rango saludable del ratio de disputas Haiku↔Sonnet (ESTUDIO-COSTES-AUDITOR §12.1).
# Por debajo del mínimo: capa 2 puede estar copiando capa 1 (sospechoso).
# Por encima del máximo: divergencia anormal entre modelos (degradación o prompt mal calibrado).
DISPUTE_RATIO_HEALTHY = (0.08, 0.25)

SYSTEM = """Eres un revisor interno de Ibiza Housing Radar, un observatorio documental de vivienda en Ibiza.

Las 5 reglas duras del observatorio (vinculantes):
1. Solo se documentan propuestas con autor identificado y URL verificable.
2. El observatorio NO genera propuestas propias.
3. Ningún actor queda excluido por filiación.
4. Balance de actores auditado y publicado.
5. Correcciones públicas con traza.

Recibes la edición recién publicada y las 3 ediciones anteriores como contexto. Analiza la nueva y puntúa de 1 a 10 en seis dimensiones:

- "reglas": cumplimiento de las 5 reglas duras (URL en cada propuesta, actor con nombre, cero inferencia, tono descriptivo).
- "rigor": rigor factual. Cifras trazables. Ausencia de generalización o redondeo sin declarar.
- "balance": diversidad de actores citados en la edición. Distribución entre tipos (público, privado, sindical, tercer sector, etc.).
- "cobertura": ¿cubre los hechos importantes de la semana con las fuentes dadas? ¿Deja fuera algo relevante de la ingesta?
- "claridad": legibilidad sin perder densidad. Estructura clara, bullets concretos, tono consistente.
- "trazabilidad": calidad de la cadena fuente→hecho. (a) ¿cada cifra cita fuente identificable?, (b) ¿la fuente es primaria (BOIB, nota oficial, web institucional, cabecera original) o agregador (MSN, Google News, otro reagregador)?, (c) ¿los agregadores están etiquetados visiblemente como tales en el cuerpo?, (d) ¿las estimaciones llevan etiqueta inline declarando su naturaleza ("estimación periodística", "dato oficial", "orientativa")? Penaliza fuerte cuando una cifra clave proviene solo de agregador sin marca, o cuando hay estimación sin etiqueta de naturaleza.

También recibes un bloque "auditor" con métricas de la auditoría interna de la semana (segunda lectura ciega Haiku↔Sonnet). Tienes que interpretar la señal "ratio_disputas":

- "ratio_disputas" es la fracción de propuestas con desacuerdo Haiku↔Sonnet de severidad crítica o menor.
- "rango_saludable" indica el intervalo [min, max] esperable. "en_rango" es true si ratio cae dentro.
- "propuestas_auditadas" indica el tamaño de muestra. Por debajo de 3, el ratio NO es estadísticamente interpretable: con n=1 cualquier desacuerdo da ratio=1.0 y con n=2 el grano es 0/0,5/1,0. Por eso el umbral de penalización solo aplica con muestra suficiente.
- **Regla con muestra suficiente (propuestas_auditadas ≥ 3):** si en_rango es false, el rigor de la edición está en duda — añade un warning concreto y baja la nota de "rigor" a 6 o menos. Razón típica: prompt degradado, modelo cambiado, o noticias inusualmente confusas.
- **Regla con muestra escasa (propuestas_auditadas < 3):** si en_rango es false, añade igualmente warning explicando el desacuerdo Haiku↔Sonnet y la limitación estadística (frase tipo "ratio fuera de rango pero n={N} no es interpretable"), pero NO bajes la nota de rigor por este motivo. La nota de rigor sigue evaluándose por el contenido del cuerpo (cifras trazables, atribuciones completas, fuentes primarias).
- Si "propuestas_flagged" > 0, son propuestas que el auditor marcó para revisión manual; cítalas en warnings con su id.

Devuelve JSON con:
{
  "scores": {
    "reglas": N,
    "rigor": N,
    "balance": N,
    "cobertura": N,
    "claridad": N,
    "trazabilidad": N
  },
  "warnings": [<lista de problemas concretos detectados, frases cortas>],
  "suggestions": [<0-3 ajustes al prompt del generador si detectas patrón degradado; si no, lista vacía>]
}

Sé estricto. Un 10 solo si es impecable en esa dimensión. Un 7 es aceptable. <7 requiere acción del editor."""


def latest_editions(n: int = 4) -> list[Path]:
    if not EDITIONS_DIR.exists():
        return []
    files = sorted(EDITIONS_DIR.glob("*.md"), reverse=True)
    return files[:n]


def auditor_signal(edition_id: str) -> dict:
    """Resume el ratio de disputas Haiku↔Sonnet de la edición.

    Lee los registros JSON escritos por ``src/audit.py`` en
    ``data/audit/{edition}/`` y agrega el bloque que se inyecta al
    payload del revisor (DISENO-AUDITOR-MVP.md §6.4). Si no hay logs,
    devuelve dict vacío de manera compatible (el revisor lo ignora).

    El edition_id de self_review llega como ``YYYY-WNN`` (mayúscula); los
    logs del auditor se escriben con ``YYYY-wNN`` (minúscula) — se
    normaliza a la baja.
    """
    edition_dir = AUDIT_DIR / edition_id.lower()
    if not edition_dir.exists():
        return {}

    files = sorted(edition_dir.glob("*.json"))
    if not files:
        return {}

    auditadas = 0
    disputadas = 0
    flagged: list[str] = []
    for f in files:
        try:
            record = json.loads(f.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            continue
        auditadas += 1
        compare = (record.get("layers") or {}).get("compare") or {}
        if compare.get("severity") in ("critical", "minor"):
            disputadas += 1
        tier_value = (record.get("tier") or {}).get("value")
        if tier_value in ("naranja", "rojo"):
            pid = record.get("proposal_id") or f.stem
            flagged.append(pid)

    if auditadas == 0:
        return {}

    ratio = round(disputadas / auditadas, 3)
    minimo, maximo = DISPUTE_RATIO_HEALTHY
    return {
        "propuestas_auditadas": auditadas,
        "propuestas_disputadas": disputadas,
        "ratio_disputas": ratio,
        "rango_saludable": [minimo, maximo],
        "en_rango": minimo <= ratio <= maximo,
        "propuestas_flagged": len(flagged),
        "flagged_ids": flagged,
    }


def review(edition_path: Path, edition_id: str) -> dict:
    # max_retries=5: reintentos automáticos ante errores transitorios de la API
    # (408/409/429/5xx, conexión). Cubre picos de saturación sin perder edición.
    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"], max_retries=5)

    prevs = [p for p in latest_editions(4) if p != edition_path][:3]
    auditor = auditor_signal(edition_id)
    payload: dict = {
        "edicion_nueva": edition_path.read_text(),
        "ediciones_anteriores": [p.read_text() for p in prevs],
    }
    if auditor:
        payload["auditor"] = auditor

    assert_budget_available(planned_cost=0.2)

    resp = client.messages.create(
        model=MODEL,
        max_tokens=2048,
        # temperature=0 reduce la varianza entre lecturas. Sonnet 4.6 sigue
        # admitiendo este parámetro (Opus 4.7 ya no). Sin esto, dos lecturas
        # de la misma edición pueden dar notas con ±2-3 puntos de diferencia.
        # Reduce ruido pero no lo elimina; los warnings cualitativos siempre
        # son la fuente más fiable.
        temperature=0,
        system=[{"type": "text", "text": SYSTEM, "cache_control": {"type": "ephemeral"}}],
        messages=[{"role": "user", "content": json.dumps(payload, ensure_ascii=False)}],
    )
    record_call(
        edition=edition_id,
        stage="self_review",
        model=MODEL,
        usage=resp.usage.model_dump() if hasattr(resp.usage, "model_dump") else dict(resp.usage),
    )

    text = "".join(b.text for b in resp.content if b.type == "text").strip()
    if text.startswith("```"):
        text = text.split("```", 2)[1]
        if text.startswith("json"):
            text = text[4:]
        text = text.strip("` \n")

    try:
        return json.loads(text)
    except json.JSONDecodeError:
        log.error("Respuesta no parseable: %s", text[:400])
        return {"scores": {}, "warnings": ["respuesta no parseable"], "suggestions": []}


def write_review_file(review_data: dict, edition_id: str) -> Path:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    slug = edition_id.lower().replace("w", "w")  # e.g. 2026-w17
    path = OUT_DIR / f"{slug}.md"
    lines = [
        f"# Self-review {edition_id}",
        "",
        f"*{datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}* · modelo `{MODEL}`.",
        "",
        "## Puntuaciones",
        "",
        "| Dimensión | Score |",
        "|---|---|",
    ]
    for k, v in review_data.get("scores", {}).items():
        lines.append(f"| {k} | **{v}** |")
    lines.append("")

    warnings = review_data.get("warnings", [])
    if warnings:
        lines.append("## Warnings")
        lines.append("")
        for w in warnings:
            lines.append(f"- ⚠️ {w}")
        lines.append("")

    suggestions = review_data.get("suggestions", [])
    if suggestions:
        lines.append("## Sugerencias de ajuste al prompt")
        lines.append("")
        for s in suggestions:
            lines.append(f"- {s}")
        lines.append("")

    path.write_text("\n".join(lines))
    return path


def append_log_if_alert(review_data: dict, edition_id: str, review_path: Path) -> bool:
    """Si algún score <7, añade entrada a private/self-review-log.md. Devuelve True si alertó."""
    scores = review_data.get("scores", {})
    if not scores:
        return False
    low = {k: v for k, v in scores.items() if isinstance(v, (int, float)) and v < 7}
    if not low:
        return False

    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    existing = LOG_PATH.read_text() if LOG_PATH.exists() else "# Log de self-reviews semanales\n\n"
    entry = (
        f"\n## {edition_id} · {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}\n"
        f"- Scores bajos: {', '.join(f'{k}={v}' for k,v in low.items())}\n"
        f"- Detalle: [{review_path.name}]({review_path.relative_to(ROOT)})\n"
    )
    LOG_PATH.write_text(existing + entry)

    try:
        from src.notify import notify

        # Descripción corta de cada dimensión para que el aviso sea
        # autoexplicativo en Telegram sin obligar a abrir el detalle
        # cada vez. La causa concreta sigue en el fichero del review.
        dim_hint = {
            "reglas": "cumplimiento de las 5 reglas duras (autor, URL, cero inferencia)",
            "rigor": "cifras o generalizaciones sin trazabilidad",
            "balance": "actores concentrados (poca diversidad)",
            "cobertura": "hechos relevantes que pudo dejar fuera",
            "claridad": "estructura o tono inconsistente",
            "trazabilidad": "fuentes agregadas no marcadas o cifras sin origen identificable",
        }
        scores_lines = "\n".join(
            f"• {k}: *{v}/10* — {dim_hint.get(k, '(dimensión sin descripción)')}"
            for k, v in low.items()
        )
        msg = (
            f"*Autoevaluación {edition_id}: notas por debajo del umbral*\n\n"
            f"La segunda lectura interna (Sonnet 4.6) puntúa la edición "
            f"en 5 dimensiones, escala 1-10. Umbral de aviso: nota <7.\n\n"
            f"{scores_lines}\n\n"
            f"Detalle: `{review_path.relative_to(ROOT)}`\n\n"
            f"Acción: revisar el detalle; si lo confirma, ajustar prompt del generador."
        )
        notify(msg, level="warning")
    except Exception as exc:  # noqa: BLE001
        log.warning("No se pudo notificar: %s", exc)
    return True


def main() -> int:
    logging.basicConfig(level=logging.INFO, format="[%(levelname)s %(name)s] %(message)s")
    edition_id = os.environ.get("EDITION", datetime.now(timezone.utc).strftime("%Y-W%V"))

    latest = latest_editions(1)
    if not latest:
        log.warning("No hay ediciones publicadas — nada que revisar.")
        return 0

    edition_path = latest[0]
    log.info("Revisando %s como edición %s", edition_path.name, edition_id)

    data = review(edition_path, edition_id)
    review_path = write_review_file(data, edition_id)
    log.info("Self-review escrito: %s", review_path)

    alerted = append_log_if_alert(data, edition_id, review_path)
    if alerted:
        log.warning("Algún score <7 — alerta disparada.")
    else:
        log.info("Todos los scores ≥7.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
