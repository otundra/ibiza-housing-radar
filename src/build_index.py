"""Regenera docs/index.md como panel editorial de la última edición.

La home ya no es una lista de ediciones: es la edición más reciente desplegada
en secciones (lectura, señales, propuestas, a-vigilar) más un archivo compacto
con las anteriores. Cada propuesta enlaza al ancla dentro de la edición.

Importante: el HTML generado va SIN sangrado porque kramdown (GFM) convierte
líneas sangradas ≥4 espacios en bloques de código; eso rompe el render cuando
el HTML envuelve bloques que procesan markdown.
"""
from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from src.labels import horizon_label, state_label

ROOT = Path(__file__).resolve().parent.parent
EDITIONS_DIR = ROOT / "docs" / "_editions"
INDEX_FILE = ROOT / "docs" / "index.md"

FRONT_RE = re.compile(r"^---\n(.*?)\n---\s*\n?(.*)$", re.DOTALL)
H2_SPLIT_RE = re.compile(r"^##\s+([^\n]+)\n(.*?)(?=^##\s|\Z)", re.DOTALL | re.MULTILINE)
PROPUESTA_SPLIT_RE = re.compile(r"^###\s+(\d+)\.\s+", re.MULTILINE)

FIELD_RE = {
    "actor": re.compile(r"^\*\*Actor que la propone:\*\*\s*(.+?)$", re.MULTILINE),
    "estado": re.compile(r"^-\s*\*\*Estado:\*\*\s*(.+?)$", re.MULTILINE),
    "horizonte": re.compile(r"^-\s*\*\*Horizonte:\*\*\s*(.+?)$", re.MULTILINE),
    "target_actor": re.compile(r"^-\s*\*\*Actor que tendría que ejecutarla:\*\*\s*(.+?)$", re.MULTILINE),
}
QUE_RE = re.compile(r"\*\*Qu[eé]:\*\*\s*(.+?)(?=\n\n|\n-\s*\*\*|\Z)", re.DOTALL)


def parse_frontmatter(text: str) -> tuple[dict[str, str], str]:
    m = FRONT_RE.match(text)
    if not m:
        return {}, text
    fm: dict[str, str] = {}
    for line in m.group(1).splitlines():
        if ":" not in line:
            continue
        k, _, v = line.partition(":")
        fm[k.strip()] = v.strip().strip('"').strip("'")
    return fm, m.group(2)


def normalize_heading(title: str) -> str:
    """Pasa el título a minúsculas y elimina símbolos/emojis para matching."""
    s = re.sub(r"[^\w\s]", "", title, flags=re.UNICODE)
    return s.strip().lower()


def split_h2(body: str) -> dict[str, str]:
    out: dict[str, str] = {}
    for m in H2_SPLIT_RE.finditer(body):
        out[normalize_heading(m.group(1))] = m.group(2).strip()
    return out


def find_section(sections: dict[str, str], keyword: str) -> str:
    kw = keyword.lower()
    for key, content in sections.items():
        if kw in key:
            return content
    return ""


def slugify_kramdown(text: str) -> str:
    """Slug que coincide con el auto_id de kramdown (GFM) por defecto.

    Pasa a minúsculas, conserva acentos y dígitos, reemplaza espacios por
    guiones y elimina signos de puntuación.
    """
    s = text.lower()
    s = re.sub(r"[^\w\s-]", "", s, flags=re.UNICODE)
    s = re.sub(r"\s+", "-", s.strip())
    s = re.sub(r"-+", "-", s)
    return s


def extract_field(pattern: re.Pattern[str], text: str) -> str:
    m = pattern.search(text)
    return m.group(1).strip() if m else ""


