# Estudio comparativo de 3 modelos de Anthropic

**Ejecución:** 2026-04-20T17:48:05.634695+00:00
**Dataset:** v1 — 20 noticias reales curadas.
**Modelos evaluados:** Haiku 4.5 (`claude-haiku-4-5`), Sonnet 4.6 (`claude-sonnet-4-6`), Opus 4.7 (`claude-opus-4-7`).
**Tareas:** clasificación (`classify`), detección de propuesta (`detect`), extracción estructurada (`extract`).

**Items evaluados:** 17 de 20 (los ausentes son discrepancias Opus↔Sonnet excluidas automáticamente).

## Resumen — precisión por modelo y tarea

| Modelo | classify | detect | extract | ∑ score |
|---|---|---|---|---|
| **haiku** | 94.1% | 94.1% | 97.1% | 2.85 |
| **sonnet** | 94.1% | 94.1% | 97.1% | 2.85 |
| **opus** | 94.1% | 94.1% | 70.6% | 2.59 |

## Coste y latencia por ejecución completa

| Modelo | Coste total (€) | Tokens in | Tokens out | Cache read | Latencia acum. (s) |
|---|---|---|---|---|---|
| haiku | 0.0358 € | 12,340 | 5,280 | 0 | 32.61 |
| sonnet | 0.1091 € | 12,360 | 5,420 | 0 | 67.87 |
| opus | 0.4479 € | 15,520 | 3,360 | 0 | 37.20 |

## Errores detectados

*Ninguno.*

## Detalle por noticia (primeros 5 items)

### n01

**Tarea: classify**

| Modelo | Output | Score |
|---|---|---|
| haiku | `{"id": "n01", "is_housing": true, "actor": "ayuntamiento", "lever": "enforcement"}` | 100% |
| sonnet | `{"is_housing": true, "actor": "ayuntamiento", "lever": "enforcement"}` | 100% |
| opus | `{"id": "n01", "is_housing": true, "actor": "ayuntamiento", "lever": "enforcement"}` | 100% |

**Tarea: detect**

| Modelo | Output | Score |
|---|---|---|
| haiku | `{"proposal_type": "ninguna", "proposal_actor_hint": null}` | 0% |
| sonnet | `{"proposal_type": "ninguna", "proposal_actor_hint": null}` | 0% |
| opus | `{"proposal_type": "ninguna", "proposal_actor_hint": null}` | 0% |

**Tarea: extract**

| Modelo | Output | Score |
|---|---|---|
| haiku | `{"news_id": "n01", "proposals": [{"actor": "Ayuntamiento de Ibiza", "actor_type": "institucional_publico", "statement...` | 50% |
| sonnet | `{"news_id": "n01", "proposals": [{"actor": "Cáritas Ibiza", "actor_type": "tercer_sector", "statement_summary": "Cári...` | 50% |
| opus | `{"news_id": "n01", "proposals": []}` | 0% |

### n02

**Tarea: classify**

| Modelo | Output | Score |
|---|---|---|
| haiku | `{"id": "n02", "is_housing": true, "actor": "trabajadores", "lever": "precio"}` | 67% |
| sonnet | `{"is_housing": true, "actor": "trabajadores", "lever": "precio"}` | 67% |
| opus | `{"id": "n02", "is_housing": true, "actor": "trabajadores", "lever": "denuncia_social"}` | 100% |

**Tarea: detect**

| Modelo | Output | Score |
|---|---|---|
| haiku | `{"proposal_type": "ninguna", "proposal_actor_hint": null}` | 100% |
| sonnet | `{"proposal_type": "ninguna", "proposal_actor_hint": null}` | 100% |
| opus | `{"proposal_type": "ninguna", "proposal_actor_hint": null}` | 100% |

**Tarea: extract**

| Modelo | Output | Score |
|---|---|---|
| haiku | `{"news_id": "n02", "proposals": []}` | 100% |
| sonnet | `{"news_id": "n02", "proposals": []}` | 100% |
| opus | `{"news_id": "n02", "proposals": []}` | 100% |

### n03

**Tarea: classify**

