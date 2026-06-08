# Control de costes — privado

*Archivo privado. No se publica en la web. Última actualización: 2026-06-08 09:26 UTC*

Tipo de cambio interno: **1 USD = 0.92 EUR** (revisar cada 3 meses).

## Mes en curso

- **Gastado 2026-06:** `1.92 €` (`$2.0907` USD)
- **Tope blando:** `12.00 €` → solo avisa por Telegram, sigue publicando
- **Tope duro:** `50.00 €` → corta el pipeline (protección runaway)
- **Consumo vs blando:** `16.0%`
- **Consumo vs duro:** `3.8%`

```
[░░░░░░░░░░░░░░░░░░░░] 3.8% del tope duro
```

**Capa actual:** 🟢 Verde (<6 €) — silencio

## Histórico mensual

| Mes | Gasto (€) | Gasto (USD) |
|---|---|---|
| 2026-06 | 1.92 € | $2.0907 |
| 2026-05 | 3.30 € | $3.5859 |
| 2026-04 | 6.86 € | $7.4611 |
| **TOTAL** | **12.09 €** | **$13.1377** |

## Gasto por fase

| Fase | Gasto (€) | % |
|---|---|---|
| generate | 8.84 € | 73.2% |
| bench_extract | 0.59 € | 4.9% |
| self_review | 0.51 € | 4.3% |
| gold_extract_opus | 0.46 € | 3.8% |
| bench_classify | 0.30 € | 2.4% |
| bench_detect | 0.28 € | 2.3% |
| classify | 0.26 € | 2.2% |
| audit_blind | 0.17 € | 1.4% |
| extract_fallback | 0.17 € | 1.4% |
| gold_classify_opus | 0.12 € | 1.0% |
| gold_detect_opus | 0.12 € | 1.0% |
| extract_validate | 0.08 € | 0.7% |
| extract_base | 0.07 € | 0.6% |
| gold_validate_task_3_extract | 0.04 € | 0.3% |
| gold_validate_task_1_classify | 0.03 € | 0.3% |
| gold_validate_task_2_proposal_detect | 0.03 € | 0.3% |

## Consumo por modelo

| Modelo | Input tokens | Output tokens | Gasto (€) |
|---|---|---|---|
| `claude-opus-4-7` | 239,247 | 94,572 | 10.59 € |
| `claude-sonnet-4-6` | 220,828 | 32,466 | 1.09 € |
| `claude-haiku-4-5-20251001` | 107,616 | 67,690 | 0.41 € |

## Últimas 20 llamadas

| Fecha | Edición | Fase | Modelo | In | Out | € |
|---|---|---|---|---|---|---|
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
| 2026-06-01 10:22 | 2026-W23 | classify | `claude-haiku-4-5-20251001` | 8,027 | 5,822 | 0.0342 € |
| 2026-05-25 09:00 | 2026-W22 | self_review | `claude-sonnet-4-6` | 18,328 | 997 | 0.0685 € |
| 2026-05-25 08:59 | 2026-W22 | generate | `claude-opus-4-7` | 14,628 | 5,782 | 0.7013 € |
| 2026-05-25 08:58 | 2026-w22 | audit_blind | `claude-sonnet-4-6` | 275 | 374 | 0.0097 € |
| 2026-05-25 08:58 | 2026-W22 | extract_validate | `claude-sonnet-4-6` | 934 | 13 | 0.0028 € |
| 2026-05-25 08:58 | 2026-W22 | extract_base | `claude-haiku-4-5-20251001` | 1,361 | 369 | 0.0029 € |

## Política de costes

- **Tope blando (12.00 €):** Telegram avisa, pero el pipeline **sigue publicando la editorial**. No se pierde informe por sobrecoste.
- **Tope duro (50.00 €):** Telegram crítico + **corte inmediato**. Protección real contra bugs o bucles runaway.

Coste esperado (pivote documental + autoevaluación 3 niveles): ~9,86 €/mes. Tras afinar reparto de modelos y con corpus estable, objetivo bajar a ~6-7 €/mes y reducir tope blando de vuelta a 8 €.

Para cambiar topes: editar `MONTHLY_SOFT_CAP_EUR` y `MONTHLY_HARD_CAP_EUR` en [`src/costs.py`](https://github.com/otundra/ibiza-housing-radar/blob/main/src/costs.py).
