# Estudio — Integración de fuentes oficiales en el observatorio

**Fecha de apertura:** 2026-05-08
**Estado:** abierto, en fase de brainstorming editorial
**Origen:** sesión 2026-05-08 con el editor. Pregunta detonante tras cerrar el bloque PI10/PI11/PI12/RT5: *"¿esto también mira en el BOIB de Baleares y demás, o todavía no estamos haciendo eso?"*. El editor decidió en la misma sesión: *"metemos integrar BOIB delante del backfill"*.

**Ámbito del estudio:** valorar si el observatorio debe integrar fuentes oficiales (BOIB, BOE Baleares, sedes electrónicas, IBAVI, CAIB, ayuntamientos pitiusos), con qué disciplina, en qué orden, y bajo qué patrones de uso. **No entra** en el cómo técnico de implementación — eso será el trabajo derivado de las decisiones que cierre este estudio.

**Sustituye y amplía:** RT22 ("Estudio de factibilidad BOIB", 2-4 h, originalmente apuntado en `ROADMAP.md` y `REVISION-FASE-0.5.md`). Lo que se planteaba como mini-estudio se convierte en estudio de fondo por insistencia del editor: *"no tenemos prisa, la prioridad es que creemos algo relevante"*.

**Sub-estudio derivado:** [ESTUDIO-CLASIFICADOR-OFICIAL.md](ESTUDIO-CLASIFICADOR-OFICIAL.md) — diseño del clasificador IA experto en derecho administrativo balear, con la frontera dura "cero supervisión jurídica humana del editor".

---

## 1. La visión del proyecto, recordada

Antes de evaluar nada, fijar la regla del juego. El observatorio se diseñó como **mapa documental de propuestas con autor identificado, URL verificable y trazabilidad**. Las cinco reglas fundacionales operan como filtro:

1. Solo propuestas con autor identificado y URL verificable.
2. El observatorio no genera propuestas propias.
3. Ningún actor queda excluido por filiación.
4. Balance auditado y publicado cada trimestre.
5. Correcciones públicas con traza.

Y la regla complementaria, fijada el 2026-04-21: **automatización máxima + veracidad pública**. El editor opera; no audita contenido a mano. El sistema se audita a sí mismo.

A esto se suma una segunda capa, recogida en la memoria del proyecto y en `EXPANSION-TEMATICA.md` §8: **no expandir sin formulación clara del problema y demanda orgánica manifiesta**. *"Si algo grita naturalmente ya lo oiremos como quien dice."*

Cualquier propuesta sobre fuentes oficiales se mide contra estas dos capas.

---

## 2. Datos verificados sobre el BOIB y otras fuentes oficiales

Investigación empírica del 2026-05-08, no suposiciones.

### 2.1 BOIB — Boletín Oficial de las Illes Balears

- **Frecuencia:** 3 boletines ordinarios por semana (martes, jueves, sábado) + extraordinarios cuando proceden.
- **5 secciones por boletín:** Disposiciones generales · Otras disposiciones · Contratación · Procedimientos judiciales · Anuncios.
- **RSS oficial existe:** `https://www.caib.es/eboibfront/indexrss.do?lang=es`. Pero **publica solo "BOIB Núm 058/2026"**, no disposiciones individuales. Cada item del feed lleva título genérico, link al sumario, fecha. Sin descripción, sin materia, sin organismo emisor en los metadatos del feed.
- **Búsqueda avanzada con campos:** sí permite filtrar por tipo de documento, organismo emisor, materia, rango de fechas. No hay API estructurada — el filtro va vía formulario web.
- **Archivo histórico:** desde 1997, accesible públicamente.
- **Formato:** sumario HTML por boletín; cada disposición individual en PDF.
- **Última edición consultada:** BOIB 057/2026 del 5 de mayo de 2026.

**Tipos de contenido recurrentes con material editorial para vivienda en Ibiza:**

- Convocatorias y bases reguladoras del IBAVI (ayudas al alquiler, Bono Alquiler Joven, listas de espera de vivienda pública, adjudicaciones). Ejemplo verificado: Orden 36/2024 de 7 de octubre.
- Decretos-ley del Govern Balear en vivienda. Ejemplo verificado: Decreto-ley 6/2023 de medidas urgentes en materia de vivienda.
- Acuerdos del Pleno del Consell d'Eivissa cuando tienen rango normativo (ordenanzas, planes territoriales, modificaciones del PTI).
- Resoluciones sancionadoras sobre alquiler turístico ilegal (HUT/ETV).
- Convocatorias municipales de los 5 ayuntamientos pitiusos (subvenciones al alquiler, ayudas a la rehabilitación). Ejemplo verificado: ayudas al alquiler del Ayuntamiento de Eivissa, anualidad 2021.
- Anuncios de información pública de planes urbanísticos, suelo dotacional, rehabilitación de barrios.

**Caso de actualidad política viva (mayo 2026) que demuestra el valor potencial del BOIB:**
PSOE/PSIB pide declarar Ibiza zona tensionada; PP (presidenta del Govern Marga Prohens y presidente del Consell Vicent Marí Triguero) se opone. Una declaración formal pasaría por el BOIB. La prensa lo cubre en términos de declaraciones políticas; el BOIB sería el árbitro autoritativo. Caso paralelo: noticia del 7 de mayo *"Prohens confirma que el local del alcalde de Ibiza no ha sido registrado como vivienda de precio limitado"* — el registro o no registro se acreditaría documentalmente vía BOIB / Registro de Vivienda.

### 2.2 BOE — Sección Baleares

- Publica normativa estatal con efecto en el archipiélago.
- RSS oficial por sección disponible.
- Frecuencia diaria.
- Ejemplo reciente verificado: Real Decreto 326/2026 de 22 de abril (Plan Estatal Vivienda 2026-2030); Real Decreto-ley 8/2026 de 20 de marzo sobre medidas en alquiler (tumbado por Congreso el 28 de abril).

### 2.3 CAIB — notas de prensa del Govern

- Web institucional de notas de prensa con RSS oficial.
- Publica antes que la prensa generalista en muchos casos.
- Cada nota es ya texto estructurado (título, fecha, organismo, cuerpo).

### 2.4 Sede electrónica del Consell d'Eivissa

- Existe en `seu.conselldeivissa.es`.
- **Sin RSS público encontrado** para órdenes del día del pleno o resoluciones.
- Acceso parcial vía portal del Consell (`conselldeivissa.es`).
- Material relevante verificable: el Consell encargó en marzo 2026 un estudio sobre viviendas vacías en la isla.

### 2.5 IBAVI — web institucional

- Sección en CAIB y web propia.
- Publica notas y resoluciones propias.
- **Sin RSS encontrado** en la indagación inicial.

### 2.6 Ayuntamientos pitiusos

