"""Vigilancia de fechas de revisión de decisiones del proyecto.

Lee `DECISIONES.md`, extrae el campo `Próxima revisión`, y si alguna
decisión vigente está vencida o próxima (ventana de 7 días), manda un
aviso por Telegram vía `src.notify`.

Desde 2026-05-05 (D24) también vigila el disparo de la **auditoría
sistémica trimestral**: lee `data/auditorias.csv` y avisa cuando han
pasado ≥90 días desde la última auditoría o han aparecido ≥5
decisiones nuevas desde la última.

Reutiliza los extractores de `src.panel` para no duplicar la lógica de
parseo.

Se ejecuta cada lunes en el workflow `weekly-report` antes de generar la
edición. Registrado como parte de las decisiones D14 y D24.

Uso:
    python -m src.decisions_watch
"""
from __future__ import annotations

import csv
import logging
import re
from datetime import date, datetime
from pathlib import Path

from src.panel import _classify, _extract_decisions_with_review

log = logging.getLogger("decisions_watch")

ROOT = Path(__file__).resolve().parent.parent
DECISIONES_MD = ROOT / "DECISIONES.md"
AUDITORIAS_CSV = ROOT / "data" / "auditorias.csv"

# Disparadores de la auditoría sistémica (D24).
SYSTEMIC_AUDIT_DAYS = 90
SYSTEMIC_AUDIT_NEW_DECISIONS = 5


def _parse_decision_id(did: str) -> int:
    """Convierte 'D24' -> 24. Devuelve -1 si no parsea."""
    m = re.match(r"^D(\d+)$", did.strip())
    return int(m.group(1)) if m else -1


def _last_decision_id() -> str | None:
    """Devuelve el D{N} con N más alto encontrado en DECISIONES.md.

    No filtra por estado (vigente/superada/revocada) porque el
    contador de "decisiones nuevas desde la última auditoría" debe
    incluir cualquier decisión registrada, también las que se han
    superado entre auditorías.
    """
    if not DECISIONES_MD.exists():
        return None
    text = DECISIONES_MD.read_text()
    ids = re.findall(r"^### (D\d+) — ", text, flags=re.MULTILINE)
    if not ids:
        return None
    return max(ids, key=_parse_decision_id)


def _last_audit_row() -> dict | None:
    """Lee la última fila de `data/auditorias.csv`. None si no existe."""
    if not AUDITORIAS_CSV.exists():
        return None
    try:
        with AUDITORIAS_CSV.open(newline="") as f:
            rows = list(csv.DictReader(f))
        return rows[-1] if rows else None
    except Exception as exc:  # noqa: BLE001
        log.warning("No pude leer data/auditorias.csv: %s", exc)
        return None


def check_systemic_audit_trigger(today: date | None = None) -> dict | None:
    """Decide si toca avisar de auditoría sistémica.

    Devuelve dict con flags si hay disparo, None en silencio. Usa la
    última fila de `data/auditorias.csv` como referencia. Sin fila,
    no dispara — la primera auditoría se registra al cierre con
    `register_audit()`.
    """
    today = today or date.today()
    last = _last_audit_row()
    if not last:
        return None
    try:
        last_date = datetime.strptime(last["date"], "%Y-%m-%d").date()
    except (ValueError, KeyError):
        log.warning("Fila de auditoría con fecha inválida: %s", last)
        return None

    days_since = (today - last_date).days
    last_id = last.get("last_decision_id", "D0")
    last_id_n = _parse_decision_id(last_id)
    current_top = _last_decision_id() or "D0"
    current_top_n = _parse_decision_id(current_top)
    decisions_added = max(0, current_top_n - last_id_n)

    by_days = days_since >= SYSTEMIC_AUDIT_DAYS
    by_decisions = decisions_added >= SYSTEMIC_AUDIT_NEW_DECISIONS
    if not (by_days or by_decisions):
        return None
    return {
        "days_since": days_since,
        "decisions_added": decisions_added,
        "last_audit_date": last_date.isoformat(),
        "last_audit_id": last_id,
        "current_top_id": current_top,
        "by_days": by_days,
        "by_decisions": by_decisions,
    }


