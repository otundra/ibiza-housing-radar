# Estudio comparativo de 3 modelos de Anthropic

**Ejecución:** 2026-04-20T17:41:13.665727+00:00
**Dataset:** v1 — 20 noticias reales curadas.
**Modelos evaluados:** Haiku 4.5 (`claude-haiku-4-5`), Sonnet 4.6 (`claude-sonnet-4-6`), Opus 4.7 (`claude-opus-4-7`).
**Tareas:** clasificación (`classify`), detección de propuesta (`detect`), extracción estructurada (`extract`).

## Resumen — precisión por modelo y tarea

| Modelo | classify | detect | extract | ∑ score |
|---|---|---|---|---|
| **haiku** | 86.7% | 92.5% | 65.0% | 2.44 |
| **sonnet** | 86.7% | 92.5% | 70.0% | 2.49 |
| **opus** | 96.7% | 92.5% | 95.0% | 2.84 |

## Coste y latencia por ejecución completa

| Modelo | Coste total (€) | Tokens in | Tokens out | Cache read | Latencia acum. (s) |
|---|---|---|---|---|---|
| haiku | 0.0361 € | 12,340 | 5,340 | 0 | 33.71 |
| sonnet | 0.1087 € | 12,360 | 5,380 | 0 | 71.13 |
| opus | 0.4282 € | 15,520 | 3,080 | 0 | 36.92 |

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
| haiku | `{"news_id": "n01", "proposals": [{"actor": "Ayuntamiento de Ibiza", "actor_type": "institucional_publico", "statement...` | 0% |
| sonnet | `{"news_id": "n01", "proposals": [{"actor": "Cáritas Ibiza", "actor_type": "tercer_sector", "statement_summary": "Cári...` | 100% |
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

## Recomendación de reparto

- **classify** → `opus` (score 96.7%, coste/ejecución 0.1196 €). ≥95% de calidad y el más barato entre los que cumplen.
- **detect** → `haiku` (score 92.5%, coste/ejecución 0.0065 €). mejor puntuación y coste aceptable.
- **extract** → `opus` (score 95.0%, coste/ejecución 0.1957 €). ≥95% de calidad y el más barato entre los que cumplen.

**Coste mensual proyectado con el reparto recomendado (sin self-review ni auditorías):** ~1.29 €/mes en las 3 tareas principales. Ampliable con el resto de fases del pipeline (rescue, verify, generate) que no entran en este benchmark.
