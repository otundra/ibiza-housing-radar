# Aprendizajes — Radar Vivienda Ibiza

Registro semanal de lo que el self-review propone y de los warnings que se repiten. Sirve para que el observatorio mejore semana a semana en lugar de tropezar dos veces con la misma piedra.

## Cómo funciona

1. **Cada lunes** el self-review (Sonnet 4.6) sugiere ajustes al prompt del generador y emite warnings sobre la edición publicada. Quedan en `private/self-review/{edicion}.md`.
2. **Al arrancar la siguiente sesión**, Claude revisa este archivo en silencio, cruza con el self-review nuevo y trae un informe corto al editor: *qué es nuevo, qué se ha aplicado, qué propone aplicar o descartar y por qué*.
3. **El editor decide.** Si está de acuerdo con la propuesta, Claude aplica y commitea citando la edición que originó el cambio. Si no, abrimos sesión específica para discutirlo.
4. **Las sugerencias aplicadas** mueven a estado *aplicada* con enlace al commit. Las descartadas con motivo. Las que siguen en curso, *en seguimiento*.

## Reglas

- **Una fila por sugerencia o warning recurrente.** Sugerencias del self-review entran como pendientes; warnings que aparezcan en 2+ ediciones consecutivas también.
- **Estados:** `[ ] pendiente` · `[x] aplicada` · `[~] descartada` · `[…] en seguimiento`.
- **Aplicada implica commit.** Sin commit que cite la edición de origen, no se marca como aplicada.
- **Warnings de una sola edición no entran aquí.** Solo en el archivo del self-review correspondiente. Si se repiten, ascienden a esta tabla.

---

## 2026-W18 (27 abril - 3 mayo 2026)

### Sugerencias del self-review

- [x] **Heredar tipología de actor entre ediciones.** Si un actor ya fue clasificado en semanas anteriores, el generador debe mantener esa tipología salvo nota explícita de cambio. *(Origen: detectado al ver "Marí" como `otro` en W18 vs `institucional_publico` en W17.)* **Aplicada el 2026-05-05** en commit `feat(generate): cerrar loop de aprendizaje W18+W19` con cambios en `src/generate.py`: prompt SYSTEM con regla "HERENCIA DE TIPOLOGÍA DE ACTOR" + nuevo INPUT 4 con la edición anterior + función `load_previous_edition()`.
- [x] **Cerrar items de "a vigilar" de la edición previa.** Si la edición anterior listó algo a vigilar y esta semana no hay novedad, el generador debe insertar línea explícita "Sin novedad registrada esta semana" en Señales o en Omisiones. *(Origen: el desalojo de Can Misses W17 desapareció sin trazo en W18.)* **Aplicada el 2026-05-05** en mismo commit con regla "CIERRE EXPLÍCITO DE A VIGILAR".
- [x] **Marcar fuentes agregadas cuando no haya primaria.** Si la URL de una propuesta apunta a un agregador (MSN, Google News) en lugar de la cabecera original, el generador debe etiquetarlo *(fuente agregada — sin primaria localizada)*. *(Origen: propuesta de "25M para vivienda pública municipal" enlazó MSN en lugar de Govern Balear.)* **Aplicada el 2026-05-05** en mismo commit con regla "FUENTE AGREGADA ETIQUETADA". Aplica a Señales detectadas, Cronología, Mapa de posiciones, Propuestas en circulación y Radar.

### Warnings concretos (esta edición)

Solo trazabilidad. No ascienden a regla salvo que se repitan.

- [W18] Marí en `actors_cited` y `blocks_cited` como `otro` cuando W17 lo clasificó como `institucional_publico`.
- [W18] "Trabajador desalojado" sale en el cuerpo pero no en `actors_cited` del frontmatter.
- [W18] `blocks_cited` solo incluye 3 tipos (sindicato, institucional_publico, otro). Falta `tercer_sector` aunque Cáritas se menciona en ediciones recientes.
- [W18] Vigilancia de Can Misses (W17) sin cierre explícito en W18.
- [W18] Bloque `auditor` ausente del payload del self-review. Causa identificada: bug del commit-back que no incluía `data/audit/`. **Arreglado en este commit; se cerrará solo en W19.**
- [W18] Inconsistencia: el self-review original dio rigor=5 al primer pase y rigor=8 al segundo (no determinismo del modelo). **Mitigado con `temperature=0` en este commit; se valida en W19.**

