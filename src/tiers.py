"""Sistema de tiers de confianza — árbol de decisión determinista.

Lee el bloque ``signals`` del registro de auditoría y devuelve el tier
(verde / amarillo / naranja / rojo) según el árbol de ESTUDIO-TIERS.md §3.

Umbrales ajustables en ``data/tiers.yml``. Si el archivo no existe se usan
los valores por defecto definidos en ``_DEFAULTS``.

Invocación directa para verificar umbrales::

    python -m src.tiers

Plano: ESTUDIO-TIERS.md §3 + §4.
"""
from __future__ import annotations

import logging
from pathlib import Path
from typing import Any

log = logging.getLogger("tiers")

ROOT = Path(__file__).resolve().parent.parent
TIERS_YML = ROOT / "data" / "tiers.yml"

_DEFAULTS: dict[str, Any] = {
    "verbatim_quote_min": 0.95,
    "verbatim_reported_min": 0.60,
    "verbatim_reported_verde": 0.80,
    "dominios_estables": [
        "boib.caib.es",
        "caib.es",
        "conselldeivissa.es",
        "diariodeibiza.es",
        "periodicodeibiza.es",
        "ibestat.cat",
    ],
    "default_paso_6": "naranja",
}

_cfg: dict[str, Any] | None = None


def _load_cfg() -> dict[str, Any]:
    global _cfg
    if _cfg is not None:
        return _cfg
    try:
        import yaml  # pyyaml ya está en requirements.txt

        if TIERS_YML.exists():
            raw = yaml.safe_load(TIERS_YML.read_text(encoding="utf-8")) or {}
            merged: dict[str, Any] = dict(_DEFAULTS)
            merged.update(raw.get("umbrales_verify") or {})
            if "dominios_estables" in raw:
                merged["dominios_estables"] = raw["dominios_estables"]
            if "default_paso_6" in raw:
                merged["default_paso_6"] = raw["default_paso_6"]
            _cfg = merged
        else:
            _cfg = dict(_DEFAULTS)
    except Exception as exc:  # noqa: BLE001
        log.warning("No se pudo cargar tiers.yml (%s) — usando defaults.", exc)
        _cfg = dict(_DEFAULTS)
    return _cfg


# ---------------------------------------------------------------------------
# Helpers internos
# ---------------------------------------------------------------------------

_TECHO_ORDEN = {"verde": 0, "amarillo": 1, "naranja": 2, "rojo": 3}


def _max_techo(current: str, nuevo: str) -> str:
    """Devuelve el techo más restrictivo (naranja > amarillo > verde)."""
    return nuevo if _TECHO_ORDEN.get(nuevo, 0) > _TECHO_ORDEN.get(current, 0) else current


def _verbatim_bloqueante(ratio: float | None, stype: str, cfg: dict) -> bool:
    """True si el ratio verbatim cae por debajo del mínimo bloqueante."""
    if ratio is None:
        return False  # incertidumbre, no fallo confirmado
    if stype == "quote":
        return ratio < cfg["verbatim_quote_min"]
    return ratio < cfg["verbatim_reported_min"]


def _verbatim_habilita_verde(ratio: float | None, stype: str, cfg: dict) -> bool:
    """True si el ratio verbatim alcanza el nivel exigido para verde."""
    if ratio is None:
        return False
    if stype == "quote":
        return ratio >= cfg["verbatim_quote_min"]
    return ratio >= cfg["verbatim_reported_verde"]


def _razon_techo(s: dict) -> str:
    parts = []
    if (s.get("n_fuentes_independientes") or 1) == 1:
        parts.append("fuente única")
    arb = s.get("arbitraje") or "no_hubo"
    if arb in ("opus_confirma_haiku", "opus_confirma_sonnet"):
        parts.append("disputa resuelta por Opus")
    if s.get("whitelist_match") == "debilita":
        parts.append("dominio no verificado")
    if s.get("wayback_snapshot") is False:
        parts.append("sin copia en Wayback")
    return "; ".join(parts) if parts else "techo activo"


def _tier(value: str, reason: str, signals: dict) -> dict[str, Any]:
    return {"value": value, "reason": reason, "signals": dict(signals)}


# ---------------------------------------------------------------------------
# Árbol de decisión principal
# ---------------------------------------------------------------------------

