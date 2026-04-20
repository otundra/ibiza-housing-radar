# Ibiza Housing Radar

Observatorio semanal de la crisis de vivienda en Ibiza, con foco en trabajadores de temporada (mayo-octubre). Cada lunes genera un informe con las señales de la semana, mapa de posiciones de los actores y propuestas reales documentadas con fuente verificable.

> ⚠️ **Pivote 2026-04-20.** El proyecto está migrando de "generador de propuestas" a **"observatorio documental"**. El LLM ya no genera propuestas propias; mapea, ordena y verifica las propuestas reales que actores con nombre formulan cada semana. Detalle en [`PIVOTE.md`](PIVOTE.md) y [`ROADMAP.md`](ROADMAP.md). El trabajo del pivote vive en el branch `pivote/observatorio-documental` hasta merge. El modelo antiguo sigue operativo en `main` hasta entonces.

- **Web pública:** <https://otundra.github.io/ibiza-housing-radar/>
- **Cadencia:** informe semanal, lunes 07:00 CEST (05:00 UTC)
- **Stack:** Python 3.12 + Anthropic API (Claude Haiku 4.5 + Sonnet 4.6 + Opus 4.7) + GitHub Actions + GitHub Pages
- **Coste (pivote documental):** 0 € de infraestructura; API ~6-7 €/mes proyectado incluyendo autoevaluación semanal con Sonnet y auditoría trimestral con Opus. Tope blando 12 €/mes (avisa, sigue publicando), tope duro 20 €/mes (corta, protección runaway).
- **Licencia:** MIT (código) + CC-BY 4.0 (contenido editorial).

## Qué hace

1. **Ingesta** por RSS: Google News + Diario de Ibiza + Periódico de Ibiza.
2. **Clasifica** cada noticia con Claude Haiku 4.5 (housing sí/no, actor, palanca).
3. **Genera** el informe con Claude Opus 4.7: 3-5 propuestas con actor responsable, coste estimado, precedente real y primer paso en ≤30 días.
4. **Publica** como Markdown en `docs/_editions/` y lo sirve por GitHub Pages. La home es un panel con la última edición desplegada (señales, propuestas, a vigilar); el archivo completo vive en `/ediciones/`.
5. **Audita** cada llamada en `data/costs.csv` + dashboard privado en `private/costs.md` (no servido por Jekyll).

## Puesta en marcha

Ya está en marcha. Los secrets necesarios están configurados en Settings → Secrets → Actions:

- `ANTHROPIC_API_KEY` — API de Anthropic. **[Configurado]**
- `TELEGRAM_BOT_TOKEN` — bot de alertas (`@ibiza_vivienda_bot`). **[Configurado]**
- `TELEGRAM_CHAT_ID` — chat personal para recibir alertas. **[Configurado]**

El workflow `weekly-report.yml` se dispara:
- Automáticamente cada lunes 05:00 UTC.
- Manualmente en Actions → Weekly report → Run workflow.

## Control de costes

Sistema de capas en euros (actualizado 2026-04-20 para absorber los 3 niveles de autoevaluación del pivote):

- **🟢 Verde (<6 €):** silencio.
- **🟡 Amarilla (6-9 €):** aviso por Telegram (FYI).
- **🟠 Naranja (9-12 €):** aviso por Telegram (atención).
- **🔴 Roja blanda (12-20 €):** aviso urgente por Telegram. **El pipeline sigue publicando**, no se pierde editorial por sobrecoste.
- **🚨 Roja dura (>20 €):** pipeline cortado + alerta crítica. Protección runaway contra bugs o bucles.

Editar `MONTHLY_SOFT_CAP_EUR` y `MONTHLY_HARD_CAP_EUR` en [`src/costs.py`](src/costs.py) para ajustar.

El histórico de cambios de umbrales vive en [`private/adjustments-log.md`](private/adjustments-log.md).

Dashboard privado en [`private/costs.md`](private/costs.md) (no se sirve en la web). Histórico completo en `data/costs.csv`.

## Ejecutar localmente

```bash
pip install -r requirements.txt
export ANTHROPIC_API_KEY=sk-ant-...
python -m src.report
```

Genera `docs/_editions/<YYYY>-w<WW>.md`, actualiza `docs/index.md` (panel de la última edición) y `private/costs.md` (dashboard privado), y registra el gasto en `data/costs.csv`. Al terminar (o si falla) envía resumen al bot de Telegram.

## Estructura

Ver [CLAUDE.md](CLAUDE.md) para detalles de arquitectura, decisiones y comandos. Ver [DIARIO.md](DIARIO.md) para el diario del proyecto.

**Roadmap activo (post-pivote):** [`ROADMAP.md`](ROADMAP.md) + documentos hermanos [`PIVOTE.md`](PIVOTE.md), [`ARQUITECTURA.md`](ARQUITECTURA.md), [`DISENO-WEB.md`](DISENO-WEB.md), [`SEO.md`](SEO.md), [`CONTENIDO-RETROACTIVO.md`](CONTENIDO-RETROACTIVO.md), [`DECISIONES-PENDIENTES.md`](DECISIONES-PENDIENTES.md). El antiguo [PLAN.md](PLAN.md) se conserva como referencia histórica.

## Aviso

**Modelo antiguo (en `main`):** las propuestas son sugerencias generadas por IA sobre prensa pública. No son análisis técnico ni asesoramiento jurídico, político o económico. Contrasta cifras con la fuente original antes de usarlas.

**Modelo nuevo (pivote, en branch):** el observatorio ya no genera propuestas propias. Documenta propuestas reales de actores identificables con URL a la fuente primaria. Política editorial con 5 reglas duras en `/politica-editorial` tras lanzamiento. Ver [`PIVOTE.md`](PIVOTE.md).
