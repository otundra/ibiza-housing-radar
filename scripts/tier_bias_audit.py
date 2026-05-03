"""Auditoría de sesgo de tiers por tipo de actor.

Lee todos los registros de data/audit/*/*.json, calcula la distribución
de tiers (verde / amarillo / naranja / rojo) por actor_type y aplica el
test de sesgo definido en ESTUDIO-TIERS.md §8.2.

Uso:
    python scripts/tier_bias_audit.py
    python scripts/tier_bias_audit.py --min-n 3   # umbral mínimo de propuestas
    python scripts/tier_bias_audit.py --json       # salida JSON en vez de tabla

Salida:
    Tabla por actor_type con recuentos y proporciones.
    Marcadores 🔴/🟡/✅ según los umbrales de alerta de §8.2.
    Línea de diagnóstico: sesgo confirmado / nota metodológica / OK.
"""
from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
AUDIT_DIR = ROOT / "data" / "audit"

ACTOR_TYPES = [
    "institucional_publico",
    "partido",
    "sindicato",
    "patronal",
    "tercer_sector",
    "colectivo_ciudadano",
    "academico",
    "judicial",
    "otro",
]

TIER_VALUES = ["verde", "amarillo", "naranja", "rojo"]

# Umbrales de alerta (ESTUDIO-TIERS.md §8.2)
UMBRAL_OK = 0.65        # ≥ 65 % del promedio global → OK
UMBRAL_NOTA = 0.50      # 50–65 % → nota metodológica
# < 50 % → mitigación obligatoria


def load_records() -> list[dict]:
    """Lee todos los JSON de data/audit/*/*.json."""
    records = []
    if not AUDIT_DIR.exists():
        return records
    for path in sorted(AUDIT_DIR.glob("*/*.json")):
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            records.append(data)
        except (json.JSONDecodeError, OSError):
            print(f"⚠  No se pudo leer {path.name}", file=sys.stderr)
    return records


def extract_fields(record: dict) -> tuple[str | None, str | None]:
    """Devuelve (tier_value, actor_type) del registro."""
    tier = record.get("tier") or {}
    # Soporta {value: ...} directo o {current: ...} (formato con historial)
    tier_value = tier.get("value") or tier.get("current")

    # actor_type vive en la extracción primaria de Haiku
    haiku_proposal = (
        (record.get("layers") or {})
        .get("haiku", {})
        .get("proposal") or {}
    )
    actor_type = haiku_proposal.get("actor_type")

    return tier_value, actor_type


def compute_distribution(records: list[dict]) -> dict[str, dict[str, int]]:
    """Devuelve {actor_type: {tier: count}}."""
    dist: dict[str, dict[str, int]] = defaultdict(lambda: defaultdict(int))
    for rec in records:
        tier_value, actor_type = extract_fields(rec)
        if not tier_value or tier_value not in TIER_VALUES:
            continue
        key = actor_type if actor_type in ACTOR_TYPES else "otro"
        dist[key][tier_value] += 1
    return {k: dict(v) for k, v in dist.items()}


def run_bias_test(
    dist: dict[str, dict[str, int]],
    min_n: int,
) -> dict:
    """Aplica el test de sesgo de §8.2. Devuelve resultados por actor_type."""
    global_verde = sum(v.get("verde", 0) for v in dist.values())
    global_total = sum(sum(v.values()) for v in dist.values())
    global_rate = global_verde / global_total if global_total else 0.0

    results = {}
    for at, counts in dist.items():
        n = sum(counts.values())
        n_verde = counts.get("verde", 0)
        rate = n_verde / n if n else 0.0
        ratio = rate / global_rate if global_rate else None

        if n < min_n or ratio is None:
            status = "⚪ insuficiente"
        elif ratio >= UMBRAL_OK:
            status = "✅ OK"
        elif ratio >= UMBRAL_NOTA:
            status = "🟡 nota metodológica"
        else:
            status = "🔴 mitigación obligatoria"

        results[at] = {
            "n": n,
            "verde": n_verde,
            "amarillo": counts.get("amarillo", 0),
            "naranja": counts.get("naranja", 0),
            "rojo": counts.get("rojo", 0),
            "rate_verde": rate,
            "ratio_vs_global": ratio,
            "status": status,
        }
    return results, global_rate, global_total


def print_table(results: dict, global_rate: float, global_total: int) -> None:
    header = f"{'Tipo de actor':<28} {'N':>4} {'🟢':>5} {'🟡':>5} {'🟠':>5} {'🔴':>5} {'%verde':>7} {'ratio':>6}  Estado"
    print(header)
    print("─" * len(header))
    for at in sorted(results, key=lambda x: results[x]["n"], reverse=True):
        r = results[at]
        ratio_str = f"{r['ratio_vs_global']:.2f}" if r["ratio_vs_global"] is not None else "  —  "
        print(
            f"{at:<28} {r['n']:>4} {r['verde']:>5} {r['amarillo']:>5} "
            f"{r['naranja']:>5} {r['rojo']:>5} "
            f"{r['rate_verde']:>6.1%} {ratio_str:>6}  {r['status']}"
        )
    print("─" * len(header))
    print(f"{'GLOBAL':<28} {global_total:>4}  —     —     —     —   {global_rate:>6.1%}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--min-n", type=int, default=5,
        help="Mínimo de propuestas por actor_type para aplicar el test (default: 5)",
    )
    parser.add_argument(
        "--json", action="store_true", dest="as_json",
        help="Salida en formato JSON",
    )
    args = parser.parse_args()

    records = load_records()
    if not records:
        print(
            "⚠  No se encontraron registros en data/audit/.\n"
            "   El script se ejecuta sobre datos reales del pipeline.\n"
            "   Espera a tener al menos 3-4 ediciones auditadas (W19-W22).",
            file=sys.stderr,
        )
        sys.exit(0)

    dist = compute_distribution(records)
    results, global_rate, global_total = run_bias_test(dist, args.min_n)

    if args.as_json:
        out = {
            "global_rate_verde": global_rate,
            "global_total": global_total,
            "min_n": args.min_n,
            "by_actor_type": results,
        }
        print(json.dumps(out, ensure_ascii=False, indent=2))
        return

    print(f"\n── Auditoría de sesgo de tiers por tipo de actor ──────────────────")
    print(f"   Registros analizados: {global_total}  ·  tasa verde global: {global_rate:.1%}")
    print(f"   Umbral mínimo de propuestas por tipo: {args.min_n}\n")
    print_table(results, global_rate, global_total)

    flagged = [at for at, r in results.items() if "🔴" in r["status"]]
    nota = [at for at, r in results.items() if "🟡" in r["status"]]

    print()
    if flagged:
        print(f"🔴 Sesgo confirmado en: {', '.join(flagged)}")
        print("   → Activar mitigación M1 (ESTUDIO-TIERS.md §8.3) para esas categorías.")
    elif nota:
        print(f"🟡 Nota metodológica recomendada para: {', '.join(nota)}")
        print("   → Añadir explicación en /metodo/#tiers sobre sesgo de cobertura mediática.")
    else:
        print("✅ Sin sesgo significativo detectado con los datos actuales.")


if __name__ == "__main__":
    main()
