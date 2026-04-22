# Experimento con Claude Design — archivo para estudio en fase de Diseño

**Fecha de recepción:** 2026-04-22
**Origen:** experimento del editor con la herramienta Claude Design.
**Estado:** archivado, **no es referencia de nada** hasta que el editor lo indique explícitamente.

## Aviso importante

El editor envió este paquete con una condición clara: **no tomarlo como referencia activa** de diseño hasta que se retome la fase de Diseño (pausada desde el 2026-04-21).

Hay cosas visuales que al editor le gustaron, pero:

- Usa **datos antiguos** (pre-pivote documental).
- **No tiene en cuenta** ninguna de las decisiones ya cerradas (D1-D13 del estudio de diseño, reglas duras del observatorio, taxonomía de 8 actores cerrada con candado, calendario editorial con opening/closing, regla de partidos en gris neutro, nombre `radar))ibiza_vivienda`, split acerca/metodo previsto, etc.).
- Es un **experimento de exploración**, no un entregable validado.

## Cuándo se estudia

En la fase de Diseño del roadmap V2 (Fase 4 del `ROADMAP.md`), tarea **RT16** de la revisión fundacional.

Proceso previsto cuando toque:

1. Claude Code abre este paquete.
2. Compara contra [`ESTUDIO-DISENO.md`](../../ESTUDIO-DISENO.md) (D1-D13 cerradas).
3. Identifica qué elementos visuales del experimento pueden incorporarse como evolución.
4. Marca qué no encaja con las reglas ya fijadas (taxonomía cerrada, partidos en gris, 5 reglas duras, modelo documental).
5. Presenta propuesta de integración al editor para decisión.

Hasta entonces: **archivo pasivo**. No se toca, no se hace referencia cruzada, no se usa como inspiración para trabajo activo.

## Contenido

- HTML pages: `Ibiza Housing Radar.html`, `actor.html`, `balance.html`, `como-usarlo.html`, `edicion.html`, `ediciones.html`, `politica-editorial.html`, `propuesta.html`, `recursos.html`.
- Componentes JSX: `app.jsx`, `components.jsx`, `design-canvas.jsx`, `mobile.jsx`, `page-shell.jsx`, `pages.jsx`, `variant-a.jsx`, `variant-b.jsx`, `variant-c.jsx`, `variant-d.jsx`.
- Estilos: `system.css`.
- Datos de ejemplo: `data.js` (datos antiguos, pre-pivote).
- Prompt de diseño: `uploads/PROMPT-DISENO-IA.md`.

## Ubicación en el repo

`private/claude-design-experiment/` — fuera del sitio Jekyll público. No se sirve en la web, no indexa, no se referencia desde ningún documento activo salvo el propio `REVISION-FASE-0.5.md` en la tarea RT16.
