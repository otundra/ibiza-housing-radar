# Revisión Fase 0.5 — auditoría fundacional previa a construcción

**Fecha apertura:** 2026-04-21
**Contexto:** antes de entrar en diseño visual y desarrollo de la web, el editor abre una fase de revisión crítica del concepto completo (método editorial, fuentes, pipeline, UX, marca, legal, financiación). Objetivo: asegurarse de que los cimientos son sólidos antes de invertir en capas de implementación.
**Método de trabajo:** Claude lanza las tareas una a una, en el orden de prioridad de abajo. Editor responde. Cuando se cierra una, se marca ✅ y se pasa a la siguiente. Si una tarea destapa decisión nueva que afecta a docs maestros, se actualizan y se registra en `DIARIO.md`.
**Estado de la web:** congelada en Paso 1 del prototipo (4 páginas HTML). No se toca el diseño visual hasta cerrar esta fase.

---

## Decisiones cerradas durante la revisión

### 2026-04-21 · Backfill de 12 semanas + Camino A + auditor IA
- **Backfill retroactivo de 12 semanas (W06-W17, ~2 feb → 20 abr)** con Google News + RSS nativos + BOIB (si factible). Motivo: tener 3 meses de corpus real para validar criterios editoriales con evidencia, no con hipótesis.
- **Camino A confirmado:** las 12 ediciones retroactivas se publican con fecha real + banner *"procesada a posteriori bajo modelo documental"*. Refuerza SEO de lanzamiento, ofrece contexto al público, y la arquitectura del schema (state + proposals_history append-only + PI3 grafo de evolución) hace defendible mostrar cambios de posición de actores como linaje, no como "pillada".
- **Sistema de auditoría IA de 5 capas** en lugar de revisión humana exhaustiva:
  - Capa 1: extracción primaria (Haiku).
  - Capa 2: auditoría ciega independiente (Sonnet).
  - Capa 3: comparador determinístico Python + verify.py (5 checks: URL 200, dominio-actor, verbatim en HTML, fecha coherente, Wayback archive).
  - Capa 4: arbitraje Opus solo para discrepancias (~15%).
  - Capa 5: editor revisa solo lo flagged + muestreo aleatorio 10% de auto-aprobadas.
- **Heurísticas sin IA:** cross-source confirmation, single-source penalty, verbatim substring match obligatorio, domain-actor whitelist, viability sanity checks.
- **Log de auditoría completo** (`data/audit/YYYY-wWW/{proposal_id}.json`) con todas las capas, timestamps y decisiones — transparencia radical como escudo legal.
- **Coste cerrado:** ~3,50 € totales (backfill + auditor + pieza retroactiva Opus). Dentro del tope blando mensual con margen.
- **Tiempo editor estimado:** ~4 h (antes 15 h).

### 2026-04-21 · Orden de ejecución reordenado
Antes de retomar ED1 (criterios de admisión), se ejecutan primero las tareas que producen la materia prima y la infraestructura para validar con datos reales:
1. **PI2-A** (append-only inmediato).
2. **PI2-B** (backfill 12 semanas).
3. **PI9** (sistema auditoría IA).
4. **ED1** (criterios validados con corpus real).
5. Resto de P0/P1 en orden original.

---

## Cómo leer esta lista

Cada tarea tiene:
- **Código** (ej. `ED1`, `FU2`) para referencias cruzadas y commits.
- **Resumen** de la pregunta/decisión pendiente.
- **Estado**: ⏳ pendiente · 🔄 en discusión · ✅ cerrada · ⏸ pausada.
- **Salida esperada**: qué debe quedar escrito/decidido/implementado al cerrarla.

Orden: P0 (fundacional, bloquea lo demás) → P1 (estructural) → P2 (UX) → P3 (operacional) → P4 (identidad/negocio) → P5 (misc).

---

## P0 — Fundacional (método editorial y fuentes)

### ED1 · Criterio de "OK" para admitir una propuesta ⏳
En qué se basa el pipeline exactamente para dar luz verde a *"autor identificado + URL verificable"*. ¿Qué cuenta como URL primaria? ¿Qué hace `verify.py` hoy vs qué debería hacer? ¿Qué pasa cuando la URL cae meses después?
**Salida:** checklist formal de verificación + árbol de decisión + actualización de `ARQUITECTURA.md §verify.py`.

