# DECISIONES — Radar Vivienda Ibiza

Registro **append-only** de decisiones del proyecto. Fuente única desde 2026-04-23.

## Reglas

1. **Una fila por decisión.** Nunca editar una fila cerrada; si cambia algo, añadir una nueva decisión que la reemplace y marcar la antigua como `superada_por: DXX`.
2. **ID correlativo `D0`, `D1`, `D2`…** Sin huecos, sin reutilizar.
3. **Decisión nueva entra aquí primero.** Otros docs referencian por ID (ej. *"ver [D7]"*), no duplican el contenido.
4. **Migración histórica pendiente.** D1-D13 de `ESTUDIO-DISENO.md` y las 16 de `DECISIONES-PENDIENTES.md` se moverán aquí durante la revisión profunda post-lanzamiento (ver `ESTUDIO-GESTION-CONOCIMIENTO.md` §3.4). Hasta entonces, ambos docs siguen siendo fuentes válidas de sus decisiones propias.

## Formato de fila

```
### D{N} — {título corto}
- **Fecha:** YYYY-MM-DD
- **Tema:** {pipeline | diseno | editorial | arquitectura | docs | costes | legal | otro}
- **Decisión:** {qué se decide, en una frase}
- **Por qué:** {motivo en 1-3 líneas}
- **Docs afectados:** {lista de archivos}
- **Estado:** vigente | superada_por:DXX | revocada
```

---

## Decisiones

### D0 — Adoptar tres reglas baratas de gestión documental

- **Fecha:** 2026-04-23
- **Tema:** docs
- **Decisión:** (1) DIARIO con fecha ISO y etiqueta temática en cada entrada; (2) DECISIONES.md como fuente única para decisiones nuevas a partir de hoy; (3) STATUS.md reducido a ≤100 líneas.
- **Por qué:** frenar entropía documental sin ejecutar la reorganización completa (ver `ESTUDIO-GESTION-CONOCIMIENTO.md`), que se deja para después del lanzamiento. Las reglas son baratas, reversibles y no rompen enlaces existentes.
- **Docs afectados:** `CLAUDE.md`, `DIARIO.md`, `STATUS.md`, `DECISIONES.md` (nuevo), `ESTUDIO-GESTION-CONOCIMIENTO.md` (nuevo), `ROADMAP.md` (tarea diferida añadida).
- **Estado:** vigente
