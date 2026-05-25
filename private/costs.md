# Control de costes — privado

*Archivo privado. No se publica en la web. Última actualización: 2026-05-25 09:00 UTC*

Tipo de cambio interno: **1 USD = 0.92 EUR** (revisar cada 3 meses).

## Mes en curso

- **Gastado 2026-05:** `3.30 €` (`$3.5859` USD)
- **Tope blando:** `12.00 €` → solo avisa por Telegram, sigue publicando
- **Tope duro:** `50.00 €` → corta el pipeline (protección runaway)
- **Consumo vs blando:** `27.5%`
- **Consumo vs duro:** `6.6%`

```
[█░░░░░░░░░░░░░░░░░░░] 6.6% del tope duro
```

**Capa actual:** 🟢 Verde (<6 €) — silencio

## Histórico mensual

| Mes | Gasto (€) | Gasto (USD) |
|---|---|---|
| 2026-05 | 3.30 € | $3.5859 |
| 2026-04 | 6.86 € | $7.4611 |
| **TOTAL** | **10.16 €** | **$11.0470** |

## Gasto por fase

| Fase | Gasto (€) | % |
|---|---|---|
| generate | 7.20 € | 70.8% |
| bench_extract | 0.59 € | 5.8% |
| gold_extract_opus | 0.46 € | 4.5% |
| self_review | 0.36 € | 3.5% |
| bench_classify | 0.30 € | 2.9% |
| bench_detect | 0.28 € | 2.7% |
| classify | 0.20 € | 2.0% |
| extract_fallback | 0.17 € | 1.7% |
| audit_blind | 0.14 € | 1.4% |
| gold_classify_opus | 0.12 € | 1.2% |
| gold_detect_opus | 0.12 € | 1.2% |
| extract_validate | 0.07 € | 0.7% |
| extract_base | 0.06 € | 0.6% |
| gold_validate_task_3_extract | 0.04 € | 0.4% |
| gold_validate_task_1_classify | 0.03 € | 0.3% |
| gold_validate_task_2_proposal_detect | 0.03 € | 0.3% |

## Consumo por modelo

| Modelo | Input tokens | Output tokens | Gasto (€) |
|---|---|---|---|
| `claude-opus-4-7` | 204,242 | 80,643 | 8.94 € |
| `claude-sonnet-4-6` | 173,884 | 28,398 | 0.89 € |
| `claude-haiku-4-5-20251001` | 88,791 | 54,730 | 0.33 € |

## Últimas 20 llamadas

| Fecha | Edición | Fase | Modelo | In | Out | € |
|---|---|---|---|---|---|---|
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
| 2026-05-18 08:46 | 2026-W21 | extract_validate | `claude-sonnet-4-6` | 837 | 126 | 0.0040 € |
| 2026-05-18 08:46 | 2026-W21 | extract_validate | `claude-sonnet-4-6` | 809 | 18 | 0.0025 € |
| 2026-05-18 08:46 | 2026-W21 | extract_fallback | `claude-opus-4-7` | 1,753 | 444 | 0.0548 € |
| 2026-05-18 08:46 | 2026-W21 | extract_validate | `claude-sonnet-4-6` | 859 | 71 | 0.0034 € |
| 2026-05-18 08:46 | 2026-W21 | extract_validate | `claude-sonnet-4-6` | 839 | 18 | 0.0026 € |
| 2026-05-18 08:46 | 2026-W21 | extract_validate | `claude-sonnet-4-6` | 888 | 18 | 0.0027 € |
| 2026-05-18 08:46 | 2026-W21 | extract_validate | `claude-sonnet-4-6` | 844 | 18 | 0.0026 € |
| 2026-05-18 08:46 | 2026-W21 | extract_validate | `claude-sonnet-4-6` | 998 | 13 | 0.0029 € |
| 2026-05-18 08:46 | 2026-W21 | extract_base | `claude-haiku-4-5-20251001` | 2,781 | 2,721 | 0.0151 € |

## Política de costes

- **Tope blando (12.00 €):** Telegram avisa, pero el pipeline **sigue publicando la editorial**. No se pierde informe por sobrecoste.
- **Tope duro (50.00 €):** Telegram crítico + **corte inmediato**. Protección real contra bugs o bucles runaway.

Coste esperado (pivote documental + autoevaluación 3 niveles): ~9,86 €/mes. Tras afinar reparto de modelos y con corpus estable, objetivo bajar a ~6-7 €/mes y reducir tope blando de vuelta a 8 €.

Para cambiar topes: editar `MONTHLY_SOFT_CAP_EUR` y `MONTHLY_HARD_CAP_EUR` en [`src/costs.py`](https://github.com/otundra/ibiza-housing-radar/blob/main/src/costs.py).