def register_audit(note: str = "") -> Path:
    """Añade fila a `data/auditorias.csv` cuando se cierra una auditoría real.

    Llamar al cerrar una sesión de auditoría sistémica para reiniciar
    el contador. La fila guarda la fecha de cierre, el último D{N}
    encontrado y el conteo de decisiones vigentes en ese momento.
    """
    from src.panel import _count_active_decisions

    AUDITORIAS_CSV.parent.mkdir(parents=True, exist_ok=True)
    today = date.today().isoformat()
    last_id = _last_decision_id() or "D0"
    active = _count_active_decisions()
    new_row = [today, last_id, str(active), "manual", note]
    if not AUDITORIAS_CSV.exists():
        AUDITORIAS_CSV.write_text(
            "date,last_decision_id,active_count,trigger,note\n"
        )
    with AUDITORIAS_CSV.open("a", newline="") as f:
        writer = csv.writer(f, quoting=csv.QUOTE_MINIMAL)
        writer.writerow(new_row)
    log.info("Auditoría registrada: %s (top=%s, vigentes=%d)", today, last_id, active)
    return AUDITORIAS_CSV


def _build_message(
    today: date,
    vencidas: list[dict],
    proximas: list[dict],
    audit_trigger: dict | None,
) -> str:
    lines: list[str] = ["*Revisión de decisiones pendientes*", ""]
    if vencidas:
        lines.append("🚨 *Vencidas:*")
        for d in vencidas:
            delta = (today - d["review_date"]).days
            unit = "día" if delta == 1 else "días"
            lines.append(f"• {d['title']} ({d['id']}) — hace {delta} {unit}")
        lines.append("")
    if proximas:
        lines.append("⚠️ *Próximas (≤7 días):*")
        for d in proximas:
            delta = (d["review_date"] - today).days
            if delta == 0:
                when = "hoy"
            else:
                unit = "día" if delta == 1 else "días"
                when = f"en {delta} {unit}"
            lines.append(f"• {d['title']} ({d['id']}) — {when}")
        lines.append("")
    if audit_trigger:
        lines.append("🩺 *Auditoría sistémica (D24): toca lanzarla.*")
        razones: list[str] = []
        if audit_trigger.get("by_days"):
            razones.append(
                f"han pasado {audit_trigger['days_since']} días desde la última "
                f"({audit_trigger['last_audit_date']})"
            )
        if audit_trigger.get("by_decisions"):
            razones.append(
                f"se han abierto {audit_trigger['decisions_added']} decisiones nuevas "
                f"desde la última ({audit_trigger['last_audit_id']} → "
                f"{audit_trigger['current_top_id']})"
            )
        for r in razones:
            lines.append(f"• {r}")
        lines.append("")
        lines.append(
            "Abrir sesión de auditoría sistémica con el asistente "
            "(plantilla: contradicciones, redundancias, zombis, presupuesto). "
            "Al cerrarla, registrar con `python -m src.decisions_watch --register-audit`."
        )
        lines.append("")
    if vencidas or proximas:
        lines.append("Abre `DECISIONES.md` para revisar y actualizar el campo.")
    return "\n".join(lines)


def run() -> int:
    today = date.today()
    decisions = _extract_decisions_with_review()
    vencidas, proximas, _ = _classify(today, decisions)
    audit_trigger = check_systemic_audit_trigger(today)
    if not vencidas and not proximas and not audit_trigger:
        log.info("Sin decisiones vencidas, próximas ni auditoría pendiente — silencio.")
        return 0
    msg = _build_message(today, vencidas, proximas, audit_trigger)
    # Nivel: warning si hay vencidas o auditoría pendiente; info si solo próximas.
    level = "warning" if (vencidas or audit_trigger) else "info"
    try:
        from src.notify import notify

        ok = notify(msg, level=level)
        log.info(
            "Aviso enviado: %s (nivel=%s, vencidas=%d, próximas=%d, audit=%s)",
            ok,
            level,
            len(vencidas),
            len(proximas),
            "sí" if audit_trigger else "no",
        )
    except Exception as exc:  # noqa: BLE001
        log.error("No pude enviar el aviso: %s", exc)
        return 1
    return 0


def main() -> int:
    import argparse
    import sys

    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0] if __doc__ else "")
    parser.add_argument(
        "--register-audit",
        action="store_true",
        help="Registra una auditoría sistémica recién cerrada en data/auditorias.csv "
             "y reinicia el contador de disparo (D24).",
    )
    parser.add_argument(
        "--audit-note",
        default="",
        help="Nota corta que acompaña al registro de la auditoría.",
    )
    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO, format="[%(levelname)s %(name)s] %(message)s")
    if args.register_audit:
        path = register_audit(note=args.audit_note)
        print(f"Auditoría registrada en {path}")
        return 0
    return run()


if __name__ == "__main__":
    import sys

    sys.exit(main())
