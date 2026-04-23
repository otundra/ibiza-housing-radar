# Comandos — Radar Ibiza

Índice de los slash commands disponibles en este proyecto. Si un comando no aparece aquí, no existe.

## Del proyecto

Viven en [`.claude/commands/`](.claude/commands/) dentro de este repo.

| Comando | Cuándo usarlo | Archivo |
|---|---|---|
| `/arranque` | Inicio de cualquier sesión. Default. Lee STATUS + DECISIONES + últimas entradas del diario y devuelve síntesis de 200 palabras. | [arranque.md](.claude/commands/arranque.md) |
| `/arranque-fase` | Tras pausa de más de una semana, al cambiar de área (pipeline ↔ diseño ↔ editorial ↔ legal), o si la tarea toca un estudio grande. Añade PLAN + ARQUITECTURA + el estudio del área. | [arranque-fase.md](.claude/commands/arranque-fase.md) |
| `/arranque-auditoria` | Auditorías estructurales, refactors grandes, decisiones de pivote o bloqueos por falta de mapa global. Escaneo completo — caro en contexto. | [arranque-auditoria.md](.claude/commands/arranque-auditoria.md) |
| `/cierre` | Cierre de sesión con checklist fijo: auditoría de cambios, actualización de docs vivos, commits atómicos, push y reporte. | [cierre.md](.claude/commands/cierre.md) |

## Globales (fuera del proyecto)

Viven en `~/.claude/commands/` y aplican a todos los proyectos.

| Comando | Para qué |
|---|---|
| `/nuevo-proyecto` | Scaffolding guiado de proyecto nuevo en `~/Documents/GitHub/`: cuestionario + repo privado en GitHub + CLAUDE.md + README.md + .gitignore + docs inicial. |
| `/actualizar-plantilla` | Edita la plantilla maestra en `~/Documents/GitHub/.claude-template/` y opcionalmente propaga el cambio a proyectos existentes. |

## Criterio de arranque

Los tres `arranque*` son escalones. Usa el mínimo que cubra la sesión:

- **Default → `/arranque`.** Vale para el 80 % de sesiones: continuaciones, tareas pequeñas, preguntas de 1-3 turnos.
- **Pausa larga o cambio de área → `/arranque-fase`.** Añade plan y estudio del área sin escanear el resto.
- **Auditoría o refactor grande → `/arranque-auditoria`.** Lee toda la capa fundacional + estudios + código relevante. Solo cuando haga falta de verdad.

Si el editor ha dicho la tarea y no cuadra con el comando que ya se lanzó, el modelo propone escalar antes de ejecutar nada.

## Reglas para esta tabla

- **Todo comando del proyecto entra en esta tabla en el mismo commit en el que se crea.** Si el archivo en `.claude/commands/` existe y la tabla no lo cita, es un bug de mantenimiento.
- **Formato del archivo:** frontmatter con campo `description:` (una frase) + cuerpo Markdown con instrucciones imperativas en segunda persona. Ver [cierre.md](.claude/commands/cierre.md) como referencia.
- **Nombres en minúsculas con guion.** `arranque-fase`, no `arranqueFase` ni `ArranqueFase`.
