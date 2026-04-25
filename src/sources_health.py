"""Salud de las fuentes RSS — registro append-only + alertas proactivas.

Filosofía: el pipeline no debe perder editorial por un fallo de fuente,
pero tampoco debe ignorar señales de degradación silenciosa. Si un RSS
deja de publicar, baja la frecuencia o cambia de estructura, queremos
saberlo antes de que afecte la cobertura del observatorio.

Diseño:
- Histórico append-only en `data/feed_health.json` (lista de runs).
- Cada run guarda fecha y métricas por feed (estado, entradas totales,
  entradas que pasan keywords, entradas dentro de la ventana, excepción).
- El histórico solo se escribe cuando `GITHUB_ACTIONS=true`. Las
  ejecuciones locales no contaminan los datos de producción.
- `evaluate_alerts(history)` es una función pura que devuelve mensajes
  legibles para Telegram. Sin I/O.

Reglas de alerta (calibrables tras ver datos reales):
- Feed muerto: dos ejecuciones seguidas con estado distinto a "ok".
- Frecuencia caída: media de noticias en ventana cae más del 50 %
  respecto a las cuatro ejecuciones anteriores.
- Vacío inesperado: estado "ok" pero cero noticias, con base ≥5.
- Estructura cambiada: estado "malformed" cuando antes estaba "ok".
"""
from __future__ import annotations

import json
import logging
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Final

log = logging.getLogger("sources_health")

ROOT = Path(__file__).resolve().parent.parent
HISTORY_FILE = ROOT / "data" / "feed_health.json"

DEAD_FEED_CONSECUTIVE_RUNS: Final[int] = 2
FREQUENCY_DROP_RATIO: Final[float] = 0.5
FREQUENCY_DROP_BASELINE_RUNS: Final[int] = 4
EMPTY_BASELINE_MIN: Final[float] = 5.0


def _is_in_actions() -> bool:
    return os.environ.get("GITHUB_ACTIONS", "").lower() == "true"


def _load_history() -> list[dict[str, Any]]:
    if not HISTORY_FILE.exists():
        return []
    try:
        data = json.loads(HISTORY_FILE.read_text())
        if isinstance(data, list):
            return data
        log.warning("Formato inesperado en %s; ignorando histórico previo.", HISTORY_FILE)
        return []
    except Exception as exc:  # noqa: BLE001
        log.warning("No se pudo leer %s: %s", HISTORY_FILE, exc)
        return []


def record_run(feed_metrics: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Devuelve el histórico actualizado en memoria. Solo escribe en Actions.

    `feed_metrics` es una lista con una entrada por feed con estos campos:
      name, status (ok|malformed|error), entries_total, entries_kept,
      entries_in_window, exception (str|None).

    Devuelve el histórico ya con la ejecución actual al final, para que el
    caller pueda pasarlo directo a `evaluate_alerts()` sin releer.
    """
    history = _load_history()
    history.append({
        "ts": datetime.now(timezone.utc).isoformat(),
        "feeds": feed_metrics,
    })

    if not _is_in_actions():
        log.info("Ejecución local — feed_health.json no se actualiza en disco.")
        return history

    HISTORY_FILE.parent.mkdir(parents=True, exist_ok=True)
    HISTORY_FILE.write_text(json.dumps(history, ensure_ascii=False, indent=2))
    log.info(
        "Salud de feeds registrada → %s (%d runs en histórico).",
        HISTORY_FILE, len(history),
    )
    return history


def _runs_for_feed(history: list[dict[str, Any]], name: str) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for run in history:
        for feed in run.get("feeds", []):
            if feed.get("name") == name:
                out.append(feed)
                break
    return out


def evaluate_alerts(history: list[dict[str, Any]]) -> list[str]:
    """Compara la última ejecución con las anteriores y devuelve mensajes humanos.

    Función pura: no toca disco ni red. El caller decide qué hacer con la
    lista (mandar por Telegram, loguear, ignorar). Devuelve [] si todo va bien.
    """
    if not history:
        return []

    latest = history[-1]
    alerts: list[str] = []

    for feed in latest.get("feeds", []):
        name = feed.get("name", "?")
        status = feed.get("status")
        in_window = feed.get("entries_in_window", 0)
        runs = _runs_for_feed(history, name)

        if len(runs) >= DEAD_FEED_CONSECUTIVE_RUNS:
            recent = runs[-DEAD_FEED_CONSECUTIVE_RUNS:]
            if all(r.get("status") != "ok" for r in recent):
                last_exc = feed.get("exception") or "estado no-ok"
                alerts.append(
                    f"Fuente caída · {name}: "
                    f"{DEAD_FEED_CONSECUTIVE_RUNS} ejecuciones seguidas con fallo ({last_exc})"
                )

        if status == "malformed" and len(runs) >= 2:
            prev_status = runs[-2].get("status")
            if prev_status == "ok":
                alerts.append(
                    f"Estructura cambiada · {name}: el feed se ha corrompido (antes funcionaba)"
                )

        if status == "ok" and len(runs) > FREQUENCY_DROP_BASELINE_RUNS:
            baseline = runs[-(FREQUENCY_DROP_BASELINE_RUNS + 1):-1]
            baseline_ok = [r for r in baseline if r.get("status") == "ok"]
            if len(baseline_ok) >= FREQUENCY_DROP_BASELINE_RUNS:
                avg = sum(r.get("entries_in_window", 0) for r in baseline_ok) / len(baseline_ok)
                if avg >= 1 and in_window < avg * FREQUENCY_DROP_RATIO:
                    alerts.append(
                        f"Bajada de noticias · {name}: "
                        f"{in_window} en ventana (media previa: {avg:.1f})"
                    )

        if status == "ok" and in_window == 0 and len(runs) > 1:
            prior_ok = [r for r in runs[:-1] if r.get("status") == "ok"]
            if prior_ok:
                avg = sum(r.get("entries_in_window", 0) for r in prior_ok) / len(prior_ok)
                if avg >= EMPTY_BASELINE_MIN:
                    alerts.append(
                        f"Sin noticias · {name}: "
                        f"0 en ventana (media previa: {avg:.1f})"
                    )

    return alerts


def main() -> int:
    """Smoke test manual: `python -m src.sources_health`. Inspecciona el histórico."""
    logging.basicConfig(level=logging.INFO, format="[%(levelname)s %(name)s] %(message)s")
    history = _load_history()
    log.info("Runs en histórico: %d", len(history))
    alerts = evaluate_alerts(history)
    if alerts:
        log.warning("Alertas pendientes en el último run:")
        for a in alerts:
            log.warning("  - %s", a)
    else:
        log.info("Sin alertas activas.")
    return 0


if __name__ == "__main__":
    import sys

    sys.exit(main())
