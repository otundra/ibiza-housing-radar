# Roadmap — radar))ibiza_vivienda

**Fecha original:** 2026-04-20 · **Reestructurado en fases ejecutables:** 2026-04-21 noche · **Fecha objetivo de relanzamiento:** lunes 13 jul 2026 (ver [D11](DECISIONES.md))
**Origen:** [CLAUDE.md](CLAUDE.md#reglas-fundacionales), [REVISION-FASE-0.5.md](REVISION-FASE-0.5.md).
**Principio base:** relanzamiento sólido, sostenido por infraestructura automatizada (el editor opera, no audita). Coste ≤12 €/mes bajo tope blando, ≤50 €/mes bajo tope duro. Reversibilidad vía histórico git.

---

## Cómo leer las estimaciones de tiempo

Desde 2026-04-23 ([D11](DECISIONES.md)) toda estimación del proyecto se expresa con tres números distintos, nunca uno solo:

- **Calendario** — semanas de reloj real. Es lo único que marca la fecha de lanzamiento.
- **Esfuerzo editor** — horas reales del editor. A ritmo sostenible el proyecto asume 15 h/sem. Incluye decisión, revisión, commits, gestión y testeo.
- **Esfuerzo Claude** — horas del asistente. No colapsa calendario: el cuello de botella es la decisión/revisión del editor. 40 h del asistente en un día no acelera la fecha si el editor no puede absorberlo al mismo ritmo.

Formato corto en docs: *"N sem calendario / ~M h editor"*. El esfuerzo del asistente se omite salvo que aporte contexto (p. ej. cuando un módulo es mayoritariamente trabajo de Claude). Las estimaciones anteriores a D11 se reinterpretan como calendario hasta reescribirse.

**Aplicado al relanzamiento del lunes 13 jul 2026:** ~12 sem calendario desde 2026-04-23 / ~180 h editor totales distribuidas en las 7 fases. Supuestos que tienen que cumplirse: 15 h/sem sostenido, sin imprevistos personales mayores de 1 semana, cero re-alcances grandes, prueba empírica del auditor MVP pasa a la primera. Si alguno falla, el calendario se desliza 1-3 semanas hacia jul-ago; el banner de rodaje absorbe el deslizamiento sin re-planificar. Red de seguridad: escenario B (12 oct 2026, cierre de temporada) si al llegar finales de junio el producto no está maduro.

---

## Roadmap V2 — 7 fases ejecutables (estructura activa)

Montado tras la revisión técnica 2026-04-21 noche. Ordena las tareas abiertas (RT1-RT24 en la revisión fundacional + bloques originales A-I) en 7 fases con ruta crítica, paralelos y dependencias. Supuestos base:

- **Ritmo:** ~15 h/semana del editor, sostenible.
- **Objetivo de lanzamiento:** soft launch mediados de mayo / junio 2026 si no entra en mayo. Escenario B (rodaje privado 6-12 meses) es válido si al terminar Fase 6 el estado no está maduro. Ver tarea RT24.
- **Prioridad:** calidad antes que velocidad. Error reputacional temprano es más caro que retraso.
- **Marca:** `radar))ibiza_vivienda` (cerrado 2026-04-21).

### Panorama

| Fase | Nombre | Duración estimada | Objetivo |
|---|---|---|---|
| 1 | Cimientos firmes | 2-3 semanas | Pipeline listo para absorber el backfill sin romperse |
| 2 | Backfill, corpus y fuentes primarias | 1-2 semanas | 12 (o 6) semanas auditadas + datos propios operativos |
| 3 | Afinado de ingesta y criterios | 1 semana | Fuentes validadas empíricamente con el corpus real |
| 4 | Web completa + trilingüe | 2-3 semanas | 15+ páginas en ES/CA/EN antes del SEO |
| 5 | SEO y distribución | 1-2 semanas | Descubribilidad multilingüe + canales activos |
| 6 | Pre-empuje | 1 semana | Sanity check externo + ensayo final |
| 7 | Empuje público + medición 90 días | continuo | Lanzamiento + evaluación con framework de señales |

**Total estimado:** 9-12 semanas a ritmo sostenible.

### Fase 1 — Cimientos firmes

**Frame de trabajo reordenado 2026-04-23 ([D6](DECISIONES.md)):** la Fase 1 se organiza en tres hitos grandes. El editor decide puntos de entrada y de cierre de cada hito; Claude lleva los pequeños dentro. Las 34 tareas restantes de la Revisión Fase 0.5 quedan en cola y se abren al cerrar el hito anterior.

**Cerradas o diferidas:**
- **Estudio preciso de costes del auditor IA** (RT14). ✅ Cerrado 2026-04-23. Entregable: [ESTUDIO-COSTES-AUDITOR.md](ESTUDIO-COSTES-AUDITOR.md).
- **Revisión profunda de arquitectura documental** (nuevo). Diferida a Fase 7 post-lanzamiento. Hasta entonces, aplicar las tres reglas baratas de [D0](DECISIONES.md).

**Hito 1 · Auditor mínimo viable publicado con una edición real (activo):**

1. **Auditor MVP** — PI9 partido en mínimo viable + iteración ([D1](DECISIONES.md)). 2 semanas: capa 2 ciega Sonnet + comparador determinista + tres heurísticas sin IA (cruce de fuentes / verbatim match / whitelist V1, ver [D3](DECISIONES.md)) + log público con campo `corrections` append-only y protocolo de correcciones en 72 h ([D2](DECISIONES.md)) + integración con `report.py`. Hueco reservado para tiers ([D5](DECISIONES.md)). Sin Opus formalizado, sin cuarentena navegable, sin dashboard. Detalle en [ESTUDIO-COSTES-AUDITOR.md §10.0](ESTUDIO-COSTES-AUDITOR.md).
2. **Prueba empírica** (RT1). Corrida del auditor MVP sobre la semana W10 (2-8 marzo 2026) antes del backfill completo.
3. **Iteración posterior del auditor** (2-3 semanas, puede solaparse con Fase 2): formalización explícita de capa 4 Opus + página `/revision-pendiente/` + dashboard público `/auditor/` + capa 5bis (repaso mensual IA de cuarentena).

**Hito 2 · Sistema de tiers cerrado e integrado (cerrado conceptualmente 2026-04-23, pendiente implementación + validación empírica):**

- **Re-estudio profundo del sistema de tiers** (RT15) ✅ **cerrada 2026-04-23**. Entregable [`ESTUDIO-TIERS.md`](ESTUDIO-TIERS.md) completo: 11 secciones + 5 decisiones operativas cerradas ([D9](DECISIONES.md)) — visibilidad mixta (🟢 sin badge, 🟡🟠🔴 con aviso), política de cambios retroactivos congelar, default paso 6 = 🟠 + alerta Telegram, Q2 diferida a datos del backfill, mockups HTML para Fase 4.
- **Cierre editorial** (RT26) ✅ cerrada 2026-04-23 con OK en bloque del editor.
- **Implementación pendiente (entra en PI10):** `src/tiers.py` con `compute_tier(signals)` + `data/tiers.yml` con los umbrales operativos + plantilla visual del badge en Jekyll + `/metodologia/#tiers` con el copy de §5 del estudio. No bloquea Hito 1; se hace como sub-tarea dentro de la iteración posterior del auditor o en Fase 2.
- **Medición empírica del sesgo** (RT25). Tras backfill de 12 semanas (PI2-B). Script `scripts/tier_bias_audit.py` (~2 h) + análisis + activación opcional de mitigación M1 en `data/tiers.yml`. Cierra §8.5 del estudio.
- **Test de usabilidad con 5 personas** (RT3). Valida en campo la decisión de visibilidad mixta (Q1). ~3 h de trabajo del editor con su red personal. Recomendable antes del empuje público.
- **Validación empírica preliminar del árbol** sobre backfill piloto W10 (RT1) — queda dentro del Hito 1; aquí solo se anota que confirma que los umbrales por defecto funcionan antes del backfill grande.

**Hito 3 · Titular legal resuelto (en paralelo, bloquea empuje público):**

- **Estudio titular legal** (RT20 + LG1 + LG2). Ver bloque *"En paralelo"*.

**En paralelo (hilos independientes):**

- **Estudio Vía A de precios** (RT12 + RT21). Matriz de fuentes, nombre público ("Observatorio de precios"), presupuesto, recomendación de cronograma.
- **Estudio titular legal** (RT20 + LG1 + LG2). Tabla comparativa + recomendación + plan de implementación. Es el Hito 3 del frame.
- **Estudio de factibilidad BOIB** (RT22). 2-4 h. Decide si sube a Fase 2 o queda en Fase 3.
- **Regla fundacional automatización + veracidad pública** (RT13) documentada en CLAUDE.md ✅ hecha 2026-04-21.

**Tests del pipeline diferidos a RT5 ([D4](DECISIONES.md)):** cobertura en un solo bloque con fixtures reales del backfill (incluye `audit.py`, `verify.py`, `balance.py`, `extract.py`, `rescue.py`). Se ejecuta cuando haya fixtures utilizables (Fase 2). El auditor MVP se valida durante construcción con la prueba empírica sobre W10.

**Decisiones cerradas en Fase 1:**
- Rol del editor = operador sin revisión de contenido (RT2 resuelto: opción B actual, opción C cuando haya tracción).
- Nombre del wordmark: `radar))ibiza_vivienda` ✅ cerrado.

**Salida de la fase:** auditor mínimo operativo + prueba empírica validada + sistema de tiers cerrado en paralelo + titular legal en trámite. Pipeline con auditor MVP listo para absorber el backfill en Fase 2.

### Fase 2 — Backfill, corpus y fuentes primarias

**Ruta crítica en serie:**

1. **Backfill real** (PI2-B). Ajustado según prueba empírica de Fase 1. 12, 6 o 4 semanas.
2. **Sistema de tiers de confianza** (PI10). Implementado sobre datos del backfill. Ajustes si el re-estudio (RT15) ha cambiado algo.
3. **Cuarentena pública** `/revision-pendiente/` (PI11).
4. **Alerta Telegram enriquecida completa** (PI12). Ahora hay datos upstream.

**En paralelo:**

- **Implementación Vía A de precios** si Fase 1 dio verde. Scripts de agregación mensual + publicación inicial de 3-6 meses de datos. Página `/precios/`.
- **BOIB watcher** si el estudio de factibilidad dio verde. Si no, queda para Fase 3.

**Salida:** 12 ediciones retroactivas publicadas, tiers operativos, cuarentena pública, posiblemente datos propios de precios y BOIB.

### Fase 3 — Afinado de ingesta y criterios

**Tareas en paralelo (todas independientes):**

- **Matriz de queries Google News** (FU2) con recall/precision empírico + catalán.
- **BOIB watcher** si no entró en Fase 2.
- **Reevaluar Hora Ibiza + Nou Diari** (FU3) con datos reales del backfill.
- **Health check de fuentes** (FU1) + script `sources_health.py` + proceso de revisión trimestral.
- **Resiliencia a cambios de modelo Anthropic** (nuevo). Auditar si el pipeline está hardcodeado a versiones concretas (Haiku 4.5, Sonnet 4.6, Opus 4.7); crear script `models_health.py` que detecte deprecaciones o versiones nuevas consultando la API de Anthropic; alerta Telegram si un modelo activo deja de estar disponible o aparece una versión mayor; protocolo documentado para actualizar la versión de un modelo y volver a ejecutar el estudio de costes (RT14) sobre el nuevo. Objetivo: que un cambio de Anthropic nunca rompa el pipeline en silencio y que subir a una versión nueva sea un proceso testeable en menos de 1 hora.
- **Criterio formal de admisión de propuestas** (ED1) validado empíricamente.
- **Imparcialidad alertable** con umbrales cerrados (ED2).
- **Horizonte temporal** fijado en UI y copy (ED4).
- **Auditoría registro completo de costes** (PI7). Verificar que `costs.csv` captura 100%.

**Salida:** sources vivas, criterios validados, alertas de imparcialidad operativas.

### Fase 4 — Web completa + trilingüe

**Ruta crítica en serie:**

1. **Incorporar propuesta visual de Claude Design** (RT16). Requiere archivos del editor; comparar con D1-D13, decidir qué se mantiene/sustituye/integra.
2. **Wireframes low-fi de todas las páginas** (UX1) con la propuesta visual ya integrada.
3. **Documento de navegación** (RT17) — propio, `NAVEGACION.md`. Top-nav con subniveles, sidebars contextuales, sitemap visual siempre accesible, breadcrumbs, internal linking denso, CTAs exploración, mobile-first.
4. **Decisión dos públicos** (UX3): home dual / toggle / dos landings.
5. **Test de usabilidad de tiers y navegación** con 3 personas (RT3 + EX1). Iterar antes de construir todas las páginas.
6. **Construcción de páginas en Jekyll** (todo el Bloque B original + las nuevas):
   - Política editorial (con las 5 reglas + regla complementaria de automatización).
   - Metodología (convertir prototipo `/metodo/` a Jekyll, con propuesta visual de Claude Design).
   - Correcciones (vacía con formato).
   - Propuestas (tracker filtrable).
   - Actores (directorio con fichas).
   - Radar (señales en movimiento).
   - Revisión-pendiente (cuarentena, ya en Fase 2).
   - Sin dato (con formulario).
   - Balance accesible doble capa (UX5).
   - Cómo usarlo (UX4 + RT11).
   - Glosario.
   - Contacto (Formspree universal).
   - Cita esto (kit de prensa).
   - Datos abiertos (CSV descargable) con disclaimer (PI4).
   - Financiación (FI1).
   - Aviso legal (con titular resuelto).
   - 404.
   - Auditoría (vacía para trimestrales).
   - Costes público.
   - Estado (histórico operacional).
   - Precios (si Vía A entró).
   - Omisiones (ED3) — página propia si se decide.
7. **Seguimiento visual de evolución de problemáticas** (RT19) — estudio de formato + mockup + implementación si hay datos suficientes.
8. **Enlace entre ediciones y evolución individual de propuestas** (PI3, el "grafo de oro").
9. **Plantilla de semana flaca** (UX6).
10. **Split `/acerca/` + `/metodo/`** (RT8, RT9). `/acerca/` corta + `/metodo/` con detalle técnico.
11. **Copy final de la home** (RT11).
12. **Componentes del estudio** finalizados en Jekyll (9 + los derivados de Claude Design).
13. **Trilingüe ES/CA/EN operativo** (RT18). Pipeline de traducción + chrome trilingüe + glosario eivissenc. Antes del SEO.
14. **OG images con Puppeteer** (Bloque D5).
15. **Modo oscuro manual + automático** (Bloque B40).

**Decisión operativa importante:** activar trilingüe desde el backfill (las 12 ediciones retroactivas salen en 3 idiomas, coste +3-4 € puntuales, corpus consistente) o solo desde el empuje público (ahorro marginal, hueco en el corpus). **Recomendación Claude: desde el backfill si el presupuesto lo permite.**

**Salida:** web completa en 3 idiomas, navegable, responsive, accesible, coherente con el modelo documental y la nueva propuesta visual.

### Fase 5 — SEO y distribución

**Ruta crítica en serie:**

1. **Dominio propio configurado** si el editor lo decide (Q3). Migración 301 desde GitHub Pages.
2. **Meta tags + schema.org + Open Graph + Twitter Cards** en las 15+ páginas × 3 idiomas.
3. **Sitemap, robots.txt, RSS completo por idioma, canonicals + hreflang.**
4. **Google Search Console + Bing Webmaster** con el dominio y los 3 idiomas.
5. **Core Web Vitals auditadas**.
6. **Páginas `/explica/` long-tail** (8 páginas × 3 idiomas). Sa Joveria, Can Misses, IBAVI, Consell d'Eivissa, Llei habitatge, alquiler turístico, vivienda temporera, VPO Ibiza.
7. **Newsletter Buttondown** + envío automático del lunes 10:00. Formulario de suscripción.
8. **Página de estadísticas** con GoatCounter + Search Console.
9. **Lista curada de 15-25 contactos directos** (periodistas, gabinetes, tercer sector, sindicatos, patronales, académicos).

**Salida:** web indexable en 3 idiomas, canales de distribución listos.

### Fase 6 — Pre-empuje

1. **Sanity check externo** con periodista local o académico UIB. 30 propuestas del backfill auditadas. 50-100 €.
2. **Test de usabilidad final** con 3 personas reales si no se completó en Fase 4.
3. **Banner de fase de rodaje** colocado (RT4): *"Observatorio en rodaje · N ediciones documentadas · próximo hito: X"*.
4. **Aviso legal operativo** con titular definitivo (RT20 cerrada).
5. **Estrategia de lanzamiento cerrada** (EX3). Recomendación: soft con envío privado a lista curada el lunes del relanzamiento.
6. **Backup automático del repo** a GitLab o Codeberg (EX4).
7. **Página de financiación** (FI1) con canales pasivos Ko-fi / GitHub Sponsors.
8. **Plan de respuesta a rectificaciones de actor** (OP1).
9. **Dashboard público de costes** (`/costes/`).
10. **Página `/estado/`** con histórico operacional.
11. **Health de feeds** (OP2).
12. **Evaluación del escenario A vs B** (RT24). Con el estado real a la vista, decidir si se lanza o se mantiene rodaje privado.

**Salida:** todo listo para el lunes del relanzamiento o decisión formal de diferir a Escenario B.

### Fase 7 — Empuje público + medición 90 días

**Día 1:** edición publica automáticamente, email manual a lista curada, vigilancia constante de Search Console + GoatCounter la primera semana.

**Primeras 4 semanas:** responder correos del formulario (48-72 h), recoger feedback real, ajustar tono si hace falta.

**Evaluación a 90 días con framework de tracción** (RT23):
- **Verde** → activar Vía B crowd-sourcing precios, bots sociales, envío personalizado semanal, consejo editorial, primer grant.
- **Amarillo** → revisión de ángulo, tono, distribución.
- **Rojo** → pasar a modo experimental, pipeline sigue, sin inversión de energía nueva. Reevaluar a 180 días.

### Diferido con criterio claro

Estas tareas siguen apuntadas pero no entran en el roadmap del relanzamiento:

- **Revisión profunda de arquitectura documental y gestión del conocimiento** — ejecutar reorganización completa descrita en [`ESTUDIO-GESTION-CONOCIMIENTO.md`](ESTUDIO-GESTION-CONOCIMIENTO.md) §3 y §7 (INDEX.md, DIARIO troceado, front-matter YAML, consolidación `estudios/`, migración histórica de decisiones, contrato de arranque formalizado). **Condición:** observatorio lanzado + primera evaluación 90 días + Revisión Fase 0.5 cerrada. Releer estudio antes de ejecutar; probable que parte esté obsoleta. Reglas baratas ya aplicadas 2026-04-23 (ver DIARIO y DECISIONES D0).
- **Balance rediseño con persistencia trimestral** (RT6) — activar a los 3 meses de datos, ~julio 2026.
- **Auditoría trimestral con Opus** — primera cuando haya 13 ediciones (Q4 2026 si todo va bien).
- **Re-benchmark mensual de modelos**.
- **Automatización anual de fechas de temporada**.
- **Notificación de alerta por email** (PI13) — cuando haya buzón propio.
- **Página `/recursos/`** (para afectados) — Fase 1 post-lanzamiento.
- **Bots Bluesky + Mastodon** — tras medición de 90 días.
- **Consejo editorial honorífico**.
- **Observatorio de precios Vía B** (crowd-sourcing ciudadano) — si Vía A se consolida.
- **BOIB watcher como servicio activo** — si no entró en Fase 2.
- **Evento anual co-organizado**.
- **Modelo de newsletter pago/híbrido**.

### Hipótesis post-tracción — Escalabilidad provincial

**Condición única:** el framework de señales de tracción a 90 días (RT23) da verde en Ibiza. Sin tracción demostrada en Ibiza, este bloque no existe.

Si el modelo funciona, replicar el observatorio a otras provincias españolas (o al resto de Baleares) tiene coste técnico bajo. Piezas reutilizables sin cambios: el pipeline Python completo, el sistema de costes, Jekyll/GitHub Pages, la taxonomía de 8 actores, el wordmark por provincia (`radar))valencia_vivienda`, `radar))mallorca_vivienda`...). Lo que varía por provincia: un archivo `config/<provincia>.yaml` con feeds RSS locales, keywords de búsqueda y contexto geográfico para los prompts.

La lógica de temporada/pre-temporada de Ibiza (ligada al ciclo de clubs) queda en su configuración propia y no contamina el motor ni un eventual observatorio nacional. Las ediciones usan fechas ISO en las URLs como eje universal — compatible con cualquier geografía.

**Arquitectura cuando llegue el momento:**
- Un repo `radar-motor/` con el pipeline compartido.
- Un `config/<provincia>.yaml` por instancia (feeds, keywords, contexto, calendario propio si aplica).
- GitHub Actions genera y empuja HTML a repos de output por provincia (`radar-ibiza/`, `radar-valencia/`...).
- Cada repo de output sirve un GitHub Pages propio con su dominio.
- El motor se mantiene en un solo sitio; un cambio de pipeline aplica a todas las instancias.

**Estimación técnica:** 1-2 semanas de trabajo para la primera réplica; marginal por cada provincia adicional.

**No hacer antes de:** tracción demostrada en Ibiza (previsto evaluar ~90 días tras relanzamiento, Q3 2026 como pronto).

### Hipótesis post-tracción — Expansión temática en Ibiza

**Condición única:** misma que escalabilidad provincial — RT23 verde en Ibiza vivienda.

Documento completo en [`EXPANSION-TEMATICA.md`](EXPANSION-TEMATICA.md) con evaluación detallada de 10+ temas candidatos. Resumen:

- **Tier 1 (encaje casi directo):** saturación turística, agua, movilidad.
- **Tier 2 (con adaptación):** trabajo de temporada, medio ambiente, residuos.
- **Tier 3 (descartados o como palancas):** sanidad, educación, energía, patrimonio, seguridad, gobernanza.
- **Recomendación de orden:** primero palancas transversales en el pipeline actual (Modelo C híbrido), graduar a vertical propio solo si la palanca demuestra demanda. Primer vertical candidato: turismo. Agua y movilidad en cola.
- **Interacción con escalabilidad provincial:** ambas hipótesis comparten condición y arquitectura técnica (motor + config). Orden sensato: primero turismo en Ibiza (misma geografía, distinto tema), luego provincias (mismo tema, distinta geografía).

**No hacer antes de:** tracción demostrada en Ibiza vivienda. Mismo horizonte que escalabilidad provincial.

---

## Fase 0 original (anexo histórico — estructura por bloques)

**Nota:** la estructura de abajo (Bloques A-I) es la planificación original del modelo documental (2026-04-20). La **estructura activa** es el Roadmap V2 de arriba. Los bloques se mantienen como referencia para ver qué se movió dónde.

---

## Contexto original del modelo documental

**Principio base:** lanzar en Fase 0 todo lo que se pueda para que el relanzamiento del proyecto sea fuerte, coherente y memorable. Coste 0 externo salvo API Anthropic. Reversible vía branch aislado.

## Estado a 2026-04-20

| Bloque | Tema | Estado |
|---|---|---|
| A | Pipeline técnico del modelo documental | ✅ **cerrado** (salvo A8 tests básicos, A13 auditoría trimestral, A14 re-benchmark mensual, A15 dashboard costes ampliado y A17 automatización temporadas — todos pendientes/diferidos) |
| B | Arquitectura web (home, /radar/, /propuestas/, /actores/, /balance/, /estadisticas/, /estado/, /sin-dato/, /sistema/, …) | ⏸ **en pausa** (21-abr tarde). Prototipo (B34) entregado y en revisión; hold a petición del editor para estudiar arquitectura antes de Paso 2 |
| C | Contenido retroactivo 8 ediciones (W10-W17) | ⏸ pendiente |
| D | SEO masivo | ⏸ pendiente |
| E | Analítica (GoatCounter, dashboard público) | ⏸ pendiente |
| F | Distribución (newsletter Buttondown gratis) | ⏸ pendiente |
| G | Utilidad pública (glosario, kit prensa) | ⏸ pendiente (/recursos/ diferido) |
| H | Legal y transparencia | ⏸ pendiente |
| I | Estudios previos bloqueantes | 🔄 parcial (estudio 3 modelos ✅ cerrado, **estudio de diseño ✅ cerrado** en [ESTUDIO-DISENO.md](ESTUDIO-DISENO.md), dominio pendiente compra, fecha relanzamiento pendiente) |

**Historia de decisiones y cambios voluntarios:** [`private/adjustments-log.md`](private/adjustments-log.md).
**Errores registrados:** [`private/postmortems.md`](private/postmortems.md).

---

## Fase 0 — Relanzamiento completo

**Objetivo:** al terminar Fase 0, el observatorio es un producto cerrado que se puede compartir sin vergüenza con un periodista, un regidor, un sindicato o un temporero.

**Duración estimada:** 5-7 días a tiempo completo, o 3-4 semanas a 10 h/semana.

**Entregables mínimos:**

1. Pipeline técnico del modelo documental operativo.
2. 4 ediciones retroactivas publicadas (W14-W17) bajo el nuevo modelo.
3. 15+ páginas web nuevas o reescritas.
4. SEO técnico completo + keywords por edición.
5. Analítica sin cookies activa.
6. Newsletter y bots sociales operativos.
7. Política editorial pública con las 5 reglas duras.
8. Balance inicial retrospectivo publicado.

### Bloque A — Pipeline técnico del modelo documental

- [ ] **A1.** Reescribir `SYSTEM` prompt de `src/generate.py` con la nueva estructura documental (señales / cronología / mapa de posiciones / propuestas documentadas / rescate / omisiones / a vigilar).
- [ ] **A2.** Ampliar schema de `src/classify.py` con campos `has_explicit_proposal`, `proposal_actor`, `proposal_actor_type`, `proposal_text`, `proposal_url`, `proposal_state`, `proposal_target_actor`, `proposal_horizon`, `proposal_viability_legal`, `proposal_viability_economic`.
- [ ] **A3.** Crear `src/extract.py` — para cada noticia con `has_explicit_proposal=true`, extrae la ficha estructurada completa.
- [ ] **A4.** Crear `src/verify.py` — verifica HTTP 200 de cada URL citada, trazabilidad de actores, fact-check de precedentes externos con Haiku. Bloqueante: si falla, no publica.
- [ ] **A5.** Crear `src/rescue.py` — lee ediciones previas, selecciona 3-5 candidatas a rescate por criterios (no ejecutada, no mencionada en últimas 4 semanas, sigue vigente).
- [ ] **A6.** Crear `src/balance.py` — calcula reparto de actores y bloques políticos en ventanas móviles, escribe a `private/balance.md` y página pública `/balance`.
- [ ] **A7.** Adaptar `src/report.py` al nuevo flujo: `ingest → classify → extract → rescue → generate → verify → write → balance → notify`.
- [ ] **A8.** Tests básicos sobre el pipeline: smoke test mínimo + verificación con dataset fake.
- [ ] **A9.** Prompt caching en Opus (`cache_control`) — ahorro ~50 % del coste Opus.
- [ ] **A10.** Resiliencia en `classify.py` ante menor cantidad devuelta.
- [ ] **A11.** Métricas de pipeline en CSV (`n_feeds_ok`, `n_items_raw`, `n_housing`, `n_proposals_extracted`, `n_duplicates`).
- [ ] **A12.** `src/self_review.py` — autoevaluación semanal con Sonnet tras publicar edición. Alerta Telegram si score < 7 en cualquier dimensión.
- [ ] **A13.** `src/quarterly_audit.py` — auditoría trimestral con Opus, output público en `/auditoria/YYYY-qN/`.
- [ ] **A14.** `src/model_rebench.py` — re-benchmark mensual de modelos, 10 noticias nuevas, alerta si ratio calidad/coste cambia >20%.
- [ ] **A15.** Ampliar `src/costs.py` con: coste por módulo, coste por modelo, cache hit rate, tendencia 8 semanas, estimación semanal/mensual/anual, alertas de desviación.
- [ ] **A16.** Subir tope blando a 12 € (nueva capa 🟠 naranja 9-12 €) para absorber los 3 niveles de autoevaluación sin cruzar umbral cada mes.
- [ ] **A17.** `src/update_temporadas.py` — tarea anual (GitHub Action) que consulta news sobre las fechas de opening/closing de las clubs grandes (Pacha, Hï, Ushuaïa, Amnesia) del año siguiente y alerta a Telegram cuando ≥3 coinciden. El editor actualiza manualmente `data/temporadas.yml`. Corre febrero/marzo/abril; recordatorio si 1 de abril sin alerta. Coste ~0,02 €/ejecución. Ver [memoria del proyecto · calendario_editorial](../../.claude/projects/-Users-raulserrano-Documents-GitHub-ibiza-housing-radar/memory/calendario_editorial.md).

### Bloque B — Arquitectura web

Detalle en [DISENO-WEB.md](DISENO-WEB.md).

**Páginas nuevas o reescritas:**

- [ ] **B1.** Home dual: hero para primer visitante + panel completo de última edición para recurrente.
- [ ] **B2.** `/politica-editorial` — las 5 reglas duras, visibles y estables.
- [ ] **B3.** `/metodologia` — método técnico, modelos usados, sesgos declarados.
- [ ] **B4.** `/balance` — página pública con reparto de actores auditado.
- [ ] **B5.** `/actores` — directorio de todos los actores citados, rol, URL oficial, posiciones expresadas.
- [ ] **B6.** `/propuestas` — tracker histórico de propuestas documentadas, filtrable.
- [ ] **B7.** `/glosario` — instituciones y términos (IBAVI, Consell, Llei 5/2018, etc.).
- [ ] **B8.** `/correcciones` — log público de correcciones con fecha y motivo.
- [ ] **B9.** `/como-usarlo` — guía en 200 palabras de qué es cada sección de la edición.
- [ ] **B10.** `/recursos` — teléfonos y direcciones útiles para quien pierde vivienda: servicios sociales de los 5 ayuntamientos, Cáritas, Cruz Roja, Oficina de Vivienda del Consell, 112 emergencia social, juzgados de guardia. Utilidad directa. Diferenciador fuerte.
- [ ] **B11.** `/contacto` — Formspree gratis, alias gmail temporal.
- [ ] **B12.** `/acerca` — reescrita, breve, con autoría y misión.
- [ ] **B13.** `/cita-esto` — kit de prensa: logo, descripción corta/larga, formato para citar, contacto.
- [ ] **B14.** `/aportar` — formulario mínimo crowd-sourcing de precios (MVP de Fase 3.1 Vía B, solo captura, publicación cuando haya umbral).
- [ ] **B15.** `/datos-abiertos` — descarga CSV de todas las propuestas documentadas, licencia CC-BY.
- [ ] **B16.** `/financiacion` — coste actual transparente (~2-3 €/mes API), sin monetización activa.
- [ ] **B17.** `/aviso-legal` — aviso mínimo, titular del sitio, contacto.
- [ ] **B18.** 404 personalizado con links a home y últimas ediciones.
- [ ] **B27.** `/sin-dato/` — archivo público de propuestas con campos "no evaluada" + formulario para aportar datos con URL obligatoria.
- [ ] **B28.** `/auditoria/` — índice de auditorías trimestrales públicas.
- [ ] **B29.** `/costes/` — dashboard público simplificado con coste agregado, capa actual y link al CSV completo.
- [ ] **B30.** `/estado/` — histórico operacional del pipeline estilo Solar Low-Tech (registro de ejecuciones, retrasos, versiones, contadores globales).
- [ ] **B31.** `/radar/` — señales en movimiento (intenciones, estudios encargados, debates sin propuesta concreta). Juego con la marca del proyecto. Ciclo de vida formal: en_movimiento → propuesta → archivo o caducada. Detalle en [DISENO-WEB.md](DISENO-WEB.md#radar-nuevo--señales-en-movimiento).
- [ ] **B32.** Generación automática del gold standard del benchmark (`scripts/generate_gold.py`): Opus con thinking + Sonnet validador. Sin revisión humana. Output: `data/bench/gold_auto_v1.json` + discrepancias aparte. Coste una vez: ~3 €. Re-ejecutable en cada re-benchmark mensual. Telegram alerta con resumen.
- [ ] **B33.** Sistema de seguimiento: alertas Telegram puntuales + `private/bench-log.md` + `private/auditoria-log.md` + `private/self-review-log.md` + `data/bench/trends.csv` + `data/audit/trends.csv`. Tú no revisas nada activamente; el sistema escribe y avisa.

**Derivados del estudio de diseño (cerrado 2026-04-21, ver [ESTUDIO-DISENO.md](ESTUDIO-DISENO.md)):**

- [~] **B34.** Prototipo HTML estático en `docs/prototype/` (Paso 1 del plan §10). 4 páginas (home, edición, ficha actor, ficha propuesta) con datos reales W17 y los 9 componentes nuevos. **Entregado 2026-04-21 tarde y en revisión** — ver [memoria prototipo_paso1_en_pausa](../../.claude/projects/-Users-raulserrano-Documents-GitHub-ibiza-housing-radar/memory/prototipo_paso1_en_pausa.md). Pausado a petición del editor para estudiar arquitectura antes de seguir con B35 (Jekyll). Al retomar: (1) revisión visual del wordmark V2 Split en cabecera real, (2) comportamiento chips coalición 6 actores en mobile, (3) decisión barra progreso 8 estados siempre o solo aplicables.
- [ ] **B35.** Implementar **9 componentes nuevos** en Jekyll (partials + CSS): chrome operacional, numeración edición por fecha, tags tipográficos, card de propuesta, pill de estado + barra de progreso (8 estados), chip de actor (8 tipos), ficha actor con sidebar sticky, margin notes (Tufte), toggle Temporada/Pre-temporada/Histórico.
- [ ] **B36.** Formulario **"Escríbenos"** flotante universal (Formspree). Botón fijo esquina inferior derecha, visible en todas las páginas salvo confirmación. Campos: mensaje (obligatorio) + nombre y email (opcionales) + auto-captura de URL origen. Honeypot anti-spam. Mono + seams.
- [ ] **B37.** Página `/sistema/` interna con `noindex,nofollow` (documentación viva del sistema visual: paleta, tipografía, los 9 componentes renderizados). Solo para editor y colaboradores vía URL directa.
- [ ] **B38.** **Wordmark tipográfico finalizado** — elección de variante entre V1 mono plano / V2 split / V3 tri / V4 underline (ver `docs/prototype/logo/preview.html`). Logo gráfico descartado 2026-04-21; la identidad se resuelve enteramente con tipografía. Incluye favicon tipográfico (opciones a probar: `))`, `r))`, o iniciales `rvi`).
- [ ] **B39.** Automatización **OG images con Puppeteer** (Node.js en runner CI). Plantilla `docs/assets/og-template.html` + script `scripts/gen_og.mjs`. Generación por edición, ficha actor, ficha palanca. OG fallback estática.
- [ ] **B40.** Modo oscuro con **toggle manual ○/●** (localStorage) además del automático por `prefers-color-scheme`. Sin opción "auto" explícita (default implícito al no tocar nada).

**Mejoras técnicas web:**

- [ ] **B19.** Accesibilidad (a11y): semántica HTML, contraste, alt en imágenes, navegación por teclado, skip-links.
- [ ] **B20.** Responsive profundo verificado en 320, 375, 640, 768, 1024, 1280, 1920 px.
- [ ] **B21.** Modo oscuro mantenido y auditado tras los cambios.
- [ ] **B22.** Licencia CC-BY en footer.
- [ ] **B23.** Navegación revisada: top-nav y footer con enlaces nuevos.
- [ ] **B24.** Estilo editorial coherente entre páginas nuevas y existentes.
- [ ] **B25.** Botón "cómo citar esto" en cada edición.
- [ ] **B26.** Ediciones enlazadas entre sí (anterior/siguiente) para navegación y SEO.

### Bloque C — Contenido retroactivo (2 meses / 8 ediciones)

Detalle en [CONTENIDO-RETROACTIVO.md](CONTENIDO-RETROACTIVO.md). Decisión editor 2026-04-20: **borrar** W16-W17 actuales (no reescribir) y producir **8 ediciones** (W10-W17) bajo modelo nuevo.

- [ ] **C1.** Borrar W16-W17 antiguas del branch (preservadas en histórico git de `main`).
- [ ] **C2.** Adaptar `ingest.py` con parámetro `--window-start/--window-end` para ejecución retroactiva.
- [ ] **C3.** Producir W17 (20-26 abr) — primera en orden inverso.
- [ ] **C4.** Producir W16 (13-19 abr).
- [ ] **C5.** Producir W15 (6-12 abr).
- [ ] **C6.** Producir W14 (30 mar - 5 abr).
- [ ] **C7.** Producir W13 (23-29 mar) — arranca búsqueda manual.
- [ ] **C8.** Producir W12 (16-22 mar).
- [ ] **C9.** Producir W11 (9-15 mar).
- [ ] **C10.** Producir W10 (2-8 mar) — la más antigua, más trabajo manual.
- [ ] **C11.** Verificación manual de todas las URLs (8 ediciones).
- [ ] **C12.** Publicar balance retrospectivo inicial 2 meses en `/balance/`.
- [ ] **C13.** Nota metodológica visible en cada edición retroactiva: "Edición procesada a posteriori sobre archivo público de prensa, bajo el modelo documental del observatorio (activo desde 2026-04-20). Fechas y fuentes reales; fecha de publicación en el observatorio posterior a la semana cubierta."
- [ ] **C14.** Commits individuales por edición en orden cronológico (W10 primero, W17 último) para progresión limpia en git log.

### Bloque D — SEO masivo (pilar fundamental)

Detalle en [SEO.md](SEO.md).

**Elementos técnicos:**

- [ ] **D1.** `<title>` y `<meta description>` únicos y optimizados por página (ediciones, home, políticas, actores, propuestas, glosario).
- [ ] **D2.** Schema.org JSON-LD: `NewsArticle` por edición, `BreadcrumbList` en todas las páginas, `Organization` en home, `WebSite` con `potentialAction`.
- [ ] **D3.** Open Graph completo en `<head>`: `og:title`, `og:description`, `og:type`, `og:url`, `og:image`, `og:locale`, `og:site_name`.
- [ ] **D4.** Twitter Cards (`summary_large_image`).
- [ ] **D5.** Open Graph images generadas por edición (script Python con Pillow o SVG template). Plantilla: título + fecha + marca.
- [ ] **D6.** `sitemap.xml` completo con `lastmod` por página.
- [ ] **D7.** `robots.txt` explícito: allow all excepto `/private/` y `/Gemfile`.
- [ ] **D8.** RSS `feed.xml` con contenido completo de edición (no excerpt) para agregadores.
- [ ] **D9.** Canonical URLs por página.
- [ ] **D10.** Internal linking dirigido: cada edición enlaza a actores citados del directorio `/actores`, a propuestas relacionadas en `/propuestas`, a ediciones anterior/siguiente, al glosario cuando se menciona un término técnico.
- [ ] **D11.** URLs semánticas auditadas: `/ediciones/2026-wWW/`, `/actores/nombre-actor/`, `/propuestas/id-propuesta/`.
- [ ] **D12.** Verificación de sitio en Google Search Console (GitHub Pages soporta verificación con meta tag).
- [ ] **D13.** Verificación en Bing Webmaster Tools.
- [ ] **D14.** Performance: Core Web Vitals auditadas (LCP, INP, CLS). Jekyll estático ayuda; no introducir JS pesado.
- [ ] **D15.** Alt text descriptivo en todas las imágenes (incluyendo OG).
- [ ] **D16.** Keywords research por edición incorporado al prompt: la edición debe incluir los términos de búsqueda más probables del tema semanal en título, H1 y primeros párrafos.

**Contenido estratégico long-tail:**

- [ ] **D17.** Página `/explica/sa-joveria` — qué es, dónde está, qué colectivos viven allí, cronología, propuestas en circulación, ediciones que la cubren.
- [ ] **D18.** Página `/explica/ibavi` — qué es, competencias, programas activos, enlaces oficiales.
- [ ] **D19.** Página `/explica/llei-habitatge-baleares` — resumen de la Llei 5/2018, qué cubre, qué no.
- [ ] **D20.** Página `/explica/alquiler-turistico-ibiza` — marco normativo, diferencia legal/ilegal, multas, historia reciente.
- [ ] **D21.** Página `/explica/vivienda-temporera` — qué diferencia tiene con el alquiler ordinario, problemas típicos, actores relevantes.
- [ ] **D22.** Identificar 5-10 long-tail adicionales tras análisis de Search Console a los 2 meses.

### Bloque E — Analítica y métricas

- [ ] **E1.** GoatCounter configurado en todas las páginas (script ligero sin cookies).
- [ ] **E2.** Panel privado de métricas en `private/metricas.md` generado mensual con tráfico + corpus editorial + operaciones.
- [ ] **E3.** Dashboard de costes ampliado con estimaciones, tendencias, alertas de desviación (ver A15).
- [ ] **E4.** Dashboard público `/costes/` con agregados mensuales.
- [ ] **E5.** Verificación del sitio en Google Search Console + Bing Webmaster Tools (solapa con D12, D13).
- [ ] **E6.** Integración Search Console → página `/estadisticas/` con top queries, top páginas, posición media por trimestre.

### Bloque F — Distribución inicial

- [ ] **F1.** Newsletter Buttondown (gratis <100 subs) **modelo gratis** en Fase 0. Formulario de suscripción en home y pie de cada edición. Modelo de pago/híbrido se evalúa en Fase 2 — ver [ESTUDIOS-PENDIENTES.md #4](ESTUDIOS-PENDIENTES.md#4-newsletter-de-pago-vs-gratis-vs-híbrido).
- [ ] **F2.** Envío automático del lunes 10:00 CEST con la edición completa. GitHub Action.
- [ ] **F3.** ⏸ Bot Bluesky — **fuera de Fase 0 por decisión editor**. Estudio en [ESTUDIOS-PENDIENTES.md #5](ESTUDIOS-PENDIENTES.md#5-redes-sociales--estrategia-antes-de-activar). Fase 1.
- [ ] **F4.** ⏸ Bot Mastodon — mismo criterio. Fase 1.
- [ ] **F5.** Lista curada de contactos directos (15-25 personas): periodistas de vivienda (Diario de Ibiza, Periódico de Ibiza, elDiario.es Baleares, Ara Balears, El País delegación Baleares), gabinetes Consell y ayuntamientos, Cáritas, GEN-GOB, sindicatos (CCOO, UGT, PIMEEF), CAEB, IBAVI.
- [ ] **F6.** Email manual de relanzamiento a la lista curada el día del lanzamiento de Fase 0 (desde formulario de contacto + BCC, sin email propio hasta tener dominio).

### Bloque G — Utilidad pública (diferenciador directo)

- [ ] **G1.** ⏸ `/recursos` — **fuera de Fase 0 por decisión del editor 2026-04-20**. Estudio previo en [ESTUDIOS-PENDIENTES.md #3](ESTUDIOS-PENDIENTES.md#3-página-recursos--qué-incluir-y-cómo-verificar). Lanzamiento Fase 1.
- [ ] **G2.** `/glosario` con los 30-50 términos más relevantes del corpus actual.
- [ ] **G3.** Directorio de colectivos ciudadanos y asociaciones relevantes en Ibiza/Formentera.
- [ ] **G4.** Kit de prensa en `/cita-esto` con descripción corta/larga, logo, cómo citar en formato APA y Chicago, contacto por formulario.

### Bloque I — Estudios previos bloqueantes

Tras las decisiones del editor 2026-04-20, estos estudios se ejecutan antes o durante Fase 0. Detalle completo en [ESTUDIOS-PENDIENTES.md](ESTUDIOS-PENDIENTES.md).

- [ ] **I1.** 🔴 **URGENTE** — Estudio integración 3 modelos (Haiku + Sonnet + Opus) + benchmark + código actualizado. Primera semana.
- [ ] **I2.** Estudio dominio propio: shortlist de nombres, disponibilidad, registrador, plan migración. 2ª semana.
- [ ] **I3.** Confirmación de fecha de relanzamiento (propuesta: lunes 18 may 2026). Esta semana.
- [ ] **I4.** Diseño del dashboard de estadísticas potente + página `/estadisticas/` complementaria a `/balance/`. Durante Fase 0.
- [ ] **I5.** Implementación de elementos de [Solar Low-Tech](https://solar.lowtechmagazine.com/) — ver [DISENO-WEB.md §Inspiración](DISENO-WEB.md). Indicadores de transparencia en footer + notas al margen + manifiesto + `/estado/`. Durante Fase 0.
- [x] **I6.** ✅ **Estudio de diseño completo** cerrado 2026-04-21. Entregable: [ESTUDIO-DISENO.md](ESTUDIO-DISENO.md) (14 secciones, 13 decisiones D1-D13 cerradas con OK del editor, salvo D2 logo diferido). Incluye: benchmark editorial con 13 referentes, sistema visual completo con 8 tipos de actor, 9 componentes especificados, plan de prototipo en 6 pasos, decisiones sobre nombre ("Radar Ibiza"), calendario editorial (opening/closing), numeración por fecha, formulario universal "Escríbenos", automatización anual para temporadas. Derivadas en B34-B40 y A17.
- [ ] **I7.** Wordmark tipográfico final: el editor elige variante entre V1-V4 de [`docs/prototype/logo/preview.html`](docs/prototype/logo/preview.html). Logo gráfico descartado 2026-04-21. Tras elección, formalizar favicon tipográfico + variantes de uso.

### Estudios diferidos (no bloquean Fase 0)

- Página `/recursos/` — ver [ESTUDIOS-PENDIENTES.md #3](ESTUDIOS-PENDIENTES.md#3-página-recursos--qué-incluir-y-cómo-verificar). Fase 1.
- Modelo de newsletter pago vs gratis vs híbrido — ver [ESTUDIOS-PENDIENTES.md #4](ESTUDIOS-PENDIENTES.md#4-newsletter-de-pago-vs-gratis-vs-híbrido). Fase 2.
- Redes sociales — ver [ESTUDIOS-PENDIENTES.md #5](ESTUDIOS-PENDIENTES.md#5-redes-sociales--estrategia-antes-de-activar). Fase 1.

### Bloque H — Legal y transparencia

- [ ] **H1.** `/politica-editorial` publicada con las 5 reglas duras del observatorio ([CLAUDE.md](CLAUDE.md#reglas-fundacionales)).
- [ ] **H2.** `/metodologia` reescrita bajo el nuevo modelo: modelos Haiku + Opus, pipeline en una página, sesgos declarados, política de verificación.
- [ ] **H3.** `/correcciones` inicializada vacía, con formato estándar.
- [ ] **H4.** `/aviso-legal` mínimo: titular del sitio, contacto, jurisdicción.
- [ ] **H5.** `/financiacion` con estado real: tiempo voluntario del editor, coste directo ~2-3 €/mes en API Anthropic costeado por Raúl Serrano.
- [ ] **H6.** Licencia CC-BY en footer y documentada en metodología.
- [ ] **H7.** `/datos-abiertos` con descarga del CSV de todas las propuestas documentadas.

---

## Fase 1 — Consolidación (4-8 semanas tras Fase 0)

Objetivo: validar el modelo documental con datos reales y empezar a construir tracción.

- [ ] Envío personalizado a lista curada de periodistas con cada edición.
- [ ] Seguimiento semanal de GoatCounter y ajustes SEO según las búsquedas reales.
- [ ] Ajuste del prompt tras 4+ ediciones bajo el modelo nuevo (cuando haya datos reales para calibrarlo).
- [ ] Primera auditoría trimestral de balance, publicada.
- [ ] Ajustes de UX según feedback real.
- [ ] Primer "Balance temporada" si toca (cierre de ciclo).
- [ ] Evaluar dominio propio si se cumplen criterios de tracción (ver PLAN.md).

## Fase 2 — Datos propios (8-12 semanas tras Fase 1)

- [ ] Observatorio de precios Vía A (agregación fuentes oficiales).
- [ ] Observatorio de precios Vía B (crowd-sourcing ciudadano con umbral).
- [ ] Página `/precios` con agregados y CSV descargable.
- [ ] Cobertura Formentera (fuentes adicionales).

## Fase 3 — Red y escala (3-6 meses tras Fase 2)

- [ ] Consejo editorial honorífico (3-5 personas con credibilidad local).
- [ ] Evento anual co-organizado con entidad local (UIB Ibiza, Cáritas, sindicatos).
- [ ] BOIB watcher (scraping BOIB filtrado por keywords).
- [ ] Serie multi-semana "Balance temporada 2026".

## Fase 4 — Trilingüe (diferido con criterios)

Detalle y criterios de reactivación en [PLAN.md](PLAN.md).

## Fase 5 — Monetización (diferido, roadmap 2027+)

Detalle en [PLAN.md](PLAN.md) sección Monetización.

---

## Tabla de seguimiento — Fase 0

| Bloque | Tarea | Prioridad | Estado |
|---|---|---|---|
| A | A1. Prompt documental | crítica | ✅ cerrado (merge 21-abr) |
| A | A2. Schema classify ampliado | crítica | ✅ cerrado |
| A | A3. `extract.py` | crítica | ✅ cerrado |
| A | A4. `verify.py` bloqueante | crítica | ✅ cerrado |
| A | A5. `rescue.py` | alta | ✅ cerrado |
| A | A6. `balance.py` | alta | ✅ cerrado |
| A | A7. Adaptación `report.py` | crítica | ✅ cerrado |
| A | A8. Tests básicos | alta | pendiente (no hay `tests/` todavía) |
| A | A9. Prompt caching Opus | media | ✅ cerrado |
| A | A10. Resiliencia classify | media | ✅ cerrado |
| A | A11. Métricas pipeline | media | ✅ cerrado |
| A | A12. `self_review.py` | alta | ✅ cerrado |
| A | A13. `quarterly_audit.py` | media | ⏸ diferido |
| A | A14. `model_rebench.py` | media | ⏸ diferido |
| A | A15. Dashboard costes ampliado | media | pendiente |
| A | A16. Tope blando 12 € | crítica | ✅ cerrado (duro subido a 50 € en 21-abr) |
| A | PI2-A. Archivado append-only | alta | ✅ cerrado 21-abr (`archive.py`) |
| B | B1. Home dual | crítica | pendiente |
| B | B2. `/politica-editorial` | crítica | pendiente |
| B | B3. `/metodologia` reescrita | crítica | pendiente |
| B | B4. `/balance` | alta | pendiente |
| B | B5. `/actores` | alta | pendiente |
| B | B6. `/propuestas` tracker | alta | pendiente |
| B | B7. `/glosario` | alta | pendiente |
| B | B8. `/correcciones` | alta | pendiente |
| B | B9. `/como-usarlo` | alta | pendiente |
| B | B10. `/recursos` | **alta (diferenciador)** | pendiente |
| B | B11. `/contacto` Formspree | alta | pendiente |
| B | B12. `/acerca` reescrita | media | pendiente |
| B | B13. `/cita-esto` kit prensa | alta | pendiente |
| B | B14. `/aportar` formulario precios | media | pendiente |
| B | B15. `/datos-abiertos` | media | pendiente |
| B | B16. `/financiacion` | media | pendiente |
| B | B17. `/aviso-legal` | media | pendiente |
| B | B18. 404 personalizado | baja | pendiente |
| B | B19. Accesibilidad | alta | pendiente |
| B | B20. Responsive auditado | alta | pendiente |
| B | B21. Modo oscuro auditado | media | pendiente |
| B | B22. CC-BY footer | alta | pendiente |
| B | B23. Navegación revisada | crítica | pendiente |
| B | B24. Estilo coherente | alta | pendiente |
| B | B25. Botón "cómo citar" | media | pendiente |
| B | B26. Anterior/siguiente ediciones | alta | pendiente |
| B | B27. `/sin-dato/` | alta | pendiente |
| B | B28. `/auditoria/` | media | pendiente |
| B | B29. `/costes/` público | media | pendiente |
| B | B30. `/estado/` | alta | pendiente |
| B | B31. `/radar/` | alta | pendiente |
| B | B34. Prototipo HTML estático | crítica | 🟡 entregado + en revisión (pausado 21-abr tarde) |
| B | B35. 9 componentes en Jekyll | crítica | pendiente |
| B | B36. Formulario "Escríbenos" | alta | pendiente |
| B | B37. Página `/sistema/` interna | media | pendiente |
| B | B38. Wordmark tipográfico (V1-V4) | alta | **pendiente editor** |
| B | B39. OG images con Puppeteer | alta | pendiente |
| B | B40. Toggle modo oscuro manual | media | pendiente |
| A | A17. `update_temporadas.py` | media | pendiente |
| I | I6. Estudio de diseño | crítica | ✅ **cerrado 2026-04-21** |
| I | I7. Wordmark tipográfico (V1-V4) | alta | **pendiente editor** |
| C | C1. Decisión W16-W17 | crítica | **pendiente editor** |
| C | C2. Ingest W14 | crítica | pendiente |
| C | C3. Pipeline W14 | crítica | pendiente |
| C | C4. Revisión y publicación W14 | crítica | pendiente |
| C | C5. W15 completo | crítica | pendiente |
| C | C6. Reescritura W16 | condicional | pendiente editor |
| C | C7. Reescritura W17 | condicional | pendiente editor |
| C | C8. Verificación URLs | crítica | pendiente |
| C | C9. Balance inicial `/balance` | alta | pendiente |
| C | C10. Nota metodológica | alta | pendiente |
| D | D1. Meta tags por página | crítica | pendiente |
| D | D2. Schema.org JSON-LD | crítica | pendiente |
| D | D3. OG `<head>` | crítica | pendiente |
| D | D4. Twitter Cards | alta | pendiente |
| D | D5. OG images generadas | alta | pendiente |
| D | D6. `sitemap.xml` | crítica | pendiente |
| D | D7. `robots.txt` | crítica | pendiente |
| D | D8. RSS completo | alta | pendiente |
| D | D9. Canonical URLs | crítica | pendiente |
| D | D10. Internal linking | alta | pendiente |
| D | D11. URLs semánticas | alta | pendiente |
| D | D12. Google Search Console | crítica | pendiente |
| D | D13. Bing Webmaster Tools | alta | pendiente |
| D | D14. Core Web Vitals | alta | pendiente |
| D | D15. Alt text imágenes | alta | pendiente |
| D | D16. Keywords en prompt | alta | pendiente |
| D | D17. `/explica/sa-joveria` | alta | pendiente |
| D | D18. `/explica/ibavi` | alta | pendiente |
| D | D19. `/explica/llei-habitatge-baleares` | media | pendiente |
| D | D20. `/explica/alquiler-turistico-ibiza` | alta | pendiente |
| D | D21. `/explica/vivienda-temporera` | alta | pendiente |
| E | E1. GoatCounter | crítica | pendiente |
| E | E2. Panel métricas privado | media | pendiente |
| F | F1. Newsletter Buttondown | alta | pendiente |
| F | F2. Envío lunes automático | alta | pendiente |
| F | F3. Bot Bluesky | alta | pendiente |
| F | F4. Bot Mastodon | media | pendiente |
| F | F5. Lista curada contactos | alta | pendiente |
| F | F6. Email de relanzamiento | alta | pendiente |
| G | G1. `/recursos` poblada | **crítica (cambio real)** | pendiente |
| G | G2. `/glosario` 30-50 términos | alta | pendiente |
| G | G3. Directorio colectivos | media | pendiente |
| G | G4. Kit de prensa | alta | pendiente |
| H | H1. Política editorial publicada | crítica | pendiente |
| H | H2. Metodología reescrita | crítica | pendiente |
| H | H3. Correcciones inicializada | alta | pendiente |
| H | H4. Aviso legal | media | pendiente |
| H | H5. Financiación pública | media | pendiente |
| H | H6. CC-BY documentada | alta | pendiente |
| H | H7. Datos abiertos CSV | media | pendiente |
