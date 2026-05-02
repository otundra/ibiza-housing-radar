# Comandos — Radar Ibiza

Índice de los slash commands disponibles en este proyecto. Si un comando no aparece aquí, no existe.

## Del proyecto

Viven en [`.claude/commands/`](.claude/commands/) dentro de este repo.

| Comando | Cuándo usarlo | Archivo |
|---|---|---|
| `/cierre` | Cierre de sesión con checklist fijo. **Hereda del global** y añade extras específicos de ibiza (etiquetas DIARIO con corchetes específicas del dominio, audita estudios `ESTUDIO-*.md`, tipo de commit `report`, aviso DIARIO >150 KB). | [cierre.md](.claude/commands/cierre.md) |

## Globales (fuera del proyecto)

Viven en `~/.claude/commands/` y aplican a todos los proyectos. Documentados en `~/.claude/CLAUDE.md` sección *Comandos globales de sesión*.

| Comando | Para qué |
|---|---|
| `/arranque` | Tier 1: contexto base + chequeo git + reporte 250 palabras + 1 recomendación. |
| `/arranque-auditoria` | Tier 2: Tier 1 + carga TODOS los docs vivos del inventario del proyecto + reporte ampliado 600-900 palabras + 1-3 recomendaciones. |
| `/arranque-total` | Tier 3: Tier 2 + capa de código (src/, configs, workflows) + reporte exhaustivo. Uso escaso. |
| `/estado` | Chequeo situacional a media sesión. |
| `/cierre` | Cierre con checklist (ver versión local arriba que hereda y extiende). |
| `/ayuda` | Lista todos los comandos disponibles. |
| `/nuevo-proyecto` | Scaffolding guiado de proyecto nuevo. |
| `/actualizar-plantilla` | Edita la plantilla maestra. |
| `/poda`, `/modelo`, `/menos-tecnico` | Mantenimiento, modelo y reescritura. |

## Criterio de arranque

Cuatro niveles del sistema de arranque global, escalables. Usa el mínimo que cubra la sesión:

- **Tier 0 — Sin comando (default).** Al abrir sesión sin invocar nada, lectura silenciosa del contexto base + respuesta directa al prompt. Sin informe.
- **Tier 1 — `/arranque`.** Lectura base + informe de 250 palabras + 1 recomendación. Cuando pides panorámica.
- **Tier 2 — `/arranque-auditoria`.** Carga el inventario completo de docs vivos del proyecto (en ibiza: fundacionales + todos los `ESTUDIO-*.md` + DECISIONES + STATUS + sub-roadmaps + etc., menos exclusiones Jekyll declaradas). Informe ampliado.
- **Tier 3 — `/arranque-total`.** Tier 2 + código (`src/`, `docs/_layouts/`, `docs/_includes/`, `docs/assets/css/`) + configs (`.github/workflows/`, `requirements.txt`). Reservado a pivotes o reescrituras.

Si el editor ha dicho la tarea y no cuadra con el tier en curso, el asistente propone escalar antes de ejecutar nada.

## Histórico

Hasta 2026-05-02 este proyecto tenía locales propios para `/arranque`, `/arranque-auditoria`, `/arranque-total` y `/ampliar`. Se borraron al unificar el sistema en globales que usan el inventario de docs vivos del `/cierre`. El local de `/cierre` se mantiene porque añade extras específicos del proyecto (etiquetas DIARIO temáticas, estudios, tipo de commit `report`, aviso de tamaño DIARIO).

`/ampliar` se borró sin reemplazo porque no se invocaba en la práctica. Si en el futuro hace falta cargar contexto adicional puntual, basta con pedir Read directo sobre los archivos relevantes.

## Reglas para esta tabla

- **Todo comando del proyecto entra en esta tabla en el mismo commit en el que se crea.** Si el archivo en `.claude/commands/` existe y la tabla no lo cita, es un bug de mantenimiento.
- **Formato del archivo:** frontmatter con campo `description:` (una frase) + cuerpo Markdown con instrucciones imperativas en segunda persona. Ver [cierre.md](.claude/commands/cierre.md) como referencia.
- **Nombres en minúsculas con guion.** `arranque-total`, no `arranqueTotal` ni `ArranqueTotal`.
