"""Tablero interno único de vigilancia del proyecto.

Agrega en un solo archivo Markdown (`private/panel.md`) las señales que
otros módulos ya producen:

- Gasto del mes (vía `src.costs`).
- Estado de la verificación de la última edición.
- Nota de la última autoevaluación.
- Histórico acumulado de propuestas.
- Última edición publicada.
- Decisiones con `Próxima revisión` pendiente, próxima o futura.

No genera datos: solo lee lo que otros módulos escriben.

Uso:
    python -m src.panel

Se ejecuta automáticamente cada lunes en el workflow `weekly-report` tras
regenerar costes y autoevaluación. Registrado como decisión D14.
"""
from __future__ import annotations

import json
import logging
import re
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Final

log = logging.getLogger("panel")

ROOT = Path(__file__).resolve().parent.parent
DECISIONES_MD = ROOT / "DECISIONES.md"
VERIFICATION_JSON = ROOT / "data" / "verification_report.json"
PROPOSALS_HISTORY = ROOT / "data" / "proposals_history.json"
SELF_REVIEW_LOG = ROOT / "private" / "self-review-log.md"
SELF_REVIEW_DIR = ROOT / "private" / "self-review"
EDITIONS_DIR = ROOT / "docs" / "_editions"
PANEL_MD = ROOT / "private" / "panel.md"
GENERATE_PY = ROOT / "src" / "generate.py"
SELF_REVIEW_PY = ROOT / "src" / "self_review.py"

WARNING_WINDOW_DAYS: Final[int] = 7

# Ventana para considerar una dimensión "candidata a retirar" si su nota ha sido
# constante durante este número de ediciones consecutivas (D24 termómetro).
ZOMBIE_DIMENSION_WINDOW: Final[int] = 4


# ---------------------------------------------------------------------------
# Extracción de decisiones con Próxima revisión
# ---------------------------------------------------------------------------

def _extract_decisions_with_review() -> list[dict]:
    """Lee `DECISIONES.md` y devuelve los bloques con fecha ISO en Próxima revisión.

    Saltamos decisiones revocadas o superadas, y las que usan `permanente` o
    `N/A` (no participan del sistema de avisos).
    """
    if not DECISIONES_MD.exists():
        return []
    text = DECISIONES_MD.read_text()
    blocks = re.split(r"(?=^### D\d+ — )", text, flags=re.MULTILINE)
    out: list[dict] = []
    for block in blocks:
        m_id = re.match(r"^### (D\d+) — (.+?)$", block, flags=re.MULTILINE)
        if not m_id:
            continue
        did = m_id.group(1)
        title = m_id.group(2).strip()
        m_rev = re.search(r"\*\*Próxima revisión:\*\*\s+(\S+)", block)
        m_estado = re.search(r"\*\*Estado:\*\*\s+(.+?)(?:\n|$)", block)
        if not m_rev:
            continue
        rev_raw = m_rev.group(1).strip().rstrip(",.")
        estado = (m_estado.group(1) if m_estado else "").strip()
        estado_lower = estado.lower()
        if "revocada" in estado_lower or "superada_por" in estado_lower:
            continue
        try:
            rev_date = datetime.strptime(rev_raw, "%Y-%m-%d").date()
        except ValueError:
            continue
        out.append({"id": did, "title": title, "review_date": rev_date})
    return out


def _classify(today: date, decisions: list[dict]) -> tuple[list[dict], list[dict], list[dict]]:
    vencidas: list[dict] = []
    proximas: list[dict] = []
    futuras: list[dict] = []
    for d in decisions:
        delta = (d["review_date"] - today).days
        if delta < 0:
            vencidas.append(d)
        elif delta <= WARNING_WINDOW_DAYS:
            proximas.append(d)
        else:
            futuras.append(d)
    vencidas.sort(key=lambda d: d["review_date"])
    proximas.sort(key=lambda d: d["review_date"])
    futuras.sort(key=lambda d: d["review_date"])
    return vencidas, proximas, futuras


# ---------------------------------------------------------------------------
# Lectores de señales agregadas
# ---------------------------------------------------------------------------

def _read_verification() -> dict | None:
    if not VERIFICATION_JSON.exists():
        return None
    try:
        return json.loads(VERIFICATION_JSON.read_text())
    except Exception as exc:  # noqa: BLE001
        log.warning("No pude leer verification_report.json: %s", exc)
        return None


