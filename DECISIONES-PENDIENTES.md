# Decisiones pendientes del editor antes de arrancar Fase 0

**Fecha:** 2026-04-20
**Origen:** [PIVOTE.md](PIVOTE.md), [ROADMAP.md](ROADMAP.md).
**Uso:** lista cerrada de decisiones que requieren sí/no del editor antes de que Claude ejecute el bloque A del ROADMAP. Cada una con opciones y recomendación explícita.

Responde con número y elección. Ejemplo válido: "1.A, 2.B, 3.A, 4.B, 5.A, 6.A, 7.A, 8.A, 9.B, 10.A, 11.A, 12.A".

---

## 1. Reescritura de W16-W17

**Contexto:** las dos ediciones actuales están bajo modelo "editor jefe" con propuestas firmadas por el observatorio. Choca con las 5 reglas duras del pivote.

- **A. Reescribir** W16-W17 bajo modelo documental nuevo + mover originales a `private/ediciones-preservadas/` + nota metodológica + entrada en `/correcciones/`.
- **B. Mantener** las originales con nota de cabecera explicando que son pre-pivote, publicar solo W14-W15 con modelo nuevo, asumir archivo híbrido.

**Recomendación: A.** Coherencia del archivo completo. Trazabilidad conservada en git y carpeta privada.

---

## 2. Contenido retroactivo W14-W15

- **A. Producir** W14 y W15 retroactivas con ingest de ventana temporal + revisión manual + nota metodológica visible en cabecera.
- **B. Plan B:** no producir retroactivo, relanzar con archivo de 0 ediciones, la primera es W18 (27-abr).

**Recomendación: A.** El relanzamiento presenta un observatorio con 1 mes de rodaje. Coste API adicional ~5,84 € dentro del tope. La nota metodológica evita percepción de falsificación.

---

## 3. Día del relanzamiento

- **A. W18 (lunes 27-abr-2026)** — Fase 0 completada en una semana a tiempo completo.
- **B. W20 (lunes 11-may-2026)** — Fase 0 completada en 3 semanas a ritmo sostenible. Dos semanas de margen para pulir.
- **C. Otra fecha** — a elegir.

**Recomendación: B.** Relanzamiento justo antes del arranque operativo de la temporada (mayo). Tres semanas de preparación dan margen para detectar errores, hacer QA y preparar el envío a periodistas. W18 es demasiado apretado para lanzar las 15+ páginas nuevas con calidad.

---

## 4. Autoría visible del observatorio

- **A. Firma con nombre** — "Editor: Raúl Serrano" en `/acerca/` y pie de ediciones. Contacto directo visible.
- **B. Autoría anónima institucional** — el proyecto se presenta como "Ibiza Housing Radar" sin nombre visible del editor. Solo contacto por formulario.
- **C. Nombre + sin email directo** — firma visible + solo contacto por formulario Formspree.

**Recomendación: C.** El nombre eleva credibilidad y evita percepción de bot anónimo. El formulario protege tu bandeja de spam y filtra contacto serio. Si en 3-6 meses se activa email directo, es fácil sumarlo.

---

## 5. Dominio propio

- **A. Adelantar** compra ya (~12 €/año, ej. `radaribiza.org`) para arrancar SEO directamente en dominio memorable. Única excepción al coste-cero.
- **B. Esperar** a cumplir criterios de tracción del PLAN.md (>20 subs newsletter o cita en prensa local o 3 meses con >200 visitas/mes).

**Recomendación: A.** SEO se cimenta en autoridad de dominio, que se gana con tiempo. Arrancar en GitHub Pages y migrar en 6 meses significa perder 6 meses de acumulación. El coste de 12 €/año es irrelevante frente al ROI SEO. Además, un dominio propio habilita Google News Publisher Center en el futuro. Sugerencias concretas de dominio:

- `radaribiza.org` (corto, memorable, sin idioma)
- `habitatgeibiza.org` (en catalán, alinea con la isla bilingüe)
- `radardevivienda.org` (descriptivo)
- `observatoriovivienda.org` (más institucional)

Si A, el editor elige el dominio y lo compra; Claude no puede registrar dominios.

---

## 6. GoatCounter (analítica) en Fase 0

- **A. Activar** en Fase 0. Desde el día 1 hay datos reales para calibrar SEO y ajustar.
- **B. Diferir** a Fase 1.

**Recomendación: A.** Es zero-cost, 5 minutos de setup, y sin métricas no sabemos si el pivote funciona. Imprescindible desde el lanzamiento.

---

## 7. Newsletter Buttondown en Fase 0

- **A. Activar** newsletter en Fase 0, con formulario de suscripción en home y pie de edición. Envío automático lunes 10:00.
- **B. Diferir** a Fase 1.

**Recomendación: A.** El lanzamiento es el momento de máxima atención; no capturar emails es desperdiciar la ola. Buttondown gratuito hasta 100 subs.

---

## 8. `/recursos/` en Fase 0

- **A. Lanzar** `/recursos/` con teléfonos y direcciones verificadas desde el día 1.
- **B. Diferir** a Fase 1.

