"""Orquestador end-to-end: ingest → classify → generate → index → costs.

Se puede invocar a mano con:
    ANTHROPIC_API_KEY=... python -m src.report

Al terminar envía resumen por Telegram (vía `src.notify`). Si el pipeline
lanza excepción, envía alerta crítica y re-lanza para que Actions marque
el workflow como fallido.
"""
from __future__ import annotations

import logging
import subprocess
import sys
from datetime import datetime, timezone
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
        raise RuntimeError(f"Fase '{step}' falló con código {result.returncode}")


def _iso_week() -> str:
    iso = datetime.now(timezone.utc).isocalendar()
    return f"{iso.year}-W{iso.week:02d}"


def _build_summary(success: bool, error: str | None = None) -> tuple[str, str]:
    """Construye (mensaje, nivel) del resumen para Telegram."""
    from src.costs import (
        MONTHLY_HARD_CAP_EUR,
        MONTHLY_SOFT_CAP_EUR,
        current_month_spend_eur,
        _current_layer,
    )

    spend_eur = current_month_spend_eur()
    layer = _current_layer(spend_eur)
    week = _iso_week()
    month = datetime.now(timezone.utc).strftime("%Y-%m")

    if success:
        msg = (
            f"*Ibiza Housing Radar — {week}*\n"
            f"Pipeline OK. Edición publicada.\n"
            f"Gasto {month}: *{spend_eur:.2f} €* "
            f"(blando {MONTHLY_SOFT_CAP_EUR:.0f} € / duro {MONTHLY_HARD_CAP_EUR:.0f} €).\n"
            f"Capa: {layer}"
        )
        return msg, "ok"

    msg = (
        f"*Ibiza Housing Radar — {week}: FALLO*\n"
        f"Pipeline abortado con error:\n```\n{error}\n```\n"
        f"Gasto {month} hasta el fallo: *{spend_eur:.2f} €*.\n"
        f"Revisar workflow en GitHub Actions."
    )
    return msg, "critical"


def main() -> int:
    logging.basicConfig(level=logging.INFO, format="[%(levelname)s %(name)s] %(message)s")
    try:
        run("ingest")
        run("classify")
        run("generate")
        run("build_index")
        run("costs")
    except Exception as exc:  # noqa: BLE001
        log.error("Pipeline falló: %s", exc)
        try:
            from src.notify import notify
            msg, level = _build_summary(success=False, error=str(exc))
            notify(msg, level=level)
        except Exception as nexc:  # noqa: BLE001
            log.error("Además falló la notificación: %s", nexc)
        raise

    log.info("✅ Pipeline completo.")
    try:
        from src.notify import notify
        msg, level = _build_summary(success=True)
        notify(msg, level=level)
    except Exception as nexc:  # noqa: BLE001
        log.error("Resumen por Telegram no se pudo enviar: %s", nexc)
    return 0


if __name__ == "__main__":
    sys.exit(main())