### ED2 · Imparcialidad medible y alertable ⏳
La imparcialidad es pilar. Hoy se mide a trimestre vista en `/balance/`. Hace falta:
- Umbrales numéricos automáticos (p.ej. si un bloque supera 55% a 8 semanas vista → alerta Telegram).
- Métrica por actor-destinatario (no solo por emisor).
- Métrica de tono (¿se cita verbatim o parafraseado? ¿con qué verbo?).
**Salida:** sección en `ARQUITECTURA.md` + umbrales en `balance.py` + hooks de notify.

### ED3 · Presencia editorial de "Omisiones" ⏳
Hoy Omisiones vive como sección 6 de la edición. ¿Es suficiente? ¿Merece página propia `/omisiones/` como tracker? ¿Debería tener peso visual en la home? Es uno de los tres diferenciales editoriales.
**Salida:** decisión sobre peso + posible nueva página + ajuste a `DISENO-WEB.md`.

### ED4 · Horizonte temporal = fecha de inicio del proyecto ⏳
Regla dura: cuando una propuesta dice *"primera vez documentada"*, se refiere al **observatorio**, no a la historia. El proyecto no pretende cubrir lo anterior a su arranque. Debe quedar explícito en UI y copy.
**Salida:** disclaimer estable + decisión de fecha-origen oficial + texto en `/metodologia/` y tooltip contextual.

### FU1 · Fuentes — estáticas vs vivas ⏳
Hoy `sources.yaml` es estático. No hay proceso de revisión. Debería haber:
- Revisión trimestral de qué fuentes están aportando señal vs ruido.
- Health-check de RSS (si un feed lleva 2 semanas sin nada útil, alerta).
- Horizonte realista de "cobertura ≈100%" o asumir que nunca lo es y cuantificar el gap.
**Salida:** proceso documentado + script `sources_health.py` + nota en metodología sobre cobertura declarada.

### FU2 · Google News — estudio de búsquedas temáticas ⏳
Las 4 búsquedas actuales (Ibiza vivienda, Ibiza trabajadores temporada, Consell Eivissa vivienda, Ibiza desahucio caravanas) se pusieron sin debate. Merece análisis: qué queries cubren mejor, qué términos faltan (ej. *"bolsa alquiler"*, *"vivienda protegida"*, *"mobbing inmobiliario"*, *"chabolismo"*, *"HUT"*, *"Llei habitatge"*), en catalán y en castellano.
**Salida:** matriz de queries puntuada por recall/precision + `sources.yaml` ampliado + método de revisión anual.

### FU3 · Hora Ibiza + Nou Diari — reevaluar ⏳
Descartados por feeds débiles. El editor pide revisión con más detalle: frecuencia real de publicación, cobertura temática, si hay alternativa vía Google News filtrado por dominio.
**Salida:** informe corto + decisión final + incorporación si procede.

### FU4 · BOIB / legal — conexión al pipeline ⏳
El Boletín Oficial de las Illes Balears publica leyes, decretos, resoluciones del Govern y Consell. Es fuente primaria pura. Hoy no está conectado. ¿Tiene RSS? ¿Hay que scrappear el buscador? ¿Coste de mantenimiento?
**Salida:** informe de factibilidad + si es viable, módulo `ingest_boib.py` o búsqueda Google News *"site:caib.es/boib"*.

---

## P1 — Estructural (pipeline, datos, contenido)

### PI1 · Revisión global del pipeline ⏳
Pasar revista a ingest → classify → extract → rescue → generate → verify → balance. Buscar:
- Pasos redundantes.
- Huecos (ej. deduplicación entre ediciones, detección de misma propuesta rebautizada).
- Seguridad: qué pasa si Anthropic cae, si un feed devuelve HTML inválido, si Opus alucina un URL.
- Innovaciones: ¿detectar cambio de posición de un actor entre ediciones? ¿agrupar propuestas equivalentes de distintos actores?
**Salida:** diff documentado sobre `ARQUITECTURA.md` + issues creados.

### PI2-A · Archivado append-only desde hoy 🔄
Hoy `ingested.json` y `classified.json` se sobreescriben en cada ejecución. Cambiar pipeline para que cada ejecución semanal archive a `data/archive/YYYY-wWW/` (ingested + classified + extracted + verify_report). No se pierde materia prima nunca más.
**Salida:** pipeline modificado + estructura `data/archive/` + nota en `ARQUITECTURA.md`.
**Prioridad ejecución:** primera del día (~1 h).

