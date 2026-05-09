# Estudio — Arquitectura dual de información para integración del BOIB

**Fecha:** 2026-05-09
**Tipo:** sub-estudio de implementación del Movimiento 1 del BOIB ([D42](DECISIONES.md)).
**Estudio padre:** [`ESTUDIO-FUENTES-OFICIALES.md`](ESTUDIO-FUENTES-OFICIALES.md).
**Sub-estudio paralelo:** [`ESTUDIO-CLASIFICADOR-OFICIAL.md`](ESTUDIO-CLASIFICADOR-OFICIAL.md).
**Origen:** §9 riesgos 3 y 5 + §17 movimiento 1 del estudio padre + [D42](DECISIONES.md).
**Alcance:** decidir cómo se reparte la información jurídica entre el público general (no técnico) y el profesional recurrente, en todos los canales del observatorio, sin que la integración del BOIB rompa la lectura del primero ni empobrezca la del segundo. Cierra con maquetas descritas y reglas duras de redacción.
**Lo que NO cubre:** clasificación técnica de disposiciones (sub-estudio paralelo). Implementación de código (siguiente fase). Patrón 5 — termómetro de cumplimiento (diferido a 3-6 meses por [D42](DECISIONES.md)).
**Estado:** abierto.

---

## Índice

1. Resumen ejecutivo
2. El problema concreto
3. Inventario de lugares afectados por la integración
4. Principios de la arquitectura dual
5. Capa por público
6. Capa por canal
7. Direccionamiento canónico de disposiciones
8. Anatomía de la ficha de propuesta con vínculo BOIB
9. Anatomía de la sección "📜 Lo publicado" en la edición semanal
10. Anatomía de la página `/normativa/`
11. Anatomía de la página `/sin-reflejo/`
12. Anatomía de la página de actor con dimensión BOIB
13. Estilo editorial — lenguaje claro vs cita técnica (con glosario)
14. Frontera con sistemas existentes (tiers, balance, correcciones)
15. Pruebas en maqueta — tres escenarios reales
16. Riesgos abiertos del sub-estudio (con apunte trilingüe)
17. Próxima revisión y criterio de revocación
18. Trazabilidad cruzada

---

## 1. Resumen ejecutivo

Este sub-estudio cierra una decisión que el estudio padre nombró pero no resolvió: cómo entra la información del BOIB en el observatorio sin que el "primer visitante no técnico" se sienta empujado a un boletín jurídico, y sin que el "profesional recurrente" se quede con un resumen que no le sirve de fuente. La respuesta es **una sola arquitectura de contenido con dos capas de lectura**: la cara general lee resumen en lenguaje claro siempre primero; la cara profesional accede al detalle normativo bajo demanda, sin fricción para quien lo busca. La separación es por *capa de lectura dentro del mismo contenido*, no por sitios distintos.

El sub-estudio cierra cuando se aceptan: **(a)** principios de la dualidad, **(b)** anatomías de los cinco componentes afectados (ficha de propuesta, sección semanal "Lo publicado", `/normativa/`, `/sin-reflejo/`, página de actor), **(c)** decisiones de canal (web, email, RSS, cara compartible, imprimible), **(d)** decisión de direccionamiento canónico de las disposiciones, **(e)** reglas duras de estilo editorial, **(f)** pruebas en maqueta de tres escenarios reales que demuestran que las dos capas conviven sin estorbarse.

---

## 2. El problema concreto

`DISENO-WEB.md §"Los dos públicos"` cierra una tabla operativa que define dos perfiles que el observatorio sirve: ciudadano de Ibiza con 30-90 segundos en móvil, y profesional (periodista, regidor, técnico, sindicalista, patronal) con 3-10 minutos en desktop. La tabla cierra con un principio: *"la home debe servir a ambos en la primera pantalla sin sacrificar a ninguno"*.

La integración del BOIB tensiona ese principio porque añade una capa nueva de información — la disposición normativa — que en su forma cruda (número de boletín, sección, artículo, fecha de publicación, organismo emisor) **es ininteligible para el primer público y de lectura obligada para el segundo**. Si se publica plana, espanta al general. Si se oculta, traiciona al profesional y desperdicia el principal valor diferenciador del Movimiento 1: poder anclar cada propuesta a su rastro normativo verificable.

El estudio padre nombró el riesgo dos veces: §9 riesgo 3 (*"editorialmente cambia el tono del observatorio"*) y §9 riesgo 5 (*"la integración cambia la naturaleza del proyecto"*). En ambos sitios la mitigación apuntada es la misma: arquitectura dual de información cerrada antes de tocar código. Eso es lo que cierra este documento.

La frontera dura del editor — *"cero supervisión jurídica humana"*, [D41](DECISIONES.md) — añade una restricción operativa: el sistema no puede asumir que el editor revise visualmente cada cita BOIB antes de publicar. La arquitectura dual tiene que ser lo bastante segura para que un fallo del clasificador (un BOIB mal etiquetado, un cruce equivocado) **no rompa la cara general** aunque el editor no lo haya visto.

---

## 3. Inventario de lugares afectados por la integración

Lugares del sistema donde una disposición BOIB puede aparecer, directa o indirectamente. Cada uno necesita decisión de qué se ve, en qué capa, y por defecto.

