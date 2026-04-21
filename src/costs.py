"""Control de costes de la API Anthropic.

- Registra cada llamada en data/costs.csv (append-only, en USD internamente).
- Regenera private/costs.md con dashboard legible en euros (no publicado).
- Topes en euros con capas de alerta. Solo corta en TOPE DURO.
- Emite alertas Telegram cuando se cruza un umbral.

Filosofía: **no perdemos editorial por sobrecoste**. Solo cortamos ante
runaway real (tope duro), que protege contra bugs/bucles. En tope blando
solo avisamos por Telegram y seguimos publicando.
"""
from __future__ import annotations

import csv
import json
import logging
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Final

log = logging.getLogger("costs")

ROOT = Path(__file__).resolve().parent.parent
COSTS_CSV = ROOT / "data" / "costs.csv"
COSTS_MD = ROOT / "private" / "costs.md"  # Fuera de docs/: no servido por Jekyll

# Precios por millón de tokens (USD). Actualizar si cambian.
# Referencia: https://www.anthropic.com/pricing (abril 2026)
PRICING = {
    "claude-opus-4-7":            {"input": 15.00, "output": 75.00},
    "claude-opus-4-6":            {"input": 15.00, "output": 75.00},
    "claude-sonnet-4-6":          {"input":  3.00, "output": 15.00},
    "claude-sonnet-4-5":          {"input":  3.00, "output": 15.00},
    "claude-haiku-4-5":           {"input":  1.00, "output":  5.00},
    "claude-haiku-4-5-20251001":  {"input":  1.00, "output":  5.00},
}

# Conversión USD → EUR usada solo para display y comparación con topes.
# Anthropic factura en USD; el CSV histórico se guarda en USD para precisión.
# Revisar cada 3 meses y ajustar si la divergencia supera el 5 %.
USD_TO_EUR: Final[float] = 0.92

# Topes mensuales en EUROS.
# Blando: solo avisa por Telegram y sigue publicando. No pierde editorial.
# Duro: corta el pipeline. Protección runaway (bug, bucle, escalada accidental).
#
# Historial:
# - 2026-04-20 v1: blando=8.00, duro=20.00 (basado en ~2 €/mes + margen trilingüe)
# - 2026-04-20 v2 (pivote documental): blando=12.00, duro=20.00. Sube para
#   absorber los 3 niveles de autoevaluación (self-review semanal con Sonnet,
#   auditoría trimestral con Opus, re-benchmark mensual). Proyección ~9,86 €/mes.
#   Objetivo: tras ~2-3 meses de datos reales, afinar reparto de modelos y
#   bajar el tope blando de nuevo.
# - 2026-04-21 v3 (Fase 0.5): duro sube a 50.00 para absorber el backfill de
#   12 semanas (W06-W17) + auditor IA de 5 capas + experimentación libre sin
#   miedo a bloqueos. Blando se mantiene en 12.00 (sigue avisando pronto).
MONTHLY_SOFT_CAP_EUR: Final[float] = 12.00
MONTHLY_HARD_CAP_EUR: Final[float] = 50.00

# Capas de alerta (en EUR). Se notifica solo al cruzar por primera vez en el mes.
# Capas (2026-04-21 v3):
#   🟢 Verde      < 6 €
#   🟡 Amarilla   6 - 9 €
#   🟠 Naranja    9 - 12 €
#   🔴 Roja blanda 12 - 50 €  (publica igual)
#   🚨 Roja dura  > 50 €      (corte)
_ALERT_THRESHOLDS_EUR: Final[list[tuple[float, str, str]]] = [
    # (umbral, nivel, etiqueta)
    (6.00,  "info",     "🟡 Amarilla"),
    (9.00,  "warning",  "🟠 Naranja"),
    (MONTHLY_SOFT_CAP_EUR, "warning",  "🔴 Roja blanda (tope blando superado, sigo publicando)"),
    (MONTHLY_HARD_CAP_EUR, "critical", "🚨 Roja dura (tope duro; el pipeline se cortará)"),
]


@dataclass
class CallRecord:
    ts: str            # ISO 8601 UTC
    edition: str       # p.ej. 2026-W16
    stage: str         # ingest | classify | generate
    model: str
    input_tokens: int
    output_tokens: int
    cache_read_tokens: int
    cache_write_tokens: int
    cost_usd: float    # Guardado en USD para precisión; display en EUR


# ---------------------------------------------------------------------------
# Conversión
# ---------------------------------------------------------------------------

def usd_to_eur(usd: float) -> float:
    return round(usd * USD_TO_EUR, 4)


