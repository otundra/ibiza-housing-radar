# Control de costes — privado

*Archivo privado. No se publica en la web. Última actualización: 2026-05-11 08:27 UTC*

Tipo de cambio interno: **1 USD = 0.92 EUR** (revisar cada 3 meses).

## Mes en curso

- **Gastado 2026-05:** `1.36 €` (`$1.4751` USD)
- **Tope blando:** `12.00 €` → solo avisa por Telegram, sigue publicando
- **Tope duro:** `50.00 €` → corta el pipeline (protección runaway)
- **Consumo vs blando:** `11.3%`
- **Consumo vs duro:** `2.7%`

```
[░░░░░░░░░░░░░░░░░░░░] 2.7% del tope duro
```

**Capa actual:** 🟢 Verde (<6 €) — silencio

## Histórico mensual

| Mes | Gasto (€) | Gasto (USD) |
|---|---|---|
| 2026-05 | 1.36 € | $1.4751 |
| 2026-04 | 6.86 € | $7.4611 |
| **TOTAL** | **8.22 €** | **$8.9362** |

## Gasto por fase

| Fase | Gasto (€) | % |
|---|---|---|
| generate | 5.67 € | 68.9% |
| bench_extract | 0.59 € | 7.2% |
| gold_extract_opus | 0.46 € | 5.6% |
| bench_classify | 0.30 € | 3.6% |
| bench_detect | 0.28 € | 3.4% |
| self_review | 0.22 € | 2.7% |
| classify | 0.14 € | 1.7% |
| gold_classify_opus | 0.12 € | 1.5% |
| gold_detect_opus | 0.12 € | 1.4% |
| audit_blind | 0.08 € | 1.0% |
| extract_fallback | 0.06 € | 0.7% |
| extract_base | 0.05 € | 0.6% |
| extract_validate | 0.04 € | 0.5% |
| gold_validate_task_3_extract | 0.04 € | 0.5% |
| gold_validate_task_1_classify | 0.03 € | 0.4% |
| gold_validate_task_2_proposal_detect | 0.03 € | 0.4% |

## Consumo por modelo

| Modelo | Input tokens | Output tokens | Gasto (€) |
|---|---|---|---|
| `claude-opus-4-7` | 169,135 | 66,586 | 7.30 € |
| `claude-sonnet-4-6` | 129,270 | 22,149 | 0.66 € |
| `claude-haiku-4-5-20251001` | 71,542 | 42,032 | 0.26 € |

## Últimas 20 llamadas

| Fecha | Edición | Fase | Modelo | In | Out | € |
|---|---|---|---|---|---|---|
| 2026-05-11 08:27 | 2026-W20 | self_review | `claude-sonnet-4-6` | 14,972 | 1,222 | 0.0582 € |
| 2026-05-11 08:26 | 2026-W20 | generate | `claude-opus-4-7` | 13,511 | 5,295 | 0.6394 € |
| 2026-05-11 08:26 | 2026-w20 | audit_blind | `claude-sonnet-4-6` | 1,678 | 1,050 | 0.0191 € |
| 2026-05-11 08:25 | 2026-W20 | extract_validate | `claude-sonnet-4-6` | 800 | 18 | 0.0025 € |
| 2026-05-11 08:25 | 2026-W20 | extract_validate | `claude-sonnet-4-6` | 829 | 18 | 0.0025 € |
| 2026-05-11 08:25 | 2026-W20 | extract_validate | `claude-sonnet-4-6` | 831 | 18 | 0.0025 € |
| 2026-05-11 08:25 | 2026-W20 | extract_base | `claude-haiku-4-5-20251001` | 2,052 | 999 | 0.0065 € |
| 2026-05-11 08:25 | 2026-W20 | classify | `claude-haiku-4-5-20251001` | 4,878 | 3,978 | 0.0228 € |
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

## Política de costes

- **Tope blando (12.00 €):** Telegram avisa, pero el pipeline **sigue publicando la editorial**. No se pierde informe por sobrecoste.
- **Tope duro (50.00 €):** Telegram crítico + **corte inmediato**. Protección real contra bugs o bucles runaway.

Coste esperado (pivote documental + autoevaluación 3 niveles): ~9,86 €/mes. Tras afinar reparto de modelos y con corpus estable, objetivo bajar a ~6-7 €/mes y reducir tope blando de vuelta a 8 €.

Para cambiar topes: editar `MONTHLY_SOFT_CAP_EUR` y `MONTHLY_HARD_CAP_EUR` en [`src/costs.py`](https://github.com/otundra/ibiza-housing-radar/blob/main/src/costs.py).
