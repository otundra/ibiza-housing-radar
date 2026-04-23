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

<!-- Más reciente arriba. -->

## 2026-04-23 · [comunicación]

**Observación:** el editor me corrigió 2026-04-23 por usar identificadores internos (`PI2-A`, `RT14`, `RT5`, `RT15`, `PI9`, `D1`, etc.) en la conversación, cuando ya existe desde hace días una memoria específica que lo prohíbe (`feedback_referencias_con_contexto.md`). Cita literal: *"lo he dicho varias veces y no lo estás aplicando"*. Me obligó a rehacer la respuesta entera.

**Patrón:** tener una regla guardada en memoria no garantiza que se aplique en el momento. El consumo pasivo de memoria al inicio de la respuesta no basta; tiendo a filtrar por *"lo que parece relevante para el contenido"* y dejo fuera reglas de estilo comunicativo, que aplican transversalmente a cualquier respuesta. Reincidencia directa sobre memoria explícita.

**Mejor próxima vez:** antes de redactar cualquier respuesta larga en este proyecto, pasar un filtro explícito por las memorias `feedback_*` de estilo de comunicación (especialmente `feedback_referencias_con_contexto.md` y `feedback_lenguaje_llano_publico.md`). Revisar lo escrito una vez antes de enviar buscando códigos internos sin glosar y tecnicismos en copy público. Tratar esas reglas como constantes de formato, no como sugerencias contextuales.

## 2026-04-23 · [proceso]

**Observación:** propuse de entrada un sistema con alcance triple (global `~/.claude/` + plantilla + los 4 proyectos del usuario) y la ruta de desactivación no estaba en la propuesta. El editor redujo a solo-ibiza y pidió explícitamente *"que sea fácil de quitar si no quiero más"* antes de aprobar. Me obligó a revertir lo que ya había aplicado en global y en la plantilla.

**Patrón:** el editor impone **reversibilidad explícita + alcance mínimo** como prerrequisitos de cualquier experimento operativo, no como características opcionales. Aprobar → ejecutar requiere ambas por defecto. Ya hay memorias previas que apuntan en esa dirección (`feedback_alcance_proyecto.md`, `feedback_esperar_demanda_organica.md`), pero sobreestimé la apetencia por escalar y subestimé el coste de "deshacer".

**Mejor próxima vez:** al proponer un sistema o proceso nuevo, desde la **primera** iteración incluir tres cosas sin que lo pida: (1) alcance más conservador que aún funcione (un solo proyecto, un solo archivo, un solo hook); (2) sección *"Cómo desactivar"* con pasos numerados concretos y commit de reversión literal; (3) la ruta de escalado como **opción B condicionada** a OK explícito, no como plan A. Ahorra una ronda entera de turnos y evita commits que luego hay que revertir.
