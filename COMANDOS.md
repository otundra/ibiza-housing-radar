# Comandos — Radar Ibiza

Índice de los slash commands disponibles en este proyecto. Si un comando no aparece aquí, no existe.

## Del proyecto

Viven en [`.claude/commands/`](.claude/commands/) dentro de este repo.

| Comando | Cuándo usarlo | Archivo |
|---|---|---|
| `/arranque` | Inicio de sesión con informe. Lee STATUS + DECISIONES + últimas entradas del diario, entrega síntesis de ~200 palabras + 1-3 recomendaciones de siguiente paso + pregunta *"¿qué hacemos?"*. **Solo cuando el editor lo pide explícitamente.** Sin comando, el modo por defecto lee los mismos docs en silencio y responde directo al prompt. | [arranque.md](.claude/commands/arranque.md) |
| `/arranque-fase` | Tras pausa de más de una semana, al cambiar de área (pipeline ↔ diseño ↔ editorial ↔ legal), o si la tarea toca un estudio grande. Añade PLAN + ARQUITECTURA + el estudio del área. Incluye 1-3 recomendaciones antes del cierre. | [arranque-fase.md](.claude/commands/arranque-fase.md) |
| `/arranque-auditoria` | Auditorías estructurales, refactors grandes, decisiones de pivote o bloqueos por falta de mapa global. Escaneo completo — caro en contexto. Incluye 1-3 recomendaciones de alcance antes del cierre. | [arranque-auditoria.md](.claude/commands/arranque-auditoria.md) |
| `/cierre` | Cierre de sesión con checklist fijo: auditoría de cambios, actualización de docs vivos, commits atómicos, push y reporte. | [cierre.md](.claude/commands/cierre.md) |

## Globales (fuera del proyecto)

Viven en `~/.claude/commands/` y aplican a todos los proyectos.

| Comando | Para qué |
|---|---|
| `/nuevo-proyecto` | Scaffolding guiado de proyecto nuevo en `~/Documents/GitHub/`: cuestionario + repo privado en GitHub + CLAUDE.md + README.md + .gitignore + docs inicial. |
| `/actualizar-plantilla` | Edita la plantilla maestra en `~/Documents/GitHub/.claude-template/` y opcionalmente propaga el cambio a proyectos existentes. |

## Criterio de arranque

Cuatro modos, en orden ascendente de contexto. Usa el mínimo que cubra la sesión:

- **Sin comando (default, desde 2026-04-24).** Al abrir sesión sin invocar nada, el asistente lee STATUS + DECISIONES + DIARIO (120 líneas) en silencio y responde directo al prompt del editor. Sin informe, sin recomendaciones, sin pregunta. Vale cuando el editor entra con una tarea ya definida.
- **Con `/arranque` explícito → Tier 1.** Misma lectura que el modo por defecto, pero entrega informe de ~200 palabras + 1-3 recomendaciones + pregunta *"¿qué hacemos?"*. Úsalo cuando el editor pide panorámica antes de decidir.
- **`/arranque-fase` → Tier 2.** Pausa larga o cambio de área. Añade plan y estudio del área sin escanear el resto. Incluye 1-3 recomendaciones antes del cierre.
- **`/arranque-auditoria` → Tier 3.** Auditoría o refactor grande. Lee toda la capa fundacional + estudios + código relevante. Solo cuando haga falta de verdad. Incluye 1-3 recomendaciones de alcance.

Si el editor ha dicho la tarea y no cuadra con el modo que está en curso, el asistente propone escalar antes de ejecutar nada.

## Reglas para esta tabla

- **Todo comando del proyecto entra en esta tabla en el mismo commit en el que se crea.** Si el archivo en `.claude/commands/` existe y la tabla no lo cita, es un bug de mantenimiento.
- **Formato del archivo:** frontmatter con campo `description:` (una frase) + cuerpo Markdown con instrucciones imperativas en segunda persona. Ver [cierre.md](.claude/commands/cierre.md) como referencia.
- **Nombres en minúsculas con guion.** `arranque-fase`, no `arranqueFase` ni `ArranqueFase`.