- Cinco ayuntamientos: Eivissa, Sant Antoni de Portmany, Santa Eulària des Riu, Sant Josep de sa Talaia, Sant Joan de Labritja. Más Formentera (que sería ampliación geográfica futura).
- Sedes electrónicas individuales, sin RSS estandarizado.

### 2.7 Mapa de viabilidad técnica

| Fuente | RSS limpio | Granularidad RSS | Coste de filtrado |
|---|---|---|---|
| BOIB | sí | boletín entero | medio (procesar sumario + PDFs) |
| BOE Baleares | sí | sección específica | bajo |
| CAIB notas prensa | sí | nota a nota | bajo |
| Sede Consell d'Eivissa | no encontrado | — | alto (scraping) |
| IBAVI propia | no encontrado | — | alto (scraping) |
| Ayuntamientos pitiusos | no encontrado | — | alto (scraping) |

**Conclusión 2.7:** las tres fuentes técnicamente limpias son BOIB, BOE Baleares y CAIB notas de prensa. Las demás requieren scraping y no son prioritarias en una primera integración.

---

## 3. Encaje del BOIB con cada regla fundacional

### Regla 1 · Solo propuestas con autor identificado y URL verificable

El BOIB **refuerza la regla**, no la desafía. El autor sigue siendo el actor (Consell, IBAVI, Govern, ayuntamiento); cambia que la URL apunta a la fuente primaria normativa en lugar de a la cobertura periodística. La trazabilidad mejora: una resolución del BOIB es citable de forma inequívoca por número y fecha.

✅ **Encaje pleno. Es más documental, no menos.**

### Regla 2 · El observatorio no genera propuestas propias

Ninguna implicación. El BOIB documenta lo ya formulado por un actor con nombre. La extracción es la misma que hoy hace `extract.py` sobre prensa: identificar `actor`, `statement_verbatim`, `palanca`, `state`, etc. Las disposiciones del BOIB son por construcción "lo que un actor ha hecho público formalmente" — encaja exactamente en el modelo documental.

✅ **Encaje pleno.**

### Regla 3 · Ningún actor queda excluido por filiación

El BOIB es ciego a la filiación. Cualquier disposición de cualquier actor con potestad publicadora aparece. **Mejora la regla**: hoy el filtro implícito es *"qué decide cubrir la prensa local"*, que tiene su propio sesgo. La fuente primaria elimina ese filtro intermedio.

✅ **Encaje pleno, además fortalece.**

### Regla 4 · Balance auditado y publicado cada trimestre

Aquí hay un matiz importante. El balance hoy se calcula sobre `actor_type` (instituciones, partidos, sindicatos…). Si el BOIB añade volumen de disposiciones del Govern + Consell + ayuntamientos, **el bloque `institucional_publico` se infla casi mecánicamente**. Una orden de IBAVI que abre convocatoria es estructuralmente "una propuesta institucional" en la taxonomía actual — pero no compite en el mismo plano que una declaración pública de un sindicato pidiendo medidas.

**Dos formas de absorberlo sin romper el balance:**

- **Opción A:** tratar las disposiciones del BOIB como un nuevo `statement_type` propio (`oficial_normativo`), separado de `quote` y `reported`. Balance segregado por `statement_type`: una columna de prensa, otra de fuente oficial. No se mezclan.
- **Opción B:** introducir un nuevo tipo de output, "decisión documentada" (≠ "propuesta documentada"), con su propia sección en la edición y su propia página `/decisiones/`. La diferencia material es que una propuesta no se ha ejecutado todavía; una decisión BOIB ya está vigente.

La Opción B es más fiel a la realidad del corpus y refuerza la Regla 4 (no infla artificialmente el balance), a cambio de un cambio editorial mayor (sección nueva en la edición).

⚠️ **Encaje viable con ajuste. El balance se reformula, no se rompe.**

### Regla 5 · Correcciones públicas con traza

El BOIB es la fuente primaria que **resuelve** correcciones, no las genera. Si la prensa reporta mal una cifra de una orden del Govern, la fuente BOIB es la verificación canónica.

✅ **Encaje pleno; el BOIB se convierte en árbitro.**

### Regla complementaria · Automatización máxima + veracidad pública

Aquí está el nudo real. El BOIB no requiere auditoría humana (es texto oficial) — pero requiere **clasificación automática fiable** sobre PDFs y sumarios HTML que no están pensados para indexación temática. La calidad del filtrado IA pasa a ser crítica, porque ya no hay un periodista que haya pre-filtrado por uno.

Hoy el observatorio confía en la prensa para descartar ruido (un decreto sobre gestión interna del IBAVI nunca llega a Diario de Ibiza). Sin ese filtro humano externo, el clasificador propio tiene que distinguir:

- *Convocatoria pública de ayudas al alquiler* → relevante.
- *Modificación de la RPT del IBAVI* → ruido (gestión interna).
- *Plan especial del PTI sobre suelo dotacional* → relevante (tarda en aparecer en prensa).
- *Anuncio de notificación a particular por sanción* → ruido (caso individual sin valor agregado).

Esto no rompe la regla, pero **carga la responsabilidad sobre el clasificador IA**. El sistema de tiers cerrado en PI10 (2026-05-08) es la red de seguridad: las disposiciones que el auditor no resuelva con confianza alta van a cuarentena. Pero la cuarentena no puede sostener el 30% del volumen — sería ingobernable.

⚠️ **Encaje condicional. Requiere que el clasificador IA sobre fuente oficial dé una precisión muy razonable desde el día uno.** Esto es testeable empíricamente con una semana de muestra antes de comprometerse — y es lo que aborda el sub-estudio del clasificador.

---

## 4. Encaje con la regla de "no expandir sin demanda orgánica"

El editor cerró esta regla el 2026-04-22 con texto inequívoco: *"si algo grita naturalmente ya lo oiremos"*. Aplicado al BOIB, hay que distinguir.

**El BOIB no es expansión temática.** Sigue siendo vivienda. La regla del editor habla de no abrir nuevos ejes (turismo, agua, movilidad) sin formulación clara del problema. El BOIB profundiza el mismo eje, no lo amplía.

Pero la disciplina subyacente — **no añadir capas que duplican esfuerzo sin demanda probada** — sí aplica parcialmente. Pregunta honesta: ¿alguien está reclamando hoy información oficial primaria de la que el observatorio carece? Respuesta empírica:

- Tráfico real medido: cero. La web no tiene analítica todavía.
- Emails recibidos pidiendo información oficial: cero (no hay buzón abierto).
- Cobertura periodística citando huecos del observatorio: cero (no estamos en el radar de la prensa).

**No hay demanda orgánica probada.** Lo que sí hay es una **observación interna**: la regla complementaria del observatorio dice "automatización máxima + veracidad pública" — y la veracidad pública es más fuerte cuando se cita la fuente primaria que cuando se cita prensa que cita la fuente primaria. Esto es razonamiento desde la propia visión del proyecto, no demanda externa.

