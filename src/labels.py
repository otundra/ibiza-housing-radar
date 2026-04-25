"""Etiquetas de presentación para códigos taxonómicos.

El pipeline guarda valores normalizados (snake_case) en el almacén interno
para mantener consistencia entre módulos. La cara pública debe mostrar la
versión legible: este módulo centraliza la traducción.

Si un código no aparece en el mapa, la función `label()` devuelve el valor
tal cual. Eso protege ante valores nuevos sin romper el render.
"""
from __future__ import annotations

from typing import Final

ACTOR_TYPE_LABELS: Final[dict[str, str]] = {
    "partido": "Partido",
    "sindicato": "Sindicato",
    "patronal": "Patronal",
    "tercer_sector": "Tercer sector",
    "academico": "Académico",
    "judicial": "Judicial",
    "institucional_publico": "Institucional público",
    "colectivo_ciudadano": "Colectivo ciudadano",
    "coalicion_intersectorial": "Coalición intersectorial",
    "coalicion_institucional": "Coalición institucional",
    "otro": "Otro",
    "desconocido": "Desconocido",
}

PALANCA_LABELS: Final[dict[str, str]] = {
    "normativa": "Normativa",
    "fiscal": "Fiscal",
    "oferta_vivienda": "Oferta de vivienda",
    "intermediacion": "Intermediación",
    "enforcement": "Aplicación de norma",
    "laboral": "Laboral",
    "judicial": "Vía judicial",
    "denuncia_social": "Denuncia social",
    "otro": "Otro",
    "desconocido": "Desconocido",
}

STATE_LABELS: Final[dict[str, str]] = {
    "propuesta": "Propuesta",
    "en_movimiento": "En movimiento",
    "en_debate": "En debate",
    "aprobada": "Aprobada",
    "en_ejecucion": "En ejecución",
    "implementada": "Implementada",
    "descartada": "Descartada",
    "pendiente_resolucion_judicial": "Pendiente de resolución judicial",
    "desconocido": "Desconocido",
}

HORIZON_LABELS: Final[dict[str, str]] = {
    "inmediato": "Inmediato",
    "corto_plazo": "Corto plazo",
    "temporada_2026": "Temporada 2026",
    "temporada_2027": "Temporada 2027",
    "estructural": "Estructural",
    "desconocido": "Desconocido",
}


def label(value: str, mapping: dict[str, str]) -> str:
    """Devuelve la etiqueta legible o el valor tal cual si no hay mapeo."""
    if not value:
        return ""
    return mapping.get(value, value)


def actor_type_label(code: str) -> str:
    return label(code, ACTOR_TYPE_LABELS)


def palanca_label(code: str) -> str:
    return label(code, PALANCA_LABELS)


def state_label(code: str) -> str:
    return label(code, STATE_LABELS)


def horizon_label(code: str) -> str:
    return label(code, HORIZON_LABELS)
