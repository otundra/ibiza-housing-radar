# Ibiza Housing Radar

Observatorio automatizado de noticias sobre la crisis de vivienda en Ibiza, centrado en trabajadores de temporada (mayo-octubre). Cada lunes genera un informe con propuestas accionables enlazadas a las noticias que las motivan.

- **Web pública:** https://otundra.github.io/ibiza-housing-radar/ *(activa tras primer deploy)*
- **Cadencia:** informe semanal, lunes 07:00 Europe/Madrid
- **Stack:** Python + Anthropic API (Claude) + GitHub Actions + GitHub Pages
- **Coste:** 0 € de infra; consumo API Anthropic ~céntimos/semana
- **Licencia:** MIT

## Qué hace

1. Ingesta por RSS: Diario de Ibiza, Periódico de Ibiza, Nou Diari, Ara Balears, BOIB.
2. Clasifica cada noticia (housing sí/no, actor, palanca) con Claude Haiku.
3. Genera informe semanal con Claude Opus: 3-5 propuestas con actor responsable, coste estimado, precedente y primer paso ejecutable.
4. Publica como Markdown en `docs/` y lo sirve por GitHub Pages.

## Configuración mínima

Al crear el repo hay que añadir un secret:

- `ANTHROPIC_API_KEY` en **Settings → Secrets and variables → Actions → New repository secret**

Sin ese secret, el workflow semanal falla pero la web sigue publicando las ediciones anteriores.

## Estado

Ver [CLAUDE.md](CLAUDE.md) para el estado del proyecto, decisiones, y próximos pasos.
