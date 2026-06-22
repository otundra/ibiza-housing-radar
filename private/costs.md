# Control de costes — privado

*Archivo privado. No se publica en la web. Última actualización: 2026-06-22 10:48 UTC*

Tipo de cambio interno: **1 USD = 0.92 EUR** (revisar cada 3 meses).

## Mes en curso

- **Gastado 2026-06:** `4.08 €` (`$4.4328` USD)
- **Tope blando:** `12.00 €` → solo avisa por Telegram, sigue publicando
- **Tope duro:** `50.00 €` → corta el pipeline (protección runaway)
- **Consumo vs blando:** `34.0%`
- **Consumo vs duro:** `8.2%`

```
[█░░░░░░░░░░░░░░░░░░░] 8.2% del tope duro
```

**Capa actual:** 🟢 Verde (<6 €) — silencio

## Histórico mensual

| Mes | Gasto (€) | Gasto (USD) |
|---|---|---|
| 2026-06 | 4.08 € | $4.4328 |
| 2026-05 | 3.30 € | $3.5859 |
| 2026-04 | 6.86 € | $7.4611 |
| **TOTAL** | **14.24 €** | **$15.4798** |

## Gasto por fase

| Fase | Gasto (€) | % |
|---|---|---|
| generate | 10.55 € | 74.1% |
| self_review | 0.69 € | 4.9% |
| bench_extract | 0.59 € | 4.2% |
| gold_extract_opus | 0.46 € | 3.2% |
| classify | 0.31 € | 2.2% |
| extract_fallback | 0.30 € | 2.1% |
| bench_classify | 0.30 € | 2.1% |
| bench_detect | 0.28 € | 2.0% |
| audit_blind | 0.22 € | 1.5% |
| gold_classify_opus | 0.12 € | 0.9% |
| gold_detect_opus | 0.12 € | 0.8% |
| extract_validate | 0.11 € | 0.7% |
| extract_base | 0.09 € | 0.7% |
| gold_validate_task_3_extract | 0.04 € | 0.3% |
| gold_validate_task_1_classify | 0.03 € | 0.2% |
| gold_validate_task_2_proposal_detect | 0.03 € | 0.2% |

## Consumo por modelo

| Modelo | Input tokens | Output tokens | Gasto (€) |
|---|---|---|---|
| `claude-opus-4-7` | 278,039 | 110,505 | 12.42 € |
| `claude-sonnet-4-6` | 274,551 | 38,972 | 1.34 € |
| `claude-haiku-4-5-20251001` | 124,373 | 79,335 | 0.48 € |

## Últimas 20 llamadas

| Fecha | Edición | Fase | Modelo | In | Out | € |
|---|---|---|---|---|---|---|
| 2026-06-22 10:48 | 2026-W26 | self_review | `claude-sonnet-4-6` | 23,392 | 1,331 | 0.0871 € |
| 2026-06-22 10:47 | 2026-W26 | generate | `claude-opus-4-7` | 17,824 | 8,192 | 0.9117 € |
| 2026-06-22 10:45 | 2026-w26 | audit_blind | `claude-sonnet-4-6` | 1,576 | 2,774 | 0.0464 € |
| 2026-06-22 10:45 | 2026-W26 | extract_validate | `claude-sonnet-4-6` | 867 | 18 | 0.0026 € |
| 2026-06-22 10:45 | 2026-W26 | extract_validate | `claude-sonnet-4-6` | 836 | 18 | 0.0026 € |
| 2026-06-22 10:45 | 2026-W26 | extract_validate | `claude-sonnet-4-6` | 814 | 18 | 0.0025 € |
| 2026-06-22 10:45 | 2026-W26 | extract_validate | `claude-sonnet-4-6` | 843 | 18 | 0.0026 € |
| 2026-06-22 10:45 | 2026-W26 | extract_validate | `claude-sonnet-4-6` | 838 | 18 | 0.0026 € |
| 2026-06-22 10:45 | 2026-W26 | extract_fallback | `claude-opus-4-7` | 1,712 | 418 | 0.0525 € |
| 2026-06-22 10:44 | 2026-W26 | extract_validate | `claude-sonnet-4-6` | 818 | 85 | 0.0034 € |
| 2026-06-22 10:44 | 2026-W26 | extract_validate | `claude-sonnet-4-6` | 852 | 18 | 0.0026 € |
| 2026-06-22 10:44 | 2026-W26 | extract_fallback | `claude-opus-4-7` | 1,728 | 418 | 0.0527 € |
| 2026-06-22 10:44 | 2026-W26 | extract_validate | `claude-sonnet-4-6` | 841 | 94 | 0.0036 € |
| 2026-06-22 10:44 | 2026-W26 | extract_base | `claude-haiku-4-5-20251001` | 3,099 | 2,702 | 0.0153 € |
| 2026-06-22 10:44 | 2026-W26 | classify | `claude-haiku-4-5-20251001` | 5,740 | 4,340 | 0.0252 € |
| 2026-06-15 10:58 | 2026-W25 | self_review | `claude-sonnet-4-6` | 21,253 | 2,048 | 0.0910 € |
| 2026-06-15 10:57 | 2026-W25 | generate | `claude-opus-4-7` | 15,833 | 6,876 | 0.7934 € |
| 2026-06-15 10:56 | 2026-W25 | extract_fallback | `claude-opus-4-7` | 1,695 | 29 | 0.0254 € |
| 2026-06-15 10:56 | 2026-W25 | extract_validate | `claude-sonnet-4-6` | 793 | 66 | 0.0031 € |
| 2026-06-15 10:56 | 2026-W25 | extract_base | `claude-haiku-4-5-20251001` | 2,015 | 391 | 0.0037 € |

## Política de costes

- **Tope blando (12.00 €):** Telegram avisa, pero el pipeline **sigue publicando la editorial**. No se pierde informe por sobrecoste.
- **Tope duro (50.00 €):** Telegram crítico + **corte inmediato**. Protección real contra bugs o bucles runaway.

Coste esperado (pivote documental + autoevaluación 3 niveles): ~9,86 €/mes. Tras afinar reparto de modelos y con corpus estable, objetivo bajar a ~6-7 €/mes y reducir tope blando de vuelta a 8 €.

Para cambiar topes: editar `MONTHLY_SOFT_CAP_EUR` y `MONTHLY_HARD_CAP_EUR` en [`src/costs.py`](https://github.com/otundra/ibiza-housing-radar/blob/main/src/costs.py).
