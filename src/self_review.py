"""Autoevaluación semanal de la edición recién publicada.

Tras escribir la edición, Sonnet revisa la edición nueva + 3 anteriores
y puntúa 5 dimensiones. Si alguna <7, alerta Telegram con link al log.

Modelo: Sonnet 4.6. Coste: ~0,15 €/edición. Decisión 2026-04-20.
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

MODEL = "claude-sonnet-4-6"

SYSTEM = """Eres un revisor interno de Ibiza Housing Radar, un observatorio documental de vivienda en Ibiza.

Las 5 reglas duras del observatorio (vinculantes):
1. Solo se documentan propuestas con autor identificado y URL verificable.
2. El observatorio NO genera propuestas propias.
3. Ningún actor queda excluido por filiación.
4. Balance de actores auditado y publicado.
5. Correcciones públicas con traza.

Recibes la edición recién publicada y las 3 ediciones anteriores como contexto. Analiza la nueva y puntúa de 1 a 10 en cinco dimensiones:

- "reglas": cumplimiento de las 5 reglas duras (URL en cada propuesta, actor con nombre, cero inferencia, tono descriptivo).
- "rigor": rigor factual. Cifras trazables. Ausencia de generalización o redondeo sin declarar.
- "balance": diversidad de actores citados en la edición. Distribución entre tipos (público, privado, sindical, tercer sector, etc.).
- "cobertura": ¿cubre los hechos importantes de la semana con las fuentes dadas? ¿Deja fuera algo relevante de la ingesta?
- "claridad": legibilidad sin perder densidad. Estructura clara, bullets concretos, tono consistente.

Devuelve JSON con:
{
  "scores": {
    "reglas": N,
    "rigor": N,
    "balance": N,
    "cobertura": N,
    "claridad": N
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


def review(edition_path: Path, edition_id: str) -> dict:
    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

    prevs = [p for p in latest_editions(4) if p != edition_path][:3]
    payload = {
        "edicion_nueva": edition_path.read_text(),
        "ediciones_anteriores": [p.read_text() for p in prevs],
    }

    assert_budget_available(planned_cost=0.2)

    resp = client.messages.create(
        model=MODEL,
        max_tokens=2048,
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
        msg = (
            f"⚠️ Self-review {edition_id}: score bajo\n"
            + "\n".join(f"- {k}: **{v}**" for k, v in low.items())
            + f"\nDetalle: `{review_path.relative_to(ROOT)}`"
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