### PI2-B · Backfill retroactivo de 12 semanas ⏳
Script one-shot `src/backfill.py` que recorre Google News con operadores temporales (`after:X before:Y`) + buscadores nativos de Diario de Ibiza / Periódico de Ibiza semana a semana desde W06 (2 feb) hasta W17 (20 abr). Dedup por URL. Salida a `data/archive/YYYY-wWW/ingested.json`. Luego ejecuta classify + extract + auditor + verify sobre todo el corpus.
**Salida:** 12 semanas de corpus real con propuestas extraídas, auditadas, verificadas y con snapshot Wayback.
**Coste:** ~3 € API + ~1 h ejecución.
**Prioridad ejecución:** tras PI2-A y PI9.

### PI9 · Sistema de auditoría IA de 5 capas ⏳ [NUEVO]
Módulo `src/audit.py` que implementa la arquitectura de 5 capas decidida hoy:
1. Extract Haiku (ya existe).
2. Audit ciego Sonnet (re-extracción sin ver la primera).
3. Comparador determinístico Python + 5 checks de verify.py + heurísticas sin IA (cross-source, verbatim substring, domain-actor whitelist, viability sanity).
4. Arbitraje Opus para discrepancias.
5. Queue de revisión humana (flagged + 10% aleatorio de aprobadas).
Log completo por propuesta en `data/audit/YYYY-wWW/{proposal_id}.json` con output literal de cada capa, timestamps y decisión final.
**Salida:** módulo + tests + documentación en `ARQUITECTURA.md` + integración en el flujo normal y en `backfill.py`.
**Coste por ejecución semanal:** ~0,25 €. Por backfill completo: ~2,70 €.

### PI3 · Enlace entre ediciones y evolución de propuestas ⏳
Esto es donde hay *oro oculto*: una propuesta que nace W15, se debate W17, se rechaza W19. Hoy el tracker enlaza débilmente. Debería haber:
- Grafo de evolución visible por propuesta.
- Detección automática de *"esta propuesta es variante de aquella"*.
- Sección "qué pasó con lo de la semana pasada" en cada edición.
**Salida:** diseño de la relación entre propuestas + ajustes a schema + nueva vista en `/propuestas/{id}/`.

### PI4 · Datos abiertos — disclaimer sobre citabilidad ⏳
Si alguien descarga el CSV, debe quedar claro: para fuente fiable, acuda al **URL original** que está en cada fila. Nuestro dato es trazabilidad, no la fuente en sí.
**Salida:** disclaimer prominente en `/datos-abiertos/` + licencia CC-BY con atribución a fuentes primarias.

### PI5 · GitHub — techos y plan B ⏳
Todo vive en GitHub (repo + Pages + Actions). Límites reales:
- Actions: 2.000 min/mes gratis en repo privado, ilimitado en público.
- Pages: 100 GB/mes bandwidth, 1 GB tamaño repo.
- Baneo político/comercial (poco probable pero contemplable).
**Salida:** análisis de techos + estrategia de migración si algún día toca (Cloudflare Pages, Netlify) + backup automático del repo a otro remoto.

### PI6 · Modelos IA — documentación viva de la decisión ⏳
Haiku clasifica/extrae, Sonnet verifica, Opus compone. ¿Cómo sabemos que es óptimo? Hace falta:
- Log de coste real por fase.
- Test periódico: mismo input con modelos distintos, comparar output.
- Criterio de upgrade si sale un modelo mejor (p.ej. Haiku 5).
**Salida:** `docs/MODELOS.md` con criterios + script de benchmark + revisión semestral.

### PI7 · Registro completo de costes ⏳
Auditar que `costs.csv` captura 100% de llamadas (incluidas las fallidas, reintentos, tests manuales). ¿Hay huecos? ¿Tenemos coste por fase/modelo/edición?
**Salida:** auditoría de 4 semanas + fixes si hay huecos + dashboard más granular.

### PI8 · Contenido — página maestra "cómo funciona" + tooltips contextuales ⏳
El resumen que se le hizo al editor hoy debe convertirse en página pública (adaptada). Decisión: qué entra, qué queda para `/metodologia/` técnica, qué va en `/politica-editorial/`. Añadir tooltips `ⓘ` al lado de cada titular de sección en ediciones + mini-tagline debajo con bajo impacto visual.
**Salida:** copy de la página + sistema de tooltips + componente reutilizable.

---

## P2 — UX y diseño

