# Ibiza Housing Radar

Observatorio semanal de la crisis de vivienda en Ibiza, con foco en trabajadores de temporada (mayo-octubre). Cada lunes genera un informe con las señales de la semana, mapa de posiciones de los actores y propuestas reales documentadas con fuente verificable.

> 🧭 **Modelo activo: observatorio documental** (desde el 2026-04-21, merge a `main`). El LLM no genera propuestas propias; documenta las que actores con nombre formulan cada semana, con URL verificable. Detalle en [`CLAUDE.md`](CLAUDE.md#reglas-fundacionales) y [`ROADMAP.md`](ROADMAP.md).

- **Web pública:** <https://otundra.github.io/ibiza-housing-radar/>
- **Cadencia:** informe semanal, lunes 07:00 CEST (05:00 UTC)
- **Stack:** Python 3.12 + Anthropic API (Claude Haiku 4.5 + Sonnet 4.6 + Opus 4.7) + GitHub Actions + GitHub Pages
- **Coste:** 0 € de infraestructura; API ~6-7 €/mes proyectado (pipeline + autoevaluación semanal + auditoría trimestral). Proyección revisable cuando haya 3 meses de datos reales en `data/costs.csv`. Tope blando 12 €/mes (avisa, sigue publicando), tope duro 50 €/mes (corta, protección runaway).
- **Licencia:** MIT (código) + CC-BY 4.0 (contenido editorial).

## Qué hace

1. **Ingesta** por RSS: Google News + Diario de Ibiza + Periódico de Ibiza.
2. **Clasifica** cada noticia con Claude Haiku 4.5 (housing sí/no, actor, palanca, si contiene propuesta explícita).
3. **Extrae** la ficha estructurada de cada propuesta detectada con Haiku + validador Sonnet (actor, URL fuente, estado, viabilidad, verbatim).
4. **Verifica** que cada URL responde, que el actor está trazable y que no aparecen verbos prohibidos (`debería`, `urge`, `proponemos`, etc.).
5. **Compone** la edición semanal con Claude Opus 4.7 a partir del material ya verificado. El Opus no genera propuestas, solo ordena y redacta.
6. **Publica** como Markdown en `docs/_editions/` y lo sirve por GitHub Pages. La home es un panel con la última edición desplegada; el archivo completo vive en `/ediciones/`.
7. **Audita** cada llamada en `data/costs.csv` + dashboard privado en `private/costs.md` (no servido por Jekyll). Archivo append-only por ejecución en `data/archive/YYYY-WNN/`.

## Puesta en marcha

Ya está en marcha. Los secrets necesarios están configurados en Settings → Secrets → Actions:

- `ANTHROPIC_API_KEY` — API de Anthropic. **[Configurado]**
- `TELEGRAM_BOT_TOKEN` — bot de alertas (`@ibiza_vivienda_bot`). **[Configurado]**
- `TELEGRAM_CHAT_ID` — chat personal para recibir alertas. **[Configurado]**

El workflow `weekly-report.yml` se dispara:
- Automáticamente cada lunes 05:00 UTC.
- Manualmente en Actions → Weekly report → Run workflow.

## Control de costes

Sistema de capas en euros (actualizado 2026-04-20 para absorber los 3 niveles de autoevaluación):

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

**Roadmap activo:** [`ROADMAP.md`](ROADMAP.md) (estructura V2 en 7 fases ejecutables) + documentos hermanos [`ARQUITECTURA.md`](ARQUITECTURA.md), [`DISENO-WEB.md`](DISENO-WEB.md), [`SEO.md`](SEO.md), [`CONTENIDO-RETROACTIVO.md`](CONTENIDO-RETROACTIVO.md), [`DECISIONES-PENDIENTES.md`](DECISIONES-PENDIENTES.md), [`REVISION-FASE-0.5.md`](REVISION-FASE-0.5.md). El antiguo [PLAN.md](PLAN.md) se conserva como referencia histórica.

## Aviso

El observatorio no genera propuestas propias. Documenta propuestas reales de actores identificables con URL a la fuente primaria. Política editorial con 5 reglas duras en `/politica-editorial` tras el relanzamiento público. Ver [`CLAUDE.md`](CLAUDE.md#reglas-fundacionales).
