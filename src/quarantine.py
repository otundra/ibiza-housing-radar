"""Cuarentena pública de propuestas con tier rojo.

Cada vez que el auditor asigna ``tier=rojo`` a una propuesta, esta entra en
``data/quarantine.json``. A los 60 días sin corroboración se archiva como
``"no_verificada"`` (no desaparece: queda en el archivo con su huella).

La página pública ``/revision-pendiente/`` se construirá sobre este archivo
en el Bloque B (Jekyll). Por ahora el pipeline la escribe y la alerta del
lunes la muestra como contador.

Invocación directa para inspeccionar el estado actual::

    python -m src.quarantine

Plano: REVISION-FASE-0.5.md PI11.
"""
from __future__ import annotations

import json
import logging
from datetime import datetime, timedelta, timezone
from pathlib import Path

log = logging.getLogger("quarantine")

ROOT = Path(__file__).resolve().parent.parent
QUARANTINE_FILE = ROOT / "data" / "quarantine.json"
AUDIT_DIR = ROOT / "data" / "audit"

ARCHIVE_DAYS = 60


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _load() -> list[dict]:
    if QUARANTINE_FILE.exists():
        try:
            data = json.loads(QUARANTINE_FILE.read_text(encoding="utf-8"))
            if isinstance(data, list):
                return data
            # schema v1: objeto con campo "proposals"
            return data.get("proposals", [])
        except Exception as exc:  # noqa: BLE001
            log.warning("quarantine.json ilegible (%s) — arrancando vacío.", exc)
    return []


def _save(proposals: list[dict]) -> None:
    QUARANTINE_FILE.parent.mkdir(parents=True, exist_ok=True)
    QUARANTINE_FILE.write_text(
        json.dumps(
            {"updated_at": _now_iso(), "proposals": proposals},
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )


def _days_in_quarantine(entry: dict) -> float:
    try:
        entered = datetime.fromisoformat(
            entry["entered_at"].replace("Z", "+00:00")
        )
        return (datetime.now(timezone.utc) - entered).total_seconds() / 86400
    except Exception:  # noqa: BLE001
        return 0.0


# ---------------------------------------------------------------------------
# API pública
# ---------------------------------------------------------------------------

def load_quarantine() -> list[dict]:
    """Devuelve la lista completa (pending + archived)."""
    return _load()


def pending_count() -> int:
    """Número de propuestas pendientes de revisión (no archivadas)."""
    return sum(1 for p in _load() if p.get("status") == "pending")


def update_quarantine(audit_records: list[dict], edition: str) -> dict:
    """Procesa los registros del auditor y actualiza quarantine.json.

    - Añade las propuestas con ``tier=rojo`` que no estaban ya.
    - Archiva las entradas ``pending`` con más de 60 días sin movimiento.

    Devuelve ``{added, archived}`` para el resumen del pipeline.
    """
    proposals = _load()
    existing_ids = {p["proposal_id"] for p in proposals}

    added = 0
    for rec in audit_records:
        tier = rec.get("tier") or {}
        if tier.get("value") != "rojo":
            continue
        pid = rec.get("proposal_id")
        if pid in existing_ids:
            continue

        haiku_prop = (rec.get("layers") or {}).get("haiku", {}).get("proposal") or {}
        proposals.append({
            "proposal_id": pid,
            "edition": edition,
            "entered_at": rec.get("created_at") or _now_iso(),
            "tier_reason": tier.get("reason", ""),
            "actor": haiku_prop.get("actor", ""),
            "actor_type": haiku_prop.get("actor_type", ""),
            "statement_summary": haiku_prop.get("statement_summary", ""),
            "url_source": haiku_prop.get("url_source", ""),
            "status": "pending",
            "archived_at": None,
        })
        existing_ids.add(pid)
        added += 1

    archived = _archive_stale(proposals)
    _save(proposals)

    log.info(
        "quarantine: +%d entrada%s, %d archivada%s (total pending: %d)",
        added, "s" if added != 1 else "",
        archived, "s" if archived != 1 else "",
        sum(1 for p in proposals if p.get("status") == "pending"),
    )
    return {"added": added, "archived": archived}


def _archive_stale(proposals: list[dict]) -> int:
    """Archiva entradas pending con ≥ ARCHIVE_DAYS días. Modifica in-place."""
    archived = 0
    for entry in proposals:
        if entry.get("status") != "pending":
            continue
        if _days_in_quarantine(entry) >= ARCHIVE_DAYS:
            entry["status"] = "no_verificada"
            entry["archived_at"] = _now_iso()
            archived += 1
    return archived


def read_audit_records(edition: str) -> list[dict]:
    """Lee todos los registros JSON del auditor para la edición dada."""
    edition_dir = AUDIT_DIR / edition
    if not edition_dir.exists():
        return []
    records = []
    for f in sorted(edition_dir.glob("*.json")):
        try:
            records.append(json.loads(f.read_text(encoding="utf-8")))
        except Exception as exc:  # noqa: BLE001
            log.warning("No se pudo leer %s: %s", f.name, exc)
    return records


# ---------------------------------------------------------------------------
# Entry point de inspección
# ---------------------------------------------------------------------------

def main() -> None:
    logging.basicConfig(level=logging.INFO, format="[%(levelname)s %(name)s] %(message)s")
    proposals = load_quarantine()
    pending = [p for p in proposals if p.get("status") == "pending"]
    archived = [p for p in proposals if p.get("status") != "pending"]
    print(f"quarantine.json: {len(proposals)} entradas total")
    print(f"  pending:     {len(pending)}")
    print(f"  archivadas:  {len(archived)}")
    if pending:
        print("\nPendientes:")
        for p in pending:
            days = _days_in_quarantine(p)
            print(f"  {p['proposal_id']}  ({days:.0f}d)  {p['tier_reason'][:60]}")


if __name__ == "__main__":
    main()