### UX1 · Mockup/wireframe antes de diseño visual ⏳
El editor nota que se está entrando en CSS antes de validar estructura. Construir wireframes low-fi de todas las páginas (grises, sin tipografía final) para iterar rápido y validar flujos.
**Salida:** wireframes de home + edición + propuestas + ficha propuesta + ficha actor + balance + recursos + cómo usarlo, en formato rápido de iterar (HTML sin CSS o Figma/Excalidraw).

### UX2 · Navegación flagship ⏳
La navegación debe invitar a cruzar secciones en cualquier dirección. Menús en múltiples lugares (top, footer, inline, breadcrumbs, "related"), versión mobile y desktop diferenciadas, links contextuales dentro del contenido, CTAs de exploración al final de cada vista.
**Salida:** estudio aparte con mapa de enlaces, patrones, estados, heurísticas. Documento propio `NAVEGACION.md`.

### UX3 · Dos públicos — toggle, versiones o home dual bien calibrada ⏳
Decidir si se mantiene home dual, se saca toggle "soy curioso / soy profesional", o se hacen dos landings distintas con misma backend.
**Salida:** decisión + prototipo de la elegida.

### UX4 · Guía rápida en el fold ⏳
En el fold de la home, guía rápida que no ocupe más del 50%. Qué es, cómo se usa, 3 claves. Reemplaza parte del hero actual.
**Salida:** copy + mockup del bloque.

### UX5 · Balance accesible a todo el público ⏳
Hoy `/balance/` es técnico. Debería tener versión *"qué está pasando con la imparcialidad esta semana, explicado"* para público general. Visualizaciones claras, lenguaje llano.
**Salida:** rediseño de `/balance/` con doble capa (resumen público + detalle técnico).

### UX6 · Semana flaca — comunicación honesta ⏳
Si una semana nadie propone nada, la edición queda vacía. Hay que tener plantilla y tono: *"esta semana no hemos detectado propuestas nuevas. El silencio también es información. Aquí lo que sí ha pasado (hechos) y propuestas anteriores que siguen vivas (rescate)."*
**Salida:** plantilla + criterio editorial + componente UI.

### UX7 · Sección "avances o éxitos" — ¿es mojarse? ⏳
Pregunta abierta: ¿se puede documentar de forma neutra qué propuestas se han implementado/avanzado/descartado sin tomar partido? Una página `/seguimiento/` o columna en `/propuestas/` con estado *implementada/descartada/en ejecución* sin valorar *"bueno/malo"*. Hay que estudiarlo.
**Salida:** decisión + si va adelante, diseño de la sección.

### UX8 · Construir la web entera aunque no se publique toda ⏳
Editor propone construir todas las páginas aunque en la Fase 1 pública solo se abra un subconjunto. Definir qué se abre en lanzamiento vs qué queda draft visible solo para editor.
**Salida:** matriz de páginas × fase pública + flag `draft: true` por página.

---

## P3 — Operacional y meta

### OP1 · Plan de respuesta a rectificación de actor ⏳
Qué pasa si un partido/institución escribe diciendo *"esa cita no es mía"* o *"el contexto es otro"*. Hoy hay `/correcciones/` pero sin SLA ni proceso.
**Salida:** protocolo + plantillas + tiempos + quién decide.

### OP2 · Health de feeds — alertas proactivas ⏳
Si un RSS deja de publicar, si baja la frecuencia, si Google News cambia su formato → alerta Telegram.
**Salida:** módulo `sources_health.py` + alertas.

---

## P4 — Identidad, legal, financiación

### ID1 · Nombre definitivo — `radar))ibiza_vivienda` vs `radar))vivienda_ibiza` ⏳
Editor prefiere la primera. Claude debe dar opinión argumentada desde SEO, legibilidad, escalabilidad a futuros verticales (`radar))ibiza_turismo`, `radar))ibiza_medioambiente`).
**Salida:** recomendación + decisión + actualización de todos los docs.

### LG1 · Anonimato legal del editor ⏳
Investigar cómo mantener el nombre del editor oculto en:
- Aviso legal (obligatorio identificar responsable según LSSI).
- Registro de dominio (WHOIS privacy).
- Cuentas redes sociales.
- GitHub (posible).
Opciones gratis (pseudónimo + buzón virtual, fundación paraguas, etc.) y de pago baratas (servicios de representante legal, SL de 1 €, etc.).
**Salida:** informe con opciones, costes y riesgos legales reales.

