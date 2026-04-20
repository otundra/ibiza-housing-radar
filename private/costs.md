# Control de costes — privado

*Archivo privado. No se publica en la web. Última actualización: 2026-04-20 18:32 UTC*

Tipo de cambio interno: **1 USD = 0.92 EUR** (revisar cada 3 meses).

## Mes en curso

- **Gastado 2026-04:** `5.02 €` (`$5.4515` USD)
- **Tope blando:** `12.00 €` → solo avisa por Telegram, sigue publicando
- **Tope duro:** `20.00 €` → corta el pipeline (protección runaway)
- **Consumo vs blando:** `41.8%`
- **Consumo vs duro:** `25.1%`

```
[█████░░░░░░░░░░░░░░░] 25.1% del tope duro
```

**Capa actual:** 🟢 Verde (<6 €) — silencio

## Histórico mensual

| Mes | Gasto (€) | Gasto (USD) |
|---|---|---|
| 2026-04 | 5.02 € | $5.4515 |
| **TOTAL** | **5.02 €** | **$5.4515** |

## Gasto por fase

| Fase | Gasto (€) | % |
|---|---|---|
| generate | 2.89 € | 57.7% |
| bench_extract | 0.59 € | 11.8% |
| gold_extract_opus | 0.46 € | 9.1% |
| bench_classify | 0.30 € | 5.9% |
| bench_detect | 0.28 € | 5.5% |
| gold_classify_opus | 0.12 € | 2.4% |
| gold_detect_opus | 0.12 € | 2.3% |
| classify | 0.06 € | 1.2% |
| self_review | 0.05 € | 1.1% |
| gold_validate_task_3_extract | 0.04 € | 0.8% |
| gold_validate_task_1_classify | 0.03 € | 0.6% |
| gold_validate_task_2_proposal_detect | 0.03 € | 0.6% |
| extract_validate | 0.02 € | 0.5% |
| extract_base | 0.02 € | 0.4% |

## Consumo por modelo

| Modelo | Input tokens | Output tokens | Gasto (€) |
|---|---|---|---|
| `claude-opus-4-7` | 113,882 | 40,593 | 4.46 € |
| `claude-sonnet-4-6` | 73,832 | 14,071 | 0.40 € |
| `claude-haiku-4-5-20251001` | 45,863 | 23,958 | 0.15 € |

## Últimas 20 llamadas

| Fecha | Edición | Fase | Modelo | In | Out | € |
|---|---|---|---|---|---|---|
| 2026-04-20 18:31 | 2026-W17 | self_review | `claude-sonnet-4-6` | 5,943 | 756 | 0.0268 € |
| 2026-04-20 18:30 | 2026-W17 | generate | `claude-opus-4-7` | 5,777 | 3,803 | 0.3462 € |
| 2026-04-20 18:29 | adhoc | extract_validate | `claude-sonnet-4-6` | 819 | 18 | 0.0025 € |
| 2026-04-20 18:29 | adhoc | extract_validate | `claude-sonnet-4-6` | 783 | 18 | 0.0024 € |
| 2026-04-20 18:29 | adhoc | extract_validate | `claude-sonnet-4-6` | 916 | 18 | 0.0028 € |
| 2026-04-20 18:29 | adhoc | extract_base | `claude-haiku-4-5-20251001` | 1,880 | 1,020 | 0.0064 € |
| 2026-04-20 18:26 | 2026-W17 | generate | `claude-opus-4-7` | 5,774 | 4,013 | 0.4074 € |
| 2026-04-20 18:25 | adhoc | extract_validate | `claude-sonnet-4-6` | 818 | 18 | 0.0025 € |
| 2026-04-20 18:25 | adhoc | extract_validate | `claude-sonnet-4-6` | 785 | 18 | 0.0024 € |
| 2026-04-20 18:25 | adhoc | extract_validate | `claude-sonnet-4-6` | 913 | 18 | 0.0028 € |
| 2026-04-20 18:25 | adhoc | extract_base | `claude-haiku-4-5-20251001` | 1,880 | 1,018 | 0.0064 € |
| 2026-04-20 18:16 | 2026-W17 | self_review | `claude-sonnet-4-6` | 6,134 | 729 | 0.0270 € |
| 2026-04-20 18:16 | 2026-W17 | generate | `claude-opus-4-7` | 5,769 | 4,067 | 0.3979 € |
| 2026-04-20 18:15 | adhoc | extract_validate | `claude-sonnet-4-6` | 819 | 18 | 0.0025 € |
| 2026-04-20 18:15 | adhoc | extract_validate | `claude-sonnet-4-6` | 784 | 18 | 0.0024 € |
| 2026-04-20 18:15 | adhoc | extract_validate | `claude-sonnet-4-6` | 910 | 18 | 0.0028 € |
| 2026-04-20 18:15 | adhoc | extract_base | `claude-haiku-4-5-20251001` | 1,542 | 1,016 | 0.0061 € |
| 2026-04-20 18:15 | adhoc | classify | `claude-haiku-4-5-20251001` | 3,922 | 3,210 | 0.0184 € |
| 2026-04-20 17:50 | bench-extract | bench_extract | `claude-opus-4-7` | 5,526 | 2,009 | 0.2149 € |
| 2026-04-20 17:50 | bench-extract | bench_extract | `claude-sonnet-4-6` | 4,391 | 4,140 | 0.0693 € |

## Política de costes

- **Tope blando (12.00 €):** Telegram avisa, pero el pipeline **sigue publicando la editorial**. No se pierde informe por sobrecoste.
- **Tope duro (20.00 €):** Telegram crítico + **corte inmediato**. Protección real contra bugs o bucles runaway.

Coste esperado (pivote documental + autoevaluación 3 niveles): ~9,86 €/mes. Tras afinar reparto de modelos y con corpus estable, objetivo bajar a ~6-7 €/mes y reducir tope blando de vuelta a 8 €.

Para cambiar topes: editar `MONTHLY_SOFT_CAP_EUR` y `MONTHLY_HARD_CAP_EUR` en [`src/costs.py`](https://github.com/otundra/ibiza-housing-radar/blob/main/src/costs.py).
