"""Orquestador end-to-end: ingest → classify → generate → index → costs.

Se puede invocar a mano con:
    ANTHROPIC_API_KEY=... python src/report.py
"""
from __future__ import annotations

import logging
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

log = logging.getLogger("report")


def run(step: str) -> None:
    log.info("▶ %s", step)
    result = subprocess.run(
        [sys.executable, "-m", f"src.{step}"],
        cwd=ROOT,
        check=False,
    )
    if result.returncode != 0:
        raise SystemExit(f"Fase '{step}' falló con código {result.returncode}")


def main() -> int:
    logging.basicConfig(level=logging.INFO, format="[%(levelname)s %(name)s] %(message)s")
    run("ingest")
    run("classify")
    run("generate")
    run("build_index")
    run("costs")
    log.info("✅ Pipeline completo.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
