"""Orquestador end-to-end del pipeline documental.

Flujo:
    ingest → classify → extract → rescue → audit → generate → verify →
        (si OK) append_history → balance → self_review → build_index → costs

El paso ``audit`` (DISENO-AUDITOR-MVP.md §6.2) escribe un JSON por propuesta
en ``data/audit/{edition}/`` con la 2ª lectura ciega + comparador +
heurísticas + bloque ``signals``. En el MVP, el badge público (tier) queda
en ``null``; el bloque se rellena para que ``compute_tier()`` real (PI10)
sólo tenga que leerlo.

Si `verify` encuentra fallos bloqueantes, se ELIMINA la edición recién
generada y se aborta la publicación con alerta crítica. El editor verá
la alerta en Telegram y en el log; no se publica nada roto.

Invocación:
    ANTHROPIC_API_KEY=... python -m src.report

Al terminar envía resumen por Telegram (vía `src.notify`). Si el pipeline
lanza excepción, envía alerta crítica y re-lanza.
"""
from __future__ import annotations

import json
import logging
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EDITIONS_DIR = ROOT / "docs" / "_editions"
EXTRACTED_FILE = ROOT / "data" / "extracted.json"
HISTORY_FILE = ROOT / "data" / "proposals_history.json"

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


def _edition_slug() -> str:
    iso = datetime.now(timezone.utc).isocalendar()
    return f"{iso.year}-w{iso.week:02d}"


def current_edition_path() -> Path:
    return EDITIONS_DIR / f"{_edition_slug()}.md"


def run_verify(edition_path: Path) -> int:
    log.info("▶ verify sobre %s", edition_path.name)
    result = subprocess.run(
        [sys.executable, "-m", "src.verify", str(edition_path)],
        cwd=ROOT,
        check=False,
    )
    return result.returncode


def append_to_history() -> None:
    """Añade las propuestas recién extraídas al histórico (dedup por url_source+actor)."""
    if not EXTRACTED_FILE.exists():
        return
    extracted = json.loads(EXTRACTED_FILE.read_text())

    history: list[dict] = []
    if HISTORY_FILE.exists():
        history = json.loads(HISTORY_FILE.read_text())

    existing_keys = {
        (p.get("url_source", ""), p.get("actor", ""))
        for p in history
    }

    now_iso = datetime.now(timezone.utc).isoformat()
    added = 0
    week = _iso_week()

    for item in extracted:
        for prop in item.get("proposals", []):
            key = (prop.get("url_source", ""), prop.get("actor", ""))
            if key in existing_keys:
                continue
            enriched = dict(prop)
            enriched["id"] = f"{_edition_slug()}-{len(history) + added + 1:03d}"
            enriched["first_seen"] = now_iso
            enriched["first_seen_edition"] = week
            history.append(enriched)
            existing_keys.add(key)
            added += 1

    HISTORY_FILE.parent.mkdir(parents=True, exist_ok=True)
    HISTORY_FILE.write_text(json.dumps(history, ensure_ascii=False, indent=2))
    log.info("proposals_history.json: +%d (total %d)", added, len(history))


def _edition_summary_stats() -> dict:
    """Cuenta ligera sobre la edición recién publicada.

    Extrae lo que se puede computar sin parsear markdown:
    - Nº propuestas y actores distintos de `extracted.json`.
    - URL pública de la edición en GitHub Pages.

    Datos pendientes (TODO, se añaden cuando los módulos upstream los emitan):
    - Nº señales / omisiones / rescate (requieren parseo del markdown o que
      `generate.py` emita un summary JSON al publicar).
    - Estado del balance trimestral (🟢/🟡/🟠/🔴) — cuando `balance.py` lo
      escriba en `data/balance_status.json`.
    - Nº propuestas en cuarentena — cuando exista el tier system.
    - Nº emails sin responder en /contacto/ — cuando haya integración.
    """
    stats: dict = {
        "edition_slug": _edition_slug(),
        "public_url": (
            "https://otundra.github.io/ibiza-housing-radar/"
            f"ediciones/{_edition_slug()}/"
        ),
    }

    if EXTRACTED_FILE.exists():
        try:
            extracted = json.loads(EXTRACTED_FILE.read_text())
            all_proposals = [
                p for item in extracted for p in item.get("proposals", [])
            ]
            actors = sorted({
                p.get("actor", "").strip()
                for p in all_proposals
                if p.get("actor")
            })
            stats["proposals_count"] = len(all_proposals)
            stats["actors"] = actors
        except Exception as exc:  # noqa: BLE001
            log.debug("No se pudieron leer stats de extracted.json: %s", exc)

    return stats


