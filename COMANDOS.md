# Comandos — Radar Ibiza

Índice de los slash commands disponibles en este proyecto. Si un comando no aparece aquí, no existe.

## Del proyecto

Viven en [`.claude/commands/`](.claude/commands/) dentro de este repo.

| Comando | Cuándo usarlo | Archivo |
|---|---|---|
| `/arranque` | Inicio de sesión con informe ligero. Lee STATUS + DECISIONES + últimas entradas del diario, entrega síntesis de ~200 palabras + 1-3 recomendaciones + pregunta *"¿qué hacemos?"*. **Solo cuando el editor lo pide explícitamente.** Sin comando, el modo por defecto lee los mismos docs en silencio y responde directo al prompt. | [arranque.md](.claude/commands/arranque.md) |
| `/arranque-auditoria` | Auditorías estructurales, refactors grandes, decisiones de pivote o bloqueos por falta de mapa global. Escaneo profundo — estudios + código + fundacionales. Incluye 1-3 recomendaciones de alcance antes del cierre. | [arranque-auditoria.md](.claude/commands/arranque-auditoria.md) |
| `/arranque-total` | Escaneo completo del proyecto sin huecos. Al arrancar hace inventario silencioso, contrasta con el mapa conocido, lee cabeceras solo de archivos nuevos o raros, propone exclusiones razonadas para que el editor confirme en una línea, y entonces lee todo lo acordado en profundidad. Uso escaso (2-3 veces al año). | [arranque-total.md](.claude/commands/arranque-total.md) |
| `/ampliar [área o descripción]` | Carga documentos de un área concreta del proyecto sin sacar informe. Transversal — usable tras cualquier arranque para subir de nivel sin repetir síntesis, o como carga puntual al empezar. Dos formas: palabra clave (*diseño*, *auditor*, *tiers*, *legal*…) o descripción libre. | [ampliar.md](.claude/commands/ampliar.md) |
| `/cierre` | Cierre de sesión con checklist fijo: auditoría de cambios, actualización de docs vivos, commits atómicos, push y reporte. | [cierre.md](.claude/commands/cierre.md) |

## Globales (fuera del proyecto)

Viven en `~/.claude/commands/` y aplican a todos los proyectos.

| Comando | Para qué |
|---|---|
| `/nuevo-proyecto` | Scaffolding guiado de proyecto nuevo en `~/Documents/GitHub/`: cuestionario + repo privado en GitHub + CLAUDE.md + README.md + .gitignore + docs inicial. |
| `/actualizar-plantilla` | Edita la plantilla maestra en `~/Documents/GitHub/.claude-template/` y opcionalmente propaga el cambio a proyectos existentes. |

## Criterio de arranque

Cuatro modos de arranque + un comando transversal. Usa el mínimo que cubra la sesión:

- **Sin comando (default, desde 2026-04-24).** Al abrir sesión sin invocar nada, el asistente lee los tres documentos clave (estado + decisiones + diario reciente) en silencio y responde directo al prompt. Sin informe, sin recomendaciones, sin pregunta. Vale cuando el editor entra con una tarea ya definida.
- **`/arranque` → ligero.** Misma lectura que el modo por defecto, pero entrega informe de ~200 palabras + 1-3 recomendaciones + pregunta *"¿qué hacemos?"*. Úsalo cuando el editor pide panorámica antes de decidir.
- **`/arranque-auditoria` → profundo.** Auditoría, refactor grande, decisión de pivote o bloqueo por falta de mapa. Lee fundacionales + todos los estudios + código relevante. Incluye recomendaciones de alcance.
- **`/arranque-total` → completo, uso escaso.** Escaneo sin huecos de todo el proyecto. Al arrancar hace inventario silencioso y propone exclusiones razonadas para que el editor confirme. Reservado a 2-3 veces al año como mucho.

Y transversal:

- **`/ampliar [área o descripción]`.** Carga contexto adicional sobre un área concreta sin sacar informe. Sirve para subir de nivel tras un arranque ligero sin repetir síntesis, o como carga puntual al empezar. Dos formas: palabra clave (*diseño*, *auditor*, *tiers*, *costes*, *legal*, *pipeline*, *seo*, *contenido*, *modelos*, *docs*) o descripción libre.

Si el editor ha dicho la tarea y no cuadra con el modo que está en curso, el asistente propone escalar (o usar `/ampliar`) antes de ejecutar nada.

## Reglas para esta tabla

- **Todo comando del proyecto entra en esta tabla en el mismo commit en el que se crea.** Si el archivo en `.claude/commands/` existe y la tabla no lo cita, es un bug de mantenimiento.
- **Formato del archivo:** frontmatter con campo `description:` (una frase) + cuerpo Markdown con instrucciones imperativas en segunda persona. Ver [cierre.md](.claude/commands/cierre.md) como referencia.
- **Nombres en minúsculas con guion.** `arranque-total`, no `arranqueTotal` ni `ArranqueTotal`.
