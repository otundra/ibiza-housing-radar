"""Regenera la edición de una semana arbitraria con el prompt actual.

Útil durante el régimen de rodaje pre-lanzamiento (D21) para iterar formato
o contenido editorial sobre ediciones ya publicadas. Solo regenera el .md
de la edición; no toca proposals_history, balance, self_review ni costs.

Datos de entrada:
    - Si existe data/archive/{YYYY-WNN}/, los lee de ahí (semanas pasadas).
    - Si no, lee data/ raíz (semana en curso).

Uso:
    export ANTHROPIC_API_KEY=sk-ant-...
    python -m scripts.regen_week --week 2026-w17
    python -m scripts.regen_week --week 2026-w18

Coste por corrida: ~0,02 € (Opus 4.7 con caché de prompt activa).
"""
from __future__ import annotations

import argparse
import json
import logging
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from src import generate as gen  # noqa: E402

log = logging.getLogger("regen_week")


def parse_week(s: str) -> tuple[int, int]:
    m = re.match(r"^(\d{4})-[wW](\d{1,2})$", s.strip())
    if not m:
        raise ValueError(f"Formato esperado YYYY-wNN, recibido: {s}")
    return int(m.group(1)), int(m.group(2))


def iso_monday_utc(year: int, week: int) -> datetime:
    """Devuelve el lunes 05:00 UTC de la semana ISO indicada.

    Coincide con el horario real del cron (workflow weekly-report.yml,
    `cron: "0 5 * * 1"`) para que `date:` del frontmatter quede igual
    que la edición original.
    """
    d = datetime.fromisocalendar(year, week, 1)
    return d.replace(hour=5, minute=0, second=0, microsecond=0, tzinfo=timezone.utc)


def find_data_dir(year: int, week: int) -> tuple[Path, str]:
    archive_dir = ROOT / "data" / "archive" / f"{year}-W{week:02d}"
    if archive_dir.exists():
        return archive_dir, "archive"
    return ROOT / "data", "current"


def load_inputs(data_dir: Path) -> tuple[list, list, list]:
    classified_path = data_dir / "classified.json"
    extracted_path = data_dir / "extracted.json"
    rescue_path = data_dir / "rescue.json"

    classified = (
        json.loads(classified_path.read_text(encoding="utf-8"))
        if classified_path.exists() else []
    )
    extracted = (
        json.loads(extracted_path.read_text(encoding="utf-8"))
        if extracted_path.exists() else []
    )
    rescue = (
        json.loads(rescue_path.read_text(encoding="utf-8"))
        if rescue_path.exists() else []
    )
    return classified, extracted, rescue


def main() -> int:
    logging.basicConfig(level=logging.INFO, format="[%(levelname)s %(name)s] %(message)s")

    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--week", required=True, help="Semana ISO en formato YYYY-wNN (ej. 2026-w17)")
    args = parser.parse_args()

    year, week = parse_week(args.week)
    now = iso_monday_utc(year, week)
    edition = gen.iso_week_string(now)
    slug = gen.edition_slug(now)

    data_dir, source = find_data_dir(year, week)
    classified, extracted, rescue = load_inputs(data_dir)

    housing = [c for c in classified if c.get("is_housing")]

    log.info("Regenerando %s desde %s (%s)", slug, source, data_dir)
    log.info("Inputs: %d housing / %d extracted / %d rescue",
             len(housing), len(extracted), len(rescue))

    if len(housing) < 3:
        log.warning("Menos de 3 señales housing; escribiendo edición 'sin señal'.")
        text = gen.empty_edition(now)
    else:
        text = gen.generate(housing, extracted, rescue, now, edition=edition)

    edition_path = ROOT / "docs" / "_editions" / f"{slug}.md"
    edition_path.write_text(text)
    log.info("✅ Edición escrita: %s (%d caracteres)", edition_path, len(text))

    return 0


if __name__ == "__main__":
    sys.exit(main())
