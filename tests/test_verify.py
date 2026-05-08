"""Tests para src/verify.py — funciones deterministas sin red."""
import pytest
from src.verify import (
    split_frontmatter,
    extract_urls,
    check_forbidden_verbs,
    check_frontmatter,
    check_proposals_have_actor,
)


# ---------------------------------------------------------------------------
# split_frontmatter
# ---------------------------------------------------------------------------

def test_split_frontmatter_basic():
    md = "---\nlayout: edition\ntitle: \"Semana 17\"\n---\n\nContenido aquí."
    fm, body = split_frontmatter(md)
    assert fm["layout"] == "edition"
    assert fm["title"] == "Semana 17"
    assert body.startswith("Contenido")


def test_split_frontmatter_no_frontmatter():
    md = "Solo cuerpo sin cabecera."
    fm, body = split_frontmatter(md)
    assert fm == {}
    assert body == md


def test_split_frontmatter_missing_close():
    md = "---\nlayout: edition\n\nSin cierre de frontmatter."
    fm, body = split_frontmatter(md)
    assert fm == {}


# ---------------------------------------------------------------------------
# extract_urls
# ---------------------------------------------------------------------------

def test_extract_urls_markdown_link():
    body = "Ver [noticia](https://diariodeibiza.es/noticia-1) para más."
    urls = extract_urls(body)
    assert "https://diariodeibiza.es/noticia-1" in urls


def test_extract_urls_autolink():
    body = "Fuente: <https://periodicodeibiza.es/nota>"
    urls = extract_urls(body)
    assert "https://periodicodeibiza.es/nota" in urls


def test_extract_urls_dedup():
    body = "[a](https://example.com) y [b](https://example.com)"
    urls = extract_urls(body)
    assert urls.count("https://example.com") == 1


def test_extract_urls_empty():
    assert extract_urls("Sin enlaces.") == []


# ---------------------------------------------------------------------------
# check_forbidden_verbs
# ---------------------------------------------------------------------------

def test_forbidden_verb_detected():
    body = "Esta propuesta debería aprobarse en el Consell."
    findings = check_forbidden_verbs(body)
    assert any(f["verb"] == "debería" for f in findings)


def test_forbidden_verb_clean_text():
    body = "El Consell aprobó el plan de residencias para temporeros."
    assert check_forbidden_verbs(body) == []


def test_forbidden_verb_not_triggered_in_url():
    # La URL contiene "deberia" pero no debe disparar el verbo prohibido
    body = "[ver](https://example.com/deberia-hacerse)"
    findings = check_forbidden_verbs(body)
    assert findings == []


def test_forbidden_verb_hay_que():
    body = "El diputado dijo que hay que actuar de inmediato."
    findings = check_forbidden_verbs(body)
    assert any("hay que" in f["verb"] for f in findings)


# ---------------------------------------------------------------------------
# check_frontmatter
# ---------------------------------------------------------------------------

def test_frontmatter_all_required():
    fm = {"layout": "edition", "title": "T", "week": "2026-w17",
          "date": "2026-04-20", "permalink": "/ediciones/2026-04-20/"}
    assert check_frontmatter(fm) == []


def test_frontmatter_missing_fields():
    fm = {"layout": "edition", "title": "T"}
    issues = check_frontmatter(fm)
    assert any("week" in i for i in issues)
    assert any("date" in i for i in issues)
    assert any("permalink" in i for i in issues)


# ---------------------------------------------------------------------------
# check_proposals_have_actor
# ---------------------------------------------------------------------------

def test_proposals_with_actor_ok():
    extracted = [{"news_id": "n1", "proposals": [
        {"actor": "Consell d'Eivissa", "url_source": "https://x.com",
         "statement_summary": "propuesta de residencias"}
    ]}]
    assert check_proposals_have_actor(extracted) == []


def test_proposals_missing_actor():
    extracted = [{"news_id": "n1", "proposals": [
        {"actor": "", "url_source": "https://x.com",
         "statement_summary": "propuesta sin actor"}
    ]}]
    missing = check_proposals_have_actor(extracted)
    assert len(missing) == 1
    assert missing[0]["news_id"] == "n1"


def test_proposals_no_proposals_key():
    extracted = [{"news_id": "n1"}]
    assert check_proposals_have_actor(extracted) == []
