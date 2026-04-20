---
layout: default
title: Costes
permalink: /costes/
---

# Control de costes

*Última actualización: 2026-04-20 06:41 UTC*

## Mes en curso

- **Gastado 2026-04:** `$1.9391` USD
- **Tope mensual:** `$5.00` USD
- **Consumo:** `38.8%` del tope

```
[███████░░░░░░░░░░░░░] 38.8%
```

## Histórico mensual

| Mes | Gasto USD |
|-----|-----------|
| 2026-04 | $1.9391 |
| **TOTAL** | **$1.9391** |

## Gasto por fase

| Fase | Gasto USD | % |
|------|-----------|---|
| generate | $1.8921 | 97.6% |
| classify | $0.0469 | 2.4% |

## Consumo por modelo

| Modelo | Input tokens | Output tokens | Gasto USD |
|--------|--------------|---------------|-----------|
| `claude-opus-4-7` | 50,466 | 15,135 | $1.8921 |
| `claude-haiku-4-5-20251001` | 11,891 | 7,009 | $0.0469 |

## Últimas 20 llamadas

| Fecha | Edición | Fase | Modelo | In | Out | USD |
|-------|---------|------|--------|-----|-----|-----|
| 2026-04-20 06:41 | 2026-W17 | generate | `claude-opus-4-7` | 8,943 | 3,999 | $0.4341 |
| 2026-04-20 06:40 | adhoc | classify | `claude-haiku-4-5-20251001` | 3,965 | 2,545 | $0.0167 |
| 2026-04-20 06:33 | 2026-W17 | generate | `claude-opus-4-7` | 21,127 | 7,040 | $0.8449 |
| 2026-04-20 06:29 | adhoc | classify | `claude-haiku-4-5-20251001` | 3,965 | 1,983 | $0.0139 |
| 2026-04-20 06:21 | 2026-W17 | generate | `claude-opus-4-7` | 20,396 | 4,096 | $0.6131 |
| 2026-04-20 06:18 | adhoc | classify | `claude-haiku-4-5-20251001` | 3,961 | 2,481 | $0.0164 |

## Política de costes

Si el gasto mensual supera **$5.00 USD**, el pipeline aborta automáticamente antes de llamar a la API. Para subir el tope, editar `MONTHLY_BUDGET_USD` en [`src/costs.py`](https://github.com/otundra/ibiza-housing-radar/blob/main/src/costs.py).

El sistema prioriza **Claude Haiku** para clasificación (~$0.01 por ejecución) y **Claude Opus** solo para generar el informe final (~$0.50 por ejecución). Coste esperado ≈ **$2/mes**.