| Lugar | Qué cambia con la integración BOIB | Capa por defecto |
|---|---|---|
| Edición semanal — sección de propuestas | Cada ficha lleva nuevo campo `verificacion_normativa` con etiqueta visible (✅/❌/🟡) | General colapsada |
| Edición semanal — sección "📜 Lo publicado" | Bloque nuevo: resumen en lenguaje claro de las disposiciones BOIB de la semana | General |
| Ficha de propuesta `/propuestas/{id}/` | Campo `verificacion_normativa` + bloque expandible "Detalle normativo" | General colapsada, expandible |
| Página de actor `/actores/{slug}/` | Sección nueva "Promesas vs reflejadas" con ratio | General |
| Página de balance `/balance/` | Posible dimensión nueva "% propuestas con respaldo normativo" — decisión cargada (ver §14) | Pendiente decisión |
| Cuarentena `/revision-pendiente/` | Disposiciones BOIB en `pendiente_clasificacion` aparecen aquí también | Profesional |
| `/sin-reflejo/` (nueva) | Página completa del patrón 2 — promesas sin reflejo en BOIB | General |
| `/normativa/` (nueva) | Hogar profesional — listado completo de disposiciones | Profesional expandida |
| Newsletter (email) | Resumen de la edición + sección "Lo publicado" sin capa expandible | General |
| RSS (`/feed.xml`) | Resumen + enlace al detalle web | General |
| OG image / cara compartible | Título + bajada en lenguaje claro; nunca código BOIB en texto compartido | General |
| Versión imprimible / PDF de la edición | Todo expandido (no hay click) | Mixto plano |

Frontera con páginas existentes que NO cambian con BOIB: `/aviso-legal/`, `/financiacion/`, `/contacto/`, `/acerca/`, `/cita-esto/`, `/datos-abiertos/` (este último gana un conjunto nuevo, ver §10), `/glosario/` (este gana entradas nuevas, ver §13).

`/sin-dato/` y `/sin-reflejo/` son páginas distintas con propósitos distintos. `/sin-dato/` ya existe en el mapa del sitio actual (`DISENO-WEB.md`) para propuestas con campos sin evaluar y formulario de aportación. `/sin-reflejo/` es nueva del Movimiento 1 BOIB y trata propuestas verificadas que no tienen reflejo normativo. La nomenclatura final puede revisarse al implementar para evitar confusión, pero conceptualmente son dos cosas separadas y este sub-estudio las trata como tales.

---

## 4. Principios de la arquitectura dual

Seis principios duros. Vinculantes. Cualquier decisión de implementación posterior debe poder defenderse contra los seis o explicar por qué la rompe.

**Principio 1 · El resumen en lenguaje claro siempre va primero.** En cualquier componente que mezcle resumen y cita técnica, el resumen ocupa la posición visible por defecto. La cita técnica vive en capa expandible, footnote o página dedicada. Si la maqueta no permite el resumen primero, la maqueta está mal.

**Principio 2 · Cada cita BOIB lleva su contraparte en lenguaje claro.** No hay BOIB suelto sin frase explicativa adyacente. La frase está redactada por la pieza editorial (el extractor o el generador), no se autogenera con el título oficial de la disposición porque ese título suele ser jerga. Sin contraparte, el contenido no se publica.

**Principio 3 · El lector general no tropieza con jerga normativa por defecto.** Términos como "BOIB núm.", "artículo", "decreto-ley", "anuncio de información pública" no aparecen en titulares, bajadas ni primer párrafo de ningún componente de la cara general. Aparecen en bloques expandibles, en `/normativa/`, o en footnotes Tufte-style cuando el contenido editorial lo justifica.

**Principio 4 · El profesional accede al detalle sin fricción.** Toda cita BOIB tiene exactamente un click, tap o tecla para expandir o navegar al detalle completo. Sin formularios, sin login, sin pasos intermedios. La capa expandible se abre con la misma interacción en todos los componentes (consistencia visual y semántica).

**Principio 5 · Defaults explícitos por contexto.** La capa profesional aparece **colapsada por defecto** en componentes de cara general (ediciones semanales, ficha de propuesta, página de actor) y **expandida por defecto** en componentes de cara profesional (`/normativa/`, cuarentena, exportables descargables). Cada componente declara su default en su sección de anatomía y nunca depende de cookies, localStorage ni preferencias del usuario — es estado del componente, no del visitante.

**Principio 6 · Sin terminología jurídica fuera de la página dedicada salvo glosario.** Si un término técnico tiene que aparecer en cara general (porque la propuesta lo cita, porque el actor lo usa), va con tooltip o nota inline que enlaza al glosario. El glosario es la única fuente de definiciones — no se duplican definiciones en cada página.

---

## 5. Capa por público

Decisión maestra: **una sola arquitectura de contenido con dos capas de lectura**. No son dos sitios. La capa profesional vive dentro de la cara general, replegada bajo control del componente, y se hace explícita en `/normativa/` como hogar dedicado.

### 5.1 Capa A — primer visitante / general

Lee el resumen, ve los iconos de verificación normativa (✅ ❌ 🟡), entiende el ratio de promesas vs reflejadas en la página de actor, y nunca tropieza con número de BOIB ni artículo de decreto. Si quiere bajar al detalle normativo, tiene tres puertas explícitas: (a) icono de verificación que abre tooltip con resumen de la disposición vinculada en lenguaje claro, (b) bloque "Detalle normativo" expandible al pie de la ficha de propuesta, (c) enlace permanente a `/normativa/{slug}` cuando quiere la página dedicada de esa disposición.

Componentes principales que sirve la capa A: home, edición semanal, ficha de propuesta colapsada, página de actor, `/sin-reflejo/`, balance, página `/explica/`, recursos, newsletter, RSS, OG.

### 5.2 Capa B — profesional recurrente

