---
description: Cierra sesión con checklist global + extras específicos de ibiza-housing-radar
---

**Hereda del global.** Lee y ejecuta `~/.claude/commands/cierre.md` completo, en orden, sin saltarte pasos. Después aplica los extras específicos de este proyecto descritos abajo.

## Extras específicos de `ibiza-housing-radar`

### Etiquetas DIARIO permitidas (paso 2)

El DIARIO de este proyecto solo admite estas etiquetas en la cabecera `## YYYY-MM-DD [tema]`:

`[pipeline]`, `[diseno]`, `[editorial]`, `[arquitectura]`, `[docs]`, `[costes]`, `[legal]`, `[feedback]`, `[sesion]` (cierre general).

### Docs vivos extra a auditar (paso 2)

Además de los del global, revisar:

| Documento | Tocar si… |
|---|---|
| Estudios activos (`ESTUDIO-*.md`, `REVISION-FASE-0.5.md`) | La sesión avanzó, cerró o cambió el contenido de ese estudio en concreto. |

### Tipo de commit extra (paso 3)

Además de los del global, este proyecto admite el tipo `report` para commits de ediciones semanales generadas por el pipeline.

### Aviso de tamaño de DIARIO (paso 5, en el reporte final)

Si `DIARIO.md` se acerca a 150 KB, avisar a Raúl en el reporte: toca considerar el troceo diferido (ver `ESTUDIO-GESTION-CONOCIMIENTO.md §3.3`).
