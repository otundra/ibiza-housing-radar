# Roadmap — Ibiza Housing Radar post-pivote

**Fecha:** 2026-04-20
**Origen:** [PIVOTE.md](PIVOTE.md).
**Principio base:** lanzar en Fase 0 todo lo que se pueda para que el relanzamiento del proyecto sea fuerte, coherente y memorable. Coste 0 externo salvo API Anthropic. Reversible vía branch aislado.

---

## Fase 0 — Relanzamiento completo

**Objetivo:** al terminar Fase 0, el observatorio es un producto cerrado que se puede compartir sin vergüenza con un periodista, un regidor, un sindicato o un temporero.

**Duración estimada:** 5-7 días a tiempo completo, o 3-4 semanas a 10 h/semana.

**Entregables mínimos:**

1. Pipeline técnico del pivote operativo.
2. 4 ediciones retroactivas publicadas (W14-W17) bajo el nuevo modelo.
3. 15+ páginas web nuevas o reescritas.
4. SEO técnico completo + keywords por edición.
5. Analítica sin cookies activa.
6. Newsletter y bots sociales operativos.
7. Política editorial pública con las 5 reglas duras.
8. Balance inicial retrospectivo publicado.

### Bloque A — Pipeline técnico del pivote

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
- [ ] **C13.** Nota metodológica visible en cada edición retroactiva: "Edición procesada a posteriori sobre archivo público de prensa, bajo modelo documental del pivote 2026-04-20. Fechas y fuentes reales; fecha de publicación en el observatorio posterior a la semana cubierta."
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
- [ ] **E2.** Panel privado de métricas en `private/metricas.md` generado mensual.
- [ ] **E3.** Dashboard de costes ya migrado (✅ hecho) — verificar que sigue coherente tras el pivote.

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

### Estudios diferidos (no bloquean Fase 0)

- Página `/recursos/` — ver [ESTUDIOS-PENDIENTES.md #3](ESTUDIOS-PENDIENTES.md#3-página-recursos--qué-incluir-y-cómo-verificar). Fase 1.
- Modelo de newsletter pago vs gratis vs híbrido — ver [ESTUDIOS-PENDIENTES.md #4](ESTUDIOS-PENDIENTES.md#4-newsletter-de-pago-vs-gratis-vs-híbrido). Fase 2.
- Redes sociales — ver [ESTUDIOS-PENDIENTES.md #5](ESTUDIOS-PENDIENTES.md#5-redes-sociales--estrategia-antes-de-activar). Fase 1.

### Bloque H — Legal y transparencia

- [ ] **H1.** `/politica-editorial` publicada con las 5 reglas duras del [PIVOTE](PIVOTE.md).
- [ ] **H2.** `/metodologia` reescrita bajo el nuevo modelo: modelos Haiku + Opus, pipeline en una página, sesgos declarados, política de verificación.
- [ ] **H3.** `/correcciones` inicializada vacía, con formato estándar.
- [ ] **H4.** `/aviso-legal` mínimo: titular del sitio, contacto, jurisdicción.
- [ ] **H5.** `/financiacion` con estado real: tiempo voluntario del editor, coste directo ~2-3 €/mes en API Anthropic costeado por Raúl Serrano.
- [ ] **H6.** Licencia CC-BY en footer y documentada en metodología.
- [ ] **H7.** `/datos-abiertos` con descarga del CSV de todas las propuestas documentadas.

---

## Fase 1 — Consolidación (4-8 semanas tras Fase 0)

Objetivo: validar el pivote con datos reales y empezar a construir tracción.

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
| A | A1. Prompt documental | crítica | pendiente |
| A | A2. Schema classify ampliado | crítica | pendiente |
| A | A3. `extract.py` | crítica | pendiente |
| A | A4. `verify.py` bloqueante | crítica | pendiente |
| A | A5. `rescue.py` | alta | pendiente |
| A | A6. `balance.py` | alta | pendiente |
| A | A7. Adaptación `report.py` | crítica | pendiente |
| A | A8. Tests básicos | alta | pendiente |
| A | A9. Prompt caching Opus | media | pendiente |
| A | A10. Resiliencia classify | media | pendiente |
| A | A11. Métricas pipeline | media | pendiente |
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
