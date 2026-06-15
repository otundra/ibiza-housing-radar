# Control de costes — privado

*Archivo privado. No se publica en la web. Última actualización: 2026-06-15 10:58 UTC*

Tipo de cambio interno: **1 USD = 0.92 EUR** (revisar cada 3 meses).

## Mes en curso

- **Gastado 2026-06:** `2.86 €` (`$3.1140` USD)
- **Tope blando:** `12.00 €` → solo avisa por Telegram, sigue publicando
- **Tope duro:** `50.00 €` → corta el pipeline (protección runaway)
- **Consumo vs blando:** `23.9%`
- **Consumo vs duro:** `5.7%`

```
[█░░░░░░░░░░░░░░░░░░░] 5.7% del tope duro
```

**Capa actual:** 🟢 Verde (<6 €) — silencio

## Histórico mensual

| Mes | Gasto (€) | Gasto (USD) |
|---|---|---|
| 2026-06 | 2.86 € | $3.1140 |
| 2026-05 | 3.30 € | $3.5859 |
| 2026-04 | 6.86 € | $7.4611 |
| **TOTAL** | **13.03 €** | **$14.1610** |

## Gasto por fase

| Fase | Gasto (€) | % |
|---|---|---|
| generate | 9.64 € | 74.0% |
| self_review | 0.61 € | 4.6% |
| bench_extract | 0.59 € | 4.5% |
| gold_extract_opus | 0.46 € | 3.5% |
| bench_classify | 0.30 € | 2.3% |
| classify | 0.29 € | 2.2% |
| bench_detect | 0.28 € | 2.1% |
| extract_fallback | 0.20 € | 1.5% |
| audit_blind | 0.17 € | 1.3% |
| gold_classify_opus | 0.12 € | 0.9% |
| gold_detect_opus | 0.12 € | 0.9% |
| extract_validate | 0.08 € | 0.6% |
| extract_base | 0.08 € | 0.6% |
| gold_validate_task_3_extract | 0.04 € | 0.3% |
| gold_validate_task_1_classify | 0.03 € | 0.2% |
| gold_validate_task_2_proposal_detect | 0.03 € | 0.2% |

## Consumo por modelo

| Modelo | Input tokens | Output tokens | Gasto (€) |
|---|---|---|---|
| `claude-opus-4-7` | 256,775 | 101,477 | 11.41 € |
| `claude-sonnet-4-6` | 242,874 | 34,580 | 1.18 € |
| `claude-haiku-4-5-20251001` | 115,534 | 72,293 | 0.44 € |

## Últimas 20 llamadas

| Fecha | Edición | Fase | Modelo | In | Out | € |
|---|---|---|---|---|---|---|
| 2026-06-15 10:58 | 2026-W25 | self_review | `claude-sonnet-4-6` | 21,253 | 2,048 | 0.0910 € |
| 2026-06-15 10:57 | 2026-W25 | generate | `claude-opus-4-7` | 15,833 | 6,876 | 0.7934 € |
| 2026-06-15 10:56 | 2026-W25 | extract_fallback | `claude-opus-4-7` | 1,695 | 29 | 0.0254 € |
| 2026-06-15 10:56 | 2026-W25 | extract_validate | `claude-sonnet-4-6` | 793 | 66 | 0.0031 € |
| 2026-06-15 10:56 | 2026-W25 | extract_base | `claude-haiku-4-5-20251001` | 2,015 | 391 | 0.0037 € |
| 2026-06-15 10:56 | 2026-W25 | classify | `claude-haiku-4-5-20251001` | 5,903 | 4,212 | 0.0248 € |
| 2026-06-08 09:26 | 2026-W24 | self_review | `claude-sonnet-4-6` | 21,766 | 1,115 | 0.0796 € |
| 2026-06-08 09:25 | 2026-W24 | generate | `claude-opus-4-7` | 19,154 | 7,264 | 0.8660 € |
| 2026-06-08 09:24 | 2026-w24 | audit_blind | `claude-sonnet-4-6` | 190 | 325 | 0.0088 € |
| 2026-06-08 09:24 | 2026-W24 | extract_validate | `claude-sonnet-4-6` | 812 | 13 | 0.0024 € |
| 2026-06-08 09:24 | 2026-W24 | extract_base | `claude-haiku-4-5-20251001` | 1,507 | 349 | 0.0030 € |
| 2026-06-08 09:24 | 2026-W24 | classify | `claude-haiku-4-5-20251001` | 7,473 | 5,558 | 0.0324 € |
| 2026-06-01 10:25 | 2026-W23 | self_review | `claude-sonnet-4-6` | 20,237 | 1,167 | 0.0761 € |
| 2026-06-01 10:24 | 2026-W23 | generate | `claude-opus-4-7` | 15,851 | 6,665 | 0.7791 € |
| 2026-06-01 10:22 | 2026-w23 | audit_blind | `claude-sonnet-4-6` | 732 | 1,386 | 0.0249 € |
| 2026-06-01 10:22 | 2026-W23 | extract_validate | `claude-sonnet-4-6` | 806 | 18 | 0.0025 € |
| 2026-06-01 10:22 | 2026-W23 | extract_validate | `claude-sonnet-4-6` | 791 | 18 | 0.0024 € |
| 2026-06-01 10:22 | 2026-W23 | extract_validate | `claude-sonnet-4-6` | 805 | 13 | 0.0024 € |
| 2026-06-01 10:22 | 2026-W23 | extract_validate | `claude-sonnet-4-6` | 805 | 13 | 0.0024 € |
| 2026-06-01 10:22 | 2026-W23 | extract_base | `claude-haiku-4-5-20251001` | 1,818 | 1,231 | 0.0073 € |

## Política de costes

- **Tope blando (12.00 €):** Telegram avisa, pero el pipeline **sigue publicando la editorial**. No se pierde informe por sobrecoste.
- **Tope duro (50.00 €):** Telegram crítico + **corte inmediato**. Protección real contra bugs o bucles runaway.

Coste esperado (pivote documental + autoevaluación 3 niveles): ~9,86 €/mes. Tras afinar reparto de modelos y con corpus estable, objetivo bajar a ~6-7 €/mes y reducir tope blando de vuelta a 8 €.

Para cambiar topes: editar `MONTHLY_SOFT_CAP_EUR` y `MONTHLY_HARD_CAP_EUR` en [`src/costs.py`](https://github.com/otundra/ibiza-housing-radar/blob/main/src/costs.py).
