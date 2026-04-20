"""Selección de propuestas previas aún vigentes (sección «Rescate»).

Lee el histórico de propuestas documentadas y selecciona 3-5 candidatas
para que el generador elija 1-2 para la sección "Rescate" de la edición
semanal.

Criterios duros para candidato a rescate (determinista, sin LLM):
1. Estado ∈ {propuesta, en_movimiento, en_debate, aprobada}. No implementadas ni
   descartadas.
2. NO mencionada en ninguna de las últimas 4 ediciones.
3. Edad entre 2 y 16 semanas.

Ranking:
- Estado (propuesta > en_debate > aprobada > en_movimiento como tiebreak editorial).
- Recencia (bonus para edad ~8 semanas, el punto medio de la ventana).

Nota de diseño: en iteraciones futuras se puede añadir verificación de vigencia
con Haiku (¿la propuesta sigue viva según cobertura posterior?), pero por ahora
el rescate es puramente basado en reglas para ser 100% determinista y auditable.
"""
from __future__ import annotations

import json
import logging
import os
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

log = logging.getLogger("rescue")

ROOT = Path(__file__).resolve().parent.parent
HISTORY_FILE = ROOT / "data" / "proposals_history.json"
EDITIONS_DIR = ROOT / "docs" / "_editions"
OUT_FILE = ROOT / "data" / "rescue.json"

MAX_CANDIDATES = 5
MIN_AGE_WEEKS = 2
MAX_AGE_WEEKS = 16
RECENT_EDITIONS_WINDOW = 4

STATE_RANK = {
    "propuesta": 4,
    "en_debate": 3,
    "aprobada": 2,
    "en_movimiento": 1,
    "en_ejecucion": 0,
    "implementada": 0,
    "descartada": -10,
    "pendiente_resolucion_judicial": 0,
}


def load_history() -> list[dict]:
    if not HISTORY_FILE.exists():
        return []
    return json.loads(HISTORY_FILE.read_text())


def recent_edition_slugs(window: int = RECENT_EDITIONS_WINDOW) -> list[str]:
    """Devuelve los slugs de las últimas N ediciones publicadas."""
    if not EDITIONS_DIR.exists():
        return []
    files = sorted([p.stem for p in EDITIONS_DIR.glob("*.md")], reverse=True)
    return files[:window]


def prop_is_mentioned_recently(prop_id: str, recent_slugs: list[str]) -> bool:
    """Busca el id de la propuesta en los archivos de las últimas ediciones."""
    for slug in recent_slugs:
        path = EDITIONS_DIR / f"{slug}.md"
        if not path.exists():
            continue
        if prop_id in path.read_text():
            return True
    return False


def age_weeks(prop: dict) -> float:
    ts = prop.get("first_seen") or prop.get("published")
    if not ts:
        return 0.0
    try:
        dt = datetime.fromisoformat(ts.replace("Z", "+00:00"))
        delta = datetime.now(timezone.utc) - dt
        return delta.days / 7.0
    except Exception:  # noqa: BLE001
        return 0.0


def score_candidate(prop: dict) -> float:
    s = 0.0
    state = (prop.get("state") or "").lower()
    s += STATE_RANK.get(state, 0) * 2
    age = age_weeks(prop)
    # Bonus si la edad está cerca del punto medio (8 semanas)
    s += max(0.0, 5.0 - abs(age - 8.0) * 0.5)
    return s


def pick_candidates(history: list[dict], recent_slugs: list[str]) -> list[dict]:
    candidates: list[dict] = []

    for prop in history:
        state = (prop.get("state") or "").lower()
        if state in ("implementada", "descartada"):
            continue

        age = age_weeks(prop)
        if age < MIN_AGE_WEEKS or age > MAX_AGE_WEEKS:
            continue

        prop_id = prop.get("id")
        if not prop_id:
            continue

        if prop_is_mentioned_recently(prop_id, recent_slugs):
            continue

        candidate = dict(prop)
        candidate["_age_weeks"] = round(age, 1)
        candidate["_score"] = score_candidate(prop)
        candidates.append(candidate)

    # Ordenar por score descendente; desempate por menor recencia
    candidates.sort(key=lambda c: (-c["_score"], -c["_age_weeks"]))
    return candidates[:MAX_CANDIDATES]


def main() -> int:
    logging.basicConfig(level=logging.INFO, format="[%(levelname)s %(name)s] %(message)s")

    history = load_history()
    if not history:
        log.info("Sin histórico de propuestas — rescate vacío.")
        OUT_FILE.write_text(json.dumps([], ensure_ascii=False, indent=2))
        return 0

    recent = recent_edition_slugs()
    log.info("Últimas ediciones consultadas: %s", recent)

    candidates = pick_candidates(history, recent)
    log.info("Candidatas a rescate: %d", len(candidates))

    OUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    OUT_FILE.write_text(json.dumps(candidates, ensure_ascii=False, indent=2))
    log.info("Escrito %s", OUT_FILE)
    return 0


if __name__ == "__main__":
    sys.exit(main())
