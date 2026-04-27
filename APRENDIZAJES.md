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

- [ ] **Heredar tipología de actor entre ediciones.** Si un actor ya fue clasificado en semanas anteriores, el generador debe mantener esa tipología salvo nota explícita de cambio. *(Origen: detectado al ver "Marí" como `otro` en W18 vs `institucional_publico` en W17.)*
- [ ] **Cerrar items de "a vigilar" de la edición previa.** Si la edición anterior listó algo a vigilar y esta semana no hay novedad, el generador debe insertar línea explícita "Sin novedad registrada esta semana" en Señales o en Omisiones. *(Origen: el desalojo de Can Misses W17 desapareció sin trazo en W18.)*
- [ ] **Marcar fuentes agregadas cuando no haya primaria.** Si la URL de una propuesta apunta a un agregador (MSN, Google News) en lugar de la cabecera original, el generador debe etiquetarlo *(fuente agregada — sin primaria localizada)*. *(Origen: propuesta de "25M para vivienda pública municipal" enlazó MSN en lugar de Govern Balear.)*

### Warnings concretos (esta edición)

Solo trazabilidad. No ascienden a regla salvo que se repitan.

- [W18] Marí en `actors_cited` y `blocks_cited` como `otro` cuando W17 lo clasificó como `institucional_publico`.
- [W18] "Trabajador desalojado" sale en el cuerpo pero no en `actors_cited` del frontmatter.
- [W18] `blocks_cited` solo incluye 3 tipos (sindicato, institucional_publico, otro). Falta `tercer_sector` aunque Cáritas se menciona en ediciones recientes.
- [W18] Vigilancia de Can Misses (W17) sin cierre explícito en W18.
- [W18] Bloque `auditor` ausente del payload del self-review. Causa identificada: bug del commit-back que no incluía `data/audit/`. **Arreglado en este commit; se cerrará solo en W19.**
- [W18] Inconsistencia: el self-review original dio rigor=5 al primer pase y rigor=8 al segundo (no determinismo del modelo). **Mitigado con `temperature=0` en este commit; se valida en W19.**

---

## Próximas revisiones programadas

- **2026-06-08 (lunes):** revisar política de alerta del self-review tras 4-6 ediciones con datos reales. Decisión D17 en [DECISIONES.md](DECISIONES.md). Aviso automático vía `decisions_watch.py`.