def _read_proposals_total() -> int | None:
    if not PROPOSALS_HISTORY.exists():
        return None
    try:
        data = json.loads(PROPOSALS_HISTORY.read_text())
        if isinstance(data, list):
            return len(data)
        if isinstance(data, dict) and "proposals" in data:
            return len(data["proposals"])
    except Exception as exc:  # noqa: BLE001
        log.warning("No pude leer proposals_history.json: %s", exc)
    return None


def _last_edition() -> str | None:
    if not EDITIONS_DIR.exists():
        return None
    files = sorted(EDITIONS_DIR.glob("*.md"))
    if not files:
        return None
    return files[-1].stem


def _last_self_review_lines() -> list[str] | None:
    """Devuelve las líneas de la última entrada del log de self-review.

    El archivo agrupa por `## YYYY-WNN · ...`; la última sección es la más
    reciente. Si no hay entradas reales (solo el placeholder), devolvemos None.
    """
    if not SELF_REVIEW_LOG.exists():
        return None
    try:
        content = SELF_REVIEW_LOG.read_text()
        sections = re.split(r"(?=^## \d{4}-W\d{2})", content, flags=re.MULTILINE)
        last = None
        for sec in sections:
            if re.match(r"^## \d{4}-W\d{2}", sec):
                last = sec
        if not last:
            return None
        lines = [l for l in last.splitlines() if l.strip()]
        return lines or None
    except Exception as exc:  # noqa: BLE001
        log.warning("No pude leer self-review-log.md: %s", exc)
        return None


# ---------------------------------------------------------------------------
# Termómetro de salud sistémica (D24)
# ---------------------------------------------------------------------------

def _count_generator_rules() -> int | None:
    """Cuenta las viñetas de "REGLAS DURAS ADICIONALES" del prompt del generador.

    Heurística simple: lee `src/generate.py`, localiza el bloque que empieza
    con la cabecera y cuenta las líneas que comienzan con "- " hasta el cierre
    `\"\"\"` del SYSTEM. Útil como termómetro de complejidad — no pretende ser
    exacto, solo orientativo.
    """
    if not GENERATE_PY.exists():
        return None
    try:
        text = GENERATE_PY.read_text()
    except Exception as exc:  # noqa: BLE001
        log.warning("No pude leer src/generate.py: %s", exc)
        return None
    m_start = re.search(r"^REGLAS DURAS ADICIONALES:\s*$", text, flags=re.MULTILINE)
    if not m_start:
        return None
    tail = text[m_start.end():]
    m_end = re.search(r'^"""', tail, flags=re.MULTILINE)
    block = tail[: m_end.start()] if m_end else tail
    return sum(1 for line in block.splitlines() if line.startswith("- "))


def _count_review_dimensions() -> int | None:
    """Cuenta las dimensiones del JSON `scores` del prompt del revisor.

    Heurística: lee `src/self_review.py`, localiza el bloque `"scores": { ... }`
    y cuenta las claves. Si el formato cambia, la heurística falla en silencio
    y devolvemos None.
    """
    if not SELF_REVIEW_PY.exists():
        return None
    try:
        text = SELF_REVIEW_PY.read_text()
    except Exception as exc:  # noqa: BLE001
        log.warning("No pude leer src/self_review.py: %s", exc)
        return None
    m = re.search(r'"scores":\s*\{([^}]+)\}', text)
    if not m:
        return None
    block = m.group(1)
    return len(re.findall(r'"\w+":', block))


def _count_active_decisions() -> int:
    """Cuenta las decisiones con Estado=vigente en DECISIONES.md."""
    if not DECISIONES_MD.exists():
        return 0
    text = DECISIONES_MD.read_text()
    blocks = re.split(r"(?=^### D\d+ — )", text, flags=re.MULTILINE)
    count = 0
    for block in blocks:
        if not re.match(r"^### D\d+ — ", block, flags=re.MULTILINE):
            continue
        m = re.search(r"\*\*Estado:\*\*\s+(.+?)(?:\n|$)", block)
        if m and m.group(1).strip().lower().startswith("vigente"):
            count += 1
    return count


