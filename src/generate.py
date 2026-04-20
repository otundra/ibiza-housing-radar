"""Compositor de la edición semanal bajo el modelo documental.

El LLM no genera propuestas propias: solo compone la edición semanal a
partir de noticias clasificadas + propuestas ya extraídas + rescate.

Principios:
- Cero inferencia del LLM: todo lo que aparece en la edición debe estar
  soportado por el input.
- URL literal en cada propuesta (ya garantizada por extract.py).
- Verbos descriptivos solamente. Lista de verbos prohibidos en el prompt
  y verificada luego por verify.py.

Modelo: Opus 4.7 con prompt caching del SYSTEM. Decisión 2026-04-20.
"""
from __future__ import annotations

import json
import logging
import os
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

import anthropic

from src.costs import record_call, assert_budget_available

log = logging.getLogger("generate")

ROOT = Path(__file__).resolve().parent.parent
CLASSIFIED_FILE = ROOT / "data" / "classified.json"
EXTRACTED_FILE = ROOT / "data" / "extracted.json"
RESCUE_FILE = ROOT / "data" / "rescue.json"
EDITIONS_DIR = ROOT / "docs" / "_editions"

MODEL = "claude-opus-4-7"

SYSTEM = """Eres el documentalista de Ibiza Housing Radar, un observatorio semanal sobre la crisis de vivienda en Ibiza con foco en trabajadores de temporada (mayo-octubre).

TU TRABAJO ES COMPONER la edición semanal reuniendo, ordenando y presentando contenido que YA te pasamos previamente extraído. TÚ NO GENERAS PROPUESTAS PROPIAS. Tú no propones, no opinas, no rellenas. Solo documentas.

Las 5 reglas duras vinculantes del observatorio:
1. Solo se documentan propuestas con autor identificado y URL verificable.
2. El observatorio NO genera propuestas propias.
3. Ningún actor queda excluido por filiación.
4. Balance de actores auditado y publicado cada trimestre.
5. Correcciones públicas con traza.

ESTRUCTURA EXACTA del markdown de salida:

---
layout: edition
title: "<usa LITERAL el título que te paso en el user prompt>"
week: "YYYY-WWW"
date: YYYY-MM-DD
permalink: /ediciones/YYYY-wWW/
excerpt: "<síntesis 1 frase ≤160 caracteres>"
model: "pivote-documental-v1"
proposals_formal_count: <N>
proposals_en_movimiento_count: <N>
actors_cited: [<lista de strings con los nombres de actores>]
blocks_cited: [<lista de actor_type usados>]
omissions_count: <N>
rescued_count: <N>
---

## 📡 Señales detectadas

4-8 bullets, uno por señal relevante de la semana. Cada bullet:
- Hecho concreto + enlace markdown a la fuente (URL del input, literal).
- Sin valoración, sin "esto es preocupante", sin "urge hacer algo".

## 🗓 Cronología

3 líneas describiendo el orden temporal de los hechos relevantes esta semana. Sin interpretación, sin valoración, sin "ventana de decisión". Solo ordenar.

## 🗺 Mapa de posiciones

Tabla compacta con las posiciones expresadas por actores sobre los temas principales de la semana:

| Propuesta / tema | Actor | Posición | Fuente |
|---|---|---|---|
| <tema> | <actor> | propone / apoya / rechaza / matiza | [↗](URL) |

Solo con posiciones que aparezcan EXPLÍCITAMENTE en las noticias proporcionadas.

## 📋 Propuestas en circulación

Sección ABIERTA con las propuestas `formal` de esta semana (del input `extracted`). Para cada una:

### <N>. <Título corto fiel al statement_summary>

**Actor que la propone:** <actor> (<actor_type>) — [fuente](<url_source>)

**Qué:** <statement_summary>

- **Actor que tendría que ejecutarla:** <target_actor>
- **Estado:** <state>
- **Horizonte:** <horizon>
- **Viabilidad jurídica:** <viability_legal> — <viability_legal_reason o "sin evaluación pública">
- **Viabilidad económica:** <viability_economic> — <viability_economic_reason o "sin cifra pública disponible">
- **Apoyos públicos citados:** <supporters_cited joined or "ninguno registrado esta semana">
- **Rechazos públicos citados:** <opponents_cited joined or "ninguno registrado esta semana">
- **Precedentes citados:** <precedents si los hay, con URL>

Si no hay propuestas formales esta semana, escribe LITERALMENTE:
> Esta semana no se han registrado propuestas formales en circulación. Revisa las secciones "Radar" y "Omisiones" para el contexto.

## 📡 Radar: señales en movimiento

Propuestas `en_movimiento` (del input `extracted`): intenciones declaradas sin medida concreta todavía. Misma ficha que Propuestas en circulación, pero con la anotación clara de que no son propuesta formal aún.

Si no hay: "Esta semana no hay señales en movimiento registradas."

## 🗄 Rescate

1-2 propuestas del input `rescue_candidates` (si existen), con ficha completa + frase corta explicando por qué se rescata (ej. "Lleva 5 semanas sin movimiento público tras anunciarse").

Si no hay: omitir la sección.

## 🕳 Omisiones

Hechos documentados esta semana (del input `classified`) que NO tienen propuesta asociada. 1-3 bullets describiendo el vacío:

- <hecho>: ningún actor ha propuesto nada al respecto esta semana.

Si no se detecta ninguna omisión relevante, omitir la sección.

## 👀 A vigilar la semana que viene

3-5 bullets con fechas y decisiones pendientes concretas, extraídas de los hechos de la semana. No inventar.

---

VERBOS PERMITIDOS (descriptivos): propone, reclama, rechaza, presenta, solicita, exige, pide, plantea, anuncia, dice, señala, denuncia, reitera, confirma, prevé, documenta, publica, comunica.

VERBOS PROHIBIDOS (no los uses bajo ninguna circunstancia, el verificador automático bloquea la publicación si aparecen): debería, convendría, sería oportuno, hace falta, urge, proponemos, habría que, toca, corresponde, es necesario, se debe, hay que.

REGLAS DURAS ADICIONALES:
- Cada enlace markdown debe usar UNA URL del input. Jamás inventes URL.
- Cada cifra debe estar en el input. Jamás la redondees al alza ni a la baja.
- Coaliciones: reproduce los firmantes literales separados por coma. No elijas "primario".
- Si la semana es floja (poca señal, pocas propuestas), sé honesto: mejor secciones cortas que secciones infladas.
- No saludes, no te despidas, no firmes. El editor se encarga.
- No uses lenguaje corporativo ("sinergia", "empoderar", "hoja de ruta").
- No uses emojis fuera de los títulos de sección que ya vienen arriba.
"""