# ---------------------------------------------------------------------------
# Pricing y registro
# ---------------------------------------------------------------------------

def price_for(model: str) -> dict[str, float]:
    if model in PRICING:
        return PRICING[model]
    for key, val in PRICING.items():
        if model.startswith(key):
            return val
    log.warning("Modelo sin tarifa registrada: %s — asumiendo Haiku.", model)
    return PRICING["claude-haiku-4-5"]


def compute_cost(model: str, usage: dict) -> float:
    """Devuelve el coste en USD para una llamada dada."""
    p = price_for(model)
    inp = usage.get("input_tokens", 0) or 0
    out = usage.get("output_tokens", 0) or 0
    cache_read = usage.get("cache_read_input_tokens", 0) or 0
    cache_write = usage.get("cache_creation_input_tokens", 0) or 0
    cost = (
        inp * p["input"] / 1_000_000
        + out * p["output"] / 1_000_000
        + cache_read * p["input"] * 0.1 / 1_000_000
        + cache_write * p["input"] * 1.25 / 1_000_000
    )
    return round(cost, 6)


def record_call(
    edition: str,
    stage: str,
    model: str,
    usage: dict,
) -> CallRecord:
    spend_before_eur = current_month_spend_eur()
    rec = CallRecord(
        ts=datetime.now(timezone.utc).isoformat(timespec="seconds"),
        edition=edition,
        stage=stage,
        model=model,
        input_tokens=usage.get("input_tokens", 0) or 0,
        output_tokens=usage.get("output_tokens", 0) or 0,
        cache_read_tokens=usage.get("cache_read_input_tokens", 0) or 0,
        cache_write_tokens=usage.get("cache_creation_input_tokens", 0) or 0,
        cost_usd=compute_cost(model, usage),
    )
    append_csv(rec)
    spend_after_eur = current_month_spend_eur()
    _maybe_notify_threshold_crossing(spend_before_eur, spend_after_eur)
    return rec


def append_csv(rec: CallRecord) -> None:
    COSTS_CSV.parent.mkdir(parents=True, exist_ok=True)
    new_file = not COSTS_CSV.exists()
    with COSTS_CSV.open("a", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(asdict(rec).keys()))
        if new_file:
            w.writeheader()
        w.writerow(asdict(rec))


def read_all_records() -> list[CallRecord]:
    if not COSTS_CSV.exists():
        return []
    out: list[CallRecord] = []
    with COSTS_CSV.open() as f:
        for row in csv.DictReader(f):
            out.append(
                CallRecord(
                    ts=row["ts"],
                    edition=row["edition"],
                    stage=row["stage"],
                    model=row["model"],
                    input_tokens=int(row["input_tokens"]),
                    output_tokens=int(row["output_tokens"]),
                    cache_read_tokens=int(row.get("cache_read_tokens", 0)),
                    cache_write_tokens=int(row.get("cache_write_tokens", 0)),
                    cost_usd=float(row["cost_usd"]),
                )
            )
    return out


# ---------------------------------------------------------------------------
# Gasto del mes y comprobaciones
# ---------------------------------------------------------------------------

def current_month_spend_usd() -> float:
    now = datetime.now(timezone.utc)
    key = now.strftime("%Y-%m")
    return round(sum(r.cost_usd for r in read_all_records() if r.ts.startswith(key)), 6)


def current_month_spend_eur() -> float:
    return usd_to_eur(current_month_spend_usd())


def assert_budget_available(planned_cost: float = 0.0) -> None:
    """Corta solo si se supera el TOPE DURO en euros (protección runaway).

    - `planned_cost` va en USD (coste estimado de la próxima llamada).
    - En tope blando NO corta: `record_call()` se encargará de notificar
      por Telegram cuando se materialice el cruce del umbral.
    """
    projected_usd = current_month_spend_usd() + planned_cost
    projected_eur = usd_to_eur(projected_usd)
    if projected_eur > MONTHLY_HARD_CAP_EUR:
        msg = (
            f"TOPE DURO SUPERADO: proyectado {projected_eur:.2f} € > "
            f"{MONTHLY_HARD_CAP_EUR:.2f} €. "
            f"Pipeline cortado para proteger contra runaway. "
            f"Revisar `private/costs.md` y gasto reciente antes de reactivar."
        )
        log.error(msg)
        try:
            from src.notify import notify  # import perezoso para evitar ciclos
            notify(msg, level="critical")
        except Exception as exc:  # noqa: BLE001
            log.error("No se pudo notificar el corte: %s", exc)
        raise RuntimeError(msg)


