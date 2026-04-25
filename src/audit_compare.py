"""Comparador determinista de extracciones capa 1 vs capa 2.

Compara dos fichas de propuesta (Haiku y Sonnet ciego) campo a campo y
clasifica los diferencias por severidad. Sin IA. Solo stdlib.

Árbol de severidad (DISENO-AUDITOR-MVP.md §2.2):
- Campos críticos (cualquier diff -> 'critical'):
    actor, target_actor, palanca, state, url_source.
- Coincidencia textual de statement_verbatim:
    ratio < 0.85          -> 'critical'
    0.85 <= ratio < 0.95  -> 'minor'
    ratio >= 0.95         -> sin diff
- Campos menores (diffs -> 'minor'):
    actor_type, viability_legal, viability_economic, horizon.

Ajuste sobre el plano: el plano original cita campos `viability_political`,
`viability_tecnica` y `statement_type` que no existen en la ficha real
emitida por src/extract.py (EXTRACT_SYSTEM). Este comparador usa los
campos reales de la ficha. statement_type entrará en fase 2 cuando se
añada a la ficha; aquí se ignora si está ausente.
"""
from __future__ import annotations

from difflib import SequenceMatcher
from typing import Any

CRITICAL_FIELDS = ("actor", "target_actor", "palanca", "state", "url_source")
MINOR_FIELDS = ("actor_type", "viability_legal", "viability_economic", "horizon")
VERBATIM_FIELD = "statement_verbatim"
VERBATIM_CRITICAL_THRESHOLD = 0.85
VERBATIM_MINOR_THRESHOLD = 0.95


def _norm(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip().lower()


def _verbatim_ratio(a: Any, b: Any) -> float:
    return SequenceMatcher(None, _norm(a), _norm(b)).ratio()


def compare_extractions(a: dict, b: dict) -> dict:
    """Compara dos fichas de propuesta y clasifica los diffs.

    Devuelve:
      {
        'identical': bool,
        'severity': 'critical' | 'minor' | 'none',
        'diffs': [{'field': str, 'a': any, 'b': any, 'reason': str}],
      }
    """
    diffs: list[dict] = []
    severity = "none"

    for field in CRITICAL_FIELDS:
        va, vb = a.get(field), b.get(field)
        if _norm(va) != _norm(vb):
            diffs.append({"field": field, "a": va, "b": vb, "reason": "diff_critico"})
            severity = "critical"

    ratio = _verbatim_ratio(a.get(VERBATIM_FIELD), b.get(VERBATIM_FIELD))
    if ratio < VERBATIM_CRITICAL_THRESHOLD:
        diffs.append({
            "field": VERBATIM_FIELD,
            "a": a.get(VERBATIM_FIELD),
            "b": b.get(VERBATIM_FIELD),
            "reason": f"ratio_{ratio:.2f}_lt_{VERBATIM_CRITICAL_THRESHOLD}",
        })
        severity = "critical"
    elif ratio < VERBATIM_MINOR_THRESHOLD:
        diffs.append({
            "field": VERBATIM_FIELD,
            "a": a.get(VERBATIM_FIELD),
            "b": b.get(VERBATIM_FIELD),
            "reason": f"ratio_{ratio:.2f}_lt_{VERBATIM_MINOR_THRESHOLD}",
        })
        if severity != "critical":
            severity = "minor"

    for field in MINOR_FIELDS:
        va, vb = a.get(field), b.get(field)
        if _norm(va) != _norm(vb):
            diffs.append({"field": field, "a": va, "b": vb, "reason": "diff_menor"})
            if severity == "none":
                severity = "minor"

    return {
        "identical": severity == "none",
        "severity": severity,
        "diffs": diffs,
    }
