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


def _resolve_gnews(url: str) -> str:
    """Resuelve una URL firmada de news.google.com al artículo original.

    Usa la librería `googlenewsdecoder` (no hace simple redirect HTTP: es un
    esquema firmado). Si falla (rate limit, cambio de protocolo, etc.),
    devuelve la URL original intacta — el click sigue funcionando via
    redirect de Google News.
    """
    try:
        from googlenewsdecoder import gnewsdecoder
        result = gnewsdecoder(url, interval=1)
        if result.get("status") and result.get("decoded_url"):
            decoded = result["decoded_url"]
            if decoded and "google.com" not in urlparse(decoded).netloc:
                return decoded
    except Exception as e:
        log.debug("gnewsdecoder falló para %s: %s", url[:80], e)
    return url


def canonical_url(url: str) -> str:
    """Limpia trackers y resuelve URL Google News al artículo original."""
    if not url:
        return url
    parsed = urlparse(url)
    if "news.google.com" in parsed.netloc:
        # Caso trivial (a veces aparece `url=` en query)
        qs = parse_qs(parsed.query)
        if "url" in qs:
            return qs["url"][0]
        # Caso general: resolver via HTTP
        return _resolve_gnews(url)
    # Limpieza de trackers en URLs normales
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
    from concurrent.futures import ThreadPoolExecutor

    cfg = load_sources()
    keywords: list[str] = cfg["keywords"]
    lookback_days: int = cfg["lookback_days"]
    cutoff = datetime.now(timezone.utc) - timedelta(days=lookback_days)

    raw_items: list[dict[str, Any]] = []

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
            raw_link = entry.get("link", "")
            if not raw_link or not title:
                continue

            haystack = f"{title} {summary}"
            if not matches_keywords(haystack, keywords):
                continue

            pub = parse_entry_date(entry)
            if pub and pub < cutoff:
                continue

            raw_items.append({
                "title": title,
                "summary": summary,
                "raw_url": raw_link,
                "source": name,
                "published": pub.isoformat() if pub else None,
            })

    # Paralelizamos la resolución de URLs (Google News redirect)
    log.info("Resolving %d URLs in parallel...", len(raw_items))
    with ThreadPoolExecutor(max_workers=10) as ex:
        resolved = list(ex.map(canonical_url, [it["raw_url"] for it in raw_items]))
    for it, final in zip(raw_items, resolved):
        it["url"] = final
        it.pop("raw_url", None)

    # Dedup por URL canónica
    collected: dict[str, dict[str, Any]] = {}
    for it in raw_items:
        key = it["url"]
        if key in collected:
            continue
        collected[key] = it

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
