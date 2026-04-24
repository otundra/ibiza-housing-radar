# Diseño web — Arquitectura de información y UX

**Fecha:** 2026-04-20
**Origen:** [CLAUDE.md](CLAUDE.md#reglas-fundacionales), [ROADMAP.md](ROADMAP.md).
**Alcance:** rediseño de la web para servir a dos públicos con intenciones distintas sin penalizar a ninguno. Arquitectura de información completa, detalle página por página, componentes reutilizables.

---

## Los dos públicos

| Dimensión | Primer visitante no técnico | Profesional recurrente |
|---|---|---|
| Perfil típico | Ciudadano de Ibiza, temporero, familiar preocupado, curioso que llega por Google | Periodista de vivienda, regidor, técnico de ayuntamiento, sindicalista, patronal, académico, profesional de tercer sector |
| Intención | Entender el problema, ver recursos prácticos, si le pagan un abuso, si hay algo que hacer | Fuente de trabajo semanal: qué ha pasado, quién propone qué, precedentes, datos |
| Tiempo disponible | 30-90 segundos antes de rebotar | 3-10 minutos, puede volver varias veces |
| Dispositivo | Móvil (70%+) | Desktop (60%+) |
| Ruta típica | Google → home → 1-2 clicks → sale o se suscribe | Directo a última edición → `/propuestas` o `/actores` → descarga CSV → vuelve el lunes siguiente |
| Qué valora | Claridad, sin jerga, "qué puedo hacer", autoridad percibida | Densidad, verificabilidad, directo al grano, citabilidad |
| Qué ahuyenta | Jerga técnica, muchos clicks, parecer activista | Relleno, tono panfletario, datos sin fuente |

**Principio de diseño:** la home debe servir a ambos en la primera pantalla sin sacrificar a ninguno. Secciones posteriores se especializan.

---

## Mapa del sitio

```
/
├── / (home dual)
├── /ediciones/ (archivo completo)
│   └── /ediciones/2026-wNN/ (cada edición)
├── /propuestas/ (tracker histórico filtrable)
│   └── /propuestas/{id}/ (ficha individual de cada propuesta)
├── /actores/ (directorio)
│   └── /actores/{slug}/ (ficha de actor)
├── /balance/ (reparto público de citas)
├── /explica/ (contenido long-tail evergreen)
│   ├── /explica/sa-joveria/
│   ├── /explica/ibavi/
│   ├── /explica/llei-habitatge-baleares/
│   ├── /explica/alquiler-turistico-ibiza/
│   └── /explica/vivienda-temporera/
├── /glosario/
├── /radar/ (intenciones y estudios en movimiento — aún no propuestas formales)
├── /sin-dato/ (propuestas con campos "no evaluada" + formulario para aportar)
├── /auditoria/ (auditorías trimestrales con Opus, públicas)
│   └── /auditoria/2026-qN/
├── /costes/ (dashboard público simplificado)
├── /estado/ (histórico operacional del pipeline, Solar Low-Tech style)
├── /recursos/ (para afectados, Fase 1)
├── /como-usarlo/ (guía para primera visita)
├── /politica-editorial/
├── /metodologia/
├── /correcciones/
├── /cita-esto/ (kit de prensa)
├── /aportar/ (formulario crowd-sourcing)
├── /datos-abiertos/ (CSV descargable)
├── /contacto/
├── /acerca/
├── /financiacion/
├── /aviso-legal/
├── /404.html
├── /feed.xml
├── /sitemap.xml
└── /robots.txt
```

---

## Home rediseñada

La home tiene que responder en los primeros 10 segundos a cuatro preguntas, sin importar quién llegue:

1. **Qué es esto** (tagline + 1 frase).
2. **Qué encuentro aquí esta semana** (panel editorial con la edición en curso).
3. **Es neutral** (visible: link a política editorial y balance).
4. **Me puedo suscribir** (CTA newsletter y RSS).

### Estructura (desktop ≥1024 px)

```
┌────────────────────────────────────────────────────────────┐
│ Logo · IHR          [Ediciones · Propuestas · Actores ·    │
│                      Recursos · Más ▾] · [Suscribir]       │  ← nav siempre visible
├────────────────────────────────────────────────────────────┤
│                                                             │
│  Hero:                                                      │
│  H1 "Ibiza Housing Radar"                                   │
│  Tagline "Observatorio semanal de vivienda en Ibiza.        │
│   Mapeamos lo que se propone, no proponemos nosotros."     │
│                                                             │
│  [¿Primera vez? → Guía rápida]  [Última edición →]         │
│                                                             │
├────────────────────────────────────────────────────────────┤
│ BLOQUE RESUMEN SEMANA                                       │
│ Semana 4 - Abril 2026 · 27-abr-2026                         │
│                                                             │
│ [N] señales · [N] propuestas · [N] omisiones · [N] rescate │
├────────────────────────────────────────────────────────────┤
│ PANEL EDITORIAL DE LA ÚLTIMA EDICIÓN                        │
│                                                             │
│ ┌─────────────────────────┐ ┌───────────────────────────┐  │
│ │ Señales (4-8 bullets)    │ │ Mapa de posiciones       │  │
│ │ con URL                  │ │ Tabla compacta           │  │
│ └─────────────────────────┘ └───────────────────────────┘  │
│                                                             │
│ Propuestas en circulación (cards)                           │
│ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐       │
│ │ Prop 1   │ │ Prop 2   │ │ Prop 3   │ │ Prop 4   │       │
│ │ Actor    │ │ Actor    │ │ Actor    │ │ Actor    │       │
│ │ Estado   │ │ Estado   │ │ Estado   │ │ Estado   │       │
│ │ Fuente↗  │ │ Fuente↗  │ │ Fuente↗  │ │ Fuente↗  │       │
│ └──────────┘ └──────────┘ └──────────┘ └──────────┘       │
│                                                             │
│ Rescate · Omisiones · A vigilar (sections compactas)       │
├────────────────────────────────────────────────────────────┤
│ ARCHIVO ÚLTIMAS 4 EDICIONES                                 │
│ Lista densa                                                 │
├────────────────────────────────────────────────────────────┤
│ SOBRE EL PROYECTO (compacto)                                │
│ 3 líneas + links: política editorial · metodología · balance│
├────────────────────────────────────────────────────────────┤
│ Footer                                                      │
└────────────────────────────────────────────────────────────┘
```

### Estructura (mobile < 640 px)

Las dos columnas del panel desktop se apilan. Cards de propuestas 1 por línea. Archive ediciones como lista vertical densa. CTA newsletter flotante en scroll.

### CTAs primarios y secundarios

- **Primario (nuevo visitante):** `[¿Primera vez? → Cómo usarlo]` lleva a `/como-usarlo/`.
- **Primario (recurrente):** `[Última edición →]` scrolls al panel.
- **Secundario visible en hero:** `[Suscribirse]` en nav + al final de home.
- **Secundario en footer:** RSS · Bluesky · Mastodon · Contacto · Política editorial · Balance.

---

## Páginas — detalle

### `/como-usarlo/`

Objetivo: que el primer visitante entienda en <60 s qué va a encontrar.

Contenido:

```
# Cómo usar este observatorio

Cada lunes publicamos una edición. Tiene 7 secciones; sabe qué buscar
en cada una y ganas tiempo.

## 1. 📡 Señales detectadas
Los hechos de la semana con enlace a la noticia original. Lo que ha pasado.

## 2. 🗓 Cronología
Tres líneas que ordenan los hechos en el tiempo. Sin interpretación nuestra.

## 3. 🗺 Mapa de posiciones
Tabla con quién ha propuesto qué y quién está a favor o en contra. Vistazo
rápido del campo de fuerzas.

## 4. 📋 Propuestas en circulación
Fichas detalladas de cada propuesta: quién la propone, dónde lo dijo, qué
actor tendría que ejecutarla, viabilidad legal y económica, precedente con
enlace.

## 5. 🗄 Rescate
Propuestas que se presentaron semanas atrás, siguen vivas y nadie está
debatiendo esta semana. Oro enterrado.

## 6. 🕳 Omisiones
Hechos documentados esta semana sobre los que ningún actor ha propuesto nada.

## 7. 👀 A vigilar
Fechas y decisiones pendientes para la próxima semana.

## Qué NO hacemos

No generamos propuestas propias. Solo documentamos las que ya existen.
No firmamos postura política. No publicamos nada sin fuente verificable.
Las 5 reglas duras están aquí: [política editorial].

## Cómo citarnos

[Botón] Ver formato para medios y académicos.
```

### `/politica-editorial/`

Contenido fijo con las 5 reglas duras del observatorio (ver [CLAUDE.md](CLAUDE.md#reglas-fundacionales)). Fecha de última revisión visible. Cambios trazables (si se modifica alguna regla se registra en `/correcciones`).

### `/metodologia/`

Reescrita. Estructura:

1. Pipeline técnico en una página (diagrama simple).
2. Modelos usados: Haiku (clasifica y extrae) + Opus (compone). Enlace a blog de Anthropic sobre cada modelo.
3. Sesgos declarados:
   - LLMs tienen sesgos estadísticos heredados del entrenamiento. Por eso no generamos propuestas propias.
   - La selección de propuestas tiene sesgo implícito por qué fuentes leemos y cómo clasificamos. Mitigación: balance público trimestral.
4. Fuentes de ingesta: lista actual de RSS y por qué cada una.
5. Política de verificación: qué comprueba `verify.py`, qué bloquea, qué no.
6. Correcciones: cómo funcionan, cómo reportarnos un error.
7. Licencia: CC-BY.

### `/balance/`

Página generada automáticamente por `balance.py`.

Contenido:

```
# Balance de actores citados

Última actualización: {{ site.time }}

## Ventana actual: últimos 90 días

{N} propuestas documentadas · {M} actores distintos citados

### Por tipo de actor
[Tabla + gráfico barras horizontales]

### Por bloque político (solo partidos y gobiernos)
[Tabla + gráfico barras horizontales]

### Por palanca
[Tabla]

## Ventana anual

[Misma estructura]

## Alertas metodológicas activas

{Si algún bloque supera 50% durante 2 meses seguidos, alerta visible aquí
con plan de mitigación.}

## Cómo se calcula

[Link a metodología]
```

### `/actores/`

Directorio alfabético de todos los actores citados alguna vez. Cada entrada lleva a una ficha.

```
# Directorio de actores

Ordena por: [Nombre | Nº citas | Última aparición]

[Tabla con: nombre, tipo, nº propuestas citadas, nº veces apoyo expresado,
nº veces rechazo expresado, última aparición, link ficha]
```

### `/actores/{slug}/`

Ficha individual. Ejemplo `/actores/consell-deivissa/`:

```
# Consell d'Eivissa

Tipo: institucional público
Web oficial: https://www.conselldeivissa.es
Bloque político actual (2023-2027): PP+Vox

## Cargos citados

- {Nombre Cargo 1}
- {Nombre Cargo 2}

## Propuestas que ha hecho o apoyado

[Lista cronológica con link a ediciones]

## Propuestas que ha rechazado públicamente

[Lista cronológica]

## Posiciones expresadas sobre vivienda

[Cronología de citas textuales con fecha y URL]
```

### `/propuestas/`

Tracker histórico. Tabla filtrable:

```
# Todas las propuestas documentadas

Filtros: Actor · Tipo de actor · Estado · Palanca · Horizonte · Año

[Tabla con: fecha, título corto, actor, estado, palanca, horizonte, edición, URL]

Descargar CSV completo: [link a /datos-abiertos/]
```

### `/propuestas/{id}/`

Ficha de propuesta individual. Útil para citar una propuesta concreta. Todos los campos del schema + historia (si la propuesta ha cambiado de estado entre ediciones).

### `/recursos/`

**Página clave para "herramienta de cambio".** Utilidad directa para afectados.

```
# Si tú también estás buscando vivienda

Este observatorio mapea la crisis, pero no sustituye a los servicios
sociales. Aquí tienes a dónde llamar si tu situación es urgente.

## Servicios sociales municipales

### Ibiza (Eivissa)
Teléfono · horario · dirección · web

### Sant Antoni de Portmany
[Igual]

### Santa Eulària des Riu
### Sant Josep de sa Talaia
### Sant Joan de Labritja

## Tercer sector

### Cáritas Ibiza
Teléfono urgente · horario · qué hacen · cómo acceder · web

### Cruz Roja Ibiza
[Igual]

## Oficina de Vivienda del Consell d'Eivissa

Dirección · teléfono · horario · qué tramita

## Emergencias sociales 24h

- 112 · 016 (violencia de género con componente de vivienda)

## Asesoramiento jurídico gratuito

### Turno de oficio (Colegio de Abogados)
### Oficines d'Orientació Jurídica

## Sindicatos (asuntos laborales y alojamiento empresa)

- CCOO Illes Balears · delegación Ibiza
- UGT Illes Balears · delegación Ibiza

## Colectivos ciudadanos

- PAH Pitiüses (si activa)
- Ens Plantem (si activa)

## Nota

Contrastamos la información de esta página cada trimestre. Si algún dato
está desactualizado o falta un recurso relevante, escríbenos:
[/contacto/]
```

### `/glosario/`

Lista alfabética de términos con enlace cuando apliquen a `/explica/`. Ejemplos: alquiler turístico, asentamiento, BOIB, Consell, desalojo administrativo, desalojo judicial, HUT, IBAVI, infravivienda, licencia turística, Llei 5/2018, PGOU, plurifamiliar, suelo dotacional, subarriendo, temporero, TSJIB, unifamiliar aislada, VPO…

### `/explica/sa-joveria/` (ejemplo de long-tail)

```
# Sa Joveria, el asentamiento de trabajadores de Ibiza

## Qué es

{Explicación plain language en 300-500 palabras: qué, dónde, desde cuándo,
cuánta gente, quiénes son, condiciones actuales.}

## Cronología

{Fechas clave con enlaces a las ediciones que las cubren.}

## Propuestas en circulación sobre sa Joveria

{Lista dinámica: tabla con propuestas del tracker filtrado por tag.}

## Cobertura de las ediciones

{Lista de ediciones que han cubierto sa Joveria.}

## Fuentes oficiales

{Enlaces a actas de pleno, informes Servicios Sociales, etc.}
```

Estructura análoga para las otras `/explica/`. Objetivo SEO: capturar búsquedas concretas ("qué es sa joveria", "asentamiento ibiza temporeros", "ibavi ibiza ayudas", "llei habitatge baleares resumen", etc.).

### `/cita-esto/` (kit de prensa)

```
# Para medios y académicos

## Cómo citarnos

APA: Ibiza Housing Radar (2026). {Título edición}. Recuperado de {URL}.

Chicago: "Título edición". Ibiza Housing Radar, {fecha}. {URL}.

## Descripción corta (para hoja sumaria)

Ibiza Housing Radar es un observatorio semanal documental sobre la crisis
de vivienda en Ibiza, con foco en trabajadores de temporada. Mapea las
propuestas que los distintos actores públicos y privados formulan cada
semana, sin generar propuestas propias.

## Descripción larga (para artículos)

{Versión 150 palabras}

## Logo

{SVG y PNG descargables}

## Contacto para medios

{Email directo o formulario}

## Licencia

El contenido está bajo Creative Commons CC-BY 4.0. Puedes reproducir
citando la fuente con enlace al artículo original.
```

### `/radar/` (nuevo — señales en movimiento)

**Propósito:** página de trazabilidad para todo lo que un actor con nombre ha anunciado o puesto en marcha **sin haber concretado medida todavía**. Intenciones, estudios encargados, debates abiertos, declaraciones de intención sin plan.

Filosofía: el observatorio distingue tres niveles:

1. **Propuesta formal** (va a `/propuestas/`): actor con nombre + medida concreta + primera acción ejecutable.
2. **En movimiento** (va aquí, a `/radar/`): actor con nombre + intención declarada + **pendiente de concretar**.
3. **Omisión** (va a la sección "Omisiones" de la edición semanal): hecho documentado sin actor que proponga nada.

**Juego con la marca:** el proyecto se llama "Housing Radar". Esta página es literalmente el radar interno del observatorio: señales débiles que aún no son propuesta firme pero están en movimiento.

**Guiño al lector:** nota en cabecera que el nombre "Housing Radar" será reevaluado cuando se elija dominio propio; mientras tanto, `/radar/` sigue siendo la página de referencia para señales tempranas independientemente del nombre final del proyecto.

```
# Radar — señales en movimiento

Cosas que actores con nombre han anunciado pero aún no han concretado.
Cuando se concretan, pasan a [Propuestas]. Mientras tanto, viven aquí
con fecha de entrada, motivo por el que no son propuesta formal todavía,
y qué esperaríamos que se concrete.

## Activas

[Tabla filtrable: actor · qué dijo · fecha · motivo "en movimiento" · 
qué se espera · edición donde apareció]

## Promovidas a propuesta formal

[Histórico de las que ya se concretaron, con enlace a su ficha en /propuestas/ 
y nota "antes en movimiento desde fecha X"]

## Caducadas

[Las que llevan >6 meses sin concretarse y no han generado movimiento nuevo.
Se archivan con motivo "sin concreción tras N meses".]
```

Cada fila tiene ficha individual en `/radar/{id}/` con:

- Declaración del actor (verbatim + URL).
- Actor, tipo, fecha.
- Motivo por el que es "en movimiento" y no "formal".
- Qué se esperaría para promoverlo a formal (ej: *"cuando el Consell publique el estudio y anuncie medida concreta"*).
- Histórico de seguimiento (si aparece en ediciones posteriores como recordatorio).

Cuando se promueve:

- `state` pasa de `en_movimiento` a `propuesta`.
- Se crea ficha en `/propuestas/{id}/`.
- `/radar/{id}/` se mantiene con redirect suave + nota "**promovida a propuesta formal el [fecha]**".

### `/sin-dato/` (nuevo — archivo de huecos de información)

**Propósito:** convertir los "no evaluada" / "sin dato público" en oportunidad para que expertos del público aporten.

Contenido:

```
# Propuestas con datos pendientes

Cuando una propuesta tiene viabilidad jurídica, viabilidad económica, actor
ejecutor o precedente en "no evaluada" o "sin dato público", aparece aquí.
Si tienes el dato con fuente verificable, puedes aportarlo.

Política: solo se incorporan aportaciones con URL a fuente primaria. Se
documenta cada cambio en [/correcciones/].

## Tabla filtrable

Filtros: Campo que falta · Actor · Palanca · Edición · Antigüedad

[Tabla con: propuesta, actor, campo(s) faltante(s), edición, fecha, 
botón "aportar este dato"]
```

Cada fila con botón → formulario Formspree pre-rellenado con propuesta ID + campo a completar. El aportante incluye URL + justificación breve.

El editor (o pipeline automatizado con `verify.py`) revisa la aportación:

- URL responde 200 y es fuente primaria.
- Dato es consistente con otros elementos de la propuesta.

Si OK, se incorpora al registro con `dateModified` y entrada en `/correcciones/` reconociendo al aportante (si quiere).

### `/auditoria/` (nuevo — transparencia radical)

Índice de auditorías trimestrales generadas por `src/quarterly_audit.py`. Cada una como documento público de 800-1.500 palabras con:

- Cumplimiento de las 5 reglas duras en el trimestre.
- Patrones emergentes detectados.
- Calidad editorial comparada con trimestre anterior.
- Recomendaciones concretas para ajustes de prompt, fuentes, criterios.
- Señales sistemáticamente perdidas.

Contenido generado por Opus. Editor puede añadir nota humana breve al principio de cada auditoría si tiene contexto relevante.

Primera auditoría: Q3 2026 (tras 13 ediciones bajo el modelo documental).

### `/costes/` (nuevo — dashboard público simplificado)

Versión pública del dashboard privado. Transparencia operacional:

- Coste acumulado del año en curso (€).
- Coste del mes en curso (€ redondeado a céntimo).
- Coste medio por edición del último trimestre.
- Mini-gráfico de evolución (SVG nativo o tabla simple).
- Capa actual (🟢/🟡/🟠/🔴/🚨).
- Nota: "Proyecto sostenido por tiempo voluntario del editor + gasto en API Anthropic, costeado por Raúl Serrano. Transparencia: [CSV completo](/data/costs.csv)."

Sin datos por modelo o por tarea (eso queda en privado). Solo agregados razonables.

### `/estado/` (nuevo — histórico operacional Solar Low-Tech)

- Registro histórico de ejecuciones del pipeline (fecha, resultado, tiempo, incidencias).
- Ediciones publicadas a tiempo vs con retraso.
- Versiones del sitio (changelog operativo).
- Número total de: ediciones, actores documentados, propuestas en seguimiento, correcciones recibidas y atendidas.
- Tiempo medio desde propuesta detectada hasta publicación.

Se alimenta automáticamente de logs del pipeline + frontmatter de ediciones + formularios recibidos.

### Resto de páginas

- `/contacto/` — Formspree con campos mínimos (email, asunto, mensaje). Alternativa formsubmit.co si se satura.
- `/correcciones/` — log público inicialmente vacío.
- `/aviso-legal/` — mínimo: titular del sitio, contacto, jurisdicción, licencia.
- `/financiacion/` — "Proyecto sostenido por tiempo voluntario de Raúl Serrano. Coste directo actual: ~5,85 €/mes en API Anthropic, costeado por el editor. Sin ingresos activos en 2026."
- `/aportar/` — formulario Formspree con campos del PLAN.md Fase 3 Vía B. Disclaimer: "Publicamos agregados por zona/tipo cuando hay ≥10 respuestas. Nunca publicamos tu email. Sesgo muestral declarado en metodología."
- `/datos-abiertos/` — descarga de `data/proposals_history.csv` y futuras datasets. Licencia CC-BY.
- `/acerca/` — una sola página breve: qué es, por qué existe, quién lo hace, cómo se financia, cómo contactar. Links a política y metodología.

---

## Navegación

### Top-nav (siempre visible)

Desktop: `Ediciones · Propuestas · Actores · Recursos · Más ▾ · [Suscribir]`
Mobile: menú hamburguesa con lo mismo.

Dropdown "Más":

- Balance
- Política editorial
- Metodología
- Explica
- Glosario
- Datos abiertos
- Kit de prensa
- Contacto

### Footer

Tres columnas (desktop, se apilan en mobile):

```
Proyecto            Transparencia       Conectar
- Acerca            - Política editorial - RSS
- Metodología       - Balance           - Bluesky
- Financiación      - Correcciones      - Mastodon
- Aviso legal       - Datos abiertos    - Newsletter

Licencia CC-BY 4.0 · Coste directo ~6 €/mes en API · Código en GitHub
```

---

## Componentes reutilizables

1. **Card de propuesta.** Título corto, actor + tipo, estado (pill), horizonte, viabilidad (dos mini-pills legal/económica), enlace a fuente, botón "ver ficha completa" a `/propuestas/{id}/`.
2. **Card de edición** (en archive). Número de semana, excerpt, N señales + N propuestas + N actores, fecha, enlace.
3. **Chip de actor** — nombre + tipo como pill colorizado por bloque (neutro, público, privado, sindicato, tercer sector, partido).
4. **Mini-tabla de mapa de posiciones** — compacta.
5. **Breadcrumb** — en cada página interna para navegación y SEO.
6. **Botón "cómo citar"** — abre modal con formatos.
7. **Banner de suscripción** — al final de cada edición y flotante en mobile.
8. **Pill de estado de propuesta** — colores distintos por estado (propuesta / en debate / aprobada / en ejecución / implementada / descartada).
9. **Callout de nota metodológica** — en ediciones retroactivas y donde aplique.

---

## Sistema visual

**Se mantiene:**

- Paleta actual: terracota + crema + negro sobre fondo blanco, modo oscuro en negro suave.
- Tipografía: Instrument Serif (headlines), Inter (cuerpo), JetBrains Mono (código y URLs).
- Diseño editorial/periódico.

**Se amplía:**

- Paleta extendida para tipificar actores (sin adscripción visual a ningún color político):
  - Institucional público → azul pizarra
  - Partido → gris neutro (**no color de partido**, es regla dura)
  - Patronal → ocre
  - Sindicato → verde musgo
  - Tercer sector → terracota (primario del sitio)
  - Académico → violeta apagado
  - Judicial → gris oscuro
  - Colectivo ciudadano → amarillo mostaza
- Iconografía consistente por sección (emoji actual se mantiene, son reconocibles y no cansan).

**Regla dura de diseño:** los partidos políticos se muestran siempre en gris neutro, nunca en su color. Esta es una decisión editorial para reforzar la imparcialidad visual.

---

## Responsive

Breakpoints:

- 320 px (iPhone SE mínimo)
- 375 px (iPhone estándar)
- 640 px (móvil grande / phablet pequeño)
- 768 px (tablet portrait)
- 1024 px (tablet landscape / laptop pequeño)
- 1280 px (laptop estándar)
- 1920 px (desktop grande)

Prioridades:

- Hero legible a 320 px sin scroll horizontal.
- Tabla "Mapa de posiciones" → colapsada a cards en móvil.
- Navegación → hamburguesa <768 px.
- Cards de propuesta → 1 col (<640), 2 (640-1024), 3 (1024-1280), 4 (>1280).

---

## Accesibilidad

- Semántica HTML correcta (`<nav>`, `<main>`, `<article>`, `<section>`, `<footer>`).
- Contraste AA mínimo verificado en light y dark.
- Todas las imágenes con `alt` descriptivo.
- Enlaces con texto descriptivo (nunca "click aquí").
- Skip-link "saltar al contenido" al principio del DOM.
- Navegación completa por teclado.
- Focus visible en todos los elementos interactivos.
- `prefers-reduced-motion` respetado si se añaden animaciones.
- Formularios con labels explícitos.
- Tablas con `<caption>` y `<th scope>`.

---

## Inspiración editorial — Solar Low-Tech Magazine

El editor señala [solar.lowtechmagazine.com](https://solar.lowtechmagazine.com/) como referencia de aproximación ética y visual. Se importan elementos concretos sin romper la identidad actual (terracota + crema editorial).

### Qué importamos

**1. Indicadores de transparencia operacional en footer (o barra fija inferior).**

Solar Low-Tech muestra el % de batería del servidor y el estado energético. Nosotros mostramos:

- Coste API del mes en curso: `0,XX €`.
- Capa de alerta actual: `🟢 verde` / `🟡 amarilla` / etc.
- Última edición publicada: `hace N días`.
- Estado del pipeline: `✅ OK última ejecución` / `⚠️ con avisos` / `🚨 fallo`.
- Ediciones publicadas: `N`.
- Actores documentados: `M`.
- Propuestas en seguimiento: `K`.

Formato monospace, actualizado automáticamente por script tras cada ejecución.

**2. Tipografía monospace para datos.**

Ya usamos JetBrains Mono. Darle más peso:

- Cifras, URLs, fechas técnicas, nombres de archivos, todo en mono.
- Fichas de propuesta: campos técnicos (estado, horizonte, viabilidad) en mono.
- Tabla de "Mapa de posiciones": columna Fuente en mono.

**3. Notas al margen (estilo Edward Tufte / libro académico).**

En ediciones largas y páginas `/explica/`, notas al margen con:

- Aclaraciones de términos técnicos.
- Referencias cruzadas a otras ediciones.
- Contexto histórico relevante.

Implementación CSS: `<aside class="margin-note">` absolutamente posicionado a la derecha en desktop (≥1024 px), plegado en `<details>` desplegable en mobile.

**4. Dithering 1-bit en imágenes OG (opcional, fase 2).**

Solar Low-Tech dithera todas sus imágenes a blanco y negro con patrón. Estéticamente muy distintivo y pesaje mínimo (10-30 kB vs 100-500 kB).

Nosotros:

- OG images de ediciones: dithering sobre paleta terracota + crema (no puro b/n), mantiene identidad.
- Genera el script de OG images (ver [SEO.md](SEO.md)) con capa de dithering Floyd-Steinberg antes de exportar PNG.
- Decisión final tras ver un prototipo (fase 2 de diseño, no bloquea Fase 0).

**5. Manifiesto visible en footer.**

Bloque estable en footer con texto corto:

> **Ibiza Housing Radar es un observatorio documental.** No genera propuestas propias. Documenta las que actores con nombre formulan cada semana, con fuente verificable. 5 reglas duras en [/politica-editorial/]. Balance público en [/balance/]. Coste de funcionamiento: 0,XX € este mes.

Transparencia = credibilidad.

**6. Rechazo radical de JS innecesario.**

Ya lo hacemos; reforzar y declarar:

- Sin frameworks client-side.
- Sin trackers de terceros (GoatCounter es self-hosted sin cookies).
- Sin webfonts pesadas (las actuales son las estrictamente necesarias).
- Toda página legible y funcional sin JS activado.
- Menú hamburguesa resuelto con `<details>` nativo, no JS.

**7. Accesibilidad radical.**

Todo contenido accesible:

- Sin JS (ya dicho).
- Sin cookies (GoatCounter no las usa).
- Sin necesidad de webfonts (fallback system fonts en caso de bloqueo).
- Contraste AAA donde se pueda (más exigente que AA).
- Navegación completa por teclado auditada.

**8. Transparencia histórica — `/estado/`.**

Página dedicada con:

- Registro histórico de fallos del pipeline (cuándo falló, por qué, cómo se resolvió).
- Coste acumulado por mes.
- Ediciones publicadas a tiempo vs con retraso.
- Versiones del sitio (changelog visible).

Más radical que `/correcciones/` (que solo cubre errores editoriales). Cubre también errores operacionales.

### Qué NO importamos

- La paleta amarillo mostaza de Solar Low-Tech. Mantenemos terracota + crema.
- El layout de 3 columnas fijas. El nuestro es más editorial fluido.
- El tono de manifiesto ecológico. Nuestro ángulo es social/vivienda, no ambiental.
- La dependencia estética extrema de monospace (Solar es 100% mono; nosotros mantenemos Instrument Serif para headlines).

### Resumen de qué cambia en Fase 0

- Componente nuevo: indicadores de transparencia en footer (6-8 datos en mono, actualizados).
- Componente nuevo: notas al margen en ediciones y `/explica/`.
- Manifiesto editorial visible en footer.
- Auditoría de accesibilidad más exigente (contraste AAA donde posible).
- Página `/estado/` con histórico operacional.
- Posible dithering en OG images (fase 2 estética, tras ver prototipo).

---

## Performance

Objetivos Core Web Vitals:

- LCP ≤ 2,5 s en 3G lento.
- INP ≤ 200 ms.
- CLS ≤ 0,1.

Medidas:

- CSS crítico inline.
- Fuentes web con `font-display: swap` + `preload` de la principal.
- Imágenes en WebP con fallback JPEG, `loading="lazy"` salvo hero.
- Sin JS salvo para menú hamburguesa y botón citar (que se puede resolver con `<details>` nativo).
- Sin librerías externas pesadas. Todo ligero.
- Jekyll estático ya es rápido; mantener.
