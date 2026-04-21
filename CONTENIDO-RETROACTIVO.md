# Contenido retroactivo — 12 ediciones de febrero a abril 2026

**Fecha del plan:** 2026-04-20 · **Ampliado:** 2026-04-21 (de 8 → 12 semanas)
**Origen:** [PIVOTE.md](PIVOTE.md), [ROADMAP.md](ROADMAP.md) bloque C, decisiones del editor 2026-04-20 y 2026-04-21.
**Alcance:** producir 12 ediciones coherentes que cubran los últimos 3 meses (semanas ISO W06-W17 de 2026) bajo el modelo documental nuevo. Relanzamiento con 3 meses de rodaje visible.

---

## Actualización 2026-04-21 — Camino A + auditor IA

Decidido en la revisión Fase 0.5 ([REVISION-FASE-0.5.md](REVISION-FASE-0.5.md)):

- **Camino A confirmado:** las 12 ediciones se publican con fecha real (W06 del 2-8 feb hasta W17 del 20-26 abr) + banner *"procesada a posteriori bajo modelo documental"*.
- **Backfill técnico vía `src/backfill.py`** con Google News + RSS nativos + BOIB. Ventana: 12 semanas.
- **Auditoría automatizada (PI9)** sustituye la revisión humana exhaustiva. El editor revisa solo (a) propuestas marcadas `flagged` por el sistema de 5 capas (~15%) y (b) muestreo aleatorio del 10% de las auto-aprobadas.
- **Coste operativo cerrado:** ~3,50 € (backfill + auditor + pieza retroactiva Opus).
- **Tiempo editor estimado:** ~4 h, no 15 h.
- **Log de auditoría completo** en `data/audit/YYYY-wWW/` para defendibilidad legal ante cualquier impugnación posterior.

Las 12 ediciones alimentan simultáneamente:
- El archivo público de ediciones (`/ediciones/2026-wNN/`).
- La base de datos de `/propuestas/`.
- Las fichas de `/actores/`.
- El cálculo de `/balance/` (con 3 meses de datos reales desde día 1).
- El grafo de evolución de propuestas (PI3).
- Las omisiones retroactivas (`/omisiones/` si se aprueba en ED3).

---

## Decisión del editor

**Borramos las 2 ediciones actuales (W16-W17 en modelo antiguo)** — se eliminan del repo. Las originales quedan en el histórico git de `main` pre-merge para auditoría. El archivo público arranca 100% bajo modelo documental.

**Producimos 8 ediciones retroactivas** cubriendo marzo (W10-W13) y abril (W14-W17). Cada una con nota metodológica visible.

---

## Ventanas temporales (ampliado a 12)

| # | Edición | Semana ISO | Lunes | Domingo | Título | Contexto temporal |
|---|---|---|---|---|---|---|
| 1 | W06 | 2026-W06 | 2 feb 2026 | 8 feb 2026 | Semana 1 - Febrero 2026 | Cierre temporada 2025, primeros balances |
| 2 | W07 | 2026-W07 | 9 feb | 15 feb | Semana 2 - Febrero 2026 | Plenos municipales, presupuestos Q1 |
| 3 | W08 | 2026-W08 | 16 feb | 22 feb | Semana 3 - Febrero 2026 | Primeros anuncios pre-temporada |
| 4 | W09 | 2026-W09 | 23 feb | 1 mar | Semana 4 - Febrero 2026 | Cierre de mes, datos económicos |
| 5 | W10 | 2026-W10 | 2 mar | 8 mar | Semana 1 - Marzo 2026 | Pre-temporada, planificación institucional Q1 |
| 6 | W11 | 2026-W11 | 9 mar | 15 mar | Semana 2 - Marzo 2026 | Arrancan primeras ofertas de habitación |
| 7 | W12 | 2026-W12 | 16 mar | 22 mar | Semana 3 - Marzo 2026 | Debate público pre-Semana Santa |
| 8 | W13 | 2026-W13 | 23 mar | 29 mar | Semana 4 - Marzo 2026 | Cierre trimestre, publicación datos Q1 |
| 9 | W14 | 2026-W14 | 30 mar | 5 abr | Semana 1 - Abril 2026 | Semana Santa, pausa institucional |
| 10 | W15 | 2026-W15 | 6 abr | 12 abr | Semana 2 - Abril 2026 | Post-Semana Santa, tensión visible en mercado |
| 11 | W16 | 2026-W16 | 13 abr | 19 abr | Semana 3 - Abril 2026 | Movimiento sobre residencias para temporeros |
| 12 | W17 | 2026-W17 | 20 abr | 26 abr | Semana 4 - Abril 2026 | Desalojo sa Joveria a 2 semanas del arranque de temporada |