def compute_tier(signals: dict[str, Any]) -> dict[str, Any]:
    """Árbol de decisión determinista sobre el bloque ``signals``.

    Devuelve ``{value, reason, signals}`` donde ``value`` es uno de:
    ``verde`` | ``amarillo`` | ``naranja`` | ``rojo``.

    Plano: ESTUDIO-TIERS.md §3.
    """
    cfg = _load_cfg()
    s = signals or {}

    stype: str = s.get("statement_type") or "reported"
    verbatim: float | None = s.get("verbatim_match_ratio")
    url_ok: bool | None = s.get("url_ok")
    traza: bool | None = s.get("traza_dominio_actor")
    whitelist: str | None = s.get("whitelist_match")
    fecha_coherente: bool | None = s.get("fecha_coherente")
    arbitraje: str = s.get("arbitraje") or "no_hubo"
    n_fuentes: int = s.get("n_fuentes_independientes") or 1
    wayback: bool | None = s.get("wayback_snapshot")
    ia_consenso: str = s.get("ia_consenso") or "desconocido"

    # ---- Paso 1: Bloqueantes → rojo -----------------------------------------
    if url_ok is False:
        return _tier("rojo", "url_ok=False: fuente inaccesible", s)

    if traza is False and whitelist == "debilita":
        return _tier("rojo", "traza_dominio_actor=False + whitelist=debilita", s)

    if _verbatim_bloqueante(verbatim, stype, cfg):
        return _tier(
            "rojo",
            f"verbatim_match_ratio={verbatim:.2f} por debajo del mínimo ({stype})",
            s,
        )

    if fecha_coherente is False:
        return _tier("rojo", "fecha_coherente=False y no es rescate declarado", s)

    if arbitraje == "opus_discrepa_ambas":
        return _tier("rojo", "arbitraje=opus_discrepa_ambas: tres capas sin acuerdo", s)

    # ---- Paso 2: Techos (aplica el más restrictivo) --------------------------
    techo = "verde"

    if n_fuentes == 1:
        techo = _max_techo(techo, "amarillo")

    if arbitraje in ("opus_confirma_haiku", "opus_confirma_sonnet"):
        techo = _max_techo(techo, "amarillo")

    if whitelist == "debilita":
        techo = _max_techo(techo, "amarillo")

    if wayback is False:
        techo = _max_techo(techo, "naranja")

    # Techo viability_con_cifra desactivado en V1: la señal en build_signals
    # busca dígitos en el campo enum (viability_economic="alta/media") en vez de
    # en statement_verbatim. Resultado: señal casi siempre False, lo que haría el
    # techo demasiado agresivo. Pendiente arreglar build_signals. Ver ESTUDIO-TIERS.md §2.6.

    # ---- Verificación básica (necesaria para pasos 4-5) ----------------------
    verify_basica_ok = (
        url_ok is not False
        and traza is not False
        and not _verbatim_bloqueante(verbatim, stype, cfg)
    )

    # ---- Paso 3: Camino a verde (sin techo, todas las señales positivas) ------
    # fecha_coherente=None se trata como "sin evidencia de problema" (en el MVP
    # los artículos vienen del RSS de la semana, así que la coherencia temporal
    # es implícita). wayback=None sí impide verde porque no podemos garantizar
    # la fuente archivada; en ese caso cae a amarillo (paso 3b).
    verde_base = (
        techo == "verde"
        and verify_basica_ok
        and ia_consenso in ("completo", "parcial")
        and arbitraje == "no_hubo"
        and url_ok is True
        and traza is True
        and fecha_coherente is not False  # None = no verificado pero sin problema
        and n_fuentes >= 2
        and whitelist in ("refuerza", "neutro")
        and _verbatim_habilita_verde(verbatim, stype, cfg)
    )
    if verde_base and wayback is True:
        reason = (
            f"consenso IA {ia_consenso} + verify OK + {n_fuentes} fuentes"
            f" + whitelist {whitelist}"
        )
        return _tier("verde", reason, s)

    # Paso 3b: señales perfectas pero wayback sin verificar (MVP normal) → amarillo
    if verde_base and wayback is None:
        reason = (
            f"consenso IA {ia_consenso} + {n_fuentes} fuentes + whitelist {whitelist}"
            " (archivo Wayback sin verificar — MVP)"
        )
        return _tier("amarillo", reason, s)

    # ---- Paso 4: Camino a amarillo -------------------------------------------
    if techo == "amarillo" and verify_basica_ok:
        return _tier("amarillo", _razon_techo(s), s)

    # ---- Paso 5: Camino a naranja --------------------------------------------
    if techo == "naranja" and verify_basica_ok:
        return _tier("naranja", _razon_techo(s), s)

    # naranja por combinaciones de avisos no bloqueantes
    if wayback is False and whitelist == "debilita" and url_ok is not False:
        return _tier("naranja", "wayback ausente + dominio no verificado", s)

    if arbitraje in ("opus_confirma_haiku", "opus_confirma_sonnet") and n_fuentes == 1:
        return _tier("naranja", "disputa resuelta por Opus + fuente única", s)

    # Propuesta que sobrevive los bloqueantes pero no cumple ningún camino positivo
    # (ej. n_fuentes=1 con techo amarillo pero verify_basica con señales None):
    if verify_basica_ok:
        return _tier("amarillo", _razon_techo(s) or "señales incompletas sin problemas confirmados", s)

    # ---- Paso 6: Default → naranja (configurable) ----------------------------
    default_val: str = cfg.get("default_paso_6", "naranja")
    log.warning("compute_tier default_path signals=%s", {k: v for k, v in s.items() if v is not None})
    return _tier(default_val, "default_path: combinación de señales no cubierta", s)


# ---------------------------------------------------------------------------
# Entry point de verificación
# ---------------------------------------------------------------------------

def main() -> None:
    import json
    cfg = _load_cfg()
    print("Umbrales activos:")
    print(json.dumps({k: v for k, v in cfg.items() if k != "dominios_estables"}, indent=2))
    print(f"Dominios estables ({len(cfg['dominios_estables'])}): {', '.join(cfg['dominios_estables'])}")
    print(f"tiers.yml: {'cargado' if TIERS_YML.exists() else 'no encontrado (usando defaults)'}")


if __name__ == "__main__":
    main()