def _zombie_dimensions(window: int = ZOMBIE_DIMENSION_WINDOW) -> list[str]:
    """Identifica dimensiones del revisor con nota constante en últimas N ediciones.

    Lee los archivos `private/self-review/{edition}.md` ordenados por nombre,
    parsea la tabla "| dimension | **N** |" de cada uno, y devuelve los nombres
    de las dimensiones cuya nota ha sido idéntica durante las últimas `window`
    ediciones consecutivas. Heurística orientativa para detectar dimensiones
    muertas candidatas a retirar (D22, D24).

    Si no hay suficientes self-reviews (< window), devuelve lista vacía.
    """
    if not SELF_REVIEW_DIR.exists():
        return []
    files = sorted(SELF_REVIEW_DIR.glob("*.md"))
    if len(files) < window:
        return []
    recent = files[-window:]
    scores_per_edition: list[dict[str, int]] = []
    for f in recent:
        try:
            text = f.read_text()
        except Exception:  # noqa: BLE001
            continue
        scores: dict[str, int] = {}
        for m in re.finditer(r"^\|\s*(\w+)\s*\|\s*\*\*(\d+)\*\*\s*\|", text, flags=re.MULTILINE):
            scores[m.group(1)] = int(m.group(2))
        if scores:
            scores_per_edition.append(scores)
    if len(scores_per_edition) < window:
        return []
    dims = set(scores_per_edition[0].keys())
    for s in scores_per_edition[1:]:
        dims &= set(s.keys())
    zombies: list[str] = []
    for d in sorted(dims):
        values = [s[d] for s in scores_per_edition]
        if len(set(values)) == 1:
            zombies.append(f"{d} (constante en {values[0]}/10 durante {window} ediciones)")
    return zombies


def _spend_line() -> str:
    try:
        from src.costs import (
            MONTHLY_HARD_CAP_EUR,
            MONTHLY_SOFT_CAP_EUR,
            _current_layer,
            current_month_spend_eur,
        )

        spend = current_month_spend_eur()
        layer = _current_layer(spend)
        return (
            f"{spend:.2f} € "
            f"(blando {MONTHLY_SOFT_CAP_EUR:.0f} € / duro {MONTHLY_HARD_CAP_EUR:.0f} €) "
            f"— {layer}"
        )
    except Exception as exc:  # noqa: BLE001
        log.warning("No pude leer gasto del mes: %s", exc)
        return "sin datos"


# ---------------------------------------------------------------------------
# Generación del tablero
# ---------------------------------------------------------------------------