def _maybe_notify_threshold_crossing(spend_before_eur: float, spend_after_eur: float) -> None:
    """Notifica por Telegram si acabamos de cruzar algún umbral de coste.

    Solo dispara cuando `before < umbral <= after`, para no spamear en cada
    llamada una vez se supera el nivel.
    """
    crossed: list[tuple[float, str, str]] = [
        (umbral, nivel, etiqueta)
        for (umbral, nivel, etiqueta) in _ALERT_THRESHOLDS_EUR
        if spend_before_eur < umbral <= spend_after_eur
    ]
    if not crossed:
        return

    # Si se cruzaron varios a la vez (improbable pero posible si una llamada
    # enorme salta de 3 a 9 €), notificamos solo el más alto.
    umbral, nivel, etiqueta = crossed[-1]
    msg = (
        f"*Coste mensual: {etiqueta}*\n"
        f"Gasto actual: *{spend_after_eur:.2f} €* "
        f"(umbral cruzado: {umbral:.2f} €).\n"
        f"Tope blando: {MONTHLY_SOFT_CAP_EUR:.2f} €. "
        f"Tope duro: {MONTHLY_HARD_CAP_EUR:.2f} €."
    )
    try:
        from src.notify import notify  # import perezoso
        notify(msg, level=nivel)
    except Exception as exc:  # noqa: BLE001
        log.error("Notificación de umbral falló: %s", exc)


# ---------------------------------------------------------------------------
# Dashboard
# ---------------------------------------------------------------------------

