# Control de costes — privado

*Archivo privado. No se publica en la web. Última actualización: 2026-04-20 18:16 UTC*

Tipo de cambio interno: **1 USD = 0.92 EUR** (revisar cada 3 meses).

## Mes en curso

- **Gastado 2026-04:** `4.21 €` (`$4.5726` USD)
- **Tope blando:** `12.00 €` → solo avisa por Telegram, sigue publicando
- **Tope duro:** `20.00 €` → corta el pipeline (protección runaway)
- **Consumo vs blando:** `35.1%`
- **Consumo vs duro:** `21.0%`

```
[████░░░░░░░░░░░░░░░░] 21.0% del tope duro
```

**Capa actual:** 🟢 Verde (<6 €) — silencio

## Histórico mensual

| Mes | Gasto (€) | Gasto (USD) |
|---|---|---|
| 2026-04 | 4.21 € | $4.5726 |
| **TOTAL** | **4.21 €** | **$4.5726** |

## Gasto por fase

| Fase | Gasto (€) | % |
|---|---|---|
| generate | 2.14 € | 50.8% |
| bench_extract | 0.59 € | 14.1% |
| gold_extract_opus | 0.46 € | 10.9% |
| bench_classify | 0.30 € | 7.0% |
| bench_detect | 0.28 € | 6.6% |
| gold_classify_opus | 0.12 € | 2.9% |
| gold_detect_opus | 0.12 € | 2.8% |
| classify | 0.06 € | 1.5% |
| gold_validate_task_3_extract | 0.04 € | 1.0% |
| gold_validate_task_1_classify | 0.03 € | 0.8% |
| gold_validate_task_2_proposal_detect | 0.03 € | 0.7% |
| self_review | 0.03 € | 0.6% |
| extract_validate | 0.01 € | 0.2% |
| extract_base | 0.01 € | 0.1% |

## Consumo por modelo

| Modelo | Input tokens | Output tokens | Gasto (€) |
|---|---|---|---|
| `claude-opus-4-7` | 102,331 | 32,777 | 3.71 € |
| `claude-sonnet-4-6` | 62,855 | 13,207 | 0.36 € |
| `claude-haiku-4-5-20251001` | 42,103 | 21,920 | 0.14 € |

## Últimas 20 llamadas

| Fecha | Edición | Fase | Modelo | In | Out | € |
|---|---|---|---|---|---|---|
| 2026-04-20 18:16 | 2026-W17 | self_review | `claude-sonnet-4-6` | 6,134 | 729 | 0.0270 € |
| 2026-04-20 18:16 | 2026-W17 | generate | `claude-opus-4-7` | 5,769 | 4,067 | 0.3979 € |
| 2026-04-20 18:15 | adhoc | extract_validate | `claude-sonnet-4-6` | 819 | 18 | 0.0025 € |
| 2026-04-20 18:15 | adhoc | extract_validate | `claude-sonnet-4-6` | 784 | 18 | 0.0024 € |
| 2026-04-20 18:15 | adhoc | extract_validate | `claude-sonnet-4-6` | 910 | 18 | 0.0028 € |
| 2026-04-20 18:15 | adhoc | extract_base | `claude-haiku-4-5-20251001` | 1,542 | 1,016 | 0.0061 € |
| 2026-04-20 18:15 | adhoc | classify | `claude-haiku-4-5-20251001` | 3,922 | 3,210 | 0.0184 € |
| 2026-04-20 17:50 | bench-extract | bench_extract | `claude-opus-4-7` | 5,526 | 2,009 | 0.2149 € |
| 2026-04-20 17:50 | bench-extract | bench_extract | `claude-sonnet-4-6` | 4,391 | 4,140 | 0.0693 € |
| 2026-04-20 17:49 | bench-extract | bench_extract | `claude-haiku-4-5-20251001` | 4,390 | 3,824 | 0.0216 € |
| 2026-04-20 17:48 | bench-detect | bench_detect | `claude-opus-4-7` | 5,064 | 631 | 0.1134 € |
| 2026-04-20 17:48 | bench-detect | bench_detect | `claude-sonnet-4-6` | 4,026 | 605 | 0.0195 € |
| 2026-04-20 17:48 | bench-detect | bench_detect | `claude-haiku-4-5-20251001` | 4,025 | 614 | 0.0065 € |
| 2026-04-20 17:48 | bench-classify | bench_classify | `claude-opus-4-7` | 4,956 | 742 | 0.1196 € |
| 2026-04-20 17:48 | bench-classify | bench_classify | `claude-sonnet-4-6` | 3,960 | 685 | 0.0204 € |
| 2026-04-20 17:48 | bench-classify | bench_classify | `claude-haiku-4-5-20251001` | 3,959 | 865 | 0.0076 € |
| 2026-04-20 17:43 | bench-extract | bench_extract | `claude-opus-4-7` | 5,526 | 1,731 | 0.1957 € |
| 2026-04-20 17:43 | bench-extract | bench_extract | `claude-sonnet-4-6` | 4,391 | 4,114 | 0.0689 € |
| 2026-04-20 17:42 | bench-extract | bench_extract | `claude-haiku-4-5-20251001` | 4,390 | 3,919 | 0.0221 € |
| 2026-04-20 17:41 | bench-detect | bench_detect | `claude-opus-4-7` | 5,064 | 624 | 0.1129 € |

## Política de costes

- **Tope blando (12.00 €):** Telegram avisa, pero el pipeline **sigue publicando la editorial**. No se pierde informe por sobrecoste.
- **Tope duro (20.00 €):** Telegram crítico + **corte inmediato**. Protección real contra bugs o bucles runaway.

Coste esperado (pivote documental + autoevaluación 3 niveles): ~9,86 €/mes. Tras afinar reparto de modelos y con corpus estable, objetivo bajar a ~6-7 €/mes y reducir tope blando de vuelta a 8 €.

Para cambiar topes: editar `MONTHLY_SOFT_CAP_EUR` y `MONTHLY_HARD_CAP_EUR` en [`src/costs.py`](https://github.com/otundra/ibiza-housing-radar/blob/main/src/costs.py).