Lectura: el BOIB **no viola la regla de demanda orgánica** porque no expande temáticamente, pero tampoco está empujado por demanda externa real. Cae en una zona donde la decisión depende del coste-beneficio interno y de la propia visión del proyecto.

---

## 5. La pregunta nuclear del editor — y cómo reordena todo

El editor planteó textualmente: *"mi duda es que vamos a validar un proyecto sin una de sus patas, que considero que puede ser el BOIB"*.

Este argumento desactiva la recomendación procedimental anterior (*"esperar al cierre del Hito 1 antes de integrar"*). Si el BOIB es estructural — parte intrínseca de qué es el observatorio — entonces:

- Validar el observatorio sin BOIB no valida el observatorio real.
- Forzar el cierre del Hito 1 (auditor MVP) sobre un sistema sin BOIB lo deja con métrica incompleta.
- **Lo correcto es redefinir el Hito 1 para que incluya la integración del BOIB validada, no acelerarlo.**

Adicionalmente, el editor confirmó *"no tenemos presión en sacar el proyecto, la prioridad es que creemos algo relevante"*. Eliminado el factor velocidad, los argumentos procedimentales pierden peso.

### 5.1 Confesión técnica: la "contaminación del auditor" era preocupación débil

La preocupación inicial *"integrar BOIB ahora arriesga la medición del auditor"* no resiste análisis honesto:

- **Tiers.** Las disposiciones del BOIB van a verde por construcción (URL del Govern siempre responde, trazabilidad organismo↔dominio trivial, verbatim literal, archivo Wayback innecesario). No estresan al auditor.
- **Cuarentena.** El BOIB no genera rojos en condiciones normales. No satura.
- **Contradicciones entre capas.** Las disposiciones del BOIB son texto oficial — la extracción Haiku y la verificación Sonnet leen el mismo texto literal. No hay margen de discrepancia interpretativa.
- **Balance público.** Sí hay efecto: las disposiciones del Consell, Govern e IBAVI inflarían mecánicamente el bloque institucional. Pero esto es **decisión editorial** (la Opción B de la Regla 4 lo resuelve), no contaminación de medición.

**Conclusión veraz:** lo llamado "contaminación" era preocupación procedimental disfrazada de técnica. La medición del Hito 1 sobre el flujo actual sigue corriendo en paralelo sobre el corpus de prensa, y el BOIB añadiría una vía de entrada nueva que el auditor procesa de forma estable.

---

## 6. La frontera dura — "cero supervisión jurídica humana del editor"

Otro pilar que el editor fijó en la sesión: *"no sé de asuntos jurídicos, ni tengo idea de leer textos técnicos de este tipo (ni me interesan). Esto debe ir tan fino hilado que no tenga que hacer nada al respecto"*.

Esta frontera es no negociable. Cualquier diseño que requiera al editor leer textos jurídicos rutinariamente está **descartado por construcción**. Implicaciones:

- **No puede haber etiquetado humano del editor.** Las propuestas iniciales del estudio (*"te llevaría 2-3 horas etiquetando 50-100 disposiciones"*) chocan de frente con esta frontera y quedaron descartadas.
- **El conjunto de prueba del clasificador se genera con sistema IA experto interno**, no con humano editor. Detalle en `ESTUDIO-CLASIFICADOR-OFICIAL.md`.
- **La calibración rutinaria del clasificador es 0 horas/mes del editor.**
- **Si el sistema falla, la respuesta correcta es parar el módulo BOIB**, no aumentar el tiempo humano.

### 6.1 Lo que sí puede hacer falta — y quién lo absorbe

Honestidad pura: hay un escenario donde se necesita criterio jurídico humano externo. Pasaría si:

1. Una disposición clasificada como "material" provoca corrección externa que demuestra error.
2. La corrección se valida.
3. El caso se acumula con otros similares formando patrón.

Cuando eso ocurra (probablemente raro), **no es el editor quien dictamina**. Es:

1. **Asesor jurídico puntual externo.** Abogado especializado en derecho administrativo balear contratado por horas sueltas. Tarifa típica 80-150 €/hora. Si se usa 1 hora cada 6 meses para revisar un lote acumulado de 5-10 casos fronterizos → coste ~160-300 €/año = ~15-25 €/mes prorrateado. **Opcional y reactivo, no recurrente.**
2. **Alternativa más barata si el editor desarrolla red:** algún actor aliado de los listados en `/recursos/` (Cáritas, sindicatos, GEN-GOB) suele tener jurista propio dispuesto a revisar 5 minutos por buena voluntad. La Fase 4 del plan general contempla un consejo editorial honorífico — un jurista en ese consejo cierra esta vía sin coste.
3. **Alternativa nula:** asumir el error, corregir vía el canal `/correcciones/` cuando llegue, ajustar el clasificador con el caso etiquetado. No contratar nada. Vía válida mientras el flujo de correcciones externas sea bajo.

**La frontera "el editor no lee nada técnico" se mantiene en los tres escenarios.** Lo que cambia es de dónde sale el criterio externo cuando hace falta.

### 6.2 La frontera irreducible — lo que ningún sistema absorbe

Tres cosas no se automatizan al 100% en ningún proyecto editorial. Ninguna carga al editor con trabajo rutinario, pero existen:

1. **Decisión de qué historias merecen subir a la edición semanal vs. quedarse en `/normativa/`.** Editorial, no jurídica. Se resuelve con regla automática: las disposiciones del Govern Balear y del Consell d'Eivissa con palanca normativa o instrumento económico suben a edición; el resto vive solo en `/normativa/`. Si la regla es buena, no requiere intervención. Si falla, la regla se ajusta.
2. **Cambios estructurales del propio BOIB.** Si en el futuro el BOIB cambia de plataforma, añade tipos de acto nuevos, o modifica el formato de PDF, el ingesta-parser puede romperse. Trabajo técnico, no del editor — aparecería como fallo del pipeline en Telegram.
3. **Correcciones recibidas por el canal público.** La regla 5 fundacional pone al editor como responsable, en cualquier caso — con BOIB o sin BOIB. No es carga nueva. Cambia que algunas correcciones podrían ser jurídicas en lugar de periodísticas; ahí entra el asesor puntual o la red del consejo editorial.

Ninguna de las tres es trabajo recurrente.

---

## 7. Cambios estructurales que requeriría la integración

### 7.1 Pipeline de ingesta

Hoy `ingest.py` lee feeds RSS, dedup por URL, vuelca a `data/ingested.json`. Con BOIB:

- Nuevo módulo `ingest_boib.py` (o ampliación) que lee el RSS BOIB, descarga cada sumario nuevo, parsea la lista de disposiciones por sección, descarga el cuerpo (PDF o HTML), extrae texto plano.
- Filtrado por palabras clave en cuerpo (lista similar a la actual: vivienda, habitatge, IBAVI, alquiler, urbanism, PTI, HUT/ETV).
- Volcado al mismo `data/ingested.json` con `kind: oficial` para que el resto del pipeline lo procese.