`/normativa/` es su hogar. Llega por enlace directo desde la capa A o por bookmark. Encuentra: listado completo de disposiciones BOIB indexadas en el observatorio, filtrable por tipo, organismo emisor, semana, palanca. Cada disposición tiene página propia `/normativa/{slug}` con cita técnica completa, enlace canónico al texto oficial, listado de propuestas que la referencian, fecha de publicación, sección del boletín, y texto completo cacheado en el repo (ver §7).

La capa B también vive expandible dentro de la capa A. Una ficha de propuesta abierta en su forma profesional muestra todo el detalle normativo desplegado por defecto — esa decisión la toma el componente según el contexto (ver Principio 5).

Componentes principales: `/normativa/` (índice y fichas), cuarentena, conjunto de datos descargable de disposiciones (ver §10), API ligera futura (patrón 7B, diferido).

---

## 6. Capa por canal

La integración BOIB sale por más canales que la web. Cada canal tiene restricciones distintas que la arquitectura dual tiene que respetar.

### 6.1 Web

Capa expandible disponible. Aplican principios 1-6 sin restricción especial. Maquetas de §8-12 se diseñan para web y son la referencia de los demás canales.

### 6.2 Newsletter (email)

Sin capa expandible — el email se lee plano. La newsletter envía: resumen completo de la edición + bloque "📜 Lo publicado" con el resumen claro de cada disposición + un enlace por disposición que lleva a `/normativa/{slug}` para quien quiera el detalle. La cita técnica completa **no va en email**. Si una propuesta lleva verificación normativa, va el icono y la frase adyacente, no la cita.

Excepción: una variante "newsletter profesional" futura podría llevar el detalle plano expandido. Diferido — la newsletter actual es única y sirve a ambos públicos.

### 6.3 RSS (`/feed.xml`)

Mismo principio que email: contenido plano, capa profesional como enlace a `/normativa/`. RSS no debe duplicar la cita técnica completa para no inflar el feed. Las disposiciones de la sección "Lo publicado" entran como ítems propios del feed con resumen claro y enlace.

### 6.4 Cara compartible (OG image y metadatos sociales)

Cuando alguien comparte una propuesta o una edición en redes, lo que se ve es el título + bajada + imagen OG. **Nunca código BOIB en el título o la bajada de OG.** Si la propuesta tiene verificación normativa, eso aparece como texto en lenguaje claro en la bajada ("verificada en boletín oficial del 5 de mayo"), no como referencia técnica. La imagen OG sigue el sistema visual cerrado en `ESTUDIO-DISENO.md` D37 (Puppeteer renderiza plantilla HTML).

### 6.5 Versión imprimible / PDF de la edición

Sin capa expandible — el papel no se hace click. La versión imprimible de una edición desarrolla **todas las capas profesionales en plano**: cada ficha de propuesta lleva su detalle normativo completo en bloque secundario tras el resumen. Esto cambia la longitud — una edición de 12 propuestas con 6 vínculos BOIB puede pasar de 8 a 12 páginas en imprimible. Aceptable: quien imprime quiere el archivo completo.

### 6.6 Conjunto de datos descargable (`/datos-abiertos/`)

CSV o JSON. Sin distinción de capa — los datos son los datos. Cada disposición exporta todos sus campos (cita, palanca, organismo, fecha, sección BOIB, enlace canónico, propuestas vinculadas). Documentación del esquema vive en `/datos-abiertos/esquema/`.

---

## 7. Direccionamiento canónico de disposiciones

Cuando se enlaza a un BOIB desde una propuesta o una sección editorial, hay tres opciones reales y una decisión que define la arquitectura.

**Opción A · Enlace directo al PDF original de boib.caib.es.** Pros: fuente primaria, cero responsabilidad de cacheado. Contras: dependencia de la disponibilidad de boib.caib.es (que puede cambiar URLs), enlaces que rompen cuando el portal reorganiza, sin control sobre qué versión se ve.

**Opción B · Enlace a versión cacheada en el repo.** Pros: estabilidad total, archivo permanente reproducible. Contras: responsabilidad legal de redistribución (los BOIB son dominio público pero su redistribución masiva sin atribución clara puede leerse como suplantación), peso en el repo.

**Opción C · URL propia `/normativa/{slug}` con cita técnica + enlace canónico al PDF original.** Pros: control de contenido y SEO, página estable que sobrevive a cambios del portal oficial, sirve como "ficha del observatorio sobre la disposición" sin pretender ser el boletín. Contras: trabajo de mantener la página, requiere que el slug sea estable.

**Decisión propuesta: opción C como dirección canónica del observatorio + opción A como enlace técnico desde dentro de C.**

`/normativa/{slug}` es la URL estable que el observatorio cita siempre. Esa página contiene: cita técnica formal de la disposición, resumen en lenguaje claro, fecha, sección BOIB, organismo emisor, listado de propuestas que la referencian dentro del observatorio, enlace canónico al PDF de boib.caib.es. La opción B (cacheado completo) queda fuera del Movimiento 1; se reabre solo si boib.caib.es deja de ser fiable y entonces se hace estudio dedicado.

**Slug:** `boib-{año}-{número-corto}-{palanca}` → ejemplo `boib-2026-58-vivienda-ibavi`. Permite filtrado por año, lectura humana del propósito y reorganizaciones futuras del portal sin romper el slug. Se decide en la implementación si añadir guión técnico interno o seguir nomenclatura del propio BOIB.

**Anchors profundos:** dentro de `/normativa/{slug}`, los artículos individuales de la disposición tienen anchors `#art-N` para que se pueda enlazar desde una propuesta a un artículo concreto. Solo se generan para disposiciones de cierta extensión (decretos, planes); órdenes y resoluciones cortas no llevan anchors internos.

