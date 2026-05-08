"""Tests para src/tiers.py — árbol de decisión determinista."""
import pytest
from src.tiers import compute_tier, _max_techo


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _signals(**kwargs):
    base = {
        "ia_consenso": "completo",
        "arbitraje": "no_hubo",
        "url_ok": True,
        "traza_dominio_actor": True,
        "fecha_coherente": None,
        "verbatim_match_ratio": 0.92,
        "wayback_snapshot": True,
        "n_fuentes_independientes": 2,
        "whitelist_match": "neutro",
        "viability_con_cifra": None,
        "statement_type": "reported",
    }
    base.update(kwargs)
    return base


# ---------------------------------------------------------------------------
# Paso 1 — Bloqueantes → rojo
# ---------------------------------------------------------------------------

def test_rojo_url_caida():
    r = compute_tier(_signals(url_ok=False))
    assert r["value"] == "rojo"
    assert "url_ok" in r["reason"]


def test_rojo_traza_mas_whitelist():
    r = compute_tier(_signals(traza_dominio_actor=False, whitelist_match="debilita"))
    assert r["value"] == "rojo"


def test_rojo_verbatim_bajo_reported():
    r = compute_tier(_signals(verbatim_match_ratio=0.40, statement_type="reported"))
    assert r["value"] == "rojo"


def test_rojo_verbatim_bajo_quote():
    r = compute_tier(_signals(verbatim_match_ratio=0.80, statement_type="quote"))
    assert r["value"] == "rojo"


def test_rojo_fecha_incoherente():
    r = compute_tier(_signals(fecha_coherente=False))
    assert r["value"] == "rojo"


def test_rojo_arbitraje_discrepa():
    r = compute_tier(_signals(arbitraje="opus_discrepa_ambas"))
    assert r["value"] == "rojo"


# ---------------------------------------------------------------------------
# Paso 2 + 3 — Techos y camino a verde
# ---------------------------------------------------------------------------

def test_verde_todas_senales_perfectas():
    r = compute_tier(_signals())
    assert r["value"] == "verde"


def test_amarillo_wayback_none_mvp():
    r = compute_tier(_signals(wayback_snapshot=None))
    assert r["value"] == "amarillo"
    assert "Wayback" in r["reason"]


def test_amarillo_fuente_unica():
    r = compute_tier(_signals(n_fuentes_independientes=1))
    assert r["value"] == "amarillo"


def test_amarillo_viability_sin_cifra():
    r = compute_tier(_signals(viability_con_cifra=False, wayback_snapshot=True))
    assert r["value"] == "amarillo"


def test_naranja_wayback_false():
    r = compute_tier(_signals(wayback_snapshot=False))
    assert r["value"] == "naranja"


def test_naranja_wayback_y_whitelist_debilita():
    r = compute_tier(_signals(
        wayback_snapshot=False,
        whitelist_match="debilita",
        traza_dominio_actor=True,
        url_ok=True,
    ))
    assert r["value"] == "naranja"


# ---------------------------------------------------------------------------
# Helpers internos
# ---------------------------------------------------------------------------

def test_max_techo_naranja_wins():
    assert _max_techo("amarillo", "naranja") == "naranja"
    assert _max_techo("naranja", "amarillo") == "naranja"


def test_max_techo_verde_base():
    assert _max_techo("verde", "amarillo") == "amarillo"
    assert _max_techo("verde", "verde") == "verde"


# ---------------------------------------------------------------------------
# Señales nulas — no bloquean
# ---------------------------------------------------------------------------

def test_none_signals_no_bloquean():
    r = compute_tier({
        "ia_consenso": "completo",
        "arbitraje": "no_hubo",
        "url_ok": True,
        "traza_dominio_actor": True,
        "verbatim_match_ratio": 0.85,
        "whitelist_match": "neutro",
        "n_fuentes_independientes": 2,
        "wayback_snapshot": None,
        "statement_type": "reported",
        # fecha_coherente, viability_con_cifra ausentes
    })
    assert r["value"] in ("verde", "amarillo")  # no rojo


def test_empty_signals_no_crash():
    r = compute_tier({})
    assert r["value"] in ("verde", "amarillo", "naranja", "rojo")