**Esfuerzo:** 1 día sólido para feed + parser + filtrado básico. Otro día para gestionar PDFs (algunos tienen OCR pobre). Mantenimiento bajo si la estructura HTML del BOIB no cambia.

### 7.2 Schema de propuesta

El schema actual (`ARQUITECTURA.md` §3) sirve casi tal cual. Cambios mínimos:

- Nuevo enum en `statement_type`: `oficial_normativo` (junto a `quote` y `reported`).
- Nuevo campo opcional `boib_ref` con número, fecha y sección.
- En `viability_legal`: cuando viene del BOIB, se rellena `alta` automáticamente con razón *"vigente, publicada en BOIB"* — la propia disposición es la prueba de viabilidad jurídica.

### 7.3 Tiers y verificación

El árbol de tiers de PI10 funciona casi sin cambios. Una disposición BOIB:

- `url_ok` = 100% (servidor del Govern).
- `traza_dominio_actor` = automática (caib.es ↔ Govern, conselldeivissa.es ↔ Consell).
- `wayback_snapshot` = innecesario (BOIB es archivo permanente por ley).
- `verbatim_match_ratio` = 1.0 trivialmente (extracción literal del texto oficial).
- Resultado por defecto: **verde**. Es el tipo de fuente que el sistema premia con confianza máxima.

**Esto simplifica la auditoría, no la complica.**

### 7.4 Edición semanal y web

Aquí el cambio editorial es real. Dos caminos:

- **Camino mínimo:** las disposiciones BOIB entran en la sección "Propuestas en circulación" como cualquier otra propuesta, distinguidas con badge visual *"📜 fuente oficial"*. Riesgo: dilución del balance (Regla 4).
- **Camino correcto:** sección nueva en la edición, *"📜 Lo publicado en boletines"*, con tabla compacta. Página propia `/normativa/` o `/oficial/` con tracker filtrable, similar a `/propuestas/`. Refuerza que el observatorio diferencia "lo propuesto" de "lo publicado", y mantiene el balance limpio.

El camino correcto es ~2-3 días en plantillas Jekyll + ajustes al generador. Encaja en Fase 4 (bloque B web) que está en pausa.

### 7.5 Coste API marginal

Volumen estimado de disposiciones BOIB relevantes para vivienda:

- ~10-25 disposiciones/semana en BOIB que pasan filtro de keywords.
- Tras clasificación: ~5-15/semana realmente sobre vivienda.
- Tras extracción: ~3-8 propuestas/decisiones nuevas/semana.

**Coste IA marginal estimado: +0,30-0,50 €/mes.** Bien dentro del tope blando de 12 €.

---

## 8. Ventajas concretas (5)

Ordenadas por peso real, con ejemplo verificable de cada una.

**1. Cierra agujeros donde la prensa no llega.**
La sanción a un alquiler turístico ilegal solo aparece en prensa si es escandalosa o el periodista tira del hilo. En BOIB aparecen todas. Lo mismo con plazos de convocatorias de IBAVI, modificaciones de bases reguladoras, planes territoriales que cambian sin que Diario de Ibiza los cubra. Hay un área de propuestas e instrumentos públicos que el observatorio actualmente no documenta porque la prensa no los cita.

**2. Resuelve disputas vivas con autoridad.**
Caso real de mayo 2026: ¿está Ibiza declarada zona tensionada? La prensa lo discute desde hace meses. El BOIB es el árbitro: o aparece la resolución del Govern, o no aparece. Si el observatorio integra BOIB, puede afirmar con autoridad documental: *"a fecha X, ningún acto en BOIB declara zona tensionada en Ibiza"*. Hoy solo puede decir *"según el periodista Y…"*.

**3. Adelanta hechos que la prensa cubre con retraso.**
Una orden de IBAVI con bases reguladoras nuevas se publica un martes en BOIB; Diario de Ibiza lo cubre el viernes (a veces el lunes siguiente). El observatorio podría ser el primer lugar donde aparece estructurado, no el último. Esto es propuesta de valor real para periodistas: *"si quieres saber qué hay en BOIB de vivienda esta semana, ya filtrado y resumido, lo tienes aquí"*.

**4. Refuerza la regla complementaria — automatización máxima + veracidad pública.**
La cadena `actor → propuesta → URL` se acorta. Hoy: *Consell propone X, según Diario de Ibiza, que enlaza al pleno*. Con BOIB: *Consell publica X en BOIB Núm. NNN/2026*. Un paso menos de mediación = mayor veracidad pública demostrable.

**5. Da material a las páginas `/explica/` y al SEO long-tail.**
`DISENO-WEB.md` planea páginas tipo `/explica/llei-habitatge-baleares/`, `/explica/ibavi/`, `/explica/alquiler-turistico-ibiza/`. Estas páginas viven mejor con citas BOIB embebidas (texto literal + número de boletín) que con citas de prensa. **El BOIB es la materia prima natural del contenido evergreen del observatorio.**

---

## 9. Inconvenientes y riesgos honestos (5)

**1. Carga el clasificador IA con responsabilidad nueva.**
Sin filtro periodístico previo, el clasificador tiene que distinguir lo material (orden de subvenciones) de lo administrativo interno (modificación de RPT, nombramientos). Riesgo: 20-30% de las disposiciones que entran al pipeline son ruido. La cuarentena no puede absorber ese volumen.
**Mitigación:** estudio dedicado del clasificador (ESTUDIO-CLASIFICADOR-OFICIAL.md) con prompt específico para BOIB + ejemplos negativos claros + filtro previo por sección del BOIB.

**2. Mantenimiento del parser PDF.**
Algunos PDFs del BOIB tienen OCR pobre, especialmente los más antiguos. Si una disposición clave no se parsea bien, la calidad del extract baja. Es deuda técnica acumulada — cada N meses habrá que ajustar el parser.
**Mitigación:** empezar leyendo solo el sumario HTML (que va bien) + texto descriptivo de cada disposición. PDF cuerpo solo cuando el sumario apunte a algo material — segunda fase.

**3. Editorialmente cambia el tono del observatorio.**
Hoy el observatorio cita prensa que cita actores. Eso es lectura natural para el público no técnico. Si pasa a citar boletines oficiales con número y fecha, el tono se vuelve más jurídico-administrativo. Riesgo de espantar al "primer visitante no técnico" que `DISENO-WEB.md` define como la mitad del público objetivo.
**Mitigación:** la edición sigue priorizando el resumen en lenguaje claro; el BOIB va como fuente, no como protagonista. Sección dedicada `/normativa/` para el lector profesional, sección "📜 Lo publicado" en la edición compacta para el general. Esta es la **arquitectura dual de información** que hay que cerrar antes de tocar código (subestudio pendiente).