---

## 8. Anatomía de la ficha de propuesta con vínculo BOIB

Aplica a cualquier ficha en `/propuestas/{id}/` cuando la propuesta tiene verificación normativa o vínculo BOIB pendiente.

### 8.1 Cabecera (visible para todos)

Encima del título de la propuesta, **una sola etiqueta visual** con la verificación normativa, en este orden de prioridad:

- **✅ Reflejada en boletín oficial** (verde) — cuando la propuesta tiene cruce confirmado con disposición BOIB. Click/tap abre tooltip con resumen de la disposición en lenguaje claro y enlace a `/normativa/{slug}`.
- **🟡 Pendiente de verificación normativa** (amarillo) — cuando hay candidato BOIB en cuarentena (clasificador con discrepancia, ver `ESTUDIO-CLASIFICADOR-OFICIAL.md` §6). Click abre tooltip que dice *"el sistema ha detectado una posible disposición relacionada en boletín oficial pendiente de revisión técnica. Pasará a 'reflejada' o 'sin reflejo' al cerrarse la verificación"*.
- **❌ Sin reflejo en boletín oficial** (gris claro, no rojo) — cuando han pasado más de 6 meses desde el anuncio en prensa y no hay vínculo BOIB. Click abre tooltip con fecha del anuncio original y nota *"sin reflejo a fecha de hoy"*. La etiqueta gris (no roja) evita lectura adversarial — el observatorio documenta ausencia, no acusa.
- **(sin etiqueta)** — para propuestas con menos de 6 meses sin cruce todavía evaluado, o propuestas cuyo tipo no admite reflejo BOIB (declaraciones políticas, mociones simbólicas). El sistema no muestra etiqueta cuando no aporta información.

### 8.2 Cuerpo (visible para todos)

Resumen editorial estándar de la propuesta — sin cambios respecto a la maqueta actual del prototipo. La verificación normativa **no contamina** el cuerpo editorial; vive solo en la cabecera y en el bloque expandible al pie.

### 8.3 Bloque expandible "Detalle normativo" (capa profesional, colapsado por defecto)

Aparece al pie de la ficha, después de los firmantes y antes del bloque de citas. Por defecto colapsado con título *"Detalle normativo (1 disposición)"* o el número correspondiente. Un click expande:

- Cita técnica de la disposición: *"Orden ABC/2026, de 5 de mayo, por la que se regulan…"* + número BOIB + sección + fecha de publicación.
- Enlace a la página `/normativa/{slug}` de la disposición.
- Si hay más de una disposición vinculada, listado.
- Si la propuesta está en estado 🟡 (pendiente), bloque adicional con la disposición candidata + nota explicativa de que el cruce está en revisión.

### 8.4 Caso especial — propuesta cuyo BOIB está en cuarentena

Si el clasificador mandó la disposición candidata a cuarentena (`pendiente_clasificacion`), la ficha lleva etiqueta 🟡 y el bloque expandible muestra la disposición con nota *"clasificación técnica pendiente — no es decisión del editor"*. La ficha permanece en cara pública porque el contenido editorial sobre la propuesta sigue siendo válido; solo la verificación normativa está en pausa. Si el clasificador tarda más de 30 días en resolver, la etiqueta cambia a (sin etiqueta) y el bloque expandible desaparece — la cuarentena no debe colgar indefinidamente de la ficha.

---

## 9. Anatomía de la sección "📜 Lo publicado" en la edición semanal

Bloque nuevo dentro de cada edición semanal, situado **después de las propuestas y antes del balance**, marcado con cabecera "📜 Lo publicado en boletín oficial esta semana".

### 9.1 Estructura

Lista plana de las disposiciones BOIB de la semana clasificadas como material por el clasificador. Cada ítem en una sola línea visual:

- Etiqueta de tipo (orden / decreto / resolución / acuerdo / anuncio).
- Resumen claro de una frase generado por el extractor (aplican principios 1 y 2).
- Organismo emisor en lenguaje natural ("Govern de les Illes Balears", no "Conselleria de Vivienda y Movilidad" salvo que sea relevante).
- Fecha en lenguaje natural ("publicada el martes 5 de mayo").
- Enlace al detalle: *"ver detalle"* → `/normativa/{slug}`.

### 9.2 Volumen máximo

Si la semana tiene más de 5 disposiciones materiales, se publican las 5 más relevantes según orden del clasificador (campo `confianza` del output del clasificador, ver `ESTUDIO-CLASIFICADOR-OFICIAL.md` §3.3) + enlace al final *"y N disposiciones más esta semana en /normativa/"*. La sección no debe inflar la edición.

### 9.3 Cuándo no aparece

Si la semana no tiene disposiciones materiales (puede pasar — agosto, semanas cortas, semana sin actividad legislativa de vivienda), la sección no aparece. No hay placeholder vacío.

### 9.4 Estilo

Lenguaje claro radical. Reglas duras:
- Ningún número BOIB en el resumen visible. El número va en el `/normativa/{slug}`.
- Verbo activo: "el Consell aprueba…" no "se aprueba por…".
- Una frase, máximo 25 palabras por ítem.
- Sin tecnicismos ("regula", "establece", "aprueba", "modifica" sí; "deroga", "promulga", "dispone" no — se traducen a verbos comunes).

---

## 10. Anatomía de la página `/normativa/`

Hogar profesional. Capa B expandida por defecto. No existe en el sitio actual, se crea con el Movimiento 1.

### 10.1 Cabecera

