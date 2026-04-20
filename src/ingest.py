"""Ingesta de noticias desde RSS (Google News + diarios locales).

Filtra por keywords + ventana temporal, deduplica por URL canónica,
y escribe JSON normalizado para la siguiente fase.
"""
from __future__ import annotations

import json
import logging
import re
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any
from urllib.parse import parse_qs, urlparse

import feedparser
import yaml
from dateutil import parser as dateparser

log = logging.getLogger("ingest")

ROOT = Path(__file__).resolve().parent.parent
SOURCES_FILE = ROOT / "src" / "sources.yaml"
OUT_FILE = ROOT / "data" / "ingested.json"


def load_sources() -> dict[str, Any]:
    with SOURCES_FILE.open() as f:
        return yaml.safe_load(f)


def canonical_url(url: str) -> str:
    """Limpia trackers y resuelve URL Google News cuando sea trivial."""
    if not url:
        return url
    # Google News a veces devuelve URLs con `url=` parameter
    parsed = urlparse(url)
    if "news.google.com" in parsed.netloc:
        qs = parse_qs(parsed.query)
        if "url" in qs:
            return qs["url"][0]
    # Quitar utm_ y similares
    if parsed.query:
        clean_q = "&".join(
            p for p in parsed.query.split("&")
            if not p.lower().startswith(("utm_", "fbclid", "gclid"))
        )
        return parsed._replace(query=clean_q).geturl()
    return url


def matches_keywords(text: str, keywords: list[str]) -> bool:
    lo = text.lower()
    return any(k.lower() in lo for k in keywords)


def strip_html(s: str) -> str:
    return re.sub(r"<[^>]+>", " ", s or "").strip()


def parse_entry_date(entry: dict[str, Any]) -> datetime | None:
    for key in ("published", "updated", "created"):
        v = entry.get(key)
        if not v:
            continue
        try:
            d = dateparser.parse(v)
            if d.tzinfo is None:
                d = d.replace(tzinfo=timezone.utc)
            return d
        except (ValueError, TypeError):
            continue
    return None


def ingest() -> list[dict[str, Any]]:
    cfg = load_sources()
    keywords: list[str] = cfg["keywords"]
    lookback_days: int = cfg["lookback_days"]
    cutoff = datetime.now(timezone.utc) - timedelta(days=lookback_days)

    collected: dict[str, dict[str, Any]] = {}

    for feed_cfg in cfg["feeds"]:
        name = feed_cfg["name"]
        url = feed_cfg["url"]
        log.info("Fetching %s", name)
        try:
            parsed = feedparser.parse(url)
        except Exception as e:  # pragma: no cover
            log.warning("Feed failed %s: %s", name, e)
            continue

        if getattr(parsed, "bozo", False) and not parsed.entries:
            log.warning("Feed empty or malformed: %s", name)
            continue

        for entry in parsed.entries:
            title = strip_html(entry.get("title", ""))
            summary = strip_html(entry.get("summary", ""))
            link = canonical_url(entry.get("link", ""))
            if not link or not title:
                continue

            haystack = f"{title} {summary}"
            if not matches_keywords(haystack, keywords):
                continue

            pub = parse_entry_date(entry)
            if pub and pub < cutoff:
                continue

            key = link
            if key in collected:
                continue
            collected[key] = {
                "title": title,
                "summary": summary,
                "url": link,
                "source": name,
                "published": pub.isoformat() if pub else None,
            }

    items = sorted(
        collected.values(),
        key=lambda x: x.get("published") or "",
        reverse=True,
    )
    return items


def main() -> int:
    logging.basicConfig(
        level=logging.INFO,
        format="[%(levelname)s %(name)s] %(message)s",
    )
    items = ingest()
    OUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    OUT_FILE.write_text(json.dumps(items, ensure_ascii=False, indent=2))
    log.info("Ingested %d items → %s", len(items), OUT_FILE)
    return 0


if __name__ == "__main__":
    sys.exit(main())
