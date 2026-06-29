# Control de costes — privado

*Archivo privado. No se publica en la web. Última actualización: 2026-06-29 09:30 UTC*

Tipo de cambio interno: **1 USD = 0.92 EUR** (revisar cada 3 meses).

## Mes en curso

- **Gastado 2026-06:** `5.26 €` (`$5.7179` USD)
- **Tope blando:** `12.00 €` → solo avisa por Telegram, sigue publicando
- **Tope duro:** `50.00 €` → corta el pipeline (protección runaway)
- **Consumo vs blando:** `43.8%`
- **Consumo vs duro:** `10.5%`

```
[██░░░░░░░░░░░░░░░░░░] 10.5% del tope duro
```

**Capa actual:** 🟢 Verde (<6 €) — silencio

## Histórico mensual

| Mes | Gasto (€) | Gasto (USD) |
|---|---|---|
| 2026-06 | 5.26 € | $5.7179 |
| 2026-05 | 3.30 € | $3.5859 |
| 2026-04 | 6.86 € | $7.4611 |
| **TOTAL** | **15.42 €** | **$16.7649** |

## Gasto por fase

| Fase | Gasto (€) | % |
|---|---|---|
| generate | 11.48 € | 74.4% |
| self_review | 0.78 € | 5.1% |
| bench_extract | 0.59 € | 3.8% |
| gold_extract_opus | 0.46 € | 3.0% |
| extract_fallback | 0.35 € | 2.3% |
| classify | 0.34 € | 2.2% |
| bench_classify | 0.30 € | 1.9% |
| bench_detect | 0.28 € | 1.8% |
| audit_blind | 0.27 € | 1.7% |
| extract_validate | 0.13 € | 0.8% |
| gold_classify_opus | 0.12 € | 0.8% |
| gold_detect_opus | 0.12 € | 0.8% |
| extract_base | 0.11 € | 0.7% |
| gold_validate_task_3_extract | 0.04 € | 0.3% |
| gold_validate_task_1_classify | 0.03 € | 0.2% |
| gold_validate_task_2_proposal_detect | 0.03 € | 0.2% |

## Consumo por modelo

| Modelo | Input tokens | Output tokens | Gasto (€) |
|---|---|---|---|
| `claude-opus-4-7` | 299,816 | 118,923 | 13.40 € |
| `claude-sonnet-4-6` | 307,252 | 43,323 | 1.50 € |
| `claude-haiku-4-5-20251001` | 133,418 | 86,730 | 0.52 € |

## Últimas 20 llamadas

| Fecha | Edición | Fase | Modelo | In | Out | € |
|---|---|---|---|---|---|---|
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
| 2026-06-29 09:27 | 2026-W27 | classify | `claude-haiku-4-5-20251001` | 6,351 | 4,795 | 0.0279 € |
| 2026-06-22 10:48 | 2026-W26 | self_review | `claude-sonnet-4-6` | 23,392 | 1,331 | 0.0871 € |
| 2026-06-22 10:47 | 2026-W26 | generate | `claude-opus-4-7` | 17,824 | 8,192 | 0.9117 € |
| 2026-06-22 10:45 | 2026-w26 | audit_blind | `claude-sonnet-4-6` | 1,576 | 2,774 | 0.0464 € |
| 2026-06-22 10:45 | 2026-W26 | extract_validate | `claude-sonnet-4-6` | 867 | 18 | 0.0026 € |
| 2026-06-22 10:45 | 2026-W26 | extract_validate | `claude-sonnet-4-6` | 836 | 18 | 0.0026 € |
| 2026-06-22 10:45 | 2026-W26 | extract_validate | `claude-sonnet-4-6` | 814 | 18 | 0.0025 € |

## Política de costes

- **Tope blando (12.00 €):** Telegram avisa, pero el pipeline **sigue publicando la editorial**. No se pierde informe por sobrecoste.
- **Tope duro (50.00 €):** Telegram crítico + **corte inmediato**. Protección real contra bugs o bucles runaway.

Coste esperado (pivote documental + autoevaluación 3 niveles): ~9,86 €/mes. Tras afinar reparto de modelos y con corpus estable, objetivo bajar a ~6-7 €/mes y reducir tope blando de vuelta a 8 €.

Para cambiar topes: editar `MONTHLY_SOFT_CAP_EUR` y `MONTHLY_HARD_CAP_EUR` en [`src/costs.py`](https://github.com/otundra/ibiza-housing-radar/blob/main/src/costs.py).
