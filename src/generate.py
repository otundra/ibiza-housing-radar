"""Genera el informe semanal con Claude Opus.

Entrada: data/classified.json (solo items is_housing=True)
Salida: docs/editions/<YYYY>-W<WW>.md con front-matter Jekyll.

Si no hay señales suficientes, escribe una edición "sin novedades" concisa.
"""
from __future__ import annotations

import json
import logging
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import anthropic

from costs import record_call, assert_budget_available

log = logging.getLogger("generate")

ROOT = Path(__file__).resolve().parent.parent
IN_FILE = ROOT / "data" / "classified.json"
EDITIONS_DIR = ROOT / "docs" / "editions"

MODEL = "claude-opus-4-7"

SYSTEM = """Eres el editor jefe de "Ibiza Housing Radar", un observatorio semanal sobre la crisis de vivienda en Ibiza con foco en trabajadores de temporada (mayo-octubre).

Tu trabajo: escribir un informe semanal en español, directo, crítico y sin adornos, con ALTA densidad informativa. Nada de lenguaje institucional ni relleno.

El informe debe tener esta ESTRUCTURA EXACTA (Markdown con front-matter Jekyll):

---
layout: edition
title: "Semana WW · YYYY"
week: "YYYY-WWW"
date: YYYY-MM-DD
permalink: /ediciones/YYYY-wWW/
excerpt: "<síntesis en 1 frase de ≤160 caracteres para preview en la home>"
---

## 📡 Señales detectadas

Lista de bullets. Cada bullet es un hecho accionable + enlace markdown a la fuente. Sin valoraciones todavía. 4-8 bullets máximo. Ordena por relevancia, no por fecha.

## 🔍 Lectura

2-3 frases. Qué está cambiando, qué NO está cambiando, dónde está la ventana de decisión esta semana. Tono directo, sin jerga.

## 🛠 Propuestas

De 3 a 5 propuestas. CADA propuesta tiene esta estructura exacta:

### {n}. {Título corto en mayúscula inicial, sin punto final}

**Qué:** 1-2 frases explicando la medida, concreta, ejecutable.

- **Actor responsable:** quién debe aprobarla/ejecutarla
- **Precedente:** un caso real en otra ciudad/isla/país con fecha y volumen cuando sea posible
- **Coste estimado:** cifra razonable en euros, marca como "orientativo" cuando aplique
- **Primer paso:** la primera acción ejecutable en <30 días
- **Por qué ahora:** vínculo directo con las señales de esta semana

## 👀 A vigilar la semana que viene

3-5 bullets con eventos, fechas, o decisiones pendientes concretas.

---

REGLAS DURAS:
- Todos los enlaces markdown deben llevar a URLs REALES presentes en el input. Nunca inventes URLs.
- Si una noticia no aporta al informe, omítela. No hay cuota de bullets.
- No uses emojis fuera de los títulos de sección que ya van arriba.
- No uses lenguaje corporativo ("sinergia", "empoderar", "hoja de ruta" cuando no la hay).
- No saludes. No te despidas. No firmes.
- Si hay menos de 3 señales útiles, dilo claramente en "Lectura" y reduce propuestas a 1-2 muy concretas o ninguna ("semana sin señal") — nunca rellenes.
- Todas las cifras deben ser verosímiles y marcarse como estimación cuando lo sean.
"""


USER_TEMPLATE = """Semana ISO: {iso_week}
Fecha corte: {cutoff_date}

Noticias clasificadas como relevantes de vivienda en Ibiza (JSON):
{payload}

Escribe el informe completo siguiendo la estructura del system prompt. Empieza por el front-matter YAML y termina con la sección "A vigilar". Nada más."""


def iso_week_string(dt: datetime) -> str:
    iso = dt.isocalendar()
    return f"{iso.year}-W{iso.week:02d}"


def edition_slug(dt: datetime) -> str:
    iso = dt.isocalendar()
    return f"{iso.year}-w{iso.week:02d}"