### LG2 · Página de estudio sin nombre del editor ⏳
Editor quiere mencionar en `/acerca/` un link a un portfolio de *"proyectos IA del estudio"* sin revelar su identidad. Ver cómo articular esto legalmente y editorialmente.
**Salida:** decisión sobre si procede + copy + link a página externa a crear.

### FI1 · Financiación desde el lanzamiento ⏳
Activar canales de ingreso desde día 1 (sin agresividad, pero presentes): Ko-fi/Buy Me a Coffee, Open Collective, Patreon, botón "donación única PayPal", propuesta de mecenazgo institucional (fundaciones, Consell Social UIB, etc.). Decidir cuáles encajan con la neutralidad del proyecto.
**Salida:** estrategia de financiación + página `/apoyar/` + criterios de qué donaciones se aceptan y cuáles no (p.ej. ¿patronal hotelera? ¿partido político?).

---

## P5 — Misc (sugerencias de Claude añadidas)

### EX1 · Test de usabilidad pre-lanzamiento con 2-3 personas reales ⏳
Antes de lanzar público, pasar la web a una periodista, un temporero y un técnico municipal. Observar. Grabar si se puede.
**Salida:** informe + ajustes.

### EX2 · SEO técnico — schema.org para propuestas ⏳
Que cada `/propuestas/{id}/` tenga structured data (ClaimReview, NewsArticle). Google adora esto. Puede traer mucho tráfico.
**Salida:** implementación + validación Rich Results Test.

### EX3 · Estrategia de lanzamiento — soft vs hard ⏳
Cómo se lanza. A quién se le dice primero. Embargo con periodista afín. Nota de prensa. O sigiloso y que el SEO haga su trabajo.
**Salida:** plan de lanzamiento con fases y fechas.

### EX4 · Backup automático del repo ⏳
Mirror automático a GitLab o Codeberg. Cero coste, seguro ante cualquier incidencia en GitHub.
**Salida:** workflow GitHub Actions que empuja a mirror.

---

## Leyenda de estados

- ⏳ pendiente — aún no tocada
- 🔄 en discusión — editor y Claude la están trabajando ahora
- ✅ cerrada — decisión tomada y docs actualizados
- ⏸ pausada — deliberadamente en espera

## Registro de progreso

| Código | Tarea | Estado | Notas |
|---|---|---|---|
| ED1 | Criterio OK propuestas | ⏳ | |
| ED2 | Imparcialidad alertable | ⏳ | |
| ED3 | Presencia de Omisiones | ⏳ | |
| ED4 | Horizonte desde inicio | ⏳ | |
| FU1 | Fuentes vivas | ⏳ | |
| FU2 | Queries Google News | ⏳ | |
| FU3 | Hora Ibiza + Nou Diari | ⏳ | |
| FU4 | BOIB | ⏳ | |
| PI1 | Revisión pipeline | ⏳ | |
| PI2-A | Archivado append-only desde hoy | 🔄 | Primera tarea a ejecutar |
| PI2-B | Backfill retroactivo 12 semanas | ⏳ | Tras PI2-A y PI9 |
| PI9 | Sistema auditoría IA 5 capas | ⏳ | Nuevo, habilita PI2-B y ED1 |
| PI3 | Enlace entre ediciones | ⏳ | |
| PI4 | Datos abiertos disclaimer | ⏳ | |
| PI5 | Techos GitHub | ⏳ | |
| PI6 | Modelos IA docs | ⏳ | |
| PI7 | Costes completos | ⏳ | |
| PI8 | Página "cómo funciona" + tooltips | ⏳ | |
| UX1 | Mockup/wireframe | ⏳ | |
| UX2 | Navegación flagship | ⏳ | |
| UX3 | Dos públicos | ⏳ | |
| UX4 | Guía en fold | ⏳ | |
| UX5 | Balance accesible | ⏳ | |
| UX6 | Semana flaca | ⏳ | |
| UX7 | Avances/éxitos | ⏳ | |
| UX8 | Construir entera | ⏳ | |
| OP1 | Rectificación actor | ⏳ | |
| OP2 | Health feeds | ⏳ | |
| ID1 | Nombre definitivo | ⏳ | |
| LG1 | Anonimato legal | ⏳ | |
| LG2 | Portfolio sin nombre | ⏳ | |
| FI1 | Financiación | ⏳ | |
| EX1 | Test usabilidad | ⏳ | |
| EX2 | SEO schema.org | ⏳ | |
| EX3 | Estrategia lanzamiento | ⏳ | |
| EX4 | Backup repo | ⏳ | |
