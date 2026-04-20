---
layout: page
title: Costes
permalink: /costes/
---

# Control de costes

*Dashboard generado automáticamente tras cada ejecución del pipeline.*

## Política

- **Tope mensual:** 5,00 USD (~4,60 €).
- Si el gasto del mes en curso supera el tope, el pipeline **aborta** antes de llamar a la API y el workflow del lunes falla en rojo.
- Coste esperado: ~2 USD/mes (~1,85 €). El 90 % de ese gasto es Claude Opus generando el informe del lunes. El resto es Claude Haiku clasificando 15-25 titulares por semana.

## Modelos y tarifas vigentes

| Modelo | Input (USD/Mtok) | Output (USD/Mtok) | Uso |
|---|---|---|---|
| `claude-haiku-4-5` | 1,00 | 5,00 | Clasificación semanal de titulares |
| `claude-opus-4-7` | 15,00 | 75,00 | Generación del informe semanal |

## Data

*El histórico real de ejecuciones aparecerá aquí tras el primer `cron` de GitHub Actions. El archivo fuente es [`data/costs.csv`](https://github.com/otundra/ibiza-housing-radar/blob/main/data/costs.csv) (append-only, commiteado en cada run).*

## Subir o bajar el tope

Editar `MONTHLY_BUDGET_USD` en [`src/costs.py`](https://github.com/otundra/ibiza-housing-radar/blob/main/src/costs.py) y hacer push. El siguiente workflow lo aplica automáticamente.
