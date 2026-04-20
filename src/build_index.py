"""Regenera docs/index.md con la lista de ediciones ordenadas DESC."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EDITIONS_DIR = ROOT / "docs" / "editions"
INDEX_FILE = ROOT / "docs" / "index.md"


FRONT_RE = re.compile(r"^---\n(.*?)\n---", re.DOTALL)


def parse_frontmatter(text: str) -> dict[str, str]:
    m = FRONT_RE.match(text)
    if not m:
        return {}
    fm: dict[str, str] = {}
    for line in m.group(1).splitlines():
        if ":" not in line:
            continue
        k, _, v = line.partition(":")
        fm[k.strip()] = v.strip().strip('"').strip("'")
    return fm


def build() -> None:
    items = []
    if EDITIONS_DIR.exists():
        for p in sorted(EDITIONS_DIR.glob("*.md"), reverse=True):
            fm = parse_frontmatter(p.read_text())
            items.append({
                "title": fm.get("title", p.stem),
                "date": fm.get("date", ""),
                "permalink": fm.get("permalink", f"/ediciones/{p.stem}/"),
                "excerpt": fm.get("excerpt", ""),
                "week": fm.get("week", ""),
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
            lines.append(f'<article class="edition-card">')
            lines.append(f'  <div class="edition-meta">{it["date"]} · {it["week"]}</div>')
            lines.append(f'  <h2><a href="{{{{ site.baseurl }}}}{it["permalink"]}">{it["title"]}</a></h2>')
            if it["excerpt"]:
                lines.append(f'  <p class="edition-excerpt">{it["excerpt"]}</p>')
            lines.append(f'  <a class="edition-cta" href="{{{{ site.baseurl }}}}{it["permalink"]}">Leer informe →</a>')
            lines.append(f"</article>")
            lines.append("")

    INDEX_FILE.write_text("\n".join(lines))
    print(f"Index escrito: {INDEX_FILE} ({len(items)} ediciones)")


if __name__ == "__main__":
    build()
