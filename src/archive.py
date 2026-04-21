"""Archivado append-only del corpus semanal.

Tras cada ejecución exitosa del pipeline, copia las snapshots de datos crudos
(ingested, classified, extracted, rescue, verification_report) a
`data/archive/YYYY-wWW/` con timestamp. Los archivos originales en `data/`
se siguen sobrescribiendo semana a semana (formato temporal de trabajo); la
materia prima histórica queda preservada aquí para reinterpretación futura,
benchmarks y reprocesos.

Motivo (Fase 0.5, PI2-A): sin esto, cada semana se pisaba la anterior. Los
futuros análisis (grafo de evolución PI3, auditorías trimestrales, re-tests
de criterios editoriales) necesitan el corpus crudo archivado, no solo la
edición publicada.

Formato del directorio:
    data/archive/2026-W17/
    ├── ingested.json
    ├── classified.json
    ├── extracted.json
    ├── rescue.json
    ├── verification_report.json
    └── snapshot_meta.json   (timestamp, slug, gasto hasta el momento)

Uso:
    from src.archive import snapshot_to_archive
    snapshot_to_archive()  # deduce semana ISO del momento actual
"""
from __future__ import annotations

import json
import logging
import shutil
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
ARCHIVE_DIR = DATA_DIR / "archive"

# Archivos del pipeline que se snapshotan cada semana.
# Si alguno no existe en el momento del archivado, se salta con warning (no fallo).
SNAPSHOT_FILES: tuple[str, ...] = (
    "ingested.json",
    "classified.json",
    "extracted.json",
    "rescue.json",
    "verification_report.json",
)

log = logging.getLogger("archive")


def _iso_week_dir(when: datetime | None = None) -> Path:
    """Devuelve `data/archive/YYYY-WNN/` (crea si no existe)."""
    ref = when or datetime.now(timezone.utc)
    iso = ref.isocalendar()
    slug = f"{iso.year}-W{iso.week:02d}"
    path = ARCHIVE_DIR / slug
    path.mkdir(parents=True, exist_ok=True)
    return path


def snapshot_to_archive(when: datetime | None = None) -> Path:
    """Copia las snapshots del pipeline a `data/archive/YYYY-WNN/`.

    No toca los archivos originales. Si un archivo esperado no existe, lo
    registra y continúa. Genera `snapshot_meta.json` con contexto.

    Args:
        when: momento de referencia para la semana ISO. Por defecto, ahora.

    Returns:
        Path del directorio de archivo usado.
    """
    target_dir = _iso_week_dir(when)
    ts = (when or datetime.now(timezone.utc)).isoformat()

    copied: list[str] = []
    missing: list[str] = []

    for name in SNAPSHOT_FILES:
        src = DATA_DIR / name
        if not src.exists():
            missing.append(name)
            continue
        dst = target_dir / name
        shutil.copy2(src, dst)
        copied.append(name)

    meta = {
        "archived_at": ts,
        "week_iso": target_dir.name,
        "files_copied": copied,
        "files_missing": missing,
        "source_dir": str(DATA_DIR.relative_to(ROOT)),
    }

    # Intentar añadir gasto del mes si `costs.py` está disponible. No crítico.
    try:
        from src.costs import current_month_spend_eur  # type: ignore
        meta["month_spend_eur"] = round(current_month_spend_eur(), 4)
    except Exception as exc:  # noqa: BLE001
        log.debug("No se pudo adjuntar spend en meta: %s", exc)

    (target_dir / "snapshot_meta.json").write_text(
        json.dumps(meta, ensure_ascii=False, indent=2)
    )

    log.info(
        "Archive %s: %d archivos copiados (%s)%s",
        target_dir.name,
        len(copied),
        ", ".join(copied),
        f" · faltaron: {', '.join(missing)}" if missing else "",
    )
    return target_dir


def main() -> None:
    """CLI: ejecutable como `python -m src.archive`."""
    logging.basicConfig(level=logging.INFO, format="[%(levelname)s %(name)s] %(message)s")
    target = snapshot_to_archive()
    print(f"Snapshot archivado en: {target}")


if __name__ == "__main__":
    main()
