"""Sistema de tiers de confianza — compute_tier() real.

Árbol determinista de 6 pasos. Diseño: ESTUDIO-TIERS.md §3.
Umbrales ajustables: data/tiers.yml (§4.2). Decisiones cerradas: D9.

Contrato público:
    compute_tier(signals: dict) -> dict con {value, reason, path, signals}

    value ∈ {"verde", "amarillo", "naranja", "rojo"}
    path  ∈ lista de strings que describe qué pasos se ejecutaron
    reason  string legible con la causa principal

Si el archivo tiers.yml no existe, se usan los defaults del módulo.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parent.parent
TIERS_YML = ROOT / "data" / "tiers.yml"

# Orden: menor = más restrictivo. Se usa para comparar techos.
_RANK: dict[str, int] = {"rojo": 0, "naranja": 1, "amarillo": 2, "verde": 3}

_DEFAULTS: dict[str, Any] = {
    "umbrales_verify": {
        "verbatim_quote_min": 0.95,
        "verbatim_reported_min": 0.60,
        "verbatim_reported_verde": 0.80,
    },
    "default_paso_6": "naranja",
}


def _load_config() -> dict[str, Any]:
    if TIERS_YML.exists():
        with TIERS_YML.open(encoding="utf-8") as fh:
            return yaml.safe_load(fh) or {}
    return _DEFAULTS.copy()


def compute_tier(signals: dict[str, Any]) -> dict[str, Any]:
    """Árbol determinista. Ver ESTUDIO-TIERS.md §3.

    Pasos en orden; el primero que aplica decide el tier.
    Paso 1: bloqueantes → rojo.
    Paso 2: techos (bajan el máximo alcanzable).
    Paso 3: camino a verde.
    Paso 5: camino a naranja (antes de paso 4 — sus condiciones excluyen paso 4).
    Paso 4: camino a amarillo.
    Paso 6: default → naranja con alerta.
    """
    cfg = _load_config()
    u = cfg.get("umbrales_verify", _DEFAULTS["umbrales_verify"])
    vq_min: float = float(u.get("verbatim_quote_min", 0.95))
    vr_min: float = float(u.get("verbatim_reported_min", 0.60))
    vr_verde: float = float(u.get("verbatim_reported_verde", 0.80))
    default_paso6: str = cfg.get("default_paso_6", "naranja")

    # Señales
    ia_consenso = signals.get("ia_consenso")
    arbitraje = signals.get("arbitraje", "no_hubo")
    url_ok = signals.get("url_ok")
    traza = signals.get("traza_dominio_actor")
    fecha_ok = signals.get("fecha_coherente")
    verbatim = signals.get("verbatim_match_ratio")
    wayback = signals.get("wayback_snapshot")
    n_fuentes: int = int(signals.get("n_fuentes_independientes") or 1)
    whitelist = signals.get("whitelist_match")
    viability_cifra = signals.get("viability_con_cifra")
    stmt_type = signals.get("statement_type", "reported")

    verbatim_min = vq_min if stmt_type == "quote" else vr_min
    verbatim_verde = vq_min if stmt_type == "quote" else vr_verde

    # -------------------------------------------------------------------
    # Paso 1 — Bloqueantes → rojo
    # -------------------------------------------------------------------
    blockers: list[str] = []

    if url_ok is False:
        blockers.append("url_ok=False")
    if traza is False and whitelist == "debilita":
        blockers.append("traza_dominio=False y whitelist=debilita")
    if verbatim is not None and verbatim < verbatim_min:
        blockers.append(
            f"verbatim_match_ratio={verbatim:.2f} < umbral_min={verbatim_min}"
        )
    if fecha_ok is False:
        blockers.append("fecha_coherente=False sin rescate declarado")
    if arbitraje == "opus_discrepa_ambas":
        blockers.append("arbitraje=opus_discrepa_ambas")

    if blockers:
        return {
            "value": "rojo",
            "reason": "; ".join(blockers),
            "path": ["paso_1_bloqueante"],
            "signals": dict(signals),
        }

    # -------------------------------------------------------------------
    # Paso 2 — Techos (el más restrictivo aplica)
    # -------------------------------------------------------------------
    max_tier = "verde"
    ceil_reasons: list[str] = []

    def _ceiling(tier: str, reason: str) -> None:
        nonlocal max_tier
        if _RANK[tier] < _RANK[max_tier]:
            max_tier = tier
        ceil_reasons.append(reason)

    if n_fuentes == 1:
        _ceiling("amarillo", "fuente única")
    if arbitraje in ("opus_confirma_haiku", "opus_confirma_sonnet"):
        _ceiling("amarillo", "arbitraje Opus resolvió disputa")
    if whitelist == "debilita":
        _ceiling("amarillo", "whitelist=debilita")
    if viability_cifra is not None and not viability_cifra:
        _ceiling("amarillo", "viability alta sin cifra declarada")
    # Wayback: sin snapshot en dominio no estable.
    # Proxy: whitelist != "refuerza" (no podemos verificar el dominio exacto
    # desde las señales; "refuerza" = dominio oficial del actor = estable).
    if wayback is False and whitelist != "refuerza":
        _ceiling("naranja", "sin wayback_snapshot en dominio no estable")

    # -------------------------------------------------------------------
    # Paso 3 — Camino a verde
    # -------------------------------------------------------------------
    if max_tier == "verde":
        verde_ok = (
            ia_consenso in ("completo", "parcial")
            and url_ok is True
            and traza is True
            and fecha_ok is True
            and verbatim is not None
            and verbatim >= verbatim_verde
            and wayback is True
            and n_fuentes >= 2
            and arbitraje == "no_hubo"
            and whitelist in ("refuerza", "neutro")
        )
        if verde_ok:
            return {
                "value": "verde",
                "reason": (
                    f"consenso IA + verify OK + "
                    f"n_fuentes={n_fuentes} + whitelist={whitelist}"
                ),
                "path": ["paso_1_ok", "paso_2_sin_techo", "paso_3_verde"],
                "signals": dict(signals),
            }

    # -------------------------------------------------------------------
    # Paso 5 — Condiciones de naranja (se evalúan antes del paso 4)
    #
    # Tres casos (ESTUDIO-TIERS.md §3.5):
    #   A. Techo del paso 2 que limita a naranja.
    #   B. Avisos no bloqueantes en verify (verbatim entre mín y verde).
    #   C. Arbitraje resuelto + fuente única simultáneamente.
    # -------------------------------------------------------------------
    naranja_warns: list[str] = []

    if max_tier == "naranja":
        naranja_warns.extend(ceil_reasons)

    if (
        verbatim is not None
        and verbatim_min <= verbatim < verbatim_verde
    ):
        naranja_warns.append(
            f"verbatim entre umbral mínimo y verde "
            f"({verbatim:.2f}, verde≥{verbatim_verde})"
        )

    if (
        arbitraje in ("opus_confirma_haiku", "opus_confirma_sonnet")
        and n_fuentes == 1
    ):
        entry = "arbitraje resuelto + fuente única"
        if entry not in naranja_warns:
            naranja_warns.append(entry)

    # Verificación básica (necesaria para publicar en naranja o amarillo)
    basic_ok = (
        url_ok is True
        and (traza is True or whitelist != "debilita")
        and (verbatim is None or verbatim >= verbatim_min)
    )

    if naranja_warns and basic_ok:
        return {
            "value": "naranja",
            "reason": "; ".join(naranja_warns),
            "path": ["paso_1_ok", "paso_5_naranja"],
            "signals": dict(signals),
        }

    # -------------------------------------------------------------------
    # Paso 4 — Camino a amarillo
    # Requiere al menos un techo del paso 2 que limite a amarillo.
    # -------------------------------------------------------------------
    if max_tier == "amarillo" and ceil_reasons and basic_ok:
        return {
            "value": "amarillo",
            "reason": "; ".join(ceil_reasons),
            "path": ["paso_1_ok", "paso_2_techo_amarillo", "paso_4_amarillo"],
            "signals": dict(signals),
        }

    # -------------------------------------------------------------------
    # Paso 6 — Default
    # Se dispara con combinaciones de señales no cubiertas por el árbol.
    # El caller debe emitir alerta Telegram para que se audite el caso.
    # -------------------------------------------------------------------
    return {
        "value": default_paso6,
        "reason": "default_path",
        "path": ["paso_1_ok", "paso_6_default"],
        "signals": dict(signals),
    }
