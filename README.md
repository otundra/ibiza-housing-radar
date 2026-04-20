# Ibiza Housing Radar

Observatorio automatizado de noticias sobre la crisis de vivienda en Ibiza, centrado en trabajadores de temporada (mayo-octubre). Cada lunes genera un informe con propuestas accionables enlazadas a las noticias que las motivan.

- **Web pública:** <https://otundra.github.io/ibiza-housing-radar/>
- **Cadencia:** informe semanal, lunes 07:00 CEST (05:00 UTC)
- **Stack:** Python 3.12 + Anthropic API (Claude) + GitHub Actions + GitHub Pages
- **Coste:** 0 € de infraestructura; consumo API ~2 USD/mes (tope duro 5 USD)
- **Licencia:** MIT

## Qué hace

1. **Ingesta** por RSS: Google News + Diario de Ibiza + Periódico de Ibiza.
2. **Clasifica** cada noticia con Claude Haiku 4.5 (housing sí/no, actor, palanca).
3. **Genera** el informe con Claude Opus 4.7: 3-5 propuestas con actor responsable, coste estimado, precedente real y primer paso en ≤30 días.
4. **Publica** como Markdown en `docs/editions/` y lo sirve por GitHub Pages.
5. **Audita** cada llamada en `data/costs.csv` + dashboard en `docs/costs.md`.

## Puesta en marcha

Ya está en marcha. Solo necesitas estos dos secretos para que el workflow pueda correr:

- `ANTHROPIC_API_KEY` — pegado en Settings → Secrets → Actions. **[Ya configurado.]**

El workflow `weekly-report.yml` se dispara:
- Automáticamente cada lunes 05:00 UTC.
- Manualmente en Actions → Weekly report → Run workflow.

## Control de costes

Tope mensual duro: **5 USD**. Si el gasto del mes en curso lo supera, el pipeline aborta antes de llamar a la API. Editar `MONTHLY_BUDGET_USD` en [`src/costs.py`](src/costs.py) para ajustar.

Ver [`docs/costs.md`](docs/costs.md) para el dashboard en vivo.

## Ejecutar localmente

```bash
pip install -r requirements.txt
export ANTHROPIC_API_KEY=sk-ant-...
python -m src.report
```

Genera `docs/editions/<YYYY>-w<WW>.md`, actualiza `docs/index.md` y `docs/costs.md`, y registra el gasto en `data/costs.csv`.

## Estructura

Ver [CLAUDE.md](CLAUDE.md) para detalles de arquitectura, decisiones y comandos. Ver [CAMBIOS.md](CAMBIOS.md) para el diario de cambios relevantes del proyecto.

## Aviso

Las propuestas son sugerencias generadas por IA sobre prensa pública. No son análisis técnico ni asesoramiento jurídico, político o económico. Contrasta cifras con la fuente original antes de usarlas.
