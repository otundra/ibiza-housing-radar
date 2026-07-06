# Control de costes — privado

*Archivo privado. No se publica en la web. Última actualización: 2026-07-06 09:03 UTC*

Tipo de cambio interno: **1 USD = 0.92 EUR** (revisar cada 3 meses).

## Mes en curso

- **Gastado 2026-07:** `0.87 €` (`$0.9471` USD)
- **Tope blando:** `12.00 €` → solo avisa por Telegram, sigue publicando
- **Tope duro:** `50.00 €` → corta el pipeline (protección runaway)
- **Consumo vs blando:** `7.3%`
- **Consumo vs duro:** `1.7%`

```
[░░░░░░░░░░░░░░░░░░░░] 1.7% del tope duro
```

**Capa actual:** 🟢 Verde (<6 €) — silencio

## Histórico mensual

| Mes | Gasto (€) | Gasto (USD) |
|---|---|---|
| 2026-07 | 0.87 € | $0.9471 |
| 2026-06 | 5.26 € | $5.7179 |
| 2026-05 | 3.30 € | $3.5859 |
| 2026-04 | 6.86 € | $7.4611 |
| **TOTAL** | **16.30 €** | **$17.7121** |

## Gasto por fase

| Fase | Gasto (€) | % |
|---|---|---|
| generate | 12.21 € | 75.0% |
| self_review | 0.87 € | 5.3% |
| bench_extract | 0.59 € | 3.6% |
| gold_extract_opus | 0.46 € | 2.8% |
| classify | 0.37 € | 2.2% |
| extract_fallback | 0.35 € | 2.2% |
| bench_classify | 0.30 € | 1.8% |
| audit_blind | 0.28 € | 1.7% |
| bench_detect | 0.28 € | 1.7% |
| extract_validate | 0.13 € | 0.8% |
| gold_classify_opus | 0.12 € | 0.7% |
| gold_detect_opus | 0.12 € | 0.7% |
| extract_base | 0.11 € | 0.7% |
| gold_validate_task_3_extract | 0.04 € | 0.2% |
| gold_validate_task_1_classify | 0.03 € | 0.2% |
| gold_validate_task_2_proposal_detect | 0.03 € | 0.2% |

## Consumo por modelo

| Modelo | Input tokens | Output tokens | Gasto (€) |
|---|---|---|---|
| `claude-opus-4-7` | 315,681 | 124,950 | 14.14 € |
| `claude-sonnet-4-6` | 332,899 | 45,436 | 1.61 € |
| `claude-haiku-4-5-20251001` | 140,492 | 91,461 | 0.55 € |

## Últimas 20 llamadas

| Fecha | Edición | Fase | Modelo | In | Out | € |
|---|---|---|---|---|---|---|
| 2026-07-06 09:03 | 2026-W28 | self_review | `claude-sonnet-4-6` | 23,359 | 1,268 | 0.0861 € |
| 2026-07-06 09:02 | 2026-W28 | generate | `claude-opus-4-7` | 15,865 | 6,027 | 0.7353 € |
| 2026-07-06 09:01 | 2026-w28 | audit_blind | `claude-sonnet-4-6` | 438 | 809 | 0.0161 € |
| 2026-07-06 09:00 | 2026-W28 | extract_validate | `claude-sonnet-4-6` | 956 | 18 | 0.0029 € |
| 2026-07-06 09:00 | 2026-W28 | extract_validate | `claude-sonnet-4-6` | 894 | 18 | 0.0027 € |
| 2026-07-06 09:00 | 2026-W28 | extract_base | `claude-haiku-4-5-20251001` | 1,743 | 834 | 0.0054 € |
| 2026-07-06 09:00 | 2026-W28 | classify | `claude-haiku-4-5-20251001` | 5,331 | 3,897 | 0.0228 € |
| 2026-06-29 09:30 | 2026-W27 | self_review | `claude-sonnet-4-6` | 24,423 | 1,320 | 0.0897 € |
| 2026-06-29 09:30 | 2026-W27 | generate | `claude-opus-4-7` | 20,058 | 8,016 | 0.9304 € |
| 2026-06-29 09:28 | 2026-w27 | audit_blind | `claude-sonnet-4-6` | 1,608 | 2,813 | 0.0470 € |
| 2026-06-29 09:27 | 2026-W27 | extract_validate | `claude-sonnet-4-6` | 774 | 18 | 0.0024 € |
| 2026-06-29 09:27 | 2026-W27 | extract_validate | `claude-sonnet-4-6` | 863 | 18 | 0.0026 € |
| 2026-06-29 09:27 | 2026-W27 | extract_validate | `claude-sonnet-4-6` | 846 | 18 | 0.0026 € |
| 2026-06-29 09:27 | 2026-W27 | extract_validate | `claude-sonnet-4-6` | 845 | 18 | 0.0026 € |
| 2026-06-29 09:27 | 2026-W27 | extract_validate | `claude-sonnet-4-6` | 887 | 18 | 0.0027 € |
| 2026-06-29 09:27 | 2026-W27 | extract_fallback | `claude-opus-4-7` | 1,719 | 402 | 0.0515 € |
| 2026-06-29 09:27 | 2026-W27 | extract_validate | `claude-sonnet-4-6` | 816 | 92 | 0.0035 € |
| 2026-06-29 09:27 | 2026-W27 | extract_validate | `claude-sonnet-4-6` | 776 | 18 | 0.0024 € |
| 2026-06-29 09:27 | 2026-W27 | extract_validate | `claude-sonnet-4-6` | 863 | 18 | 0.0026 € |
| 2026-06-29 09:27 | 2026-W27 | extract_base | `claude-haiku-4-5-20251001` | 2,694 | 2,600 | 0.0144 € |

## Política de costes

- **Tope blando (12.00 €):** Telegram avisa, pero el pipeline **sigue publicando la editorial**. No se pierde informe por sobrecoste.
- **Tope duro (50.00 €):** Telegram crítico + **corte inmediato**. Protección real contra bugs o bucles runaway.

Coste esperado (pivote documental + autoevaluación 3 niveles): ~9,86 €/mes. Tras afinar reparto de modelos y con corpus estable, objetivo bajar a ~6-7 €/mes y reducir tope blando de vuelta a 8 €.

Para cambiar topes: editar `MONTHLY_SOFT_CAP_EUR` y `MONTHLY_HARD_CAP_EUR` en [`src/costs.py`](https://github.com/otundra/ibiza-housing-radar/blob/main/src/costs.py).
