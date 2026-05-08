"""Tests para src/quarantine.py — gestión de cuarentena sin I/O real."""
import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest

from src.quarantine import (
    update_quarantine,
    pending_count,
    _archive_stale,
    ARCHIVE_DAYS,
)


def _audit_rec(proposal_id, tier_value="rojo", actor="Consell", url="https://x.com"):
    return {
        "proposal_id": proposal_id,
        "week": "2026-w19",
        "created_at": "2026-05-08T03:00:00Z",
        "tier": {
            "value": tier_value,
            "reason": "url_ok=False: fuente inaccesible",
            "signals": {},
        },
        "layers": {
            "haiku": {
                "proposal": {
                    "actor": actor,
                    "actor_type": "institucional_publico",
                    "statement_summary": "Propuesta de prueba.",
                    "url_source": url,
                }
            }
        },
    }


@pytest.fixture
def quarantine_file(tmp_path, monkeypatch):
    """Redirige QUARANTINE_FILE a un archivo temporal."""
    import src.quarantine as qmod
    qfile = tmp_path / "quarantine.json"
    monkeypatch.setattr(qmod, "QUARANTINE_FILE", qfile)
    return qfile


# ---------------------------------------------------------------------------
# update_quarantine — añadir entradas
# ---------------------------------------------------------------------------

def test_add_rojo_to_quarantine(quarantine_file):
    records = [_audit_rec("p001", tier_value="rojo")]
    result = update_quarantine(records, "2026-w19")
    assert result["added"] == 1
    data = json.loads(quarantine_file.read_text())
    assert len(data["proposals"]) == 1
    assert data["proposals"][0]["proposal_id"] == "p001"
    assert data["proposals"][0]["status"] == "pending"


def test_skip_non_rojo(quarantine_file):
    records = [_audit_rec("p001", tier_value="amarillo")]
    result = update_quarantine(records, "2026-w19")
    assert result["added"] == 0
    data = json.loads(quarantine_file.read_text())
    assert data["proposals"] == []


def test_no_duplicate_adds(quarantine_file):
    records = [_audit_rec("p001", tier_value="rojo")]
    update_quarantine(records, "2026-w19")
    result = update_quarantine(records, "2026-w19")
    assert result["added"] == 0
    data = json.loads(quarantine_file.read_text())
    assert len(data["proposals"]) == 1


def test_multiple_records_mixed(quarantine_file):
    records = [
        _audit_rec("p001", tier_value="rojo"),
        _audit_rec("p002", tier_value="amarillo"),
        _audit_rec("p003", tier_value="rojo"),
    ]
    result = update_quarantine(records, "2026-w19")
    assert result["added"] == 2


# ---------------------------------------------------------------------------
# _archive_stale — regla de 60 días
# ---------------------------------------------------------------------------

def test_archive_stale_after_60_days():
    old_date = (datetime.now(timezone.utc) - timedelta(days=ARCHIVE_DAYS + 1)).strftime(
        "%Y-%m-%dT%H:%M:%SZ"
    )
    proposals = [{"proposal_id": "p001", "status": "pending", "entered_at": old_date}]
    archived = _archive_stale(proposals)
    assert archived == 1
    assert proposals[0]["status"] == "no_verificada"
    assert proposals[0]["archived_at"] is not None


def test_no_archive_recent():
    recent = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    proposals = [{"proposal_id": "p001", "status": "pending", "entered_at": recent}]
    archived = _archive_stale(proposals)
    assert archived == 0
    assert proposals[0]["status"] == "pending"


def test_no_archive_already_archived():
    old_date = (datetime.now(timezone.utc) - timedelta(days=ARCHIVE_DAYS + 5)).strftime(
        "%Y-%m-%dT%H:%M:%SZ"
    )
    proposals = [{"proposal_id": "p001", "status": "no_verificada", "entered_at": old_date}]
    archived = _archive_stale(proposals)
    assert archived == 0


# ---------------------------------------------------------------------------
# pending_count
# ---------------------------------------------------------------------------

def test_pending_count(quarantine_file):
    import src.quarantine as qmod
    records = [
        _audit_rec("p001", tier_value="rojo"),
        _audit_rec("p002", tier_value="rojo"),
    ]
    update_quarantine(records, "2026-w19")

    # Arquear manualmente una
    data = json.loads(quarantine_file.read_text())
    data["proposals"][0]["status"] = "no_verificada"
    quarantine_file.write_text(json.dumps(data))

    assert qmod.pending_count() == 1
