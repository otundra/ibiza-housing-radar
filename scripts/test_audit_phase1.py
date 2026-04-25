"""Prueba manual de la fase 1 del auditor (capa 2 ciega + comparador).

Uso:
    python scripts/test_audit_phase1.py            # 3 items, gasta API
    python scripts/test_audit_phase1.py --limit 1  # 1 item, gasta menos
    python scripts/test_audit_phase1.py --dry-run  # sin API, sanity check del comparador

Requiere ANTHROPIC_API_KEY salvo en --dry-run.
Lee data/classified.json como input. Imprime por pantalla las extracciones
de capa 1 (Haiku) y capa 2 (Sonnet ciego), y para cada propuesta el
resultado del comparador campo a campo.

Plano: DISENO-AUDITOR-MVP.md §9 fase 1, criterios de éxito en §10.
"""
from __future__ import annotations

import argparse
import json
import logging
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from src.audit import run_blind_audit  # noqa: E402
from src.audit_compare import compare_extractions  # noqa: E402
from src.extract import extract_with_haiku  # noqa: E402

CLASSIFIED = ROOT / "data" / "classified.json"
EXTRACTED = ROOT / "data" / "extracted.json"


def _load_candidates(limit: int) -> list[dict]:
    if not CLASSIFIED.exists():
        sys.exit(f"Falta {CLASSIFIED}. Ejecuta `python -m src.classify` antes.")
    classified = json.loads(CLASSIFIED.read_text())
    candidates = [
        c for c in classified
        if c.get("is_housing") and c.get("proposal_type") in ("formal", "en_movimiento")
    ]
    for i, c in enumerate(candidates):
        c.setdefault("id", f"item-{i:03d}")
    return candidates[:limit]


def _print_proposal(label: str, prop: dict) -> None:
    print(f"  [{label}]")
    for key in ("actor", "actor_type", "palanca", "target_actor", "state",
                "horizon", "viability_legal", "viability_economic"):
        print(f"    {key}: {prop.get(key)!r}")
    verbatim = prop.get("statement_verbatim", "") or ""
    print(f"    statement_verbatim: {verbatim[:140]!r}")


def _print_compare(result: dict) -> None:
    print(f"  comparador → severity={result['severity']}, identical={result['identical']}")
    if result["diffs"]:
        print("    diffs:")
        for d in result["diffs"]:
            print(f"      - {d['field']} ({d['reason']})")
            print(f"          haiku : {d['a']!r}")
            print(f"          sonnet: {d['b']!r}")


def _dry_run() -> None:
    print("DRY RUN — sanity check del comparador con fixture local")
    if not EXTRACTED.exists():
        sys.exit(f"Falta {EXTRACTED}. Ejecuta `python -m src.extract` antes o usa modo real.")
    extracted = json.loads(EXTRACTED.read_text())
    sample = next(
        (r for r in extracted if r.get("proposals")), None,
    )
    if not sample:
        sys.exit("No hay propuestas en data/extracted.json para comparar.")

    prop = sample["proposals"][0]

    print("\n[caso 1] Comparar una ficha contra sí misma (esperado: severity=none).")
    res = compare_extractions(prop, prop)
    _print_compare(res)
    assert res["severity"] == "none" and res["identical"], "Comparar consigo mismo debería dar identical"

    print("\n[caso 2] Cambiar el actor (esperado: severity=critical).")
    mutated = {**prop, "actor": "Otro Actor S.L."}
    res = compare_extractions(prop, mutated)
    _print_compare(res)
    assert res["severity"] == "critical"

    print("\n[caso 3] Cambiar viability_economic (esperado: severity=minor).")
    mutated = {**prop, "viability_economic": "baja"} if prop.get("viability_economic") != "baja" else {**prop, "viability_economic": "alta"}
    res = compare_extractions(prop, mutated)
    _print_compare(res)
    assert res["severity"] == "minor", f"Esperado minor, recibido {res['severity']}"

    print("\n[caso 4] Recortar el verbatim al 50% (esperado: severity=critical por ratio bajo).")
    verbatim = prop.get("statement_verbatim", "") or ""
    if len(verbatim) > 30:
        mutated = {**prop, "statement_verbatim": verbatim[: len(verbatim) // 2]}
        res = compare_extractions(prop, mutated)
        _print_compare(res)
        assert res["severity"] == "critical", f"Esperado critical, recibido {res['severity']}"
    else:
        print("  (verbatim demasiado corto para esta prueba; saltado)")

    print("\nDRY RUN OK — el comparador clasifica las severidades como esperado.")


def main() -> int:
    logging.basicConfig(level=logging.INFO, format="[%(levelname)s %(name)s] %(message)s")

    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--limit", type=int, default=3, help="Número de items a auditar (default 3).")
    parser.add_argument("--dry-run", action="store_true", help="Sin API: comprobar comparador con fixture local.")
    args = parser.parse_args()

    if args.dry_run:
        _dry_run()
        return 0

    if "ANTHROPIC_API_KEY" not in os.environ:
        sys.exit("Falta ANTHROPIC_API_KEY. Exporta la variable o usa --dry-run.")

    items = _load_candidates(args.limit)
    if not items:
        sys.exit("Sin candidatos en classified.json (proposal_type formal/en_movimiento).")

    import anthropic

    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    edition = os.environ.get("EDITION", "audit-phase1-test")

    print(f"\nItems candidatos: {len(items)}")
    for it in items:
        print(f"  - {it['id']}: {it['title'][:90]}")

    print("\n=== Capa 1 (Haiku) ===")
    haiku = extract_with_haiku(client, items, edition=edition)
    for nid, props in haiku.items():
        print(f"\n{nid} → {len(props)} propuesta(s)")
        for p in props:
            _print_proposal("haiku", p)

    print("\n=== Capa 2 ciega (Sonnet) ===")
    sonnet = run_blind_audit(client, items, edition=edition)
    for nid, props in sonnet.items():
        print(f"\n{nid} → {len(props)} propuesta(s)")
        for p in props:
            _print_proposal("sonnet", p)

    print("\n=== Comparación campo a campo ===")
    for nid in sorted(set(haiku) | set(sonnet)):
        h = haiku.get(nid, [])
        s = sonnet.get(nid, [])
        print(f"\n{nid}: haiku={len(h)} prop, sonnet={len(s)} prop")
        if not h and not s:
            print("  ambas vacías; sin comparar.")
            continue
        if len(h) != len(s):
            print(f"  ⚠ número de propuestas distinto ({len(h)} vs {len(s)}); comparo por orden hasta el mínimo.")
        for i in range(min(len(h), len(s))):
            print(f"\n  propuesta #{i}:")
            _print_proposal("haiku", h[i])
            _print_proposal("sonnet", s[i])
            res = compare_extractions(h[i], s[i])
            _print_compare(res)

    print("\nFin de la prueba. Revisa el dashboard de costes con `python -m src.costs` si quieres ver el gasto.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