| Modelo | Output | Score |
|---|---|---|
| haiku | `{"id": "n03", "is_housing": true, "actor": "ayuntamiento", "lever": "enforcement"}` | 100% |
| sonnet | `{"is_housing": true, "actor": "ayuntamiento", "lever": "enforcement"}` | 100% |
| opus | `{"id": "n03", "is_housing": true, "actor": "ayuntamiento", "lever": "enforcement"}` | 100% |

**Tarea: detect**

| Modelo | Output | Score |
|---|---|---|
| haiku | `{"proposal_type": "ninguna", "proposal_actor_hint": null}` | 100% |
| sonnet | `{"proposal_type": "ninguna", "proposal_actor_hint": null}` | 100% |
| opus | `{"proposal_type": "ninguna", "proposal_actor_hint": null}` | 100% |

**Tarea: extract**

| Modelo | Output | Score |
|---|---|---|
| haiku | `{"news_id": "n03", "proposals": []}` | 100% |
| sonnet | `{"news_id": "n03", "proposals": []}` | 100% |
| opus | `{"news_id": "n03", "proposals": []}` | 100% |

### n04

**Tarea: classify**

| Modelo | Output | Score |
|---|---|---|
| haiku | `{"id": "n04", "is_housing": true, "actor": "tercer_sector", "lever": "denuncia_social"}` | 100% |
| sonnet | `{"is_housing": true, "actor": "tercer_sector", "lever": "denuncia_social"}` | 100% |
| opus | `{"id": "n04", "is_housing": true, "actor": "tercer_sector", "lever": "denuncia_social"}` | 100% |

**Tarea: detect**

| Modelo | Output | Score |
|---|---|---|
| haiku | `{"proposal_type": "formal", "proposal_actor_hint": "Cáritas Ibiza"}` | 100% |
| sonnet | `{"proposal_type": "formal", "proposal_actor_hint": "Cáritas Ibiza"}` | 100% |
| opus | `{"proposal_type": "formal", "proposal_actor_hint": "Cáritas Ibiza"}` | 100% |

**Tarea: extract**

| Modelo | Output | Score |
|---|---|---|
| haiku | `{"news_id": "n04", "proposals": [{"actor": "Cáritas Ibiza", "actor_type": "tercer_sector", "statement_summary": "Pide...` | 100% |
| sonnet | `{"news_id": "n04", "proposals": [{"actor": "Cáritas Ibiza", "actor_type": "tercer_sector", "statement_summary": "Cári...` | 100% |
| opus | `{"news_id": "n04", "proposals": [{"actor": "Cáritas Ibiza", "actor_type": "tercer_sector", "statement_summary": "Cári...` | 100% |

### n05

**Tarea: classify**

| Modelo | Output | Score |
|---|---|---|
| haiku | `{"id": "n05", "is_housing": true, "actor": "otro", "lever": "precio"}` | 100% |
| sonnet | `{"is_housing": true, "actor": "otro", "lever": "precio"}` | 100% |
| opus | `{"id": "n05", "is_housing": true, "actor": "propietarios", "lever": "precio"}` | 67% |

**Tarea: detect**

| Modelo | Output | Score |
|---|---|---|
| haiku | `{"proposal_type": "ninguna", "proposal_actor_hint": null}` | 100% |
| sonnet | `{"proposal_type": "ninguna", "proposal_actor_hint": null}` | 100% |
| opus | `{"proposal_type": "ninguna", "proposal_actor_hint": null}` | 100% |

**Tarea: extract**

| Modelo | Output | Score |
|---|---|---|
| haiku | `{"news_id": "n05", "proposals": []}` | 100% |
| sonnet | `{"news_id": "n05", "proposals": []}` | 100% |
| opus | `{"news_id": "n05", "proposals": []}` | 100% |

## Recomendación de reparto

- **classify** → `haiku` (score 94.1%, coste/ejecución 0.0065 €). mejor puntuación y coste aceptable.
- **detect** → `haiku` (score 94.1%, coste/ejecución 0.0055 €). mejor puntuación y coste aceptable.
- **extract** → `haiku` (score 97.1%, coste/ejecución 0.0184 €). ≥95% de calidad y el más barato entre los que cumplen.

**Coste mensual proyectado con el reparto recomendado (sin self-review ni auditorías):** ~0.12 €/mes en las 3 tareas principales. Ampliable con el resto de fases del pipeline (rescue, verify, generate) que no entran en este benchmark.
