"""Orquestador del benchmark completo.

Ejecuta en orden, sin posibilidad de desajuste:
1. `generate_gold.py` — si no existe gold_auto o se fuerza con --regen-gold.
2. `run_benchmark.py` — siempre, contra el gold auto más reciente.

Es el comando recomendado para el editor. Los scripts individuales quedan
como de bajo nivel para casos especiales (debug, solo gold, solo bench).

Uso:
    export ANTHROPIC_API_KEY=sk-ant-...
    python -m scripts.bench_full

Opciones:
    --regen-gold     Regenera el gold aunque exista (coste extra ~0,80 €).
    --skip-gold      No toca el gold existente (útil si solo quieres re-benchmarkar).
    --dry-run        Muestra qué haría sin llamar a la API.

Protección: si no se detecta ANTHROPIC_API_KEY, no ejecuta.
"""
from __future__ import annotations

import argparse
import json
import logging
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

log = logging.getLogger("bench-full")

ROOT = Path(__file__).resolve().parent.parent
GOLD_AUTO = ROOT / "data" / "bench" / "gold_auto_v1.json"
DATASET = ROOT / "data" / "bench" / "dataset_v1.json"


def gold_status() -> tuple[bool, str]:
    """Devuelve (existe, mensaje explicativo)."""
    if not GOLD_AUTO.exists():
        return False, "gold_auto_v1.json NO existe — hay que generarlo."
    try:
        data = json.loads(GOLD_AUTO.read_text())
        meta = data.get("_metadata", {})
        ts = meta.get("timestamp", "desconocido")
        items = sum(1 for k in data if not k.startswith("_"))
        return True, f"gold_auto_v1.json existe — {items} items, generado {ts}"
    except Exception as exc:  # noqa: BLE001
        return False, f"gold_auto_v1.json existe pero no parseable: {exc}"


def run_step(name: str, cmd: list[str], dry_run: bool) -> int:
    log.info("=== %s ===", name)
    log.info("Comando: %s", " ".join(cmd))
    if dry_run:
        log.info("(dry-run; no se ejecuta)")
        return 0
    result = subprocess.run(cmd)
    if result.returncode != 0:
        log.error("Paso %s falló con código %d. Abortando.", name, result.returncode)
    return result.returncode


def main() -> int:
    logging.basicConfig(level=logging.INFO, format="[%(levelname)s %(name)s] %(message)s")
    parser = argparse.ArgumentParser()
    parser.add_argument("--regen-gold", action="store_true",
                        help="Regenera gold aunque exista (coste ~0,80 €).")
    parser.add_argument("--skip-gold", action="store_true",
                        help="No toca gold. Usa el existente (o aborta si no hay).")
    parser.add_argument("--dry-run", action="store_true",
                        help="Muestra qué haría sin ejecutar.")
    args = parser.parse_args()

    if not args.dry_run and not os.environ.get("ANTHROPIC_API_KEY"):
        log.error("ANTHROPIC_API_KEY no definida en el entorno. Abortando.")
        return 2

    exists, status_msg = gold_status()
    log.info("Estado del gold: %s", status_msg)

    # Decidir si regenerar
    regen = args.regen_gold or (not exists and not args.skip_gold)
    if args.skip_gold and not exists:
        log.error("--skip-gold pero no hay gold_auto_v1.json. Abortando.")
        return 3

    started = datetime.now(timezone.utc)

    if regen:
        rc = run_step("Paso 1/2 — generar gold (Opus thinking + Sonnet validador)",
                      [sys.executable, "-m", "scripts.generate_gold"], args.dry_run)
        if rc != 0:
            return rc

    rc = run_step("Paso 2/2 — benchmark 3 modelos contra gold auto",
                  [sys.executable, "-m", "scripts.run_benchmark"], args.dry_run)
    if rc != 0:
        return rc

    dt = datetime.now(timezone.utc) - started
    log.info("=== COMPLETADO en %.1fs ===", dt.total_seconds())
    log.info("Resultados: data/bench/results_v1.json")
    log.info("Informe: REPORTE-BENCHMARK.md")
    return 0


if __name__ == "__main__":
    sys.exit(main())
