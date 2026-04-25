"""Prueba manual de la fase 2 del auditor (heurísticas + tier stub).

Sin API. Usa ``data/extracted.json`` (fichas reales de Haiku) +
``data/classified.json`` (mismas noticias clasificadas) +
``data/actor_domains.yml`` (whitelist V1) y corre las 3 heurísticas para
cada propuesta. Para cada una, imprime:

- bloque ``layers.heuristics`` (cross_source, verbatim_match, whitelist).
- bloque ``signals`` reconstruido por ``build_signals()``.
- salida de ``compute_tier(signals)`` (que en MVP es siempre value=None).

Uso:
    python scripts/test_audit_phase2.py             # con red, fetch real
    python scripts/test_audit_phase2.py --no-http   # salta verbatim_match

Plano: DISENO-AUDITOR-MVP.md §9 fase 2, criterios de éxito en §10.
"""
from __future__ import annotations

import argparse
import json
import logging
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from src.audit import build_signals, compute_tier  # noqa: E402
from src.audit_compare import compare_extractions  # noqa: E402
from src.audit_heuristics import (  # noqa: E402
    check_cross_source,
    check_verbatim_match,
    check_whitelist,
    load_actor_domains,
)

CLASSIFIED = ROOT / "data" / "classified.json"
EXTRACTED = ROOT / "data" / "extracted.json"
ACTOR_DOMAINS = ROOT / "data" / "actor_domains.yml"

EXPECTED_SIGNALS = (
    "ia_consenso",
    "arbitraje",
    "url_ok",
    "traza_dominio_actor",
    "fecha_coherente",
    "verbatim_match_ratio",
    "wayback_snapshot",
    "n_fuentes_independientes",
    "whitelist_match",
    "viability_con_cifra",
    "statement_type",
)


def _load(path: Path) -> list | dict:
    if not path.exists():
        sys.exit(f"Falta {path}.")
    return json.loads(path.read_text(encoding="utf-8"))


def _print_block(label: str, value) -> None:
    print(f"  [{label}]")
    print("    " + json.dumps(value, ensure_ascii=False, indent=2).replace("\n", "\n    "))


def main() -> int:
    logging.basicConfig(level=logging.INFO, format="[%(levelname)s %(name)s] %(message)s")
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--no-http", action="store_true",
        help="Salta verbatim_match (no descarga HTML).",
    )
    args = parser.parse_args()

    extracted = _load(EXTRACTED)
    classified = _load(CLASSIFIED)
    actor_domains = load_actor_domains(ACTOR_DOMAINS)

    print(f"Whitelist V1: {len(actor_domains.get('actors') or {})} actores, "
          f"{len(actor_domains.get('medios_cobertura_aceptada') or [])} medios.")
    print(f"Noticias clasificadas: {len(classified)} ítems.")
    print(f"Propuestas en extracted.json: "
          f"{sum(len(it.get('proposals', [])) for it in extracted)}.\n")

    total_props = 0
    total_signals_ok = 0
    total_tier_ok = 0
    cross_results: list[int] = []
    whitelist_results: list[str] = []
    verbatim_results: list[float | None] = []

    for record in extracted:
        nid = record.get("news_id")
        proposals = record.get("proposals") or []
        if not proposals:
            continue
        for i, p in enumerate(proposals):
            total_props += 1
            print(f"=== {nid} · propuesta #{i} — actor={p.get('actor')!r}, "
                  f"palanca={p.get('palanca')!r} ===")

            cross = check_cross_source(p, classified)
            whitelist = check_whitelist(p, actor_domains)
            if args.no_http:
                verbatim = {
                    "ratio": None,
                    "statement_type": p.get("statement_type") or "reported",
                    "threshold_blocking": 0.60,
                    "threshold_green": 0.80,
                    "passed_blocking": None,
                    "passed_green": None,
                    "html_cache_hit": False,
                    "url_ok": None,
                    "error": "skipped_no_http",
                }
            else:
                verbatim = check_verbatim_match(p)

            heuristics = {
                "cross_source": cross,
                "verbatim_match": verbatim,
                "whitelist": whitelist,
            }

            cross_results.append(cross.get("n_fuentes_independientes", 0))
            whitelist_results.append(whitelist.get("match", "?"))
            verbatim_results.append(verbatim.get("ratio"))

            _print_block("heuristics", heuristics)

            # Para signals, simulamos compare_result severity=none (la prueba
            # de Fase 1 ya cubrió el comparador real). El objetivo aquí es
            # verificar que las 11 señales se pueblan correctamente.
            compare_self = compare_extractions(p, p)
            signals = build_signals(p, compare_self, heuristics, verify_result=None)
            _print_block("signals", signals)

            missing = [k for k in EXPECTED_SIGNALS if k not in signals]
            if missing:
                print(f"  ⚠ faltan señales: {missing}")
            else:
                total_signals_ok += 1

            tier = compute_tier(signals)
            _print_block("tier", tier)
            if (tier.get("value") is None
                    and tier.get("reason") == "pendiente_estudio"
                    and tier.get("signals") == signals):
                total_tier_ok += 1
            else:
                print("  ⚠ compute_tier no devuelve el contrato esperado.")

            print()

    print("=" * 60)
    print(f"Propuestas analizadas: {total_props}")
    print(f"Con las 11 señales OK: {total_signals_ok}/{total_props}")
    print(f"compute_tier OK:       {total_tier_ok}/{total_props}")
    print(f"Cross-source distinct domains: {cross_results}")
    print(f"Whitelist matches:             {whitelist_results}")
    print(f"Verbatim ratios:               {verbatim_results}")
    print("Fin de la prueba de fase 2.")
    return 0 if total_signals_ok == total_props == total_tier_ok else 1


if __name__ == "__main__":
    sys.exit(main())