def regenerate_dashboard() -> None:
    records = read_all_records()
    spend_usd = current_month_spend_usd()
    spend_eur = usd_to_eur(spend_usd)
    now = datetime.now(timezone.utc)

    by_month_usd: dict[str, float] = {}
    by_stage_usd: dict[str, float] = {}
    by_model: dict[str, dict] = {}
    for r in records:
        month = r.ts[:7]
        by_month_usd[month] = by_month_usd.get(month, 0) + r.cost_usd
        by_stage_usd[r.stage] = by_stage_usd.get(r.stage, 0) + r.cost_usd
        m = by_model.setdefault(r.model, {"in": 0, "out": 0, "cost_usd": 0.0})
        m["in"] += r.input_tokens
        m["out"] += r.output_tokens
        m["cost_usd"] += r.cost_usd

    total_usd = sum(r.cost_usd for r in records)
    soft_pct = (spend_eur / MONTHLY_SOFT_CAP_EUR * 100) if MONTHLY_SOFT_CAP_EUR else 0
    hard_pct = (spend_eur / MONTHLY_HARD_CAP_EUR * 100) if MONTHLY_HARD_CAP_EUR else 0

    lines: list[str] = []
    lines.append(f"# Control de costes — privado")
    lines.append("")
    lines.append(
        f"*Archivo privado. No se publica en la web. "
        f"Última actualización: {now.strftime('%Y-%m-%d %H:%M UTC')}*"
    )
    lines.append("")
    lines.append(f"Tipo de cambio interno: **1 USD = {USD_TO_EUR:.2f} EUR** "
                 f"(revisar cada 3 meses).")
    lines.append("")

    # Mes en curso
    lines.append("## Mes en curso")
    lines.append("")
    lines.append(f"- **Gastado {now.strftime('%Y-%m')}:** `{spend_eur:.2f} €` (`${spend_usd:.4f}` USD)")
    lines.append(f"- **Tope blando:** `{MONTHLY_SOFT_CAP_EUR:.2f} €` "
                 f"→ solo avisa por Telegram, sigue publicando")
    lines.append(f"- **Tope duro:** `{MONTHLY_HARD_CAP_EUR:.2f} €` "
                 f"→ corta el pipeline (protección runaway)")
    lines.append(f"- **Consumo vs blando:** `{soft_pct:.1f}%`")
    lines.append(f"- **Consumo vs duro:** `{hard_pct:.1f}%`")
    lines.append("")

    # Barra visual (respecto al tope duro)
    filled = min(int(hard_pct / 5), 20)
    bar = "█" * filled + "░" * (20 - filled)
    lines.append(f"```\n[{bar}] {hard_pct:.1f}% del tope duro\n```")
    lines.append("")

    # Capa actual
    current_layer = _current_layer(spend_eur)
    lines.append(f"**Capa actual:** {current_layer}")
    lines.append("")

    if by_month_usd:
        lines.append("## Histórico mensual")
        lines.append("")
        lines.append("| Mes | Gasto (€) | Gasto (USD) |")
        lines.append("|---|---|---|")
        for m in sorted(by_month_usd.keys(), reverse=True):
            eur = usd_to_eur(by_month_usd[m])
            lines.append(f"| {m} | {eur:.2f} € | ${by_month_usd[m]:.4f} |")
        lines.append(
            f"| **TOTAL** | **{usd_to_eur(total_usd):.2f} €** | **${total_usd:.4f}** |"
        )
        lines.append("")

    if by_stage_usd:
        lines.append("## Gasto por fase")
        lines.append("")
        lines.append("| Fase | Gasto (€) | % |")
        lines.append("|---|---|---|")
        for s in sorted(by_stage_usd.keys(), key=lambda k: -by_stage_usd[k]):
            pct = by_stage_usd[s] / total_usd * 100 if total_usd else 0
            lines.append(f"| {s} | {usd_to_eur(by_stage_usd[s]):.2f} € | {pct:.1f}% |")
        lines.append("")

    if by_model:
        lines.append("## Consumo por modelo")
        lines.append("")
        lines.append("| Modelo | Input tokens | Output tokens | Gasto (€) |")
        lines.append("|---|---|---|---|")
        for m in sorted(by_model.keys(), key=lambda k: -by_model[k]["cost_usd"]):
            d = by_model[m]
            lines.append(
                f"| `{m}` | {d['in']:,} | {d['out']:,} | {usd_to_eur(d['cost_usd']):.2f} € |"
            )
        lines.append("")

    if records:
        lines.append("## Últimas 20 llamadas")
        lines.append("")
        lines.append("| Fecha | Edición | Fase | Modelo | In | Out | € |")
        lines.append("|---|---|---|---|---|---|---|")
        for r in records[-20:][::-1]:
            lines.append(
                f"| {r.ts[:16].replace('T',' ')} | {r.edition} | {r.stage} "
                f"| `{r.model}` | {r.input_tokens:,} | {r.output_tokens:,} "
                f"| {usd_to_eur(r.cost_usd):.4f} € |"
            )
        lines.append("")

    lines.append("## Política de costes")
    lines.append("")
    lines.append(
        f"- **Tope blando ({MONTHLY_SOFT_CAP_EUR:.2f} €):** Telegram avisa, "
        f"pero el pipeline **sigue publicando la editorial**. "
        f"No se pierde informe por sobrecoste."
    )
    lines.append(
        f"- **Tope duro ({MONTHLY_HARD_CAP_EUR:.2f} €):** Telegram crítico + "
        f"**corte inmediato**. Protección real contra bugs o bucles runaway."
    )
    lines.append("")
    lines.append(
        f"Coste esperado (pivote documental + autoevaluación 3 niveles): "
        f"~9,86 €/mes. Tras afinar reparto de modelos y con corpus estable, "
        f"objetivo bajar a ~6-7 €/mes y reducir tope blando de vuelta a 8 €."
    )
    lines.append("")
    lines.append(
        f"Para cambiar topes: editar `MONTHLY_SOFT_CAP_EUR` y "
        f"`MONTHLY_HARD_CAP_EUR` en "
        f"[`src/costs.py`](https://github.com/otundra/ibiza-housing-radar/blob/main/src/costs.py)."
    )
    lines.append("")

    COSTS_MD.parent.mkdir(parents=True, exist_ok=True)
    COSTS_MD.write_text("\n".join(lines))
    log.info("Dashboard regenerado → %s", COSTS_MD)


def _current_layer(spend_eur: float) -> str:
    if spend_eur < 6.00:
        return "🟢 Verde (<6 €) — silencio"
    if spend_eur < 9.00:
        return "🟡 Amarilla (6-9 €) — FYI"
    if spend_eur < MONTHLY_SOFT_CAP_EUR:
        return "🟠 Naranja (9-12 €) — atención"
    if spend_eur < MONTHLY_HARD_CAP_EUR:
        return f"🔴 Roja blanda ({MONTHLY_SOFT_CAP_EUR:.0f}-{MONTHLY_HARD_CAP_EUR:.0f} €) — publica igual"
    return f"🚨 Roja dura (>{MONTHLY_HARD_CAP_EUR:.0f} €) — pipeline cortado"


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> int:
    logging.basicConfig(level=logging.INFO, format="[%(levelname)s %(name)s] %(message)s")
    regenerate_dashboard()
    print(json.dumps({
        "spend_current_month_eur": current_month_spend_eur(),
        "spend_current_month_usd": current_month_spend_usd(),
        "soft_cap_eur": MONTHLY_SOFT_CAP_EUR,
        "hard_cap_eur": MONTHLY_HARD_CAP_EUR,
    }, indent=2))
    return 0


if __name__ == "__main__":
    import sys

    sys.exit(main())
