"""Tests para src/rescue.py — lógica de puntuación y selección de candidatos."""
from datetime import datetime, timedelta, timezone
import pytest
from src.rescue import age_weeks, score_candidate, pick_candidates


def _prop(state="en_debate", weeks_ago=5, prop_id="p1"):
    first_seen = (datetime.now(timezone.utc) - timedelta(weeks=weeks_ago)).isoformat()
    return {"id": prop_id, "state": state, "first_seen": first_seen}


# ---------------------------------------------------------------------------
# age_weeks
# ---------------------------------------------------------------------------

def test_age_weeks_recent():
    prop = _prop(weeks_ago=2)
    assert 1.8 < age_weeks(prop) < 2.2


def test_age_weeks_old():
    prop = _prop(weeks_ago=12)
    assert 11.5 < age_weeks(prop) < 12.5


def test_age_weeks_no_date():
    assert age_weeks({}) == 0.0


# ---------------------------------------------------------------------------
# score_candidate
# ---------------------------------------------------------------------------

def test_score_propuesta_higher_than_en_debate():
    # STATE_RANK: propuesta=4 > en_debate=3
    p_propuesta = _prop(state="propuesta", weeks_ago=8)
    p_debate = _prop(state="en_debate", weeks_ago=8)
    assert score_candidate(p_propuesta) > score_candidate(p_debate)


def test_score_sweet_spot_age():
    p_near = _prop(state="en_debate", weeks_ago=8)
    p_far = _prop(state="en_debate", weeks_ago=1)
    assert score_candidate(p_near) > score_candidate(p_far)


# ---------------------------------------------------------------------------
# pick_candidates
# ---------------------------------------------------------------------------

def test_pick_candidates_filters_too_recent():
    history = [_prop(weeks_ago=1, prop_id="recent")]
    result = pick_candidates(history, recent_slugs=[])
    assert not any(c["id"] == "recent" for c in result)


def test_pick_candidates_filters_too_old():
    history = [_prop(weeks_ago=20, prop_id="old")]
    result = pick_candidates(history, recent_slugs=[])
    assert not any(c["id"] == "old" for c in result)


def test_pick_candidates_filters_terminal_states():
    for state in ("implementada", "descartada"):
        history = [_prop(state=state, weeks_ago=6, prop_id=f"p_{state}")]
        result = pick_candidates(history, recent_slugs=[])
        assert result == [], f"Estado '{state}' no debería ser candidato"


def test_pick_candidates_max_5():
    history = [_prop(weeks_ago=6, prop_id=f"p{i}") for i in range(10)]
    result = pick_candidates(history, recent_slugs=[])
    assert len(result) <= 5


def test_pick_candidates_ordered_by_score():
    # STATE_RANK: propuesta(4) > en_debate(3) → propuesta aparece primero
    p_debate = _prop(state="en_debate", weeks_ago=8, prop_id="debate")
    p_propuesta = _prop(state="propuesta", weeks_ago=8, prop_id="propuesta")
    result = pick_candidates([p_debate, p_propuesta], recent_slugs=[])
    ids = [c["id"] for c in result]
    assert ids.index("propuesta") < ids.index("debate")


def test_pick_candidates_no_id_skipped():
    history = [{"state": "en_debate", "first_seen": _prop(weeks_ago=6)["first_seen"]}]
    result = pick_candidates(history, recent_slugs=[])
    assert result == []