---

## 2026-W19 (4 - 10 mayo 2026)

### Sugerencias del self-review

- [x] **Aumentar n mínimo de propuestas auditadas a 2 por edición.** Con n=1 cualquier desacuerdo Haiku↔Sonnet da ratio=1.0 y dispara penalización obligatoria del rigor (artefacto, no señal). *(Origen: W19 con n=1 disputado obligó rigor=5 sin que el cuerpo lo justificara.)* **Aplicada de forma diferente el 2026-05-05** en commit `fix(self-review): no degradar rigor por disputas con muestra <3`: en lugar de exigir n≥2 al auditor (decisión que pertenece al diseño del auditor, no al revisor), se cambia la regla del revisor para que no penalice rigor cuando n<3. La señal sigue llegando como warning. Ver `src/self_review.py`.
- [x] **Añadir campo 'fuente_tipo' (primaria/agregador/periodística).** *(Origen: cifra "25M" de MSN sin marca de fuente agregada.)* **Aplicada de forma adyacente el 2026-05-05** en commit `feat(generate): cerrar loop de aprendizaje W18+W19`: la regla "FUENTE AGREGADA ETIQUETADA" del prompt del generador cubre el caso desde el lado del cuerpo (etiqueta inline visible). El campo estructurado en `extract.py` se difiere — coste/beneficio favorable al etiquetado inline porque ya cubre la auditoría del revisor con la nueva dimensión "trazabilidad" (D22).
- [x] **Generar `actors_cited` y `blocks_cited` al final, tras el cuerpo.** *(Origen: incoherencia metadata/cuerpo en W18 y W19 — Burón en mapa pero no en frontmatter, blocks_cited incompleto.)* **Aplicada el 2026-05-05** en mismo commit con regla "FRONTMATTER GENERADO AL FINAL".

### Warnings concretos (esta edición)

- [W19] Cifra "25M para vivienda pública municipal" enlazó MSN, no fuente primaria del Govern. *(Repetición del W18; ascendido a sugerencia aplicada arriba.)*
- [W19] Cifra "30 veces más cara" sin metodología declarada ni fuente estadística oficial.
- [W19] Actor "Mateo (concejal)" sin municipio ni partido. **Promovido a sugerencia aplicada** como regla "IDENTIFICACIÓN DE CARGOS PÚBLICOS" en el prompt del generador (commit del 2026-05-05). Versión refinada: trabajar con lo que la fuente da y etiquetar visiblemente los huecos, sin completar con info posterior.
- [W19] Burón en el mapa de posiciones con URL pero ausente de `actors_cited`. *(Cubierto por la regla "FRONTMATTER GENERADO AL FINAL".)*
- [W19] `blocks_cited` solo recoge 2 tipos cuando aparecen 5 actor_types en el cuerpo. *(Mismo cubrimiento.)*
- [W19] Drone vigilancia descartada como propuesta habitacional pero presente en la tabla del Mapa de posiciones. *(No regla nueva — ambigüedad puntual; corregida en la edición W19 bajo D21.)*
- [W19] Ausencia de voz sindical local o patronal frente a testimonios de temporeros. *(Es omisión, no error; queda en seguimiento — si se repite en W20-W21 asciende a sugerencia.)*

---

## Seguimiento

- **Claridad como dimensión muerta** (en seguimiento desde 2026-05-05). Tres semanas (W17, W18, W19) dando 9/10 sin warning concreto. La nueva dimensión "trazabilidad" entra en W20 como sexta. Si tras W20-W21 claridad sigue dando 9/10 sin warnings concretos, se propondrá retirarla y consolidar en cinco dimensiones útiles (reglas, rigor, balance, cobertura, trazabilidad). Si en algún punto baja, se mantiene. Decisión asociada: [D22](DECISIONES.md#d22--trazabilidad-de-fuente-como-sexta-dimensión-del-self-review).

---

## Próximas revisiones programadas

- **2026-06-08 (lunes):** revisar política de alerta del self-review tras 4-6 ediciones con datos reales. Decisión D17 en [DECISIONES.md](DECISIONES.md). Aviso automático vía `decisions_watch.py`.
- **Tras W23 (semana del 1-7 junio 2026):** revisar trazabilidad como dimensión propia tras 4 ediciones (W20-W23). Decisión D22.
