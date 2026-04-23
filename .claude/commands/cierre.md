---
description: Cierra la sesión con checklist fijo — actualiza docs, commit atómico y push
---

Estás cerrando una sesión de trabajo en `ibiza-housing-radar`. Ejecuta este checklist **en orden**, sin saltarte pasos. Al final da un reporte corto al editor.

## 1. Inventario de cambios

- `git status` + `git diff --stat` para ver qué se tocó en disco.
- Repaso mental de la conversación: ¿hubo decisiones, feedback del editor, hitos, acuerdos o cambios de rumbo que se hablaron pero NO se han escrito a ningún archivo?

## 2. Auditoría cruzada de docs vivos

Revisa uno a uno y decide si tocar. No tocar por tocar; tocar si hay algo nuevo que reflejar.

| Documento | Tocar si… |
|---|---|
| `DIARIO.md` | Hubo hito, decisión, fix estructural, cambio de rumbo, feedback del editor o aprendizaje relevante. Cabecera `## YYYY-MM-DD [tema]` obligatoria ([D0](../../DECISIONES.md)). Temas: `[pipeline]`, `[diseno]`, `[editorial]`, `[arquitectura]`, `[docs]`, `[costes]`, `[legal]`, `[feedback]`, `[sesion]`. |
| `STATUS.md` | Cambió lo activo/pausado/en curso, se cerró o abrió un hito, cambió el próximo hito operativo. **Mantener ≤ 100 líneas.** |
| `DECISIONES.md` | Se tomó cualquier decisión nueva en la sesión. Fila nueva con ID `D{N}` correlativo. Otros docs que la referencien usan el ID, no duplican contenido. |
| `ROADMAP.md` | Se cerró una tarea, se añadió una nueva, cambió el orden o la fase de algo. |
| `CLAUDE.md` (proyecto) | Hubo decisión estructural durable (stack, convención, regla "qué NO hacer", contrato de arranque). Raro. |
| Memoria `.claude/projects/.../memory/` | Hubo feedback nuevo del editor sobre cómo trabajar, o decisión reutilizable que merece persistir entre sesiones. Actualizar `MEMORY.md` índice si se añade archivo. |
| Estudios activos (`ESTUDIO-*.md`, `REVISION-FASE-0.5.md`) | La sesión avanzó, cerró o cambió el contenido de ese estudio en concreto. |

**Regla:** si dudas si tocar un doc, pregunta al editor antes de editarlo. No ejecutes ediciones dudosas por tu cuenta (regla `feedback_esperar_ok_antes_de_editar.md`).

## 3. Commits atómicos

- Un commit por cambio lógico. No bundles.
- Formato: `tipo(ámbito): descripción en español`. Tipos: `docs`, `feat`, `fix`, `config`, `refactor`, `chore`, `pipeline`, `report`.
- Co-author: `Co-Authored-By: Claude Opus 4.7 <noreply@anthropic.com>`.
- Nunca `git add -A` ciego; añade archivos explícitos.
- Nunca `--no-verify`.

## 4. Push

- `git push` si hay remoto y hay commits locales. Si falla por divergencia, `git pull --rebase` y vuelve a empujar. No force-push.

## 5. Reporte final al editor

Formato corto (viñetas, sin adornos):

- **Archivos tocados:** lista.
- **Commits creados:** N commits, primera línea de cada uno.
- **Push:** OK / no aplicable / falló (con motivo).
- **NO toqué:** docs que podrían haber necesitado actualización pero no toqué + razón en una línea. Esto sirve para que el editor detecte omisiones.
- **Dudas abiertas:** si hubo algo que no supe resolver solo.

## Reglas duras

- Si en cualquier paso detectas que falta contexto o hay una decisión que el editor no ha aprobado explícitamente, **PARA y pregunta**. No improvises.
- No marques tareas del ROADMAP como completadas si no hubo OK explícito del editor en la sesión.
- Si el DIARIO se acerca a 150 KB, avisa al editor en el reporte: toca considerar el troceo diferido (ver `ESTUDIO-GESTION-CONOCIMIENTO.md §3.3`).
