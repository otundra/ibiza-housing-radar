# Control de costes — privado

*Archivo privado. No se publica en la web. Última actualización: 2026-04-20 13:43 UTC*

Tipo de cambio interno: **1 USD = 0.92 EUR** (revisar cada 3 meses).

## Mes en curso

- **Gastado 2026-04:** `1.78 €` (`$1.9391` USD)
- **Tope blando:** `8.00 €` → solo avisa por Telegram, sigue publicando
- **Tope duro:** `20.00 €` → corta el pipeline (protección runaway)
- **Consumo vs blando:** `22.3%`
- **Consumo vs duro:** `8.9%`

```
[█░░░░░░░░░░░░░░░░░░░] 8.9% del tope duro
```

**Capa actual:** 🟢 Verde (<4 €) — silencio

## Histórico mensual

| Mes | Gasto (€) | Gasto (USD) |
|---|---|---|
| 2026-04 | 1.78 € | $1.9391 |
| **TOTAL** | **1.78 €** | **$1.9391** |

## Gasto por fase

| Fase | Gasto (€) | % |
|---|---|---|
| generate | 1.74 € | 97.6% |
| classify | 0.04 € | 2.4% |

## Consumo por modelo

| Modelo | Input tokens | Output tokens | Gasto (€) |
|---|---|---|---|
| `claude-opus-4-7` | 50,466 | 15,135 | 1.74 € |
| `claude-haiku-4-5-20251001` | 11,891 | 7,009 | 0.04 € |

## Últimas 20 llamadas

| Fecha | Edición | Fase | Modelo | In | Out | € |
|---|---|---|---|---|---|---|
| 2026-04-20 06:41 | 2026-W17 | generate | `claude-opus-4-7` | 8,943 | 3,999 | 0.3993 € |
| 2026-04-20 06:40 | adhoc | classify | `claude-haiku-4-5-20251001` | 3,965 | 2,545 | 0.0154 € |
| 2026-04-20 06:33 | 2026-W17 | generate | `claude-opus-4-7` | 21,127 | 7,040 | 0.7773 € |
| 2026-04-20 06:29 | adhoc | classify | `claude-haiku-4-5-20251001` | 3,965 | 1,983 | 0.0128 € |
| 2026-04-20 06:21 | 2026-W17 | generate | `claude-opus-4-7` | 20,396 | 4,096 | 0.5641 € |
| 2026-04-20 06:18 | adhoc | classify | `claude-haiku-4-5-20251001` | 3,961 | 2,481 | 0.0151 € |

## Política de costes

- **Tope blando (8.00 €):** Telegram avisa, pero el pipeline **sigue publicando la editorial**. No se pierde informe por sobrecoste.
- **Tope duro (20.00 €):** Telegram crítico + **corte inmediato**. Protección real contra bugs o bucles runaway.

Coste esperado actual: ~2 €/mes. Con trilingüe activo (diferido): ~3,15 €/mes. Los topes cubren ambos escenarios sin retoque.

Para cambiar topes: editar `MONTHLY_SOFT_CAP_EUR` y `MONTHLY_HARD_CAP_EUR` en [`src/costs.py`](https://github.com/otundra/ibiza-housing-radar/blob/main/src/costs.py).
