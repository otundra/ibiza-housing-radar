"""Balance público de actores citados.

Calcula el reparto de citas por actor_type, palanca y horizonte sobre
ventanas móviles (30d, 90d, 180d, 365d). Escribe:

- `private/balance.md` — dashboard privado con desglose completo.
- `docs/balance.md` — versión pública simplificada (alineada con `/balance/`).

Alerta Telegram si algún bloque supera 50% durante 2 meses consecutivos
(señal de sesgo en la selección). Regla vinculante del pivote.
"""
from __future__ import annotations

import json
import logging
import re
import sys
from collections import Counter
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

log = logging.getLogger("balance")

ROOT = Path(__file__).resolve().parent.parent
HISTORY_FILE = ROOT / "data" / "proposals_history.json"
PRIVATE_OUT = ROOT / "private" / "balance.md"
PUBLIC_OUT = ROOT / "docs" / "balance.md"

WINDOWS_DAYS = {
    "30d": 30,
    "90d": 90,
    "180d": 180,
    "365d": 365,
}


def load_history() -> list[dict]:
    if not HISTORY_FILE.exists():
        return []
    return json.loads(HISTORY_FILE.read_text())


def iso_to_dt(s: str) -> datetime | None:
    if not s:
        return None
    try:
        return datetime.fromisoformat(s.replace("Z", "+00:00"))
    except Exception:  # noqa: BLE001
        return None


def filter_window(props: list[dict], days: int) -> list[dict]:
    cutoff = datetime.now(timezone.utc) - timedelta(days=days)
    out = []
    for p in props:
        dt = iso_to_dt(p.get("first_seen") or p.get("published"))
        if dt and dt >= cutoff:
            out.append(p)
    return out


def count_dimension(props: list[dict], field: str) -> dict[str, int]:
    return dict(Counter((p.get(field) or "desconocido") for p in props))


def render_table(title: str, counts: dict[str, int]) -> list[str]:
    total = sum(counts.values())
    lines = [f"### {title}", ""]
    if total == 0:
        lines.append("*Sin datos en esta ventana.*")
        lines.append("")
        return lines
    lines.append("| Categoría | N | % |")
    lines.append("|---|---|---|")
    for k in sorted(counts, key=lambda x: -counts[x]):
        pct = counts[k] / total * 100
        lines.append(f"| {k} | {counts[k]} | {pct:.1f}% |")
    lines.append("")
    return lines


def alert_if_concentrated(counts: dict[str, int]) -> list[str]:
    total = sum(counts.values())
    if total == 0:
        return []
    alerts = []
    for k, v in counts.items():
        pct = v / total * 100
        if pct >= 50.0:
            alerts.append(f"{k} concentra {pct:.1f}% de las citas (>50%).")
    return alerts


def build_private(history: list[dict]) -> str:
    lines = [
        "# Balance de actores — dashboard privado",
        "",
        f"*Última actualización: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}*",
        "",
        f"Histórico total: {len(history)} propuestas documentadas.",
        "",
    ]

    for win_name, days in WINDOWS_DAYS.items():
        filtered = filter_window(history, days)
        lines.append(f"## Ventana {win_name} ({len(filtered)} propuestas)")
        lines.append("")
        for field, title in [
            ("actor_type", "Por tipo de actor"),
            ("palanca", "Por palanca"),
            ("horizon", "Por horizonte"),
            ("state", "Por estado"),
        ]:
            counts = count_dimension(filtered, field)
            lines.extend(render_table(title, counts))

        alerts = alert_if_concentrated(count_dimension(filtered, "actor_type"))
        if alerts and days >= 60:
            lines.append("**Alertas de concentración:**")
            lines.append("")
            for a in alerts:
                lines.append(f"- ⚠️ {a}")
            lines.append("")

    return "\n".join(lines)


def build_public(history: list[dict]) -> str:
    """Versión pública simplificada, alineada con /balance/."""
    lines = [
        "---",
        'layout: page',
        'title: "Balance"',
        'permalink: /balance/',
        "---",
        "",
        "# Balance de actores citados",
        "",
        f"*Última actualización: {datetime.now(timezone.utc).strftime('%Y-%m-%d')}. Recalculado automáticamente tras cada edición.*",
        "",
        f"Total de propuestas documentadas: **{len(history)}**.",
        "",
    ]

    filtered_90 = filter_window(history, 90)
    lines.append(f"## Últimos 90 días — {len(filtered_90)} propuestas")
    lines.append("")
    for field, title in [
        ("actor_type", "Por tipo de actor"),
        ("palanca", "Por palanca"),
    ]:
        counts = count_dimension(filtered_90, field)
        lines.extend(render_table(title, counts))

    filtered_365 = filter_window(history, 365)
    lines.append(f"## Últimos 365 días — {len(filtered_365)} propuestas")
    lines.append("")
    for field, title in [
        ("actor_type", "Por tipo de actor"),
        ("palanca", "Por palanca"),
    ]:
        counts = count_dimension(filtered_365, field)
        lines.extend(render_table(title, counts))

    alerts = alert_if_concentrated(count_dimension(filtered_90, "actor_type"))
    if alerts:
        lines.append("## Alertas metodológicas activas")
        lines.append("")
        for a in alerts:
            lines.append(f"- {a}")
        lines.append("")
        lines.append("Si una concentración >50% persiste durante 2 trimestres consecutivos, ")
        lines.append("revisamos los criterios de admisión y las fuentes de ingesta. Ver ")
        lines.append("[política editorial](/politica-editorial/).")
        lines.append("")

    lines.append("## Metodología")
    lines.append("")
    lines.append("El balance se calcula sobre el archivo de propuestas documentadas ")
    lines.append("en `data/proposals_history.json`. Cada propuesta cuenta una vez por ")
    lines.append("edición en la que aparece. Detalle técnico en [/metodologia/](/metodologia/).")
    lines.append("")

    return "\n".join(lines)


def maybe_alert(history: list[dict]) -> None:
    filtered_60 = filter_window(history, 60)
    if len(filtered_60) < 5:
        return  # demasiado pronto para alertar
    counts = count_dimension(filtered_60, "actor_type")
    alerts = alert_if_concentrated(counts)
    if not alerts:
        return
    try:
        from src.notify import notify
        msg = "⚠️ Balance: concentración detectada (últimos 60d)\n" + "\n".join(f"- {a}" for a in alerts)
        notify(msg, level="warning")
    except Exception as exc:  # noqa: BLE001
        log.warning("No se pudo notificar: %s", exc)


def main() -> int:
    logging.basicConfig(level=logging.INFO, format="[%(levelname)s %(name)s] %(message)s")

    history = load_history()
    log.info("Propuestas en histórico: %d", len(history))

    PRIVATE_OUT.parent.mkdir(parents=True, exist_ok=True)
    PRIVATE_OUT.write_text(build_private(history))
    log.info("Dashboard privado → %s", PRIVATE_OUT)

    PUBLIC_OUT.parent.mkdir(parents=True, exist_ok=True)
    PUBLIC_OUT.write_text(build_public(history))
    log.info("Dashboard público → %s", PUBLIC_OUT)

    maybe_alert(history)

    return 0


if __name__ == "__main__":
    sys.exit(main())
