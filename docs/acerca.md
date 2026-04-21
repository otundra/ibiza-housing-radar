---
layout: page
title: Acerca
permalink: /acerca/
---

> ⚠️ **Página en reescritura.** Desde el 2026-04-21 el proyecto funciona bajo modelo documental: el LLM no genera propuestas propias, documenta las que actores con nombre formulan cada semana con URL verificable. Los números de esta página están al día (coste proyectado ~6-7 €/mes, tope blando 12 €/mes, tope duro 50 €/mes); el texto conceptual se reescribe en breve.

## Qué es esto

**Ibiza Housing Radar** es un observatorio automatizado sobre la crisis de vivienda en Ibiza, con foco en los trabajadores de temporada que cada año se ven empujados a caravanas, sofás compartidos o a renunciar a la isla directamente.

Cada lunes a las 7:00 de la mañana (CEST), un pipeline lee la prensa local de los últimos 10 días, filtra lo relevante, y produce un informe con:

1. **Señales detectadas** — los hechos enlazados a la fuente original.
2. **Lectura** — qué cambia esta semana y dónde está la ventana de decisión.
3. **Propuestas accionables** — con actor responsable, coste estimado, precedente real en otra ciudad, y primer paso ejecutable en menos de 30 días.
4. **A vigilar** — fechas, decisiones y eventos pendientes concretos.

## Cómo funciona

| Fase | Herramienta | Coste |
|---|---|---|
| Ingesta | Feeds RSS de Google News + Diario de Ibiza + Periódico de Ibiza | 0 € |
| Clasificación | Claude Haiku 4.5 (Anthropic) | ~0,01 €/semana |
| Generación del informe | Claude Opus 4.7 (Anthropic) | ~0,50 €/semana |
| Publicación | GitHub Pages (Jekyll) | 0 € |
| Scheduler | GitHub Actions (cron semanal) | 0 € |
| **Total proyectado** | | **~6-7 €/mes** |

Todo el código es abierto y está en [github.com/otundra/ibiza-housing-radar](https://github.com/otundra/ibiza-housing-radar). El pipeline tiene topes de gasto automáticos (tope blando 12 €/mes con aviso, tope duro 50 €/mes con corte por protección runaway).

## Qué NO es

- **No es una fuente primaria.** Resume y enlaza. Si una cifra importa, contrasta con la noticia original.
- **No es análisis técnico.** Las propuestas son sugerencias generadas por IA sobre prensa pública. Un análisis real de vivienda necesita datos de catastro, padrón y registros que este sistema no tiene.
- **No es asesoramiento jurídico, político ni económico.**
- **No pretende reemplazar al periodismo local.** Al contrario: depende de él. Si quieres que esto siga existiendo, suscríbete a los diarios que producen la información original.

## Por qué Ibiza

Porque 1.200 personas estaban en infravivienda según el último censo de Cruz Roja, una habitación se alquila por 2.100 €/mes, y cada año la temporada empieza con trabajadores durmiendo en coches. Con ese stock de datos, las ideas no escasean — escasea el canal que las conecte con quien decide.

## Quién lo mantiene

Raúl Serrano ([@otundra](https://github.com/otundra)). Proyecto experimental, sin ánimo de lucro, sin anuncios, sin tracking.

¿Propuestas, correcciones o una noticia que deberíamos cubrir? Abre un [issue en GitHub](https://github.com/otundra/ibiza-housing-radar/issues).
