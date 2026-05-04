# Control de costes — privado

*Archivo privado. No se publica en la web. Última actualización: 2026-05-04 07:50 UTC*

Tipo de cambio interno: **1 USD = 0.92 EUR** (revisar cada 3 meses).

## Mes en curso

- **Gastado 2026-05:** `0.60 €` (`$0.6560` USD)
- **Tope blando:** `12.00 €` → solo avisa por Telegram, sigue publicando
- **Tope duro:** `50.00 €` → corta el pipeline (protección runaway)
- **Consumo vs blando:** `5.0%`
- **Consumo vs duro:** `1.2%`

```
[░░░░░░░░░░░░░░░░░░░░] 1.2% del tope duro
```

**Capa actual:** 🟢 Verde (<6 €) — silencio

## Histórico mensual

| Mes | Gasto (€) | Gasto (USD) |
|---|---|---|
| 2026-05 | 0.60 € | $0.6560 |
| 2026-04 | 6.86 € | $7.4611 |
| **TOTAL** | **7.47 €** | **$8.1172** |

## Gasto por fase

| Fase | Gasto (€) | % |
|---|---|---|
| generate | 5.03 € | 67.3% |
| bench_extract | 0.59 € | 7.9% |
| gold_extract_opus | 0.46 € | 6.1% |
| bench_classify | 0.30 € | 4.0% |
| bench_detect | 0.28 € | 3.7% |
| self_review | 0.16 € | 2.2% |
| gold_classify_opus | 0.12 € | 1.6% |
| classify | 0.12 € | 1.6% |
| gold_detect_opus | 0.12 € | 1.6% |
| extract_fallback | 0.06 € | 0.8% |
| audit_blind | 0.06 € | 0.8% |
| gold_validate_task_3_extract | 0.04 € | 0.5% |
| extract_base | 0.04 € | 0.5% |
| extract_validate | 0.03 € | 0.5% |
| gold_validate_task_1_classify | 0.03 € | 0.4% |
| gold_validate_task_2_proposal_detect | 0.03 € | 0.4% |

## Consumo por modelo

| Modelo | Input tokens | Output tokens | Gasto (€) |
|---|---|---|---|
| `claude-opus-4-7` | 155,624 | 61,291 | 6.66 € |
| `claude-sonnet-4-6` | 110,160 | 19,823 | 0.58 € |
| `claude-haiku-4-5-20251001` | 64,612 | 37,055 | 0.23 € |

## Últimas 20 llamadas

| Fecha | Edición | Fase | Modelo | In | Out | € |
|---|---|---|---|---|---|---|
| 2026-05-04 07:50 | 2026-W19 | self_review | `claude-sonnet-4-6` | 10,246 | 875 | 0.0404 € |
| 2026-05-04 07:49 | 2026-W19 | generate | `claude-opus-4-7` | 8,303 | 4,098 | 0.4607 € |
| 2026-05-04 07:48 | 2026-w19 | audit_blind | `claude-sonnet-4-6` | 1,375 | 453 | 0.0100 € |
| 2026-05-04 07:48 | 2026-W19 | extract_fallback | `claude-opus-4-7` | 1,814 | 528 | 0.0615 € |
| 2026-05-04 07:48 | 2026-W19 | extract_validate | `claude-sonnet-4-6` | 1,063 | 68 | 0.0039 € |
| 2026-05-04 07:48 | 2026-W19 | extract_base | `claude-haiku-4-5-20251001` | 1,778 | 528 | 0.0041 € |
| 2026-05-04 07:48 | 2026-W19 | classify | `claude-haiku-4-5-20251001` | 4,705 | 4,066 | 0.0230 € |
| 2026-04-28 20:39 | 2026-W17 | generate | `claude-opus-4-7` | 5,981 | 4,007 | 0.3641 € |
| 2026-04-28 20:38 | 2026-W18 | generate | `claude-opus-4-7` | 5,981 | 3,294 | 0.3149 € |
| 2026-04-28 20:37 | 2026-W18 | generate | `claude-opus-4-7` | 5,981 | 3,647 | 0.3975 € |
| 2026-04-27 10:29 | 2026-W18 | self_review | `claude-sonnet-4-6` | 8,018 | 711 | 0.0319 € |
| 2026-04-27 09:46 | 2026-W18 | self_review | `claude-sonnet-4-6` | 8,101 | 876 | 0.0344 € |
| 2026-04-27 09:46 | 2026-W18 | generate | `claude-opus-4-7` | 13,682 | 5,124 | 0.5966 € |
| 2026-04-27 09:45 | 2026-w18 | audit_blind | `claude-sonnet-4-6` | 1,743 | 1,005 | 0.0187 € |
| 2026-04-27 09:44 | adhoc | extract_validate | `claude-sonnet-4-6` | 908 | 18 | 0.0028 € |
| 2026-04-27 09:44 | adhoc | extract_validate | `claude-sonnet-4-6` | 841 | 13 | 0.0025 € |
| 2026-04-27 09:44 | adhoc | extract_validate | `claude-sonnet-4-6` | 819 | 13 | 0.0024 € |
| 2026-04-27 09:44 | adhoc | extract_base | `claude-haiku-4-5-20251001` | 1,933 | 1,010 | 0.0064 € |
| 2026-04-27 09:44 | adhoc | classify | `claude-haiku-4-5-20251001` | 7,121 | 6,091 | 0.0346 € |
| 2026-04-25 15:40 | audit-phase1-test | audit_blind | `claude-sonnet-4-6` | 1,881 | 1,348 | 0.0238 € |

## Política de costes

- **Tope blando (12.00 €):** Telegram avisa, pero el pipeline **sigue publicando la editorial**. No se pierde informe por sobrecoste.
- **Tope duro (50.00 €):** Telegram crítico + **corte inmediato**. Protección real contra bugs o bucles runaway.

Coste esperado (pivote documental + autoevaluación 3 niveles): ~9,86 €/mes. Tras afinar reparto de modelos y con corpus estable, objetivo bajar a ~6-7 €/mes y reducir tope blando de vuelta a 8 €.

Para cambiar topes: editar `MONTHLY_SOFT_CAP_EUR` y `MONTHLY_HARD_CAP_EUR` en [`src/costs.py`](https://github.com/otundra/ibiza-housing-radar/blob/main/src/costs.py).