**4. Solapamiento parcial con prensa que ya integramos.**
Una orden importante saldrá en BOIB el martes y en Diario de Ibiza el viernes. Si el pipeline las trata como propuestas distintas, dedup falla y aparece dos veces. Si las funde, hay que resolver "cuál es la fuente canónica".
**Mitigación:** regla clara — cuando exista BOIB, BOIB es la fuente primaria y la prensa pasa a `additional_sources`. El extract.py ya tiene la mecánica de consolidar; hay que extender la heurística de dedup.

**5. La integración cambia la naturaleza del proyecto.**
El observatorio pasa de comentario sobre prensa a herramienta documental con autoridad jurídica. Esto cambia el tono y atrae un perfil de lector diferente. El diseño dual amortigua el efecto, pero el riesgo está.
**Mitigación:** el sub-estudio de arquitectura dual cierra esto antes de tocar código. Las maquetas del camino correcto demuestran cómo se mantienen los dos públicos.

---

## 10. Estimación de costes (cifras concretas)

### A. Coste recurrente mensual de IA

| Concepto | Estimación mensual |
|---|---|
| Filtrado por sección + palabras clave (sin IA) | 0 € |
| Panel cruzado del clasificador (Opus + Sonnet + Haiku sobre ~50-100 disposiciones/semana) | 1,50-2,50 € |
| Validador Sonnet sobre las que pasan a "material" | 0,40-0,60 € |
| Extractor de ficha estructurada (mismo módulo actual, más volumen) | 0,30-0,50 € |
| Verificador Opus puntual para casos fronterizos | 0,30-0,50 € |
| **Suma BOIB recurrente** | **2,50-4,00 €/mes** |
| Coste actual del proyecto (sin BOIB) | ~6-7 €/mes |
| **Total proyectado tras integración** | **~9-11 €/mes** |

Sigue dentro del tope blando vigente (12 €). El tope duro (50 €) ni se acerca.

### B. Coste de implementación inicial (una vez)

| Fase | Tiempo de trabajo | Coste tokens IA |
|---|---|---|
| Estudio 1 — clasificador oficial | 2-3 días | 1-2 € |
| Estudio 2 — arquitectura dual | 1 día | 0,20 € |
| Estudio 3 — prueba en seco | 1 día | 0,50-1 € |
| Implementación ingesta + parser BOIB | 2-3 días | 0,30 € |
| Implementación clasificador + integración pipeline | 2-3 días | 0,50 € |
| Sección editorial + página `/normativa/` + tracker | 2-3 días | 0,30 € |
| Validación con primera edición real integrada | 1 semana observación | 0,20 € |
| **Total inicial** | **~10-13 días** | **~3-5 € tokens** |

**Tiempo del editor:** 0-1 hora total, repartida en 2-3 momentos de revisión visual de maquetas y decisión de continuar/parar tras cada estudio. **Cero lectura de textos jurídicos.**

### C. Coste del backfill retroactivo si se decide hacer

Si tras integración se decide reprocesar 12 semanas pasadas para que el archivo sea coherente:

- ~600-1.200 disposiciones BOIB del periodo W06-W17.
- Procesamiento completo con panel cruzado: **3-6 € de tokens IA**.
- Una sola vez.

### D. Coste de mantenimiento humano recurrente

| Concepto | Tiempo del editor mensual |
|---|---|
| Revisar ediciones con sección BOIB integrada (igual que ahora) | sin cambio |
| Calibrar clasificador rutinariamente | **0 horas** |
| Leer disposiciones BOIB | **0 horas** (regla absoluta) |
| Asesor jurídico externo si llegan correcciones | 0 horas del editor; ~15-25 €/mes prorrateado *si* se decide contratar — opcional |
| Corregir errores técnicos del parser | 0 horas del editor; aparecen como fallo Telegram |

**Cero horas de mantenimiento jurídico recurrente.** Si esto se rompe, la respuesta correcta es parar el módulo BOIB, no aumentar tiempo humano.

### E. Cifra única para resumir

Si se ejecuta todo:

- **Una vez:** ~12-15 días de trabajo de implementación + ~5-10 € de tokens.
- **Cada mes a partir de entonces:** +3-4 € de IA sobre la factura actual = ~10 €/mes total.
- **Tiempo recurrente del editor:** 0 horas.

Sin coste oculto adicional salvo si se decide contratar asesoría jurídica externa puntual.

---

## 11. Modo "cuarentena agresiva" al inicio

Para que la frontera "cero supervisión humana" no se convierta en *"hemos publicado tres errores jurídicos antes de darnos cuenta"*, el módulo BOIB nace en modo cuarentena agresiva las primeras 4-6 semanas:

1. Toda disposición clasificada como material entra al pipeline pero **no se publica directamente en edición**. Va a `/revision-pendiente/` (cuarentena pública existente, cerrada en PI11) marcada como `pendiente_validacion_oficial`.
2. La edición semanal cita la cuarentena de forma agregada: *"Esta semana 4 nuevas disposiciones del BOIB entran en revisión pública"*, con enlace a `/revision-pendiente/`.
3. Si tras 2-3 semanas ningún caso recibe corrección externa que demuestre error, el modo se relaja: las disposiciones con consenso fuerte del panel pasan directas a edición; solo las dudosas quedan en cuarentena.
4. Si llega una corrección que demuestra error material → caso entra al conjunto de prueba como ejemplo negativo, el clasificador se re-calibra automáticamente, modo cuarentena agresiva se mantiene una semana más.

**Esta gradación protege la autoridad documental del observatorio sin pedir vigilancia activa al editor.** La cuarentena pública ya tiene la regla de archivo a 60 días — el sistema absorbe los casos no resueltos sin intervención.

---

## 12. Riesgo residual honesto

Lo peor que puede pasar tras seguir todo el recorrido con disciplina:

1. **El panel IA tiene un sesgo común no detectado** y clasifica sistemáticamente mal un tipo de disposición. Probabilidad: baja pero no nula. Mitigación: el modo cuarentena agresiva inicial + canal `/correcciones/` activo. Cuando aparezca el primer reporte externo, el caso se identifica y se ajusta el prompt.
2. **Volumen del BOIB sobrecarga la cuarentena.** El umbral de 20 propuestas pendientes ya genera alerta en el sistema actual. Si BOIB satura, llegará Telegram. Mitigación: ajustar filtros previos por sección. No carga humana — trabajo técnico reactivo.
3. **El asesor externo no aparece cuando se necesita.** Si llega corrección compleja y no hay jurista accesible, el caso queda como "pendiente de revisión" en cuarentena pública el tiempo necesario. La regla 5 (correcciones públicas con traza) se cumple igual: *"caso reportado, en revisión, pendiente de criterio jurídico externo"*. Esto es honesto y no daña la credibilidad — la mata el silenciamiento, no la lentitud.
4. **El proyecto cambia de naturaleza al integrar BOIB.** El observatorio pasa de comentario sobre prensa a herramienta documental con autoridad jurídica. El diseño dual amortigua el efecto, pero el riesgo está. Mitigación: el sub-estudio de arquitectura dual cierra esto antes de tocar código.