def generate_panel() -> None:
    today = date.today()
    now = datetime.now(timezone.utc)
    decisions = _extract_decisions_with_review()
    vencidas, proximas, futuras = _classify(today, decisions)

    lines: list[str] = []
    lines.append("# Tablero interno — monitorización del proyecto")
    lines.append("")
    lines.append(
        f"*Archivo privado. No se publica en la web. "
        f"Última actualización: {now.strftime('%Y-%m-%d %H:%M UTC')}.*"
    )
    lines.append("")
    lines.append(
        "Agrega las señales que otros módulos ya producen: gasto del mes, "
        "autoevaluación, verificación, decisiones con revisión pendiente, "
        "última edición. No genera datos propios. Ver decisión D14."
    )
    lines.append("")

    # --- Costes ---
    lines.append("## Costes del mes")
    lines.append("")
    lines.append(f"- **Gasto actual:** {_spend_line()}")
    lines.append("- **Dashboard detallado:** [`costs.md`](costs.md)")
    lines.append("")

    # --- Decisiones ---
    lines.append("## Decisiones con revisión pendiente")
    lines.append("")
    if vencidas:
        lines.append("### 🚨 Vencidas")
        lines.append("")
        for d in vencidas:
            delta = (today - d["review_date"]).days
            unit = "día" if delta == 1 else "días"
            lines.append(
                f"- **{d['title']}** ({d['id']}) — vencía el "
                f"{d['review_date'].isoformat()} (hace {delta} {unit})"
            )
        lines.append("")
    if proximas:
        lines.append("### ⚠️ Próximas (≤7 días)")
        lines.append("")
        for d in proximas:
            delta = (d["review_date"] - today).days
            if delta == 0:
                when = "hoy"
            else:
                unit = "día" if delta == 1 else "días"
                when = f"en {delta} {unit}"
            lines.append(
                f"- **{d['title']}** ({d['id']}) — vence el "
                f"{d['review_date'].isoformat()} ({when})"
            )
        lines.append("")
    if not vencidas and not proximas:
        if futuras:
            nxt = futuras[0]
            lines.append(
                f"_Ninguna decisión vencida ni próxima. Siguiente revisión: "
                f"**{nxt['title']}** ({nxt['id']}) el "
                f"{nxt['review_date'].isoformat()}._"
            )
        else:
            lines.append("_Sin decisiones con revisión fechada._")
        lines.append("")
    if futuras:
        lines.append("### 📆 Futuras (informativo)")
        lines.append("")
        for d in futuras[:10]:
            lines.append(
                f"- {d['title']} ({d['id']}) — {d['review_date'].isoformat()}"
            )
        if len(futuras) > 10:
            lines.append(f"- _…y {len(futuras) - 10} más._")
        lines.append("")

    # --- Última edición ---
    lines.append("## Última edición publicada")
    lines.append("")
    edition = _last_edition()
    if edition:
        lines.append(f"- `{edition}`")
    else:
        lines.append("_Sin ediciones registradas aún._")
    lines.append("")

    # --- Propuestas ---
    lines.append("## Histórico de propuestas")
    lines.append("")
    total = _read_proposals_total()
    if total is not None:
        lines.append(f"- **Total acumulado:** {total}")
    else:
        lines.append("_Sin historial de propuestas aún._")
    lines.append("")

    # --- Verificación ---
    lines.append("## Verificación (última ejecución)")
    lines.append("")
    vr = _read_verification()
    if vr:
        blocking = vr.get("blocking_failures") or []
        soft = vr.get("soft_warnings") or []
        urls_failed = vr.get("urls_failed") or []
        actors_untr = vr.get("actors_untraceable") or []
        status = "✅ sin fallos bloqueantes" if not blocking else f"❌ {len(blocking)} fallo(s) bloqueante(s)"
        lines.append(f"- **Resultado:** {status}")
        lines.append(f"- **URLs comprobadas:** {vr.get('urls_checked', 'N/D')}, caídas: {len(urls_failed)}")
        lines.append(f"- **Actores comprobados:** {vr.get('actors_checked', 'N/D')}, no trazables: {len(actors_untr)}")
        lines.append(f"- **Avisos blandos:** {len(soft)}")
    else:
        lines.append("_Sin informe de verificación disponible._")
    lines.append("")

    # --- Self-review ---
    lines.append("## Autoevaluación (último corte)")
    lines.append("")
    sr_lines = _last_self_review_lines()
    if sr_lines:
        for sline in sr_lines:
            lines.append(sline)
    else:
        lines.append("_Sin autoevaluación registrada aún._")
    lines.append("")

    # --- Salud sistémica (D24) ---
    lines.append("## Salud sistémica (termómetro de complejidad)")
    lines.append("")
    lines.append(
        "Termómetro orientativo para detectar pozo de modificación infinita. "
        "Disparador de auditoría sistémica (D24) cuando los conteos crezcan "
        "más rápido que la utilidad real."
    )
    lines.append("")
    gen_rules = _count_generator_rules()
    rev_dims = _count_review_dimensions()
    active_decs = _count_active_decisions()
    zombies = _zombie_dimensions()
    lines.append(
        f"- **Reglas duras adicionales en el prompt del generador:** "
        f"{gen_rules if gen_rules is not None else 'no detectado'}"
    )
    lines.append(
        f"- **Dimensiones del revisor (self-review):** "
        f"{rev_dims if rev_dims is not None else 'no detectado'}"
    )
    lines.append(f"- **Decisiones vigentes en `DECISIONES.md`:** {active_decs}")
    if zombies:
        lines.append(
            f"- **Candidatas a retirar** (dimensiones con nota constante en "
            f"últimas {ZOMBIE_DIMENSION_WINDOW} ediciones):"
        )
        for z in zombies:
            lines.append(f"    - {z}")
    else:
        lines.append(
            f"- **Candidatas a retirar:** ninguna detectada con la heurística "
            f"actual (ventana {ZOMBIE_DIMENSION_WINDOW} ediciones)."
        )
    lines.append("")

    # --- Pie ---
    lines.append("---")
    lines.append("")
    lines.append(
        "Fuente de datos: `DECISIONES.md`, `data/costs.csv` (vía `src.costs`), "
        "`data/verification_report.json`, `data/proposals_history.json`, "
        "`private/self-review-log.md`, `docs/_editions/`. Regenerado por `src.panel`."
    )

    PANEL_MD.parent.mkdir(parents=True, exist_ok=True)
    PANEL_MD.write_text("\n".join(lines) + "\n")
    log.info("Tablero regenerado → %s", PANEL_MD)


def main() -> int:
    logging.basicConfig(level=logging.INFO, format="[%(levelname)s %(name)s] %(message)s")
    generate_panel()
    return 0


if __name__ == "__main__":
    import sys

    sys.exit(main())
