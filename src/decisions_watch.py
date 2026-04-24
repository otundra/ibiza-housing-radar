"""Vigilancia de fechas de revisión de decisiones del proyecto.

Lee `DECISIONES.md`, extrae el campo `Próxima revisión`, y si alguna
decisión vigente está vencida o próxima (ventana de 7 días), manda un
aviso por Telegram vía `src.notify`.

Reutiliza los extractores de `src.panel` para no duplicar la lógica de
parseo.

Se ejecuta cada lunes en el workflow `weekly-report` antes de generar la
edición. Registrado como parte de la decisión D14.

Uso:
    python -m src.decisions_watch
"""
from __future__ import annotations

import logging
from datetime import date

from src.panel import _classify, _extract_decisions_with_review

log = logging.getLogger("decisions_watch")


def _build_message(today: date, vencidas: list[dict], proximas: list[dict]) -> str:
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
    lines.append("Abre `DECISIONES.md` para revisar y actualizar el campo.")
    return "\n".join(lines)


def run() -> int:
    today = date.today()
    decisions = _extract_decisions_with_review()
    vencidas, proximas, _ = _classify(today, decisions)
    if not vencidas and not proximas:
        log.info("Sin decisiones vencidas o próximas — silencio.")
        return 0
    msg = _build_message(today, vencidas, proximas)
    level = "warning" if vencidas else "info"
    try:
        from src.notify import notify

        ok = notify(msg, level=level)
        log.info(
            "Aviso enviado: %s (nivel=%s, vencidas=%d, próximas=%d)",
            ok,
            level,
            len(vencidas),
            len(proximas),
        )
    except Exception as exc:  # noqa: BLE001
        log.error("No pude enviar el aviso: %s", exc)
        return 1
    return 0


def main() -> int:
    logging.basicConfig(level=logging.INFO, format="[%(levelname)s %(name)s] %(message)s")
    return run()


if __name__ == "__main__":
    import sys

    sys.exit(main())