Ninguno de estos riesgos obliga al editor a leer textos técnicos. Ninguno carga con horas recurrentes.

---

## 13. Brainstorming — siete patrones de uso del BOIB

Petición explícita del editor (sesión 2026-05-08, último turno largo): *"hazme un brainstorming profundo sobre múltiples maneras de poder aplicar el BOIB al proyecto sin ser una fuente más como hacemos con prensa"*.

### 13.1 Cinco principios que filtran las ideas

Antes de listar, fijar el principio que las hila a todas. Si convertimos el BOIB en una entrada más al pipeline de prensa, lo despojamos de su valor único: que no es un comentario sobre la realidad, **es la realidad jurídica**. La prensa cuenta lo que pasa; el boletín establece lo que es. Esa diferencia no se aprovecha si todo termina en la misma "Propuesta nº 17" de la edición semanal.

Cinco principios sirven de filtro:

1. **El BOIB nunca genera una pieza editorial propia en la edición semanal.** Vive adyacente.
2. **La voz del BOIB se mantiene como dato y referencia**, nunca como narrativa redactada.
3. **El usuario general nunca aterriza en él directamente.** El profesional sí.
4. **El procesamiento es diferido**, no compite por el pipeline del lunes.
5. **Sus salidas alimentan estructuras paralelas**, no la sección estrella.

### 13.2 Patrón 1 — Espejo de promesas (verificación silenciosa)

**Idea nuclear.** Cada propuesta documentada en la edición semanal arrastra un campo invisible al lector general pero útil para el sistema: `verificado_en_boletin: pendiente | si | no`. Cuando la propuesta llega al boletín, el campo cambia automáticamente. La edición semanal no se modifica; la ficha permanente de la propuesta se enriquece sola.

**Variantes:**
- **A · Mínima.** Campo cruzado en la ficha, visible como icono pequeño *"📜 publicada"* en `/propuestas/{id}/`.
- **B · Activa.** Cuando una propuesta lleva 6 meses con `pendiente` y el actor es uno de los grandes (Govern, Consell, IBAVI), aparece automáticamente en la sección "🗄 Rescate" de la edición correspondiente con la nota *"propuesta hace 6 meses, sin reflejo aún en boletín oficial"*.

**Ventaja.** Convierte el observatorio en sistema de seguimiento del cumplimiento sin redactar una palabra extra. La presión sobre los actores se ejerce por contraste documental, no por opinión editorial.

**Riesgo.** Requiere matching robusto entre lo que dice una propuesta de prensa y lo que aparece en boletín — una orden puede salir con título distinto al anuncio en rueda de prensa.

**Esfuerzo.** Bajo. ~3 días.

### 13.3 Patrón 2 — Detector de silencios

**Idea nuclear.** Lo importante a veces no es qué entra al boletín — es qué nunca entró. Registro público autónomo, separado de la edición semanal, llamado *"Promesas sin reflejo oficial"*. Lista de propuestas anunciadas en prensa que llevan más de N meses sin aparecer en boletín, con fecha del anuncio, actor, y nota *"sin reflejo en boletín a fecha X"*.

**Variantes:**
- **A · Tabla simple.** Página `/sin-reflejo/` con filtros por actor, palanca y antigüedad. Auto-generada cada lunes tras el cruce.
- **B · Cronología por actor.** Cada actor del directorio `/actores/` tiene una sección *"Promesas pendientes"* en su ficha.
- **C · Edición mensual paralela.** Newsletter o canal específico que cada mes envía *"Lo que se prometió en marzo y no llegó al boletín"*. Producto distinto de la edición semanal.

**Ventaja.** Material editorial profundamente original. Ningún medio local sostiene una vigilancia documental así. Crea ángulo diferenciador que la prensa no puede replicar (su economía de atención no se lo permite).

**Riesgo.** El observatorio se vuelve más "vigilante" que "documental". Hay que cuidar el tono — la regla 2 dice que no proponemos. Lo que sí podemos hacer es reflejar ausencia documentada. La línea es fina.

**Esfuerzo.** Medio. ~5 días.

### 13.4 Patrón 3 — Árbitro reactivo de disputas vivas

**Idea nuclear.** El BOIB no se procesa rutinariamente para alimentar el pipeline. Se activa cuando aparece una controversia política viva que la prensa no resuelve por sí misma. Ejemplo del momento: *"¿está Ibiza declarada zona tensionada?"*. El sistema detecta la pregunta como pendiente y consulta el boletín como árbitro.

**Variantes:**
- **A · Manual con asistencia.** Cuando un lector escribe al canal de contacto preguntando *"¿qué pasa con X?"*, el sistema asiste con consulta automática al boletín y devuelve respuesta documentada. Función de buzón inteligente.
- **B · Automática.** El clasificador de prensa detecta cuando una disputa lleva varias semanas sin resolución (PSOE pide X, PP responde Y, sin avance). En la edición de esa semana se incluye un bloque "📜 ¿qué dice el boletín?" con la respuesta documental.
- **C · Suscripción a vigilancia.** Página `/vigilancia/` donde el lector se suscribe a temas concretos. Cuando hay novedad en boletín, recibe aviso. El observatorio funciona como infraestructura de alerta personalizada.

**Ventaja.** Resuelve la regla 2 elegantemente: el observatorio cita autoridad, no opina. Crea utilidad pública directa — el ciudadano que pregunta tiene respuesta sin esperar a que un periódico la cubra.

**Riesgo.** Si la lógica que decide qué es disputa viva falla, el módulo pierde valor rápido.

**Esfuerzo.** Medio-alto en variante B. Bajo en A. ~5-8 días según variante.

### 13.5 Patrón 4 — Materia prima de contenido evergreen

**Idea nuclear.** Las páginas `/explica/` que el diseño web ya plantea (sa Joveria, IBAVI, ley de vivienda, alquiler turístico) son contenido evergreen — viven aparte de la edición semanal y se nutren de revisiones periódicas. El BOIB se convierte en su materia prima privilegiada: cada vez que aparece algo del tema en boletín, la página correspondiente se actualiza automáticamente con la nueva referencia, sin tocar la edición semanal.

**Variantes:**
- **A · Cronología legal por tema.** Cada `/explica/` lleva una sección *"Recorrido en boletines"* — cronología auto-generada con todos los hitos normativos del tema. Crece sola con el tiempo.
- **B · Estado regulatorio actual.** Cada `/explica/` lleva una sección *"Qué está vigente ahora"* — auto-actualizada cuando una norma del tema entra o sale. Termómetro vivo del marco legal.
- **C · Páginas `/cronologia/` autónomas.** Series temáticas independientes: *"El alquiler turístico en Ibiza, 2008-2026"*, con las 30-40 normas relevantes ordenadas, cada una con resumen en lenguaje claro y enlace al texto oficial.

