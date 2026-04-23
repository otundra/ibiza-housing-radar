# APRENDIZAJE — ibiza-housing-radar

Log experimental de feedback formativo sobre **cómo** el editor desarrolla este proyecto. Cada entrada es una observación concreta de una sesión, el patrón que refleja y una acción específica para la próxima vez.

Lo rellena Claude al final de cada sesión cuando ejecuta `/cierre` (Paso 6), **solo si hay algo concreto que anotar**. Si no hay, el reporte del cierre dice *"sin feedback hoy"* y no se añade entrada.

> ⚗️ **Experimental.** Solo en este proyecto, no en el resto. Si deja de aportar, se desactiva en 30 segundos (ver sección *"Cómo desactivar"*).

## Reglas

1. **Una entrada por cierre como máximo**, y solo si hay observación concreta. No inflar con generalidades.
2. **Formato fijo**:
   ```
   ## YYYY-MM-DD · [etiqueta]
   **Observación:** hecho concreto de la sesión.
   **Patrón:** qué tendencia refleja.
   **Mejor próxima vez:** acción específica.
   ```
3. **Etiquetas** sugeridas: `[alcance]`, `[decisión]`, `[docs]`, `[coste]`, `[proceso]`, `[comunicación]`, `[delegación]`, `[priorización]`, `[verificación]`.
4. **Reincidencia ≠ entrada nueva.** Si el patrón ya está anotado, añade una línea bajo la entrada existente: `— reincidencia YYYY-MM-DD: <1 línea>`. Esto mide si el aprendizaje se asienta o se repite.
5. **Sin adulación.** El feedback debe ser útil, concreto y crítico. Si no hay nada que aporte, no escribas. Mejor un cierre sin entrada que una entrada genérica.
6. **Revisión manual.** Cuando el editor lo pida, releer el archivo y destilar patrones recurrentes a una sección *"Principios"* al final.

## Cómo desactivar

Dos pasos, ~30 segundos:

1. `git rm APRENDIZAJE.md`
2. Quitar la sección `## 6. Feedback formativo` del `.claude/commands/cierre.md`.

Commit único: `chore(cierre): retira experimento de feedback formativo`.

## Entradas

<!-- Más reciente arriba. Primera entrada se añadirá en el próximo /cierre con feedback concreto. -->
