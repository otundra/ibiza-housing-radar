"""Regenera docs/propuestas.md como vista global de todas las propuestas.

La página `/propuestas/` es el mapa completo del observatorio: todas las
propuestas documentadas en el histórico, agrupadas por estado y con
enlace a la edición que las introdujo y a la fuente original.

Lee `data/proposals_history.json` y emite un Markdown con frontmatter
Jekyll + HTML inline. El bot del cron commitea el resultado igual que
`build_index.py`. No usa LLM.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from src.labels import (
    actor_type_label,
    horizon_label,
    palanca_label,
    state_label,
)

ROOT = Path(__file__).resolve().parent.parent
HISTORY_FILE = ROOT / "data" / "proposals_history.json"
OUT_FILE = ROOT / "docs" / "propuestas.md"

# Orden de presentación de los estados. Avances primero, en proceso en
# medio, cierres y desconocidos al final. Coherente con la lectura natural
# del observatorio: lo más concreto arriba.
STATE_ORDER = [
    "implementada",
    "en_ejecucion",
    "aprobada",
    "en_debate",
    "en_movimiento",
    "propuesta",
    "descartada",
    "pendiente_resolucion_judicial",
    "desconocido",
]


def edition_slug_to_link(edition: str) -> str:
    """Convierte 2026-W17 → /ediciones/2026-w17/."""
    return f"{{{{ site.baseurl }}}}/ediciones/{edition.lower()}/"


def render_propuesta_row(p: dict[str, Any]) -> list[str]:
    """Renderiza una fila de la tabla compacta para una propuesta."""
    actor = p.get("actor", "—") or "—"
    actor_type = actor_type_label(p.get("actor_type", "")) or "—"
    summary = p.get("statement_summary", "") or p.get("statement_verbatim", "") or "—"
    palanca = palanca_label(p.get("palanca", "")) or "—"
    horizon = horizon_label(p.get("horizon", "")) or "—"
    first_edition = p.get("first_seen_edition", "") or "—"
    url_source = p.get("url_source", "")

    lines: list[str] = []
    lines.append('<article class="prop-card">')
    lines.append(f'<h3 class="prop-card-actor">{actor} <span class="prop-card-type">· {actor_type}</span></h3>')
    lines.append(f'<p class="prop-card-summary">{summary}</p>')
    lines.append('<dl class="prop-card-meta">')
    lines.append(f'<dt>Palanca</dt><dd>{palanca}</dd>')
    lines.append(f'<dt>Horizonte</dt><dd>{horizon}</dd>')
    if first_edition and first_edition != "—":
        edition_link = edition_slug_to_link(first_edition)
        lines.append(f'<dt>Vista por primera vez</dt><dd><a href="{edition_link}">{first_edition}</a></dd>')
    lines.append('</dl>')
    if url_source:
        lines.append(f'<a class="prop-card-source" href="{url_source}" target="_blank" rel="noopener">Fuente original →</a>')
    lines.append('</article>')
    return lines


def group_by_state(proposals: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
    """Agrupa propuestas por su campo state (con fallback a desconocido)."""
    grouped: dict[str, list[dict[str, Any]]] = {}
    for p in proposals:
        state = p.get("state", "desconocido") or "desconocido"
        grouped.setdefault(state, []).append(p)
    return grouped


def render_empty() -> str:
    return """---
layout: page
title: Propuestas
permalink: /propuestas/
---

<section class="prop-empty">
<p><em>Aún no hay propuestas en el histórico. La primera entrará tras la primera edición publicada.</em></p>
</section>
"""


def render_page(proposals: list[dict[str, Any]]) -> str:
    if not proposals:
        return render_empty()

    grouped = group_by_state(proposals)
    total = len(proposals)
    n_actores = len({p.get("actor", "") for p in proposals if p.get("actor")})

    out: list[str] = [
        "---",
        "layout: page",
        "title: Propuestas",
        "permalink: /propuestas/",
        "---",
        "",
    ]

    # ---------- HEADER ----------
    # No usamos h1: el layout `page` ya emite el título de la página en h1.
    out.append('<section class="prop-intro">')
    out.append(f'<p class="prop-intro-kicker">Mapa completo del observatorio</p>')
    out.append(f'<p class="prop-intro-count"><strong>{total} propuestas documentadas · {n_actores} actores distintos</strong></p>')
    out.append(
        f'<p class="prop-intro-lead">Cada propuesta la formuló un actor con nombre y fuente verificable. '
        f'Aquí están todas las que el observatorio ha registrado desde su primera edición, agrupadas por estado actual.</p>'
    )
    out.append('</section>')
    out.append('')

    # ---------- ÍNDICE DE ESTADOS ----------
    out.append('<nav class="prop-nav" aria-label="Saltar a estado">')
    out.append('<ul class="prop-nav-list">')
    for state in STATE_ORDER:
        items = grouped.get(state, [])
        if not items:
            continue
        anchor = state.replace("_", "-")
        label = state_label(state)
        out.append(f'<li><a href="#{anchor}">{label} <span class="prop-nav-count">{len(items)}</span></a></li>')
    out.append('</ul>')
    out.append('</nav>')
    out.append('')

    # ---------- BLOQUES POR ESTADO ----------
    for state in STATE_ORDER:
        items = grouped.get(state, [])
        if not items:
            continue
        anchor = state.replace("_", "-")
        label = state_label(state)
        out.append(f'<section class="prop-state" id="{anchor}">')
        out.append('<header class="prop-state-header">')
        out.append(f'<h2>{label}</h2>')
        out.append(f'<p class="prop-state-count">{len(items)} {"propuesta" if len(items) == 1 else "propuestas"}</p>')
        out.append('</header>')
        out.append('<div class="prop-state-grid">')
        for p in items:
            out.extend(render_propuesta_row(p))
        out.append('</div>')
        out.append('</section>')
        out.append('')

    return "\n".join(out)


def build() -> None:
    proposals: list[dict[str, Any]] = []
    if HISTORY_FILE.exists():
        try:
            proposals = json.loads(HISTORY_FILE.read_text())
        except json.JSONDecodeError:
            proposals = []
    OUT_FILE.write_text(render_page(proposals))
    print(f"Propuestas escritas: {OUT_FILE} ({len(proposals)} propuestas)")


if __name__ == "__main__":
    build()
