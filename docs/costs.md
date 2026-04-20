---
layout: default
title: Costes
permalink: /costes/
---

# Control de costes

*Última actualización: 2026-04-20 06:33 UTC*

## Mes en curso

- **Gastado 2026-04:** `$1.4883` USD
- **Tope mensual:** `$5.00` USD
- **Consumo:** `29.8%` del tope

```
[█████░░░░░░░░░░░░░░░] 29.8%
```

## Histórico mensual

| Mes | Gasto USD |
|-----|-----------|
| 2026-04 | $1.4883 |
| **TOTAL** | **$1.4883** |

## Gasto por fase

| Fase | Gasto USD | % |
|------|-----------|---|
| generate | $1.4580 | 98.0% |
| classify | $0.0302 | 2.0% |

## Consumo por modelo

| Modelo | Input tokens | Output tokens | Gasto USD |
|--------|--------------|---------------|-----------|
| `claude-opus-4-7` | 41,523 | 11,136 | $1.4580 |
| `claude-haiku-4-5-20251001` | 7,926 | 4,464 | $0.0302 |

## Últimas 20 llamadas

| Fecha | Edición | Fase | Modelo | In | Out | USD |
|-------|---------|------|--------|-----|-----|-----|
| 2026-04-20 06:33 | 2026-W17 | generate | `claude-opus-4-7` | 21,127 | 7,040 | $0.8449 |
| 2026-04-20 06:29 | adhoc | classify | `claude-haiku-4-5-20251001` | 3,965 | 1,983 | $0.0139 |
| 2026-04-20 06:21 | 2026-W17 | generate | `claude-opus-4-7` | 20,396 | 4,096 | $0.6131 |
| 2026-04-20 06:18 | adhoc | classify | `claude-haiku-4-5-20251001` | 3,961 | 2,481 | $0.0164 |

## Política de costes

Si el gasto mensual supera **$5.00 USD**, el pipeline aborta automáticamente antes de llamar a la API. Para subir el tope, editar `MONTHLY_BUDGET_USD` en [`src/costs.py`](https://github.com/otundra/ibiza-housing-radar/blob/main/src/costs.py).

El sistema prioriza **Claude Haiku** para clasificación (~$0.01 por ejecución) y **Claude Opus** solo para generar el informe final (~$0.50 por ejecución). Coste esperado ≈ **$2/mes**.