def clean_actor(actor: str) -> str:
    """Deja solo el nombre del actor para mostrar en el card de la home.

    Los valores del markdown vienen como:
      "Consell d'Eivissa, patronales, sindicatos (Coalición institucional) — [fuente](URL)"
    En el card queremos solo los nombres, sin el tipo entre paréntesis ni el
    enlace. La regex final cubre tanto la forma legible (con espacios) como
    los códigos heredados (con guion bajo) por si quedan ediciones antiguas.
    """
    s = actor
    s = re.sub(r"\s*—\s*\[fuente\]\([^)]+\).*$", "", s)
    s = re.sub(r"\s*\([^)]+\)\s*$", "", s)
    return s.strip()


def pluralize(n: int, singular: str, plural: str) -> str:
    return f"{n} {singular}" if n == 1 else f"{n} {plural}"


def parse_propuestas(content: str) -> list[dict[str, Any]]:
    parts = PROPUESTA_SPLIT_RE.split(content)
    if len(parts) < 3:
        return []
    results: list[dict[str, Any]] = []
    for i in range(1, len(parts) - 1, 2):
        num = int(parts[i])
        body = parts[i + 1].strip()
        if not body:
            continue
        title_line, _, rest = body.partition("\n")
        titulo = title_line.strip()
        results.append({
            "num": num,
            "titulo": titulo,
            "slug": slugify_kramdown(f"{num}-{titulo}"),
            "que": extract_field(QUE_RE, rest),
            "actor": clean_actor(extract_field(FIELD_RE["actor"], rest)),
            "estado": extract_field(FIELD_RE["estado"], rest),
            "horizonte": extract_field(FIELD_RE["horizonte"], rest),
            "target_actor": extract_field(FIELD_RE["target_actor"], rest),
        })
    return results


def parse_edition(path: Path) -> dict[str, Any]:
    text = path.read_text()
    fm, body = parse_frontmatter(text)
    sections = split_h2(body)
    return {
        "title": fm.get("title", path.stem),
        "date": fm.get("date", ""),
        "week": fm.get("week", ""),
        "permalink": fm.get("permalink", f"/ediciones/{path.stem}/"),
        "excerpt": fm.get("excerpt", ""),
        "senales": find_section(sections, "senales") or find_section(sections, "señales"),
        "cronologia": find_section(sections, "cronologia") or find_section(sections, "cronología"),
        "propuestas": parse_propuestas(find_section(sections, "propuestas en circulación") or find_section(sections, "propuestas")),
        "a_vigilar": find_section(sections, "vigilar"),
    }


def count_bullets(markdown_block: str) -> int:
    return len(re.findall(r"^[-*]\s+", markdown_block, re.MULTILINE))


def render_empty() -> str:
    return """---
layout: home
title: Inicio
permalink: /
---

<section class="dash-empty">
<p><em>Aún no hay ediciones publicadas. La primera saldrá el próximo lunes.</em></p>
</section>
"""


