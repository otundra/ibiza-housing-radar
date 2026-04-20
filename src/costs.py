"""Control de costes de la API Anthropic.

- Registra cada llamada en data/costs.csv (append-only)
- Regenera docs/costs.md con dashboard legible
- Tope mensual configurable; si se supera, aborta
"""
from __future__ import annotations

import csv
import json
import logging
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path

log = logging.getLogger("costs")

ROOT = Path(__file__).resolve().parent.parent
COSTS_CSV = ROOT / "data" / "costs.csv"
COSTS_MD = ROOT / "docs" / "costs.md"

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

# Tope de gasto mensual en USD. Si se supera, el pipeline aborta.
MONTHLY_BUDGET_USD = 5.00


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
    cost_usd: float


def price_for(model: str) -> dict[str, float]:
    if model in PRICING:
        return PRICING[model]
    # Fallback: busca por prefijo
    for key, val in PRICING.items():
        if model.startswith(key):
            return val
    log.warning("Modelo sin tarifa registrada: %s — asumiendo Haiku.", model)
    return PRICING["claude-haiku-4-5"]


def compute_cost(model: str, usage: dict) -> float:
    """usage es el objeto `response.usage` (o dict con esos campos)."""
    p = price_for(model)
    inp = usage.get("input_tokens", 0) or 0
    out = usage.get("output_tokens", 0) or 0
    cache_read = usage.get("cache_read_input_tokens", 0) or 0
    # cache_creation tiene recargo (1.25x sobre input base)
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


def current_month_spend() -> float:
    now = datetime.now(timezone.utc)
    key = now.strftime("%Y-%m")
    total = 0.0
    for r in read_all_records():
        if r.ts.startswith(key):
            total += r.cost_usd
    return round(total, 4)


def assert_budget_available(planned_cost: float = 0.0) -> None:
    spent = current_month_spend()
    projected = spent + planned_cost
    if projected > MONTHLY_BUDGET_USD:
        raise RuntimeError(
            f"Presupuesto mensual excedido: gastado {spent:.4f} USD + "
            f"previsto {planned_cost:.4f} USD > tope {MONTHLY_BUDGET_USD} USD. "
            f"Revisa docs/costs.md y sube el tope si procede."
        )


def regenerate_dashboard() -> None:
    records = read_all_records()
    spend = current_month_spend()
    now = datetime.now(timezone.utc)

    # Agregados por mes
    by_month: dict[str, float] = {}
    by_stage: dict[str, float] = {}
    by_model: dict[str, dict] = {}
    for r in records:
        month = r.ts[:7]
        by_month[month] = by_month.get(month, 0) + r.cost_usd
        by_stage[r.stage] = by_stage.get(r.stage, 0) + r.cost_usd
        m = by_model.setdefault(r.model, {"in": 0, "out": 0, "cost": 0.0})
        m["in"] += r.input_tokens
        m["out"] += r.output_tokens
        m["cost"] += r.cost_usd

    total_cost = sum(r.cost_usd for r in records)
    budget_pct = (spend / MONTHLY_BUDGET_USD * 100) if MONTHLY_BUDGET_USD else 0

    lines: list[str] = []
    lines.append("---")
    lines.append("layout: default")
    lines.append("title: Costes")
    lines.append("permalink: /costes/")
    lines.append("---")
    lines.append("")
    lines.append("# Control de costes")
    lines.append("")
    lines.append(f"*Última actualización: {now.strftime('%Y-%m-%d %H:%M UTC')}*")
    lines.append("")
    lines.append("## Mes en curso")
    lines.append("")
    lines.append(f"- **Gastado {now.strftime('%Y-%m')}:** `${spend:.4f}` USD")
    lines.append(f"- **Tope mensual:** `${MONTHLY_BUDGET_USD:.2f}` USD")
    lines.append(f"- **Consumo:** `{budget_pct:.1f}%` del tope")
    lines.append("")

    # Barra visual
    filled = min(int(budget_pct / 5), 20)
    bar = "█" * filled + "░" * (20 - filled)
    lines.append(f"```\n[{bar}] {budget_pct:.1f}%\n```")
    lines.append("")

    if by_month:
        lines.append("## Histórico mensual")
        lines.append("")
        lines.append("| Mes | Gasto USD |")
        lines.append("|-----|-----------|")
        for m in sorted(by_month.keys(), reverse=True):
            lines.append(f"| {m} | ${by_month[m]:.4f} |")
        lines.append(f"| **TOTAL** | **${total_cost:.4f}** |")
        lines.append("")

    if by_stage:
        lines.append("## Gasto por fase")
        lines.append("")
        lines.append("| Fase | Gasto USD | % |")
        lines.append("|------|-----------|---|")
        for s in sorted(by_stage.keys(), key=lambda k: -by_stage[k]):
            pct = by_stage[s] / total_cost * 100 if total_cost else 0
            lines.append(f"| {s} | ${by_stage[s]:.4f} | {pct:.1f}% |")
        lines.append("")

    if by_model:
        lines.append("## Consumo por modelo")
        lines.append("")
        lines.append("| Modelo | Input tokens | Output tokens | Gasto USD |")
        lines.append("|--------|--------------|---------------|-----------|")
        for m in sorted(by_model.keys(), key=lambda k: -by_model[k]["cost"]):
            d = by_model[m]
            lines.append(
                f"| `{m}` | {d['in']:,} | {d['out']:,} | ${d['cost']:.4f} |"
            )
        lines.append("")

    if records:
        lines.append("## Últimas 20 llamadas")
        lines.append("")
        lines.append("| Fecha | Edición | Fase | Modelo | In | Out | USD |")
        lines.append("|-------|---------|------|--------|-----|-----|-----|")
        for r in records[-20:][::-1]:
            lines.append(
                f"| {r.ts[:16].replace('T',' ')} | {r.edition} | {r.stage} "
                f"| `{r.model}` | {r.input_tokens:,} | {r.output_tokens:,} "
                f"| ${r.cost_usd:.4f} |"
            )
        lines.append("")

    lines.append("## Política de costes")
    lines.append("")
    lines.append(
        f"Si el gasto mensual supera **${MONTHLY_BUDGET_USD:.2f} USD**, el "
        "pipeline aborta automáticamente antes de llamar a la API. "
        "Para subir el tope, editar `MONTHLY_BUDGET_USD` en "
        "[`src/costs.py`](https://github.com/otundra/ibiza-housing-radar/blob/main/src/costs.py)."
    )
    lines.append("")
    lines.append(
        "El sistema prioriza **Claude Haiku** para clasificación "
        "(~$0.01 por ejecución) y **Claude Opus** solo para generar el "
        "informe final (~$0.50 por ejecución). Coste esperado ≈ **$2/mes**."
    )
    lines.append("")

    COSTS_MD.parent.mkdir(parents=True, exist_ok=True)
    COSTS_MD.write_text("\n".join(lines))
    log.info("Dashboard regenerado → %s", COSTS_MD)


def main() -> int:
    logging.basicConfig(level=logging.INFO, format="[%(levelname)s %(name)s] %(message)s")
    regenerate_dashboard()
    print(json.dumps({"spend_current_month_usd": current_month_spend()}))
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