**Recomendación: A.** Diferenciador fundamental entre "observatorio" y "herramienta de cambio". Es lo que convierte a un temporero en lector recurrente. Coste: 3-4 h de investigación y verificación manual.

---

## 9. Balance público `/balance/`

- **A. Publicar** el balance público desde el día 1, incluso con pocos datos, mostrando la metodología.
- **B. Esperar** a tener 13 ediciones (3 meses) antes de publicar para tener datos más estables.

**Recomendación: A.** Transparencia desde el principio es parte del pivote. La página puede decir "ventana actual: 4 ediciones, datos indicativos" sin quedar mal. Publicar tarde mina el mensaje de imparcialidad.

---

## 10. Reescritura del modelo visual de la web

- **A. Conservar** el CSS actual y añadir componentes nuevos (cards de propuesta, chips de actor, etc.). Evolución incremental.
- **B. Rediseñar** la identidad visual completa desde cero.

**Recomendación: A.** El diseño actual es bueno, ya está pulido y es coherente. Lo que hace falta son **componentes nuevos** para las secciones nuevas, no cambiar identidad. La regla dura de "partidos en gris neutro" se añade al sistema existente.

---

## 11. Dominio del sitio para SEO: `otundra.github.io` vs dominio propio

**Dependiente de la decisión 5.** Si la 5 es A, esto se resuelve solo. Si la 5 es B, confirmar que aceptamos el techo de SEO de subdominio GitHub hasta tracción.

- **A. Asumido por la decisión 5A** — dominio propio.
- **B. Confirmar que aceptamos el subdominio GitHub como base de SEO** de arranque.

---

## 12. Bluesky + Mastodon: ambas redes o solo una

- **A. Ambas** (Bluesky + Mastodon). Máxima cobertura, esfuerzo doble de mantenimiento.
- **B. Solo Bluesky** (mayor tracción en ecosistema periodístico español 2026).
- **C. Solo Mastodon** (más establecido en Baleares por IB3 y colectivos).

**Recomendación: A.** Ambas. El bot las maneja automáticamente, el esfuerzo incremental es nulo tras montaje inicial. Esperar datos 3 meses para ver cuál funciona y eventualmente podar.

---

## 13. Cuándo crear el alias Gmail de contacto

- **A. Ya** — `ibizahousingradar@gmail.com` o similar. Desvinculado del email personal.
- **B. Cuando haya dominio** propio y sea `hola@radaribiza.org`.
- **C. No** — usar email personal del editor mientras no haya dominio.

**Recomendación: A.** Alias gratuito, profesional, protege la bandeja personal. Formspree lo usa como destino.

---

## 14. Privacidad del editor

- **A. Página `/acerca/` con foto y biografía breve.**
- **B. Página `/acerca/` solo con nombre y descripción profesional, sin foto.**
- **C. Solo firma en ediciones, sin página dedicada.**

**Recomendación: B.** Nombre + descripción es suficiente para credibilidad. Foto es opcional y personal; se puede añadir después.

---

## 15. Confirmación del modelo de IA

Hoy el pipeline usa Haiku 4.5 y Opus 4.7. El pivote mantiene ambos pero amplía el uso de Haiku (extracción, verificación, rescate). El coste sube de ~2 €/mes a ~5,85 €/mes, dentro del tope blando 8 €.

- **A. Confirmar** uso continuado de ambos modelos con los nuevos roles.
- **B. Usar Sonnet 4.6** en la generación de Opus para ahorrar, asumiendo riesgo de menor calidad editorial.

**Recomendación: A.** El coste entra en el tope y la calidad editorial de Opus es clave para que la edición semanal aguante crítica. Ahorro marginal (~1,5 €/mes) no justifica degradación.

---

## 16. Licencia del dataset de propuestas

- **A. CC-BY 4.0** (atribución, más permisiva).
- **B. CC-BY-SA 4.0** (atribución + share-alike, forzando que los derivados también sean abiertos).
- **C. CC0** (dominio público, sin atribución).

**Recomendación: A.** CC-BY es el estándar en datos abiertos académicos y periodísticos. Facilita reutilización sin forzar cadena de licencias. El proyecto gana visibilidad con atribución.

---

## Plantilla de respuesta

Responde con este formato (se pueden incluir comentarios tras cada elección):

```
1. A
2. A
3. B
4. C
5. A — dominio elegido: radaribiza.org
6. A
7. A
8. A
9. A
10. A
11. (asumido por 5A)
12. A
13. A — alias: ibizahousingradar@gmail.com
14. B
15. A
16. A
```

Cualquier opción con "A" no requiere explicación; si eliges algo distinto o tienes matiz, pone el motivo en una línea.

---

## Decisiones que NO requieren tu input (ejecutables directamente)

- Estructura del pipeline (ingest → classify → extract → rescue → generate → verify → balance): cerrada.
- Nombre de módulos, paths de archivos, formato de schema de datos: cerrado.
- Estructura de las secciones de la edición: cerrada.
- Sistema visual existente + ampliación: cerrada.
- Breakpoints responsive: cerrados.
- Stack técnico (Python + Jekyll + GitHub Pages): cerrado.
- Licencia del sitio CC-BY 4.0: asumido, parte del estudio.

Si quieres mover alguna de estas a "decisión del editor", dímelo.