def render_index(editions: list[dict[str, Any]]) -> str:
    if not editions:
        return render_empty()

    latest = editions[0]
    others = editions[1:]
    baseurl = "{{ site.baseurl }}"
    permalink = f"{baseurl}{latest['permalink']}"
    n_senales = count_bullets(latest["senales"])
    n_vigilar = count_bullets(latest["a_vigilar"])
    n_propuestas = len(latest["propuestas"])

    out: list[str] = [
        "---",
        "layout: home",
        "title: Inicio",
        "permalink: /",
        "---",
        "",
    ]

    # ---------- COVER (above-the-fold) ----------
    out.append('<section class="dash-cover">')
    out.append('<p class="dash-cover-kicker">')
    out.append('<span class="dash-pulse" aria-hidden="true"></span>')
    out.append(f'<span>Informe semanal · actualizado {latest["date"]}</span>')
    out.append('</p>')
    out.append('<div class="dash-cover-grid">')

    # Main: headline + cronología + CTAs
    out.append('<div class="dash-cover-main">')
    out.append(f'<p class="dash-cover-eyebrow">{latest["title"]}</p>')
    out.append(f'<h1 class="dash-cover-headline">{latest["excerpt"]}</h1>')
    if latest["cronologia"]:
        out.append('<div class="dash-cover-lectura" markdown="1">')
        out.append('')
        out.append(latest["cronologia"])
        out.append('')
        out.append('</div>')
    out.append('<div class="dash-cover-ctas">')
    out.append(f'<a href="{permalink}" class="dash-cta-primary">Leer informe completo →</a>')
    if n_senales:
        out.append(f'<a href="#senales" class="dash-cta-secondary">Ver las {n_senales} señales ↓</a>')
    out.append('</div>')
    out.append('</div>')

    # Aside: preview de propuestas + a-vigilar compacto
    out.append('<aside class="dash-cover-aside">')
    if latest["propuestas"]:
        out.append('<section class="dash-aside-block">')
        out.append(f'<p class="dash-aside-kicker">{pluralize(n_propuestas, "propuesta documentada", "propuestas documentadas")}</p>')
        out.append('<h2 class="dash-aside-title">Qué se ha propuesto esta semana</h2>')
        out.append('<ol class="dash-aside-list dash-aside-propuestas">')
        for p in latest["propuestas"]:
            link = f"{permalink}#{p['slug']}"
            out.append('<li>')
            out.append(f'<span class="dash-aside-num">{p["num"]:02d}</span>')
            out.append(f'<a href="{link}">{p["titulo"]}</a>')
            out.append('</li>')
        out.append('</ol>')
        out.append('<a href="#propuestas" class="dash-aside-more">Detalle de las propuestas ↓</a>')
        out.append('</section>')
    if latest["a_vigilar"]:
        out.append('<section class="dash-aside-block">')
        out.append(f'<p class="dash-aside-kicker">{n_vigilar} puntos</p>')
        out.append('<h2 class="dash-aside-title">A vigilar</h2>')
        out.append('<div class="dash-aside-vigilar" markdown="1">')
        out.append('')
        out.append(latest["a_vigilar"])
        out.append('')
        out.append('</div>')
        out.append('</section>')
    out.append('</aside>')

    out.append('</div>')
    out.append('</section>')
    out.append('')

    # ---------- SEÑALES ----------
    if latest["senales"]:
        out.append('<section class="dash-senales" id="senales">')
        out.append('<header class="dash-section-header">')
        out.append('<p class="dash-section-kicker">Señales detectadas</p>')
        out.append(f'<h2>{n_senales} hechos publicados esta semana</h2>')
        out.append('<p class="dash-section-lead">Cada punto enlaza a la noticia original en su medio. Sin resumen sesgado: cifras y fechas tal como se publicaron.</p>')
        out.append('</header>')
        out.append('<div class="dash-senales-list" markdown="1">')
        out.append('')
        out.append(latest["senales"])
        out.append('')
        out.append('</div>')
        out.append('</section>')
        out.append('')

    # ---------- PROPUESTAS (cards detalladas) ----------
    if latest["propuestas"]:
        out.append('<section class="dash-propuestas" id="propuestas">')
        out.append('<header class="dash-section-header">')
        out.append('<p class="dash-section-kicker">Propuestas documentadas</p>')
        out.append(f'<h2>{pluralize(n_propuestas, "propuesta en circulación", "propuestas en circulación")} esta semana</h2>')
        out.append('<p class="dash-section-lead">Cada propuesta la ha formulado un actor con nombre, con fuente verificable. El observatorio no genera propuestas propias.</p>')
        out.append('</header>')
        out.append('<div class="dash-propuestas-grid">')
        for p in latest["propuestas"]:
            link = f"{permalink}#{p['slug']}"
            out.append('<article class="dash-propuesta">')
            out.append(f'<div class="dash-propuesta-num">{p["num"]:02d}</div>')
            out.append(f'<h3 class="dash-propuesta-title"><a href="{link}">{p["titulo"]}</a></h3>')
            if p["que"]:
                out.append(f'<p class="dash-propuesta-que">{p["que"]}</p>')
            out.append('<dl class="dash-propuesta-meta">')
            if p["actor"]:
                out.append(f'<dt>Propone</dt><dd>{p["actor"]}</dd>')
            if p["estado"]:
                out.append(f'<dt>Estado</dt><dd>{state_label(p["estado"])}</dd>')
            if p["horizonte"]:
                out.append(f'<dt>Horizonte</dt><dd>{horizon_label(p["horizonte"])}</dd>')
            out.append('</dl>')
            out.append(f'<a class="dash-propuesta-link" href="{link}">Ver ficha y fuentes →</a>')
            out.append('</article>')
        out.append('</div>')
        out.append('</section>')
        out.append('')

    # ---------- A VIGILAR (sección completa) ----------
    if latest["a_vigilar"]:
        out.append('<section class="dash-vigilar" id="a-vigilar">')
        out.append('<header class="dash-section-header">')
        out.append('<p class="dash-section-kicker">A vigilar la próxima semana</p>')
        out.append(f'<h2>{n_vigilar} decisiones o fechas pendientes</h2>')
        out.append('<p class="dash-section-lead">Lo que aún no ha pasado pero condiciona la agenda de las próximas semanas.</p>')
        out.append('</header>')
        out.append('<div class="dash-vigilar-list" markdown="1">')
        out.append('')
        out.append(latest["a_vigilar"])
        out.append('')
        out.append('</div>')
        out.append('</section>')
        out.append('')

    # ---------- ARCHIVO COMPACTO ----------
    if others:
        preview = others[:4]
        out.append('<section class="dash-archivo">')
        out.append('<header class="dash-section-header">')
        out.append('<p class="dash-section-kicker">Informes anteriores</p>')
        if len(others) == 1:
            out.append('<h2>1 edición publicada antes de esta</h2>')
        else:
            out.append(f'<h2>{len(others)} ediciones publicadas antes de esta</h2>')
        out.append('</header>')
        out.append('<ol class="dash-archivo-list">')
        for e in preview:
            elink = f"{baseurl}{e['permalink']}"
            out.append('<li>')
            out.append(f'<time datetime="{e["date"]}">{e["date"]}</time>')
            out.append(f'<h3><a href="{elink}">{e["title"]}</a></h3>')
            if e["excerpt"]:
                out.append(f'<p>{e["excerpt"]}</p>')
            out.append('</li>')
        out.append('</ol>')
        out.append(f'<a href="{baseurl}/ediciones/" class="dash-archivo-cta">Ir al archivo completo →</a>')
        out.append('</section>')
        out.append('')

    # ---------- SOBRE EL PROYECTO ----------
    out.append('<section class="dash-about">')
    out.append('<div class="dash-about-inner">')
    out.append('<p><strong>Observatorio documental.</strong> Cada lunes un sistema automático lee la prensa local (Diario de Ibiza, Periódico de Ibiza, Google News), identifica propuestas que actores con nombre han formulado públicamente esa semana, las contrasta con fuente primaria y publica la edición. No genera propuestas propias.</p>')
    out.append(f'<p>Editado por Raúl S. Coste operativo ~6-7 €/mes proyectado, con topes automáticos. <a href="{baseurl}/acerca/">Sobre el proyecto →</a></p>')
    out.append('</div>')
    out.append('</section>')
    out.append('')

    return "\n".join(out)


def build() -> None:
    editions: list[dict[str, Any]] = []
    if EDITIONS_DIR.exists():
        for p in sorted(EDITIONS_DIR.glob("*.md"), reverse=True):
            editions.append(parse_edition(p))
    INDEX_FILE.write_text(render_index(editions))
    print(f"Index escrito: {INDEX_FILE} ({len(editions)} ediciones)")


if __name__ == "__main__":
    build()