**Ventaja.** Contenido SEO long-tail de altísima calidad documental con esfuerzo editorial cero por entrada nueva. **Mejor retorno acumulado a largo plazo del catálogo.** Cada disposición que aparece en boletín deja huella en una página existente y mejora su autoridad.

**Riesgo.** Las cronologías generadas automáticamente pueden incluir disposiciones técnicas irrelevantes que rompen el flujo de lectura. El filtro tiene que ser muy bueno.

**Esfuerzo.** Alto en infraestructura inicial, bajo después. ~7-10 días arranque, casi cero mantenimiento.

### 13.6 Patrón 5 — Termómetro de cumplimiento institucional

**Idea nuclear.** El observatorio gana una dimensión que hoy no tiene: medir, no solo documentar. Cada actor institucional (Consell, ayuntamientos, Govern, IBAVI) recibe una puntuación visible *"X de Y propuestas hechas en prensa han pasado a boletín en los últimos 12 meses"*. Métrica fría, transparente, citable. Se publica trimestralmente con la auditoría.

**Variantes:**
- **A · Score discreto en `/actores/{slug}/`.** Cada ficha de actor incluye un indicador de cumplimiento documental con desglose por palanca.
- **B · Página `/cumplimiento/` pública.** Tabla pública con el ranking de cumplimiento por actor institucional. Generada trimestralmente, citable por la prensa.
- **C · Métrica integrada en la edición semanal.** Cuando un actor cae bajo cierto umbral (menos del 20% de cumplimiento documental en 90 días), aparece nota en la sección "🕳 Omisiones" de la edición. Sin opinión: dato.

**Ventaja.** Da al observatorio un papel de **infraestructura de rendición de cuentas**, no solo de documentación. Esto puede atraer la primera cita en prensa que la fase 2 del plan general persigue. Es el rasgo diferenciador más claro.

**Riesgo.** Riesgo metodológico real: medir cumplimiento normativo correctamente es difícil. Una propuesta puede no llegar al boletín por razones legítimas (rechazo democrático, modificación legal del proyecto, fusión con otra norma). Si la métrica no maneja matices, se vuelve injusta y pierde autoridad.

**Pregunta abierta delicada:** ¿la regla 3 (ningún actor excluido por filiación) admite que se mida a actores con criterio público? Lectura: la regla dice no excluir por filiación, no que no se mida. Pero la frontera importa y debe revisarse antes de implementar este patrón.

**Esfuerzo.** Alto. Requiere los patrones 1 y 2 funcionando bien + diseño metodológico cuidadoso. ~12-15 días.

### 13.7 Patrón 6 — Capa estructurada de cambio de estado

**Idea nuclear.** El esquema actual de las propuestas tiene un campo `state` con valores *propuesta · en_movimiento · en_debate · aprobada · en_ejecucion · implementada · descartada*. Hoy ese campo lo decide el extractor en el momento de procesar una noticia, y rara vez se actualiza después. El BOIB pasa a ser **el motor automático de actualización del campo de estado**: cuando una propuesta documentada aparece publicada en boletín, su `state` salta automáticamente a `aprobada` o `implementada` con marca de fecha y referencia.

**Variantes:**
- **A · Pasiva.** El cambio se aplica solo si el sistema detecta el cruce con confianza alta. Las dudas quedan como están.
- **B · Activa.** El cambio se aplica con todos los matches dudosos pero queda visible una nota *"estado actualizado por cruce automático con boletín — revisar si el cruce es exacto"*. Activa la mecánica de correcciones públicas existente sin invadir al editor.

**Ventaja.** Resuelve un problema interno conocido: las propuestas se quedan congeladas en su estado original mucho después de haber evolucionado. El boletín es la fuente legítima del cambio de estado, no un periodista.

**Riesgo.** El matching erróneo aquí es más caro que en otros patrones — un cambio de estado falso da por implementada una propuesta que no lo está. Hace falta umbral alto de confianza y la variante B con marca visible.

**Esfuerzo.** Medio. ~5 días.

### 13.8 Patrón 7 — Infraestructura de servicio para terceros

**Idea nuclear.** El observatorio deja de ser solo un medio de lectura y se convierte también en **infraestructura que otros usan**. El BOIB filtrado y estructurado por temas de vivienda en Ibiza se publica como conjunto de datos abierto descargable y como API ligera consultable. Periodistas, sindicatos, investigadores universitarios y particulares pueden construir encima.

**Variantes:**
- **A · Conjunto de datos abierto.** Página `/datos-abiertos/` con descarga de los conjuntos generados. Licencia abierta. Sin consulta interactiva.
- **B · Boletín de novedades.** Newsletter o canal específico que reenvía cada semana lo nuevo del boletín filtrado por vivienda en Ibiza, con resumen automático. Suscriptores: la lista de periodistas y profesionales que la fase 2 del plan general ya identifica.
- **C · Buscador público.** Página `/buscar/` con búsqueda por palabra clave sobre el archivo histórico de disposiciones publicadas.

**Ventaja.** Crea utilidad para colectivos profesionales sin obligar al observatorio a hacer su trabajo por ellos. **Lo más "infraestructura pública" del catálogo.** Encaja con la naturaleza de transparencia radical del proyecto.

**Riesgo.** Si el conjunto de datos contiene errores, se propagan a quienes lo usen. Hay responsabilidad reputacional en abrir API o conjunto de datos. Requiere disciplina de versionado y notas de cambios.

**Esfuerzo.** Bajo en variante A (export estático). Medio en B. Alto en C. 3-15 días según variante.

---

## 14. Combinaciones especialmente potentes

Algunas parejas se refuerzan más que la suma de sus partes.

**1 + 2 · Espejo + Silencios.** El campo de verificación cruzada (1) alimenta automáticamente el archivo de promesas sin reflejo (2). Una sola pieza de infraestructura, dos productos editoriales distintos. **El más eficiente del catálogo.**

**4 + 6 · Evergreen + Cambio de estado.** Las páginas explica se actualizan no solo por nuevas disposiciones sino también porque las propuestas que cubren cambian de estado al aparecer en boletín. La sensación de "página viva" se multiplica. Bueno para SEO sostenido.

**1 + 5 · Espejo + Cumplimiento.** El score de cumplimiento institucional sale gratis cuando ya tenemos espejo de promesas funcionando. El paso de uno al otro es agregación estadística. Permite empezar conservador (1) y graduar a métrica pública (5) cuando hay corpus suficiente.

**3 + 7B · Árbitro + Boletín a profesionales.** Cuando el sistema detecta una disputa viva y produce respuesta documental, la respuesta sale también por el canal de envío directo a periodistas. La función de árbitro se convierte en servicio activo a la prensa local. Combinación muy alineada con la fase 2 del plan general.

---

## 15. Tabla resumen para decidir