def _build_alerts_block() -> str:
    """Bloque ⚠ con avisos proactivos. Vacío si no hay nada que reportar.

    Fuentes (a medida que existan):
    - `data/balance_status.json` para alertas de imparcialidad.
    - `data/quarantine.json` para propuestas en cuarentena.
    - Email inbox (futuro, cuando integremos el buzón).

    Por ahora devuelve cadena vacía — el bloque solo aparecerá cuando alguna
    de estas fuentes emita datos.
    """
    alerts: list[str] = []

    # Balance trimestral (placeholder; activar cuando balance.py escriba status)
    balance_status_file = ROOT / "data" / "balance_status.json"
    if balance_status_file.exists():
        try:
            status = json.loads(balance_status_file.read_text())
            if status.get("alert_level") in {"warning", "critical"}:
                alerts.append(
                    f"• Balance trimestral: {status.get('label', 'revisar')}"
                )
        except Exception:  # noqa: BLE001
            pass

    # Cuarentena (placeholder; activar cuando exista el tier system)
    quarantine_file = ROOT / "data" / "quarantine.json"
    if quarantine_file.exists():
        try:
            q = json.loads(quarantine_file.read_text())
            count = len(q) if isinstance(q, list) else 0
            if count > 0:
                alerts.append(
                    f"• {count} propuesta{'s' if count != 1 else ''} en "
                    f"cuarentena (baja confianza)"
                )
        except Exception:  # noqa: BLE001
            pass

    if not alerts:
        return ""

    return "\n\n⚠ *Atención esta semana:*\n" + "\n".join(alerts)


def _build_summary(success: bool, error: str | None = None) -> tuple[str, str]:
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
        stats = _edition_summary_stats()
        actors_line = ""
        counts_line = ""

        if "proposals_count" in stats:
            counts_line = f"\n• {stats['proposals_count']} propuestas extraídas"
        if stats.get("actors"):
            # Cap a 6 actores para no saturar el mensaje de Telegram
            shown = stats["actors"][:6]
            suffix = f" · +{len(stats['actors']) - 6}" if len(stats["actors"]) > 6 else ""
            actors_line = f"\n• Actores: {', '.join(shown)}{suffix}"

        alerts_block = _build_alerts_block()

        msg = (
            f"📡 *Radar Vivienda Ibiza — {week}*\n"
            f"{stats['public_url']}\n"
            f"{counts_line}"
            f"{actors_line}\n"
            f"\nPipeline OK · Gasto {month}: *{spend_eur:.2f} €* · Capa: {layer}"
            f"{alerts_block}"
        )
        return msg, "ok"

    msg = (
        f"*Radar Vivienda Ibiza — {week}: FALLO*\n"
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
        run("extract")
        run("rescue")
        run("audit")
        run("generate")

        # Verificar la edición antes de publicar. Si falla, la borramos.
        edition_path = current_edition_path()
        if not edition_path.exists():
            raise RuntimeError(f"generate.py no produjo edición en {edition_path}")

        verify_rc = run_verify(edition_path)
        if verify_rc != 0:
            log.error("Verificación bloqueante. Eliminando edición %s.", edition_path.name)
            try:
                edition_path.unlink()
            except Exception as exc:  # noqa: BLE001
                log.error("No pude eliminar la edición rota: %s", exc)
            raise RuntimeError("verify falló; edición eliminada para no publicar contenido roto.")

        # Publicable: persistir al histórico, archivar snapshot crudo y regenerar derivados
        append_to_history()
        try:
            from src.archive import snapshot_to_archive
            snapshot_to_archive()
        except Exception as exc:  # noqa: BLE001
            # El archivado nunca debe tumbar el pipeline; solo logueamos.
            log.error("Archive falló (no bloqueante): %s", exc)
        run("balance")
        run("self_review")
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
