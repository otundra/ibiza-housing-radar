# Control de costes — privado

*Archivo privado. No se publica en la web. Última actualización: 2026-06-01 10:25 UTC*

Tipo de cambio interno: **1 USD = 0.92 EUR** (revisar cada 3 meses).

## Mes en curso

- **Gastado 2026-06:** `0.93 €` (`$1.0123` USD)
- **Tope blando:** `12.00 €` → solo avisa por Telegram, sigue publicando
- **Tope duro:** `50.00 €` → corta el pipeline (protección runaway)
- **Consumo vs blando:** `7.8%`
- **Consumo vs duro:** `1.9%`

```
[░░░░░░░░░░░░░░░░░░░░] 1.9% del tope duro
```

**Capa actual:** 🟢 Verde (<6 €) — silencio

## Histórico mensual

| Mes | Gasto (€) | Gasto (USD) |
|---|---|---|
| 2026-06 | 0.93 € | $1.0123 |
| 2026-05 | 3.30 € | $3.5859 |
| 2026-04 | 6.86 € | $7.4611 |
| **TOTAL** | **11.09 €** | **$12.0593** |

## Gasto por fase

| Fase | Gasto (€) | % |
|---|---|---|
| generate | 7.98 € | 71.9% |
| bench_extract | 0.59 € | 5.3% |
| gold_extract_opus | 0.46 € | 4.1% |
| self_review | 0.43 € | 3.9% |
| bench_classify | 0.30 € | 2.7% |
| bench_detect | 0.28 € | 2.5% |
| classify | 0.23 € | 2.1% |
| extract_fallback | 0.17 € | 1.5% |
| audit_blind | 0.16 € | 1.5% |
| gold_classify_opus | 0.12 € | 1.1% |
| gold_detect_opus | 0.12 € | 1.1% |
| extract_validate | 0.08 € | 0.7% |
| extract_base | 0.07 € | 0.6% |
| gold_validate_task_3_extract | 0.04 € | 0.4% |
| gold_validate_task_1_classify | 0.03 € | 0.3% |
| gold_validate_task_2_proposal_detect | 0.03 € | 0.3% |

## Consumo por modelo

| Modelo | Input tokens | Output tokens | Gasto (€) |
|---|---|---|---|
| `claude-opus-4-7` | 220,093 | 87,308 | 9.72 € |
| `claude-sonnet-4-6` | 198,060 | 31,013 | 1.00 € |
| `claude-haiku-4-5-20251001` | 98,636 | 61,783 | 0.37 € |

## Últimas 20 llamadas

| Fecha | Edición | Fase | Modelo | In | Out | € |
|---|---|---|---|---|---|---|
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
| 2026-05-25 08:58 | 2026-W22 | classify | `claude-haiku-4-5-20251001` | 6,347 | 4,518 | 0.0266 € |
| 2026-05-18 08:49 | 2026-W21 | self_review | `claude-sonnet-4-6` | 16,466 | 1,568 | 0.0712 € |
| 2026-05-18 08:48 | 2026-W21 | generate | `claude-opus-4-7` | 17,000 | 7,384 | 0.8317 € |
| 2026-05-18 08:47 | 2026-w21 | audit_blind | `claude-sonnet-4-6` | 1,695 | 2,997 | 0.0498 € |
| 2026-05-18 08:46 | 2026-W21 | extract_validate | `claude-sonnet-4-6` | 842 | 18 | 0.0026 € |
| 2026-05-18 08:46 | 2026-W21 | extract_fallback | `claude-opus-4-7` | 1,726 | 447 | 0.0547 € |

## Política de costes

- **Tope blando (12.00 €):** Telegram avisa, pero el pipeline **sigue publicando la editorial**. No se pierde informe por sobrecoste.
- **Tope duro (50.00 €):** Telegram crítico + **corte inmediato**. Protección real contra bugs o bucles runaway.

Coste esperado (pivote documental + autoevaluación 3 niveles): ~9,86 €/mes. Tras afinar reparto de modelos y con corpus estable, objetivo bajar a ~6-7 €/mes y reducir tope blando de vuelta a 8 €.

Para cambiar topes: editar `MONTHLY_SOFT_CAP_EUR` y `MONTHLY_HARD_CAP_EUR` en [`src/costs.py`](https://github.com/otundra/ibiza-housing-radar/blob/main/src/costs.py).
