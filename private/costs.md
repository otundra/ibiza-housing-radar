# Control de costes — privado

*Archivo privado. No se publica en la web. Última actualización: 2026-04-27 09:46 UTC*

Tipo de cambio interno: **1 USD = 0.92 EUR** (revisar cada 3 meses).

## Mes en curso

- **Gastado 2026-04:** `5.76 €` (`$6.2563` USD)
- **Tope blando:** `12.00 €` → solo avisa por Telegram, sigue publicando
- **Tope duro:** `50.00 €` → corta el pipeline (protección runaway)
- **Consumo vs blando:** `48.0%`
- **Consumo vs duro:** `11.5%`

```
[██░░░░░░░░░░░░░░░░░░] 11.5% del tope duro
```

**Capa actual:** 🟢 Verde (<6 €) — silencio

## Histórico mensual

| Mes | Gasto (€) | Gasto (USD) |
|---|---|---|
| 2026-04 | 5.76 € | $6.2563 |
| **TOTAL** | **5.76 €** | **$6.2563** |

## Gasto por fase

| Fase | Gasto (€) | % |
|---|---|---|
| generate | 3.49 € | 60.6% |
| bench_extract | 0.59 € | 10.3% |
| gold_extract_opus | 0.46 € | 8.0% |
| bench_classify | 0.30 € | 5.1% |
| bench_detect | 0.28 € | 4.8% |
| gold_classify_opus | 0.12 € | 2.1% |
| gold_detect_opus | 0.12 € | 2.0% |
| classify | 0.10 € | 1.7% |
| self_review | 0.09 € | 1.5% |
| audit_blind | 0.05 € | 0.9% |
| gold_validate_task_3_extract | 0.04 € | 0.7% |
| extract_base | 0.03 € | 0.6% |
| gold_validate_task_1_classify | 0.03 € | 0.6% |
| extract_validate | 0.03 € | 0.5% |
| gold_validate_task_2_proposal_detect | 0.03 € | 0.5% |

## Consumo por modelo

| Modelo | Input tokens | Output tokens | Gasto (€) |
|---|---|---|---|
| `claude-opus-4-7` | 127,564 | 45,717 | 5.06 € |
| `claude-sonnet-4-6` | 89,458 | 17,716 | 0.49 € |
| `claude-haiku-4-5-20251001` | 58,129 | 32,461 | 0.20 € |

## Últimas 20 llamadas

| Fecha | Edición | Fase | Modelo | In | Out | € |
|---|---|---|---|---|---|---|
| 2026-04-27 09:46 | 2026-W18 | self_review | `claude-sonnet-4-6` | 8,101 | 876 | 0.0344 € |
| 2026-04-27 09:46 | 2026-W18 | generate | `claude-opus-4-7` | 13,682 | 5,124 | 0.5966 € |
| 2026-04-27 09:45 | 2026-w18 | audit_blind | `claude-sonnet-4-6` | 1,743 | 1,005 | 0.0187 € |
| 2026-04-27 09:44 | adhoc | extract_validate | `claude-sonnet-4-6` | 908 | 18 | 0.0028 € |
| 2026-04-27 09:44 | adhoc | extract_validate | `claude-sonnet-4-6` | 841 | 13 | 0.0025 € |
| 2026-04-27 09:44 | adhoc | extract_validate | `claude-sonnet-4-6` | 819 | 13 | 0.0024 € |
| 2026-04-27 09:44 | adhoc | extract_base | `claude-haiku-4-5-20251001` | 1,933 | 1,010 | 0.0064 € |
| 2026-04-27 09:44 | adhoc | classify | `claude-haiku-4-5-20251001` | 7,121 | 6,091 | 0.0346 € |
| 2026-04-25 15:40 | audit-phase1-test | audit_blind | `claude-sonnet-4-6` | 1,881 | 1,348 | 0.0238 € |
| 2026-04-25 15:40 | audit-phase1-test | extract_base | `claude-haiku-4-5-20251001` | 1,880 | 1,028 | 0.0065 € |
| 2026-04-25 15:34 | audit-phase1-test | audit_blind | `claude-sonnet-4-6` | 1,333 | 372 | 0.0088 € |
| 2026-04-25 15:34 | audit-phase1-test | extract_base | `claude-haiku-4-5-20251001` | 1,332 | 374 | 0.0029 € |
| 2026-04-20 18:31 | 2026-W17 | self_review | `claude-sonnet-4-6` | 5,943 | 756 | 0.0268 € |
| 2026-04-20 18:30 | 2026-W17 | generate | `claude-opus-4-7` | 5,777 | 3,803 | 0.3462 € |
| 2026-04-20 18:29 | adhoc | extract_validate | `claude-sonnet-4-6` | 819 | 18 | 0.0025 € |
| 2026-04-20 18:29 | adhoc | extract_validate | `claude-sonnet-4-6` | 783 | 18 | 0.0024 € |
| 2026-04-20 18:29 | adhoc | extract_validate | `claude-sonnet-4-6` | 916 | 18 | 0.0028 € |
| 2026-04-20 18:29 | adhoc | extract_base | `claude-haiku-4-5-20251001` | 1,880 | 1,020 | 0.0064 € |
| 2026-04-20 18:26 | 2026-W17 | generate | `claude-opus-4-7` | 5,774 | 4,013 | 0.4074 € |
| 2026-04-20 18:25 | adhoc | extract_validate | `claude-sonnet-4-6` | 818 | 18 | 0.0025 € |

## Política de costes

- **Tope blando (12.00 €):** Telegram avisa, pero el pipeline **sigue publicando la editorial**. No se pierde informe por sobrecoste.
- **Tope duro (50.00 €):** Telegram crítico + **corte inmediato**. Protección real contra bugs o bucles runaway.

Coste esperado (pivote documental + autoevaluación 3 niveles): ~9,86 €/mes. Tras afinar reparto de modelos y con corpus estable, objetivo bajar a ~6-7 €/mes y reducir tope blando de vuelta a 8 €.

Para cambiar topes: editar `MONTHLY_SOFT_CAP_EUR` y `MONTHLY_HARD_CAP_EUR` en [`src/costs.py`](https://github.com/otundra/ibiza-housing-radar/blob/main/src/costs.py).