def generate(items: list[dict[str, Any]], now: datetime, edition: str) -> str:
    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

    # Reducimos el payload para no inflar tokens
    slim = [
        {
            "title": it["title"],
            "summary": it["summary"][:500],
            "url": it["url"],
            "source": it["source"],
            "published": it.get("published", ""),
            "actor": it.get("actor", ""),
            "lever": it.get("lever", ""),
            "headline_es": it.get("headline_es", ""),
        }
        for it in items
    ]

    prompt = USER_TEMPLATE.format(
        iso_week=iso_week_string(now),
        cutoff_date=now.strftime("%Y-%m-%d"),
        payload=json.dumps(slim, ensure_ascii=False, indent=2),
    )

    assert_budget_available(planned_cost=1.0)

    log.info("Generating edition with %s (items=%d)", MODEL, len(items))
    resp = client.messages.create(
        model=MODEL,
        max_tokens=4096,
        system=SYSTEM,
        messages=[{"role": "user", "content": prompt}],
    )
    record_call(
        edition=edition,
        stage="generate",
        model=MODEL,
        usage=resp.usage.model_dump() if hasattr(resp.usage, "model_dump") else dict(resp.usage),
    )

    text = "".join(block.text for block in resp.content if block.type == "text").strip()
    # Sanity: debe empezar por '---'
    if not text.startswith("---"):
        log.warning("La salida no empezaba por front-matter. Añadiendo uno mínimo.")
        text = minimal_frontmatter(now) + "\n\n" + text
    return text


def minimal_frontmatter(now: datetime) -> str:
    iso = now.isocalendar()
    return (
        "---\n"
        f'layout: edition\n'
        f'title: "Semana {iso.week} · {iso.year}"\n'
        f'week: "{iso.year}-W{iso.week:02d}"\n'
        f'date: {now.strftime("%Y-%m-%d")}\n'
        f'permalink: /ediciones/{iso.year}-w{iso.week:02d}/\n'
        f'excerpt: "Informe automático — revisar salida."\n'
        "---"
    )


def write_edition(text: str, now: datetime) -> Path:
    EDITIONS_DIR.mkdir(parents=True, exist_ok=True)
    path = EDITIONS_DIR / f"{edition_slug(now)}.md"
    path.write_text(text)
    return path


def empty_edition(now: datetime, edition: str) -> str:
    iso = now.isocalendar()
    return f"""---
layout: edition
title: "Semana {iso.week} · {iso.year}"
week: "{edition}"
date: {now.strftime('%Y-%m-%d')}
permalink: /ediciones/{edition_slug(now)}/
excerpt: "Semana sin señal: no se han detectado noticias relevantes sobre vivienda en Ibiza."
---

## 📡 Señales detectadas

*No se han encontrado noticias relevantes esta semana sobre vivienda o trabajadores de temporada en Ibiza.*

## 🔍 Lectura

Silencio informativo. Puede significar (a) ausencia real de actividad pública, (b) ciclo de agenda política, o (c) un bug en la ingesta. Revisar manualmente los diarios locales antes de asumir (a).

## 👀 A vigilar la semana que viene

- Revisar manualmente Diario de Ibiza, Periódico de Ibiza y BOIB.
- Comprobar logs del workflow en GitHub Actions.
"""


def main() -> int:
    logging.basicConfig(level=logging.INFO, format="[%(levelname)s %(name)s] %(message)s")
    now = datetime.now(timezone.utc)
    edition = iso_week_string(now)
    os.environ["EDITION"] = edition

    items = json.loads(IN_FILE.read_text()) if IN_FILE.exists() else []
    log.info("Items clasificados: %d", len(items))

    if len(items) < 3:
        log.warning("Menos de 3 items relevantes, generando edición 'sin señal'.")
        text = empty_edition(now, edition)
    else:
        text = generate(items, now, edition=edition)

    path = write_edition(text, now)
    log.info("Edición escrita: %s", path)
    print(str(path))
    return 0


if __name__ == "__main__":
    sys.exit(main())
