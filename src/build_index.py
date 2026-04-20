"""Regenera docs/index.md con la lista de ediciones ordenadas DESC.

Cada tarjeta muestra, además del título y el excerpt, la sección "Lectura"
completa de la edición (2-3 frases con enlaces y negritas) para dar al lector
una idea sustancial del informe sin tener que entrar.
"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EDITIONS_DIR = ROOT / "docs" / "editions"
INDEX_FILE = ROOT / "docs" / "index.md"


FRONT_RE = re.compile(r"^---\n(.*?)\n---\s*\n?(.*)$", re.DOTALL)
# Captura el contenido desde "## ... Lectura" hasta el siguiente `## ` o fin.
LECTURA_RE = re.compile(
    r"^##\s+[^\n]*Lectura\s*\n(.*?)(?=^##\s|\Z)",
    re.DOTALL | re.MULTILINE,
)


def parse_file(text: str) -> tuple[dict[str, str], str]:
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


def extract_lectura(body: str) -> str:
    m = LECTURA_RE.search(body)
    if not m:
        return ""
    return m.group(1).strip()


def build() -> None:
    items = []
    if EDITIONS_DIR.exists():
        for p in sorted(EDITIONS_DIR.glob("*.md"), reverse=True):
            fm, body = parse_file(p.read_text())
            items.append({
                "title": fm.get("title", p.stem),
                "date": fm.get("date", ""),
                "permalink": fm.get("permalink", f"/ediciones/{p.stem}/"),
                "excerpt": fm.get("excerpt", ""),
                "week": fm.get("week", ""),
                "lectura": extract_lectura(body),
            })

    lines = [
        "---",
        "layout: home",
        "title: Inicio",
        "permalink: /",
        "---",
        "",
    ]

    if not items:
        lines.append("*Aún no hay ediciones publicadas. La primera saldrá el próximo lunes.*")
    else:
        for it in items:
            permalink = f'{{{{ site.baseurl }}}}{it["permalink"]}'
            lines.append('<article class="edition-card" markdown="1">')
            lines.append("")
            lines.append(f'<div class="edition-meta">{it["date"]} · {it["week"]}</div>')
            lines.append("")
            lines.append(f'## [{it["title"]}]({permalink})')
            lines.append("")
            if it["excerpt"]:
                lines.append(f'<p class="edition-excerpt">{it["excerpt"]}</p>')
                lines.append("")
            if it["lectura"]:
                lines.append('<div class="edition-lectura" markdown="1">')
                lines.append("")
                lines.append(it["lectura"])
                lines.append("")
                lines.append("</div>")
                lines.append("")
            lines.append(f'[Leer informe →]({permalink}){{:.edition-cta}}')
            lines.append("")
            lines.append("</article>")
            lines.append("")

    INDEX_FILE.write_text("\n".join(lines))
    print(f"Index escrito: {INDEX_FILE} ({len(items)} ediciones)")


if __name__ == "__main__":
    build()