Título *"Normativa de vivienda en Ibiza — disposiciones del boletín oficial"* + bajada profesional: *"Listado de disposiciones del BOIB indexadas por el observatorio. Para detalle técnico, fuente primaria y citación. Para lectura general, [ediciones semanales]."*

### 10.2 Filtros (sticky en desktop, plegables en mobile)

- Por tipo de acto (orden, decreto, resolución, acuerdo, anuncio).
- Por organismo emisor (Govern · Consell d'Eivissa · Ayuntamientos · IBAVI · otros).
- Por palanca (suelo · alquiler · ayudas · turístico · habitabilidad · otros).
- Por semana ISO (rango).
- Por estado de cruce con propuestas del observatorio (con propuesta vinculada / sin propuesta vinculada).
- Por estado del clasificador (verificada / en cuarentena).

### 10.3 Listado

Cada fila: tipo + título técnico + fecha + organismo + número BOIB + N propuestas vinculadas + enlace a `/normativa/{slug}`. Densidad alta tipo tabla — el profesional valora densidad sobre estética.

### 10.4 Página individual `/normativa/{slug}`

- Cabecera con cita técnica completa.
- Resumen en lenguaje claro (heredado del bloque "Lo publicado" o ampliado).
- Metadatos: organismo emisor, fecha de publicación, sección del BOIB, número, palanca asignada por el clasificador, confianza del clasificador.
- Enlace canónico al PDF de boib.caib.es.
- Texto completo cacheado opcional (ver §7, decisión diferida — por ahora solo enlace).
- Listado de propuestas del observatorio que referencian esta disposición.
- Anchors profundos `#art-N` cuando aplique.

### 10.5 Conjunto de datos descargable

`/normativa/datos.csv` y `.json` con todos los campos de todas las disposiciones indexadas. Documentado en `/datos-abiertos/esquema/normativa`.

---

## 11. Anatomía de la página `/sin-reflejo/`

Página del patrón 2 del estudio padre. Capa A — cara general. No existe en el sitio actual, se crea con el Movimiento 1.

### 11.1 Cabecera

Título *"Promesas sin reflejo en boletín oficial"* + bajada: *"Propuestas anunciadas en prensa por actores con nombre que llevan más de 6 meses sin aparecer en el boletín oficial de las Illes Balears. Documentación de ausencia. No es opinión: es lo que el sistema observa."*

### 11.2 Estructura

Lista de propuestas con etiqueta ❌ activa, ordenada por antigüedad descendente. Cada entrada:

- Resumen editorial breve de la propuesta.
- Actor que la formuló (con enlace a `/actores/{slug}/`).
- Fecha del anuncio original.
- Tiempo transcurrido en lenguaje natural ("hace 8 meses").
- Enlace a la ficha completa `/propuestas/{id}/`.

### 11.3 Filtros

- Por actor.
- Por palanca.
- Por antigüedad (6-12 meses · 12-24 meses · más de 24 meses).
- Por bloque (gobierno autonómico · gobierno local · oposición · sociedad civil) — sin colorear partidos (regla del estudio de diseño D32).

### 11.4 Ciclo de vida de cada entrada

- Entra a `/sin-reflejo/` cuando una propuesta cruza el umbral de 6 meses sin vínculo BOIB.
- Sale de `/sin-reflejo/` cuando aparece vínculo BOIB válido (etiqueta cambia a ✅ y la propuesta deja la lista).
- También sale cuando el actor retira públicamente la propuesta (estado `descartada` en el ciclo D33 de la propuesta, ver §14).
- **No sale por antigüedad.** Una propuesta sin reflejo a los 5 años sigue apareciendo. Es el sentido de la página.

### 11.5 Lo que NO hace `/sin-reflejo/`

No emite juicio sobre por qué falta el reflejo. No clasifica las propuestas como "incumplidas" — pueden estar en debate, en redacción, fusionadas con otra norma, retiradas tácticamente. La página documenta la ausencia normativa y nada más. Esa contención es lo que la mantiene dentro de la regla fundacional 2 (no proponer) y la regla 1 (autor identificado y URL verificable — la URL es la del anuncio original en prensa).

### 11.6 Frontera con `/sin-dato/` (página existente)

`/sin-dato/` ya existe en el mapa del sitio (`DISENO-WEB.md`) para propuestas con campos sin evaluar y formulario de aportación de información. `/sin-reflejo/` es nueva y trata propuestas evaluadas que no tienen reflejo normativo. Son páginas distintas. Si en implementación se decide unificarlas o renombrar para evitar confusión, queda como decisión de la sesión específica.

---

## 12. Anatomía de la página de actor con dimensión BOIB

Aplica a `/actores/{slug}/`. Sección nueva al pie de la ficha actual, antes del bloque de citas históricas. Capa A — cara general.

### 12.1 Cabecera de la sección

Título *"Promesas vs reflejo en boletín oficial"* + ratio textual: *"De N propuestas documentadas, M han pasado al boletín oficial (k%) — calculado sobre los últimos 12 meses"*. La frase es plana, sin gráfico de barras: el ratio se lee en cifra y porcentaje. Un gráfico añadiría densidad sin añadir información.

### 12.2 Subsecciones

- **Reflejadas (M propuestas)** — listado breve con vínculo a la ficha de cada una.
- **Sin reflejo (k propuestas)** — listado breve con fecha del anuncio y tiempo transcurrido. Enlace al final a `/sin-reflejo/?actor={slug}` para ver el listado completo filtrado.
- **Pendientes de verificación (j propuestas)** — solo si hay propuestas con etiqueta 🟡 vinculadas a este actor. Lista breve.

### 12.3 Ventana temporal

12 meses por defecto. Sin selector de ventana en la cara A — el selector pertenece al balance trimestral, no a la ficha de actor (decisión para mantener simplicidad de la cara general).

### 12.4 Contención editorial

La sección **no compara entre actores**. Cada actor lee su propio ratio. La comparación entre actores vive en el balance trimestral (cuando se decida si la dimensión BOIB entra al balance, ver §14). Sin comparación inline, la sección no se vuelve adversarial.

### 12.5 Cuándo no aparece la sección

Si el actor no ha hecho propuestas evaluables en los últimos 12 meses (ej. actor reactivo, actor histórico, actor con perfil de comentario y no de propuesta), la sección no aparece. Sin placeholder vacío.

---

## 13. Estilo editorial — lenguaje claro vs cita técnica (con glosario)

Reglas duras de redacción para todo el sistema cuando aparezca contenido BOIB.

### 13.1 Reglas para texto en cara general

1. **Sustantivo común antes de tecnicismo.** "Una orden de subvenciones de vivienda (BOIB del 5 de mayo)" sí. "BOIB 58/2026 sobre subvenciones" no.
2. **Fechas en lenguaje natural.** "publicada el 5 de mayo" o "del martes pasado" sí. "ISO 2026-05-05" o "BOIB de fecha 05/05/26" no.
3. **Verbo activo, sujeto explícito.** "El Govern aprueba…" sí. "Se aprueba por…" no.
4. **Sin tecnicismos opcionales.** "Aprueba", "regula", "modifica" sí (son comunes). "Deroga", "promulga", "dispone", "preceptúa" no — sustituir por "deja sin efecto", "publica", "establece".
5. **Cero referencia a artículos individuales.** "El artículo 7 establece…" no aparece en cara general. Va en `/normativa/{slug}` o en el expandible.
6. **Sin nombres formales de organismos cuando hay versión común.** "Conselleria d'Habitatge" no; "el Govern (área de vivienda)" sí.

### 13.2 Reglas para texto en cara profesional (`/normativa/`, expandibles)

Lo opuesto: cita técnica completa, número BOIB, artículo, fecha ISO, nombre formal del organismo, sección del boletín. No es regla nueva — es lo que el profesional espera. Lo importante es que esto **vive solo en la capa B**.

### 13.3 Glosario

Ya existe `/glosario/` en el mapa del sitio actual. Se amplía con las entradas necesarias del Movimiento 1: BOIB, sección de disposiciones generales, orden, decreto, decreto-ley, resolución, acuerdo de pleno, anuncio de información pública, IBAVI, Consell, palanca (interno del observatorio).

Cada término que aparezca en cara general por necesidad editorial (porque la propuesta lo cita literal, porque el actor lo nombró así) lleva un asterisco discreto que enlaza a su entrada del glosario al lado de la primera aparición. Sin tooltip al hover por defecto en mobile (no funciona); solo enlace.

### 13.4 Lo que NO hace este apartado

No define el tono editorial general del observatorio — eso está cerrado en `ESTUDIO-DISENO.md` D31-D40. Solo añade reglas duras adicionales para el caso BOIB. Si hay conflicto entre estas reglas y el tono general, gana el tono general y se modifica este apartado.

---

## 14. Frontera con sistemas existentes

Tres sistemas ya cerrados que la integración BOIB roza. Cada uno necesita decisión explícita.

### 14.1 Tiers de confianza ([D9](DECISIONES.md))

El sistema de tiers calcula color (🟢🟡🟠🔴) según señales de la propuesta (fuentes, verbatim, viability, wayback). La pregunta: **¿una propuesta con vínculo BOIB confirmado salta automáticamente a 🟢 aunque otras señales sean débiles?**

**Decisión propuesta: no.** El vínculo BOIB es una señal nueva más, no un override. El árbol determinista de `compute_tier()` (`src/tiers.py`) puede incorporar la verificación normativa como señal adicional en una iteración futura — el campo `verificado_en_boletin` de la propuesta entra como input al árbol, y se decide en una sesión específica de evolución del sistema de tiers (no de este sub-estudio) qué peso le da. Mientras tanto, el vínculo BOIB se muestra en cabecera de ficha (§8.1) sin tocar el cálculo de tiers existente.

Razón: convertir BOIB en override automático rompería la trazabilidad de `compute_tier()` y mezclaría dos dimensiones que conviene mantener separadas (calidad de la fuente periodística vs. respaldo normativo). Ambas son señales legítimas pero no son la misma cosa.

### 14.2 Balance trimestral (regla fundacional 4)

El balance audita reparto de actores. La pregunta: **¿se añade dimensión "% propuestas con respaldo normativo por actor" al balance trimestral?**

**Decisión propuesta: no en el Movimiento 1, reabrir junto con el patrón 5 cuando haya corpus.** El balance trimestral mide cobertura editorial (cuánto cita el observatorio a cada actor); medir cumplimiento normativo institucional es exactamente el patrón 5 (termómetro de cumplimiento), que el editor difirió a 3-6 meses por [D42](DECISIONES.md). Mezclar ambas mediciones en el balance ahora confundiría dos cosas distintas y precipitaría un debate (frontera con regla 3 de no exclusión por filiación) que la decisión D42 quiso evitar.

Cuando se reabra el patrón 5, la dimensión BOIB del balance se evalúa entonces como decisión propia.

### 14.3 Correcciones (regla fundacional 5)

El protocolo de correcciones de 72h cubre errores editoriales. La pregunta: **¿una corrección de cómo el observatorio resume un BOIB cae bajo el mismo protocolo o necesita variante?**

**Decisión propuesta: mismo protocolo, sin variante.** Si un actor (o cualquier lector) detecta que el resumen claro de una disposición es incorrecto, técnicamente impreciso o sesgado, abre incidencia por el canal estándar y se corrige bajo el protocolo de 72h. La corrección queda registrada en `/correcciones/` con el campo nuevo `tipo_corrección` que distingue (a) error editorial (resumen mal redactado) de (b) error técnico (parser BOIB extrajo mal) — ambos siguen el mismo flujo, solo con etiqueta interna distinta para análisis posterior.

Lo que **no** hace esta decisión: dar a actores citados un derecho ampliado de revisión previa antes de publicar. La cita de la disposición es pública y dominio público; el observatorio no necesita autorización para citarla. La corrección llega tras publicar, como en cualquier otro contenido editorial.

---

## 15. Pruebas en maqueta — tres escenarios reales

Lo que cierra el sub-estudio. Tres escenarios que demuestran que la dualidad funciona sin que las dos capas se estorben.

### Escenario A — Una orden importante se publica y cruza con propuesta documentada

**Situación.** En la edición W22 se documentó que la Conselleria de Vivienda anunció en prensa una orden de bases de subvenciones de rehabilitación. En el BOIB del martes 26 de mayo aparece la orden con título técnico distinto al anuncio. El clasificador la detecta como material con confianza 0,94. El cruce determinista con la propuesta del observatorio se confirma con verbatim alto (los actores y palancas coinciden).

**Cara general.** En la ficha de la propuesta (`/propuestas/{id}/`) la cabecera muestra ✅ verde. Tooltip al click: *"Reflejada en boletín oficial del martes 26 de mayo: orden de bases de subvenciones de rehabilitación. Ver detalle →"*. El cuerpo editorial sin cambio. En la edición semanal de esa semana, la sección "📜 Lo publicado" lleva la línea *"Orden de bases de subvenciones de rehabilitación. El Govern (área de vivienda) regula las ayudas anunciadas en marzo. Publicada el martes 26 de mayo. ver detalle →"*.

**Cara profesional.** Bloque "Detalle normativo" expandido al pie de la ficha: *"Orden VIV/12/2026, de 26 de mayo, por la que se aprueban las bases reguladoras de las ayudas a la rehabilitación. BOIB núm. 78, sección de disposiciones generales. Texto completo →"*. Página `/normativa/boib-2026-78-vivienda-rehabilitacion/` con cita técnica completa, anchors `#art-N`, enlace canónico al PDF, listado de propuestas que la referencian (esta y otras dos previas).

**Lo que demuestra.** Capa A nunca tropieza con "VIV/12/2026" ni con "art. 7"; capa B accede a todo en un click; no hay duplicación; el resumen claro está donde tiene que estar.

### Escenario B — Una propuesta cumple 6 meses sin reflejo y entra en `/sin-reflejo/`

**Situación.** El PSIB-PSOE anunció en noviembre la creación de una mesa autonómica del alquiler temporada. Han pasado 6 meses sin BOIB equivalente. El sistema dispara el cambio automático.

**Cara general.** La ficha de la propuesta cambia la cabecera de (sin etiqueta) a ❌ gris claro. Tooltip al click: *"Sin reflejo en boletín oficial a fecha 9 de mayo. Anuncio original: 5 de noviembre"*. La propuesta aparece en `/sin-reflejo/` automáticamente, en la sección "6-12 meses" con filtro de actor activable. La página de actor `/actores/psib-psoe/` actualiza el ratio y lista esta propuesta en su sección "sin reflejo".

**Cara profesional.** Sin cambios — `/normativa/` no aplica (no hay disposición que indexar). La acción es solo de cara general.

**Lo que demuestra.** El cambio automático se gestiona sin intervención editorial; la propuesta sigue accesible con su contenido original; la documentación de ausencia es plana y verificable.

### Escenario C — Disposición fronteriza pendiente del clasificador

**Situación.** En el BOIB aparece una resolución sobre modificación parcial de plantilla del IBAVI con tres puestos nuevos en gestión de vivienda social. El clasificador grueso (Haiku) la marca como material; el validador (Sonnet) la marca como ruido. Pasa a cuarentena `pendiente_clasificacion` por discrepancia. Hay candidato cruce con propuesta reciente del Govern sobre refuerzo de IBAVI.

**Cara general.** La ficha de la propuesta del Govern muestra cabecera 🟡 amarilla. Tooltip al click: *"El sistema ha detectado una posible disposición relacionada en boletín oficial pendiente de revisión técnica. Pasará a 'reflejada' o 'sin reflejo' al cerrarse la verificación"*. La propuesta sigue publicada con su contenido. La sección "📜 Lo publicado" de la edición de esa semana **no incluye** esta disposición (cuarentena no entra al feed editorial).

**Cara profesional.** En `/normativa/` la disposición aparece bajo el filtro "en cuarentena" (no en el listado por defecto). Página `/normativa/boib-2026-XX-cuarentena/` con cita técnica + nota *"clasificación técnica pendiente — disposición no validada por el sistema"*. La cuarentena es transparente públicamente — esa es la garantía editorial.

**Lo que demuestra.** Las dos capas absorben la incertidumbre del clasificador sin engañar al lector ni romper el contenido editorial; la cuarentena se hace visible al profesional sin ensuciar la cara general; el sistema no toma decisiones que requieran al editor leer el texto jurídico.

---

## 16. Riesgos abiertos del sub-estudio

Cinco riesgos que la arquitectura dual no resuelve por sí sola y se compensan en otra capa.

**1. Fallo del clasificador que pase como ✅.** Si el clasificador marca como material una disposición que no lo es, y el cruce con propuesta lo confirma incorrectamente, la cabecera muestra ✅ verde falso. Mitigación: protocolo de correcciones (§14.3) + tasa de cuarentena <15% como criterio de éxito del clasificador (`ESTUDIO-CLASIFICADOR-OFICIAL.md` §3.6) + revisión manual del editor sobre muestras aleatorias **del clasificador**, no del contenido jurídico, una vez al trimestre.

**2. Drift de tono editorial.** Aunque la arquitectura dual contiene la jerga, el equilibrio de la edición puede irse hacia el polo profesional con el tiempo (más BOIB, menos prensa). Mitigación: regla dura de mantener proporción — ninguna edición semanal debe tener más del 30% de su superficie editorial dedicada a BOIB. Se mide en el self-review automático (sumar caracteres del bloque "Lo publicado" + bloques expandibles abiertos vs total).

**3. Carga de mantenimiento de `/normativa/{slug}`.** Cada disposición es una página nueva. En 12 meses puede haber 200-400 fichas. El mantenimiento manual cero (las páginas se generan desde el clasificador), pero si el portal boib.caib.es cambia URLs, los enlaces canónicos rompen masivamente. Mitigación: monitor de salud de enlaces ya operativo (`src/sources_health.py`) extendido a `/normativa/` con regla "si más del 5% de enlaces canónicos rompen en una semana, alerta crítica".

**4. Trilingüe (ES/CA/EN) en Fase 4.** Las disposiciones BOIB salen en CA y/o ES. El roadmap planea trilingüe en Fase 4. Decisión que este sub-estudio no toma: ¿la cita en `/normativa/` va en idioma original o se traduce? ¿La cara CA del observatorio cita BOIB CA y la cara ES cita la versión ES (cuando la hay)? Mitigación: dejar el texto técnico citado en idioma original siempre y traducir solo el resumen claro; cuando se aborde Fase 4, abrir sub-estudio específico.

**5. Cambio de naturaleza del proyecto.** El estudio padre identificó este riesgo (§9 riesgo 5). La arquitectura dual amortigua pero no elimina — un lector general que llega por Google a la edición y encuentra ✅❌🟡 en cabeceras puede leer el observatorio como herramienta jurídica más que como medio. Mitigación final: las páginas `/como-usarlo/` y `/acerca/` explican explícitamente que las etiquetas son verificación documental al servicio del lector general, no jerga técnica para profesionales — texto editorial que cierra el bucle de expectativa.

---

## 17. Próxima revisión y criterio de revocación

- **Próxima revisión:** al cierre de la primera edición real con Movimiento 1 publicado en cara pública. Evaluar si las etiquetas de cabecera y la sección "📜 Lo publicado" funcionan en lectura real. Diferir 2-4 ediciones consecutivas antes de evaluar (paralelismo con [D20](DECISIONES.md)).
- **Criterio de revocación del sub-estudio:** si en la primera edición real con Movimiento 1 las maquetas resultan inviables en mobile (densidad excesiva), o si el self-review automático detecta drift de tono persistente (>30% de superficie editorial BOIB en dos ediciones consecutivas), reabrir este sub-estudio con sesión específica antes de continuar. Si el sub-estudio paralelo del clasificador no alcanza criterios objetivos (precisión ≥85%, exhaustividad ≥80%, tasa de cuarentena <15%), el Movimiento 1 ni arranca y este sub-estudio queda dormido sin revocar.

---

## 18. Trazabilidad cruzada

- [`ESTUDIO-FUENTES-OFICIALES.md`](ESTUDIO-FUENTES-OFICIALES.md) — estudio padre. §9 riesgos 3 y 5 motivan este sub-estudio. §13 patrones 1 y 2 son los implementados por el Movimiento 1. §17 movimiento escalonado.
- [`ESTUDIO-CLASIFICADOR-OFICIAL.md`](ESTUDIO-CLASIFICADOR-OFICIAL.md) — sub-estudio paralelo. §3.6 criterios objetivos de éxito que condicionan el arranque del Movimiento 1. §6 modo cuarentena agresiva alimenta la etiqueta 🟡 de §8.1 de este documento.
- [`DISENO-WEB.md`](DISENO-WEB.md) — sección "Los dos públicos" cierra la dualidad de público que este sub-estudio asume. Mapa del sitio referenciado en §3.
- [`ESTUDIO-DISENO.md`](ESTUDIO-DISENO.md) — sistema visual cerrado en D28-D40. Las maquetas de §15 se renderizan dentro de ese sistema sin nuevas decisiones de diseño visual.
- [D9](DECISIONES.md) — sistema de tiers. Frontera tratada en §14.1.
- [D27](DECISIONES.md) — barra de progreso de propuestas. Frontera con campo `state` que el patrón 6 BOIB tocará si se activa (diferido).
- [D32](DECISIONES.md) — paleta extendida por tipo de actor. Aplicable a la sección de actor en §12 (sin colorear partidos).
- [D41](DECISIONES.md) — BOIB es pata estructural + cero supervisión jurídica humana del editor. Restricciones operativas centrales de este sub-estudio.
- [D42](DECISIONES.md) — Movimiento 1 = patrones 1+2. Origen formal de este sub-estudio.
- [`CLAUDE.md`](CLAUDE.md) reglas fundacionales 1-5 + regla complementaria. Toda la arquitectura dual sirve a las 5 reglas duras y a la regla complementaria sobre cero supervisión humana.