| Patrón | Cambio estructural | Esfuerzo inicial | Coste IA recurrente | Visible al lector general | Visible al profesional |
|---|---|---|---|---|---|
| 1 · Espejo de promesas | bajo | 3 días | bajo | indirecto (icono) | sí (campo en ficha) |
| 2 · Detector de silencios | medio | 5 días | bajo | sí (página propia) | sí |
| 3 · Árbitro reactivo | medio-alto | 5-8 días | medio | sí (cuando hay disputa) | sí |
| 4 · Materia evergreen | alto en infraestructura, bajo después | 7-10 días | bajo | sí (páginas explica) | sí (cronologías) |
| 5 · Termómetro cumplimiento | alto | 12-15 días | medio | sí (página pública) | sí (auditorías) |
| 6 · Cambio de estado automático | medio | 5 días | bajo | indirecto | sí |
| 7 · Infraestructura servicio | variable según variante | 3-15 días | bajo | no | sí (alta) |

---

## 16. Lectura propuesta del catálogo

Sin presionar. Notas de Claude para discusión con el editor.

**El más subestimado: patrón 1 (espejo de promesas).** Menor esfuerzo, mayor retorno acumulado, ningún riesgo editorial real, abre la puerta a varios otros (2, 5, 6 dependen de él). Es el primer movimiento natural. No genera contenido nuevo aparente pero cambia la naturaleza interna del observatorio.

**El más diferenciador: patrón 2 (detector de silencios).** Material editorial que ningún otro medio puede producir con la economía de atención que tienen. Si hubiera que elegir un solo producto editorial nuevo del catálogo BOIB, este es el ganador. La frase *"el observatorio que documenta lo que no llega"* posiciona el proyecto de forma única.

**El más arriesgado y más ambicioso: patrón 5 (termómetro de cumplimiento).** Tiene el potencial de generar la primera cita en prensa que el plan general persigue, pero también el riesgo más alto si la metodología no es sólida. Reservar para un segundo paso, cuando los patrones 1 y 2 lleven 3-6 meses funcionando y hayan generado el corpus de cruces necesario.

**El más infraestructural: patrón 7B (boletín a profesionales).** Encaja perfecto con la fase 2 del plan general. Convierte al observatorio en algo que los periodistas usan, no algo que leen. Esto cambia incentivos a largo plazo.

**Posibles a dejar fuera por ahora:**
- Patrón 3 variante B (árbitro automático en edición). Demasiada lógica nueva para arrancar; mejor empezar por 3A (manual con asistencia) cuando llegue el primer email a través del canal de contacto.
- Patrón 5C (métrica integrada en edición semanal). Demasiado intrusivo si la metodología no está madura. La página propia (5B) sí, pero después de tener corpus.

---

## 17. Movimiento escalonado propuesto

Una secuencia escalonada que respeta *"no hay presión de tiempo"* y prueba el valor antes de comprometer trabajo grande:

**Movimiento 1, en 3-5 semanas:** patrones 1 + 2 juntos (comparten infraestructura). Resultado tangible: cada propuesta tiene campo de verificación, y existe `/sin-reflejo/` autónoma. Bajo riesgo editorial. Si en 2 meses no genera tráfico ni mención externa, sabremos que el ángulo no engancha y pararemos sin haber comprometido más.

**Movimiento 2, si el primero da señal positiva, en otras 3-4 semanas:** patrón 4 (materia evergreen alimentando explica). El observatorio gana profundidad SEO. Material de archivo creciendo solo.

**Movimiento 3, cuando haya 3-6 meses de corpus:** patrón 5B (termómetro de cumplimiento). Ya con datos para que la métrica sea robusta.

**Movimiento 4, paralelo y al ritmo del editor:** patrón 7B (canal a profesionales) cuando la fase 2 del plan general llegue al envío directo a periodistas.

Los patrones 3 y 6 quedan como segundo plano: se incorporan si emerge necesidad concreta (una disputa viva que repite, o un caso donde el `state` mal actualizado causa problema).

---

## 18. Cosas no decididas — preguntas abiertas para el editor

El estudio queda en este punto. Para cerrarlo y pasar a implementación, hay tres preguntas pendientes de respuesta del editor:

1. **¿De los siete patrones, cuáles le parecen alineados con la idea del proyecto y cuáles forzarían el observatorio en una dirección que no quiere?**
2. **¿La idea de "termómetro de cumplimiento institucional" — patrón 5 — encaja con la regla 3 (ningún actor excluido por filiación) o la complica?** Lectura honesta: la regla dice no excluir por filiación, no que no se mida. Pero la frontera importa.
3. **¿Empezamos por la combinación 1+2 como movimiento de prueba, o prefiere explorar otro punto del catálogo primero?**

Cuando el editor responda, este estudio cierra y se abren los sub-estudios de implementación correspondientes.

---

## 19. Próxima revisión y criterio de revocación

- **Próxima revisión:** al recibir respuesta del editor a las tres preguntas de §18.
- **Criterio de revocación del estudio:** si en cualquier punto del recorrido la prueba empírica del Estudio 3 (prueba en seco del clasificador) no pasa los criterios objetivos de éxito (precisión ≥85%, exhaustividad ≥80% — ver `ESTUDIO-CLASIFICADOR-OFICIAL.md`), se cierra el estudio sin integración. La empresa no es heroica; es honesta. Mejor un observatorio fiable basado en prensa que un observatorio ambicioso que escupe ruido normativo.

---

## 20. Trazabilidad — referencias cruzadas

- [ESTUDIO-CLASIFICADOR-OFICIAL.md](ESTUDIO-CLASIFICADOR-OFICIAL.md) — sub-estudio derivado
- [CLAUDE.md](CLAUDE.md#reglas-fundacionales) — 5 reglas duras + regla complementaria
- [DECISIONES.md](DECISIONES.md) — registro canónico de decisiones del proyecto
- [ARQUITECTURA.md](ARQUITECTURA.md) — pipeline técnico actual
- [DISENO-WEB.md](DISENO-WEB.md) — arquitectura de información de la web (los dos públicos)
- [PLAN.md](PLAN.md) — plan general (Fase 3.3 menciona "BOIB watcher" como contenido diferencial; este estudio lo amplía sustancialmente)
- [ROADMAP.md](ROADMAP.md) — roadmap V2 (RT22 reformulado por este estudio)
- [REVISION-FASE-0.5.md](REVISION-FASE-0.5.md) — auditoría fundacional (RT22 enlazado)
- [EXPANSION-TEMATICA.md](EXPANSION-TEMATICA.md) §8 — regla *"no expandir sin demanda orgánica"*
- [ESTUDIO-TIERS.md](ESTUDIO-TIERS.md) — sistema de tiers que el BOIB hereda
- [ESTUDIO-COSTES-AUDITOR.md](ESTUDIO-COSTES-AUDITOR.md) — sistema auditor IA al que se conecta
- Memoria del proyecto: `feedback_esperar_demanda_organica.md` (regla del editor 2026-04-22)