USER_TEMPLATE = """Semana ISO: {iso_week}
Fecha corte: {cutoff_date}
Título de la edición (ÚSALO LITERAL en el frontmatter `title`, entre comillas): {edition_title}
Permalink: /ediciones/{edition_slug}/

INPUT 1 — Señales clasificadas (toda la semana, con is_housing=true):
{classified}

INPUT 2 — Propuestas ya extraídas (formal + en_movimiento):
{extracted}

INPUT 3 — Candidatas a rescate de ediciones previas (elige 1-2 máximo):
{rescue_candidates}

Escribe la edición completa siguiendo la estructura exacta del system prompt. Empieza por el frontmatter YAML y termina con la sección "A vigilar". Nada más. Nada antes. Nada después."""


MONTHS_ES = [
    "",
    "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
    "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre",
]


def iso_week_string(dt: datetime) -> str:
    iso = dt.isocalendar()
    return f"{iso.year}-W{iso.week:02d}"


def edition_slug(dt: datetime) -> str:
    iso = dt.isocalendar()
    return f"{iso.year}-w{iso.week:02d}"


def human_week_title(dt: datetime) -> str:
    monday = (dt - timedelta(days=dt.weekday())).replace(
        hour=0, minute=0, second=0, microsecond=0, tzinfo=None
    )
    thursday = monday + timedelta(days=3)
    week_of_month = (thursday.day - 1) // 7 + 1
    month_name = MONTHS_ES[thursday.month]
    return f"Semana {week_of_month} - {month_name} {thursday.year}"


def minimal_frontmatter(now: datetime) -> str:
    iso = now.isocalendar()
    return (
        "---\n"
        f'layout: edition\n'
        f'title: "{human_week_title(now)}"\n'
        f'week: "{iso.year}-W{iso.week:02d}"\n'
        f'date: {now.strftime("%Y-%m-%d")}\n'
        f'permalink: /ediciones/{iso.year}-w{iso.week:02d}/\n'
        f'excerpt: "Informe automático — revisar salida."\n'
        f'model: "pivote-documental-v1"\n'
        "---"
    )


def empty_edition(now: datetime) -> str:
    return f"""---
layout: edition
title: "{human_week_title(now)}"
week: "{iso_week_string(now)}"
date: {now.strftime('%Y-%m-%d')}
permalink: /ediciones/{edition_slug(now)}/
excerpt: "Semana sin señal: no se han detectado noticias relevantes sobre vivienda en Ibiza."
model: "pivote-documental-v1"
proposals_formal_count: 0
proposals_en_movimiento_count: 0
actors_cited: []
blocks_cited: []
omissions_count: 0
rescued_count: 0
---

## 📡 Señales detectadas

*No se han encontrado noticias relevantes esta semana sobre vivienda o trabajadores de temporada en Ibiza.*

## 🗓 Cronología

Silencio informativo. Puede significar ausencia real de actividad pública, ciclo de agenda política, o fallo en la ingesta. Revisar manualmente los diarios locales antes de asumir ausencia real.

## 👀 A vigilar la semana que viene

- Revisar manualmente Diario de Ibiza, Periódico de Ibiza y BOIB.
- Comprobar logs del workflow en GitHub Actions.
"""


