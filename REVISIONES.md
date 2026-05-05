# REVISIONES — Radar Vivienda Ibiza

Registro narrativo de las **revisiones post-publicación** que el editor hace sobre las ediciones recién publicadas, normalmente disparadas por las alertas del self-review automático del lunes. Sirve para entender el viaje del observatorio: qué se observó, qué se debatió, qué se decidió y por qué, con detalle suficiente para volver atrás si la decisión envejece mal.

Las revisiones individuales viven en [`private/revisiones/`](private/revisiones/) (no servido por GitHub Pages). Este archivo raíz es solo el índice.

---

## Para qué sirve este registro

El observatorio nace en rodaje y cada lunes el self-review emite avisos sobre la edición recién publicada. Hasta que el sistema ruede solo, esas alertas obligan al editor a abrir conversación crítica con el asistente para decidir qué hacer: ¿corregir la edición?, ¿ajustar el prompt del generador?, ¿afinar las reglas del revisor?, ¿dejarlo pasar?

Esa conversación contiene material de mucho valor — alternativas evaluadas, motivos de cada decisión, opciones descartadas con razón explícita — que **no cabe en el DIARIO ni en APRENDIZAJES**:

- El **DIARIO** es entrada cronológica de hitos: refleja qué cambió, no por qué se llegó ahí.
- **APRENDIZAJES** es tabla de sugerencias del revisor automático con su estado (pendiente / aplicada / descartada): refleja la lección destilada, no el debate.
- **DECISIONES** registra decisiones canónicas con criterio de revocación, no la narrativa que llevó a ellas.

Las revisiones rellenan ese hueco. Una revisión es la **memoria viva del razonamiento**: si dentro de tres meses una decisión envejece mal y hay que revertirla, el archivo de revisión deja entender el contexto original sin tener que reconstruirlo de cero.

## Estructura de una revisión

Cada archivo sigue la plantilla:

```markdown
# Revisión 2026-WNN

- **Fecha:** YYYY-MM-DD
- **Disparador:** [alerta de self-review / lectura proactiva del editor / feedback externo]
- **Edición revisada:** /ediciones/YYYY-wNN/
- **Modelo activo durante la sesión:** opus | sonnet | haiku · effort

## Resumen ejecutivo

3-5 líneas que un lector futuro pueda leer en 15 segundos y entender la sesión.

## Diagnóstico de la edición

Lista de problemas detectados, con su gravedad y su origen (warning del revisor, observación humana, comparación con ediciones anteriores).

## Debate y alternativas

Núcleo del documento. Cómo se llegó a las decisiones. Qué alternativas se consideraron. Qué se descartó y por qué. Si hubo cambio de opinión a mitad del debate, dejarlo registrado.

## Decisiones tomadas

Lista numerada. Cada decisión con:
- Qué se decide
- Si abre entrada nueva en DECISIONES.md (D**N**) o queda dentro del paraguas de una decisión existente
- Si entra como sugerencia aplicada en APRENDIZAJES.md
- Commits asociados (hashes cortos al final)

## Cambios aplicados

Resumen operativo de los archivos tocados, agrupado por commit.

## Seguimiento

Qué hay que vigilar en próximas ediciones para validar o revocar las decisiones de esta sesión.

## Revisar si

Señales que romperían las decisiones de esta sesión y obligarían a reabrirla.
```

## Cuándo se crea una revisión

- **Siempre que dispare una alerta de self-review** (nota <7 en alguna dimensión) y la conversación con el editor produzca cambios o decisiones explícitas. Si la alerta se descarta sin más ("no procede acción"), no hace falta archivo: una nota de una línea en APRENDIZAJES basta.
- **Cuando el editor pida lectura proactiva** de una edición sin alerta automática y esa lectura genere debate sustantivo.
- **Cuando una observación externa (lector, periodista, actor citado)** obligue a debatir una corrección o un ajuste.

Revisiones triviales (correcciones de typos, fix de un enlace roto sin debate) no crean archivo: van directo al commit.

## Distinción con APRENDIZAJES.md

|  | APRENDIZAJES | REVISIONES |
|---|---|---|
| Origen del contenido | Sugerencias destiladas del revisor automático | Conversación humana sobre la edición |
| Granularidad | Una fila por sugerencia o warning recurrente | Un archivo por sesión de revisión |
| Estado | pendiente / aplicada / descartada / en seguimiento | narrativa cerrada (con seguimiento al final) |
| Lectura típica | "¿qué le toca al sistema cambiar este mes?" | "¿por qué decidimos esto en mayo?" |
| Tamaño | 1-3 líneas por entrada | 200-800 palabras por archivo |
| Vida útil | Hasta que la sugerencia se aplique o se descarte | Permanente (referencia histórica) |

Pueden cruzarse: si una revisión genera una lección que se traslada al generador, esa lección entra en APRENDIZAJES como sugerencia aplicada **con enlace al archivo de revisión** que la originó. La revisión es el origen, APRENDIZAJES el destino destilado.

## Reglas

- **Una revisión, un archivo.** Nombre `YYYY-wNN.md` (la edición que revisa) si va asociada a alerta semanal; si es revisión proactiva sin edición concreta, usar `YYYY-MM-DD-tema.md`.
- **Append-only.** No editar revisiones cerradas. Si una decisión se reabre meses después, abrir nueva revisión que cite la antigua.
- **Cierra con seguimiento.** Cada revisión termina con la lista de cosas a vigilar. Sin esa lista no se considera cerrada.
- **Cita commits y decisiones por ID.** Hashes cortos (7 caracteres) y D**N** literales para que el documento sea trazable.

## Índice

| Edición / Tema | Fecha | Disparador | Cambios aplicados | Archivo |
|---|---|---|---|---|
| W19 | 2026-05-05 | Alerta Telegram (rigor=5, balance=6) | 5 ajustes al sistema (4 commits) + correcciones a edición W19 (1 commit) | [`private/revisiones/2026-w19.md`](private/revisiones/2026-w19.md) |

---

*Última actualización: 2026-05-05.*
