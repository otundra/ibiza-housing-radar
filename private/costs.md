# Control de costes — privado

*Archivo privado. No se publica en la web. Última actualización: 2026-07-20 08:10 UTC*

Tipo de cambio interno: **1 USD = 0.92 EUR** (revisar cada 3 meses).

## Mes en curso

- **Gastado 2026-07:** `3.10 €` (`$3.3699` USD)
- **Tope blando:** `12.00 €` → solo avisa por Telegram, sigue publicando
- **Tope duro:** `50.00 €` → corta el pipeline (protección runaway)
- **Consumo vs blando:** `25.8%`
- **Consumo vs duro:** `6.2%`

```
[█░░░░░░░░░░░░░░░░░░░] 6.2% del tope duro
```

**Capa actual:** 🟢 Verde (<6 €) — silencio

## Histórico mensual

| Mes | Gasto (€) | Gasto (USD) |
|---|---|---|
| 2026-07 | 3.10 € | $3.3699 |
| 2026-06 | 5.26 € | $5.7179 |
| 2026-05 | 3.30 € | $3.5859 |
| 2026-04 | 6.86 € | $7.4611 |
| **TOTAL** | **18.52 €** | **$20.1349** |

## Gasto por fase

| Fase | Gasto (€) | % |
|---|---|---|
| generate | 13.94 € | 75.3% |
| self_review | 1.04 € | 5.6% |
| bench_extract | 0.59 € | 3.2% |
| extract_fallback | 0.51 € | 2.8% |
| gold_extract_opus | 0.46 € | 2.5% |
| classify | 0.42 € | 2.3% |
| audit_blind | 0.35 € | 1.9% |
| bench_classify | 0.30 € | 1.6% |
| bench_detect | 0.28 € | 1.5% |
| extract_validate | 0.16 € | 0.9% |
| extract_base | 0.13 € | 0.7% |
| gold_classify_opus | 0.12 € | 0.7% |
| gold_detect_opus | 0.12 € | 0.6% |
| gold_validate_task_3_extract | 0.04 € | 0.2% |
| gold_validate_task_1_classify | 0.03 € | 0.2% |
| gold_validate_task_2_proposal_detect | 0.03 € | 0.2% |

## Consumo por modelo

| Modelo | Input tokens | Output tokens | Gasto (€) |
|---|---|---|---|
| `claude-opus-4-7` | 356,263 | 141,259 | 16.03 € |
| `claude-sonnet-4-6` | 390,365 | 51,974 | 1.87 € |
| `claude-haiku-4-5-20251001` | 157,923 | 104,953 | 0.63 € |

## Últimas 20 llamadas

| Fecha | Edición | Fase | Modelo | In | Out | € |
|---|---|---|---|---|---|---|
| 2026-07-20 08:10 | 2026-W30 | self_review | `claude-sonnet-4-6` | 23,231 | 1,373 | 0.0872 € |
| 2026-07-20 08:09 | 2026-W30 | generate | `claude-opus-4-7` | 19,484 | 7,651 | 0.8973 € |
| 2026-07-20 08:07 | 2026-w30 | audit_blind | `claude-sonnet-4-6` | 1,383 | 2,445 | 0.0413 € |
| 2026-07-20 08:07 | 2026-W30 | extract_fallback | `claude-opus-4-7` | 1,750 | 459 | 0.0558 € |
| 2026-07-20 08:07 | 2026-W30 | extract_validate | `claude-sonnet-4-6` | 870 | 60 | 0.0032 € |
| 2026-07-20 08:07 | 2026-W30 | extract_validate | `claude-sonnet-4-6` | 814 | 18 | 0.0025 € |
| 2026-07-20 08:07 | 2026-W30 | extract_validate | `claude-sonnet-4-6` | 923 | 18 | 0.0028 € |
| 2026-07-20 08:07 | 2026-W30 | extract_fallback | `claude-opus-4-7` | 1,684 | 362 | 0.0482 € |
| 2026-07-20 08:07 | 2026-W30 | extract_validate | `claude-sonnet-4-6` | 786 | 92 | 0.0034 € |
| 2026-07-20 08:07 | 2026-W30 | extract_validate | `claude-sonnet-4-6` | 846 | 18 | 0.0026 € |
| 2026-07-20 08:07 | 2026-W30 | extract_validate | `claude-sonnet-4-6` | 729 | 18 | 0.0023 € |
| 2026-07-20 08:07 | 2026-W30 | extract_validate | `claude-sonnet-4-6` | 925 | 18 | 0.0028 € |
| 2026-07-20 08:07 | 2026-W30 | extract_base | `claude-haiku-4-5-20251001` | 2,599 | 2,365 | 0.0133 € |
| 2026-07-20 08:06 | 2026-W30 | classify | `claude-haiku-4-5-20251001` | 6,465 | 4,939 | 0.0287 € |
| 2026-07-13 08:21 | 2026-W29 | self_review | `claude-sonnet-4-6` | 23,620 | 1,196 | 0.0858 € |
| 2026-07-13 08:20 | 2026-W29 | generate | `claude-opus-4-7` | 15,957 | 7,412 | 0.8321 € |
| 2026-07-13 08:18 | 2026-w29 | audit_blind | `claude-sonnet-4-6` | 657 | 1,178 | 0.0218 € |
| 2026-07-13 08:18 | 2026-W29 | extract_validate | `claude-sonnet-4-6` | 993 | 13 | 0.0029 € |
| 2026-07-13 08:18 | 2026-W29 | extract_fallback | `claude-opus-4-7` | 1,707 | 425 | 0.0529 € |
| 2026-07-13 08:18 | 2026-W29 | extract_validate | `claude-sonnet-4-6` | 820 | 73 | 0.0033 € |

## Política de costes

- **Tope blando (12.00 €):** Telegram avisa, pero el pipeline **sigue publicando la editorial**. No se pierde informe por sobrecoste.
- **Tope duro (50.00 €):** Telegram crítico + **corte inmediato**. Protección real contra bugs o bucles runaway.

Coste esperado (pivote documental + autoevaluación 3 niveles): ~9,86 €/mes. Tras afinar reparto de modelos y con corpus estable, objetivo bajar a ~6-7 €/mes y reducir tope blando de vuelta a 8 €.

Para cambiar topes: editar `MONTHLY_SOFT_CAP_EUR` y `MONTHLY_HARD_CAP_EUR` en [`src/costs.py`](https://github.com/otundra/ibiza-housing-radar/blob/main/src/costs.py).