Las 12 ediciones conforman un arco narrativo extendido: **"del cierre de la temporada 2025 al desalojo de los asentamientos en vísperas de la temporada 2026"**. Lectura completa muestra al lector nuevo un producto maduro con 3 meses de cobertura real y continuidad editorial sólida.

---

## Veracidad y honestidad

Cada edición retroactiva lleva un callout visible en cabecera:

> *Edición procesada a posteriori sobre el archivo público de prensa de la semana indicada, bajo el modelo documental del pivote 2026-04-20. Las fechas de los hechos, URLs de las fuentes y declaraciones son reales y verificables. La fecha de publicación en el observatorio es posterior a la semana cubierta. Política editorial y metodología: [/politica-editorial/], [/metodologia/].*

**No se inventan:**

- Fechas de hechos.
- Actores ni declaraciones.
- URLs (todas llevan a fuente primaria publicada en la semana correspondiente).
- Precedentes (solo se citan cuando el actor los mencionó en su propia declaración original).

**Se declara con total transparencia:**

- Que las ediciones se produjeron el mismo día o los días siguientes al 2026-04-20.
- Que el pipeline técnico y el modelo editorial son los del pivote.
- Que el repositorio git contiene la traza completa de cuándo se crearon los archivos.

**Riesgo reputacional:** bajo. Cualquier auditor que quiera reconstruir nuestras semanas encuentra las mismas noticias en los mismos diarios. El único "tiempo no lineal" es el momento en que se empaqueta la edición.

---

## Proceso de generación

Por cada edición:

1. **Ingesta retroactiva** — `ingest.py --window-start {lunes} --window-end {domingo}` contra feeds actuales. Para W10-W13 (más de 3 semanas atrás) los RSS pueden devolver cobertura limitada. Se complementa con búsqueda manual en:
   - [Archivo Diario de Ibiza](https://www.diariodeibiza.es/) con filtro por fecha.
   - [Archivo Periódico de Ibiza](https://www.periodicodeibiza.es/) con filtro por fecha.
   - Google con operador `site:diariodeibiza.es after:YYYY-MM-DD before:YYYY-MM-DD vivienda`.
   - Google con operador análogo para `periodicodeibiza.es`, `lavozdeibiza.com`, `elpais.com`, `arabalears.cat`.
2. **Clasificación y extracción** con pipeline nuevo (módulos A1-A8 ya operativos).
3. **Rescate** — aplica a partir de W11 (la primera semana ya puede rescatar de W10).
4. **Generación** con Opus bajo prompt documental.
5. **Verificación** con `verify.py` — esperado: 0 fallos bloqueantes. Si aparecen, ajustar y reintentar.
6. **Revisión humana exhaustiva** — para ediciones retroactivas la revisión es más cuidadosa que para ediciones futuras en tiempo real. ~30-45 min/edición = 4-6 h total.
7. **Publicación** en `docs/_editions/2026-wNN.md` con `date` = lunes ISO.
8. **Commit individual** por edición: `report(2026-wNN): edición retroactiva bajo modelo documental`.

### Orden de producción

**Orden sugerido: hacia atrás desde la más reciente.**

1. W17 primero (datos más frescos, el pipeline los recuerda mejor).
2. W16.
3. W15.
4. W14.
5. W13 (primera edición con dificultad de cobertura RSS).
6. W12.
7. W11.
8. W10 (la más antigua, mayor trabajo manual esperado).

Ventajas de este orden:

- Las más fáciles primero. Experiencia acumulada para las más antiguas.
- El historial de propuestas crece hacia atrás pero `rescue.py` también puede trabajar "hacia adelante" cuando se publiquen en orden cronológico natural al archivo.
- Si algo falla en el pipeline, se detecta antes con W17 (reciente) que con W10 (lejana).

Tras producirlas todas, **se publican en orden cronológico natural** en git commits separados (W10 primero, luego W11, …, W17). Así el archivo muestra progresión limpia.

---

## Hipótesis por edición (antes de ejecutar el ingest)

Las hipótesis calibran expectativas. Si el ingest real se desvía mucho, señal de bug o de semana sin cobertura.

### W10 — Semana 1 - Marzo 2026

**Contexto:** arranque de marzo, pre-temporada. Planificación institucional Q1. Expectativas:

- Notas de prensa del Consell sobre planes 2026.
- Cierre de presupuestos municipales del año.
- Posibles primeras convocatorias IBAVI.
- Declaraciones de patronales sobre temporada (CAEB, PIMEEF).

Propuestas esperadas: 1-3. Temas posibles: residencias temporeros (propuesta recurrente de patronales y sindicatos), ampliación VPO, ajustes en ordenanzas municipales.

### W11 — Semana 2 - Marzo 2026

**Contexto:** primeras ofertas de habitación para temporada arrancan a publicarse (idealista, Milanuncios, Facebook Groups).

- Alertas de colectivos y Cáritas sobre precios.
- Posibles propuestas de sindicatos sobre alojamiento empresarial.
- Inicio del debate público anual.

Propuestas esperadas: 2-4. Primer rescate posible: propuestas de W10.

### W12 — Semana 3 - Marzo 2026

**Contexto:** semana anterior a Semana Santa (este año del 29 marzo al 5 abril). Actividad institucional intensa antes del parón.

- Plenos ordinarios con mociones sobre vivienda.
- Posibles anuncios sobre proyectos concretos.
- Datos trimestrales de IBESTAT / Ministerio si tocan.

Propuestas esperadas: 3-5.

### W13 — Semana 4 - Marzo 2026

**Contexto:** última semana antes de Semana Santa. Cierre Q1.

- Balances de enforcement Q1 (alquiler turístico ilegal).
- Declaraciones de cierre antes del receso.
- Últimas posiciones institucionales pre-receso.

Propuestas esperadas: 2-4.

### W14 — Semana 1 - Abril 2026 (30 mar - 5 abr)

**Contexto:** Semana Santa. Actividad institucional reducida pero actividad mediática alta (drama humano visible).

- Reportajes humanos (drama habitacional).
- Posibles acciones puntuales de servicios sociales con motivo de la Semana Santa.
- Poca propuesta formal, más omisiones (hecho sin propuesta).

Propuestas esperadas: 1-3. Edición posiblemente más corta y honesta.

### W15 — Semana 2 - Abril 2026 (6-12 abr)

**Contexto:** ya cubierto en corpus analizado (era la actualidad al momento del estudio).

Señales confirmadas (con URLs ya verificadas):

- 9-abr: oferta turística ilegal cae 70% (2.800 anuncios retirados, 14.500 plazas) — [Periódico de Ibiza](https://www.periodicodeibiza.es/pitiusas/ibiza/2026/04/09/2606075/desploma-oferta-ilegal-viviendas-turisticas-ibiza.html).
- 10-abr: habitación 3.500 €/mes temporada — [Diario de Ibiza](https://www.diariodeibiza.es/ibiza/2026/04/10/vivienda-ibiza-alquiler-habitacion-verano-128942285.html).
- 10-abr: inquilina realquila fraudulentamente — [Periódico de Ibiza](https://www.periodicodeibiza.es/pitiusas/ibiza/2026/04/10/2606451/otra-realidad-vivienda-ibiza-inquilina-deja-pagar-renta-realquila-piso-decenas-personas.html).
- 11-abr: dos sofás 500€ cada uno — [Periódico de Ibiza](https://www.periodicodeibiza.es/pitiusas/ibiza/2026/04/11/2606865/estupor-ibiza-ante-anuncio-dos-sofas-alquiler-por-500-euros-cada-uno-mismo-salon.html).
- 11-abr: patronales + sindicatos a favor de residencias — [Periódico de Ibiza](https://www.periodicodeibiza.es/pitiusas/ibiza/2026/04/11/2606853/patronales-sindicatos-favor-residencias-ibiza-para-trabajadores-temporada.html).
- 11-abr: Cáritas preocupada por desalojos — [Diario de Ibiza](https://www.diariodeibiza.es/ibiza/2026/04/11/preocupacion-caritas-ibiza-desalojo-asentamientos-128948679.html).

Propuestas esperadas: 3-5. Patronales+CCOO+UGT sobre residencias; Cáritas sobre realojo; posibles otras.

Omisiones esperadas: qué hacer con el mercado negro del subarriendo (caso documentado sin propuesta legislativa).

### W16 — Semana 3 - Abril 2026 (13-19 abr)

Señales confirmadas:

- 16-abr: plazo 7 VPO sa Penya abre — [Periódico de Ibiza](https://www.periodicodeibiza.es/pitiusas/ibiza/2026/04/16/2610695/plazo-para-optar-las-siete-vpo-penya-abre-este-viernes.html), [Diario de Ibiza](https://www.diariodeibiza.es/ibiza/2026/04/16/siete-viviendas-protegidas-ibiza-alquiler-129182651.html).
- 16-abr: infractores españoles residentes Baleares — [Periódico de Ibiza](https://www.periodicodeibiza.es/pitiusas/ibiza/2026/04/16/2610505/alquiler-turistico-ilegal-ibiza-infractores-son-espanoles-residentes-baleares.html).
- 17-abr: Consell retira 700 anuncios — [Diario de Ibiza](https://www.diariodeibiza.es/ibiza/2026/04/17/consell-retira-700-anuncios-129197215.html), [Ara Balears](https://es.arabalears.cat/sociedad/ibiza-consolida-control-alquiler-ilegal-260-expedientes-2025_1_5709512.html).
- 17-abr: TSJIB avala denegación licencia turística unifamiliar — [Periódico de Ibiza](https://www.periodicodeibiza.es/pitiusas/ibiza/2026/04/17/2610881/tsjib-avala-denegacion-licencia-turistica-vivienda-por-ser-unifamiliar-aislada.html).
- 2 M€ multas en 2 años — [OkDiario](https://okdiario.com/baleares/ibiza-recauda-mas-dos-millones-euros-dos-anos-multas-alquiler-vacacional-ilegal-16619680).

Propuestas esperadas: 3-5.

### W17 — Semana 4 - Abril 2026 (20-26 abr)

Señales confirmadas:

- 15-abr: testimonio sa Joveria preferir caravana — [Cadena SER](https://cadenaser.com/baleares/2026/04/15/lucia-residente-en-el-asentamiento-de-sa-joveria-vivo-mejor-en-mi-caravana-equipada-que-en-una-habitacion-compartida-por-mil-euros-radio-ibiza/).
- 19-abr: desalojo 200 personas anunciado — [El País](https://elpais.com/espana/2026-04-19/ibiza-desalojara-a-200-trabajadores-de-sus-asentamientos-a-las-puertas-de-la-temporada.html), [RTVE](https://www.rtve.es/play/videos/telediario-fin-de-semana/ibiza-desalojara-asentamientos-trabajadores/17031240/).
- Consell+patronales+sindicatos respaldan residencias — [La Voz de Ibiza](https://lavozdeibiza.com/ibiza/consell-patronales-y-sindicatos-respaldan-la-creacion-de-residencias-para-temporeros/).

Propuestas esperadas: 3-6. Edición probable con más volumen por la concurrencia de hechos.

---

## Balance retrospectivo inicial

Con 8 ediciones publicadas, `balance.py` corre por primera vez y produce el reparto inicial de 2 meses.

- 8 ediciones × 3-5 propuestas por edición = ~24-40 propuestas documentadas.
- Cobertura de actores esperada: Consell, 5 ayuntamientos, partidos (PP, PSOE, Més, Vox), sindicatos (CCOO, UGT), patronales (CAEB, PIMEEF, FEHIF), tercer sector (Cáritas, Cruz Roja, GEN-GOB), académicos (UIB), judicial (TSJIB).
- 24-40 es cantidad estadísticamente suficiente para detectar sesgos de actor y ajustar antes del lanzamiento público.

Balance se publica como "Balance Marzo-Abril 2026" en `/balance/` con nota: *"Balance retrospectivo de los primeros 2 meses del observatorio bajo el modelo documental. Ventana: 2-mar-2026 a 26-abr-2026."*

Si el reparto está muy desequilibrado, antes del relanzamiento se revisan:

- Criterios de admisión de propuestas.
- Fuentes RSS (posibles sesgos por qué medios leemos).
- Prompt de extracción (posibles sesgos al detectar "hay propuesta" vs "no la hay").

---

## Coste y tiempo estimados

**Coste API**:

- 8 × ~1,69 € (bajo reparto 3 modelos de [ESTUDIOS-PENDIENTES.md](ESTUDIOS-PENDIENTES.md)) = **~13,52 €**.
- Se ejecuta en 1-2 semanas concentradas.
- Si todo cae en el mes de abril: gasto total mes ≈ 16-18 € (≥ actual + retroactivos). **Cruza tope blando 8 €**, no corta (tope duro 20 €).
- Alternativa: distribuir ejecución en abril + primera semana mayo para mantener cada mes dentro de tope blando. Preferido si no hay prisa.

**Tiempo humano**:

- Ejecución pipeline: 2-3 h total (automático, con supervisión pasiva).
- Búsqueda manual complementaria W10-W13: 4-8 h (archivos de diarios).
- Revisión humana de cada edición: 30-45 min × 8 = 4-6 h.
- Total: **10-17 h** concentradas en 1-2 semanas.

---

## Riesgos del contenido retroactivo

1. **Cobertura incompleta de los feeds retroactivos.** RSS devuelve pocas semanas atrás. Mitigación: búsqueda manual obligatoria en W10-W13.
2. **Alucinación del extractor.** El LLM puede inferir propuestas donde no las hay si el texto es ambiguo. Mitigación: regla dura "URL obligatoria y statement_verbatim atribuible" en `extract.py`.
3. **Semanas "vacías".** Puede haber alguna semana con pocas noticias relevantes. Mitigación: plantilla "semana sin señal" ya existente + omisiones honestas.
4. **Coste temporal.** 10-17 h es bloque de trabajo significativo. Mitigación: ejecutar en paralelo a tareas de Bloque A-B.
5. **Percepción de "falsificación".** Mitigación: nota metodológica visible en cada edición retroactiva + entrada pública en `/correcciones/` describiendo el proceso del pivote.
6. **Cruce de tope blando 8 €.** No afecta al pipeline (no corta). Solo notifica. Asumible puntualmente.

---

## Plan B

Si durante la ejecución se descubre que W10-W13 tienen cobertura muy pobre (caso de que pre-marzo no haya actividad real suficiente), el plan de contingencia es:

- Publicar solo W11-W17 (7 ediciones).
- W10 se presenta como "semana sin señal" con nota específica.
- El arco narrativo arranca un poco más tarde pero sigue siendo completo.

No se degradará el modelo editorial por completar cuota. El principio "si no hay señal, lo decimos" es innegociable.
