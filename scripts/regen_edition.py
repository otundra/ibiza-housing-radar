"""Regenera la edición actual sin volver a ingestar ni reclasificar.

Útil para iterar sobre el prompt de `generate.py` (o mejoras en `extract.py`)
sin gastar API en ingest/classify que no cambian.

Flujo:
    extract → rescue → generate → verify → (si OK) append_history → balance → self_review

Asume que existe data/classified.json de una ejecución previa.

Uso:
    export ANTHROPIC_API_KEY=sk-ant-...
    python -m scripts.regen_edition
"""
from __future__ import annotations

import json
import logging
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

log = logging.getLogger("regen")

ROOT = Path(__file__).resolve().parent.parent
CLASSIFIED = ROOT / "data" / "classified.json"
EDITIONS_DIR = ROOT / "docs" / "_editions"


def run(step: str) -> None:
    log.info("▶ %s", step)
    result = subprocess.run(
        [sys.executable, "-m", f"src.{step}"],
        cwd=ROOT,
        check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(f"Fase '{step}' falló con código {result.returncode}")


def _edition_slug() -> str:
    iso = datetime.now(timezone.utc).isocalendar()
    return f"{iso.year}-w{iso.week:02d}"


def main() -> int:
    logging.basicConfig(level=logging.INFO, format="[%(levelname)s %(name)s] %(message)s")

    if not os.environ.get("ANTHROPIC_API_KEY"):
        log.error("ANTHROPIC_API_KEY no definida.")
        return 2

    if not CLASSIFIED.exists():
        log.error(
            "Falta %s. Ejecuta primero `python -m src.report` para generar "
            "data/classified.json, luego puedes usar este script para iterar.",
            CLASSIFIED,
        )
        return 3

    try:
        run("extract")
        run("rescue")
        run("generate")

        edition_path = EDITIONS_DIR / f"{_edition_slug()}.md"
        if not edition_path.exists():
            raise RuntimeError(f"generate.py no produjo edición en {edition_path}")

        # Verify — si falla, la borramos
        verify_rc = subprocess.run(
            [sys.executable, "-m", "src.verify", str(edition_path)],
            cwd=ROOT, check=False,
        ).returncode
        if verify_rc != 0:
            log.error("Verificación bloqueante. Eliminando edición.")
            try:
                edition_path.unlink()
            except Exception as exc:  # noqa: BLE001
                log.error("No pude eliminar: %s", exc)
            raise RuntimeError("verify falló; edición eliminada.")

        # Append history + derivados
        from src.report import append_to_history
        append_to_history()
        run("balance")
        run("self_review")
    except Exception as exc:  # noqa: BLE001
        log.error("Regeneración falló: %s", exc)
        return 1

    log.info("✅ Regeneración completa. Edición: %s", EDITIONS_DIR / f"{_edition_slug()}.md")
    log.info("Self-review: private/self-review/%s.md", _edition_slug())
    return 0


if __name__ == "__main__":
    sys.exit(main())