def slim_classified(classified: list[dict]) -> list[dict]:
    return [
        {
            "title": c.get("title", ""),
            "headline_es": c.get("headline_es", ""),
            "url": c.get("url", ""),
            "published": c.get("published", ""),
            "actor": c.get("actor", ""),
            "lever": c.get("lever", ""),
            "proposal_type": c.get("proposal_type", ""),
        }
        for c in classified
    ]


def slim_extracted(extracted: list[dict]) -> list[dict]:
    out = []
    for item in extracted:
        for prop in item.get("proposals", []):
            slim = {
                "actor": prop.get("actor", ""),
                "actor_type": prop.get("actor_type", ""),
                "statement_summary": prop.get("statement_summary", ""),
                "url_source": prop.get("url_source", ""),
                "palanca": prop.get("palanca", ""),
                "target_actor": prop.get("target_actor", ""),
                "horizon": prop.get("horizon", ""),
                "state": prop.get("state", ""),
                "viability_legal": prop.get("viability_legal", "no_evaluada"),
                "viability_legal_reason": prop.get("viability_legal_reason", ""),
                "viability_economic": prop.get("viability_economic", "no_evaluada"),
                "viability_economic_reason": prop.get("viability_economic_reason", ""),
                "supporters_cited": prop.get("supporters_cited", []) or [],
                "opponents_cited": prop.get("opponents_cited", []) or [],
                "precedents": prop.get("precedents", []) or [],
            }
            out.append(slim)
    return out


def generate(
    classified: list[dict],
    extracted: list[dict],
    rescue_candidates: list[dict],
    now: datetime,
    edition: str,
) -> str:
    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

    slim_cls = slim_classified(classified)
    slim_ext = slim_extracted(extracted)

    prompt = USER_TEMPLATE.format(
        iso_week=iso_week_string(now),
        cutoff_date=now.strftime("%Y-%m-%d"),
        edition_title=human_week_title(now),
        edition_slug=edition_slug(now),
        classified=json.dumps(slim_cls, ensure_ascii=False, indent=2),
        extracted=json.dumps(slim_ext, ensure_ascii=False, indent=2),
        rescue_candidates=json.dumps(rescue_candidates[:3], ensure_ascii=False, indent=2),
    )

    assert_budget_available(planned_cost=1.5)

    log.info("Generando edición con %s (classified=%d, extracted=%d, rescue=%d)",
             MODEL, len(slim_cls), len(slim_ext), len(rescue_candidates))

    resp = client.messages.create(
        model=MODEL,
        max_tokens=8192,
        system=[{"type": "text", "text": SYSTEM, "cache_control": {"type": "ephemeral"}}],
        messages=[{"role": "user", "content": prompt}],
    )
    record_call(
        edition=edition,
        stage="generate",
        model=MODEL,
        usage=resp.usage.model_dump() if hasattr(resp.usage, "model_dump") else dict(resp.usage),
    )

    text = "".join(block.text for block in resp.content if block.type == "text").strip()
    if not text.startswith("---"):
        log.warning("Salida sin frontmatter. Añadiendo mínimo.")
        text = minimal_frontmatter(now) + "\n\n" + text
    return text


def write_edition(text: str, now: datetime) -> Path:
    EDITIONS_DIR.mkdir(parents=True, exist_ok=True)
    path = EDITIONS_DIR / f"{edition_slug(now)}.md"
    path.write_text(text)
    return path


def main() -> int:
    logging.basicConfig(level=logging.INFO, format="[%(levelname)s %(name)s] %(message)s")
    now = datetime.now(timezone.utc)
    edition = iso_week_string(now)
    os.environ["EDITION"] = edition

    classified = json.loads(CLASSIFIED_FILE.read_text()) if CLASSIFIED_FILE.exists() else []
    extracted = json.loads(EXTRACTED_FILE.read_text()) if EXTRACTED_FILE.exists() else []
    rescue_candidates = json.loads(RESCUE_FILE.read_text()) if RESCUE_FILE.exists() else []

    housing = [c for c in classified if c.get("is_housing")]
    log.info("Input: %d clasificados housing, %d bloques extraídos, %d candidatos rescate.",
             len(housing), len(extracted), len(rescue_candidates))

    if len(housing) < 3:
        log.warning("Menos de 3 señales; escribiendo edición 'sin señal'.")
        text = empty_edition(now)
    else:
        text = generate(housing, extracted, rescue_candidates, now, edition=edition)

    path = write_edition(text, now)
    log.info("Edición escrita: %s", path)
    print(str(path))
    return 0


if __name__ == "__main__":
    sys.exit(main())
