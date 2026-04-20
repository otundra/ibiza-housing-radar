# Plan de mejora — Ibiza Housing Radar

Estrategia para convertir el proyecto en un observatorio de referencia sobre vivienda de trabajadores en Ibiza. Registro vivo: actualizar al cerrar cada fase.

Última revisión: 2026-04-20.

## Principio económico

**Coste-cero salvo IA.** Único gasto aceptado: llamadas a la API de Anthropic. Coste actual ~2 €/mes. Topes definidos en € dentro de `src/costs.py`: **tope blando 8 €/mes** (avisa por Telegram pero sigue publicando) y **tope duro 20 €/mes** (corta para proteger contra runaway). Trilingüe ES/CA/EN previsto subiría a ~3,15 €/mes cuando se active; margen del tope ya contempla ese escenario. Toda herramienta externa debe tener alternativa 0 € o quedar diferida hasta que el proyecto demuestre tracción.

**Dominio propio diferido.** `radaribiza.org` o similar (~12 €/año) es el único gasto externo que merece la pena pagar, pero se aplaza hasta ver que el proyecto tiene tracción. Mientras tanto se trabaja sobre `otundra.github.io/ibiza-housing-radar`.

## Diagnóstico

**Lo que funciona.** Pipeline limpio, control de costes sólido, theme profesional, calidad editorial de la W17 alta (propuestas accionables, precedentes verificables, tono directo). La parte técnica está casi terminada.

**El problema real no es técnico, es de impacto.** Un observatorio que nadie lee no cambia nada. Estado actual:

- **0 distribución.** URL GitHub Pages sin dominio propio. No memorizable ni citable en prensa (aceptado hasta tracción).
- **0 tracking.** Sin analítica. Decisiones a ciegas.
- **0 feedback.** Vía de un solo sentido. Nadie puede contactar, corregir o aportar datos.
- **0 red.** Cáritas, IBAVI, sindicatos y periodistas aparecen en los informes pero no saben que existes.
- **Fuente secundaria pura.** Solo noticias refritas. Ningún dato original. Eso te deja como "blog más".
- **Monolingüe (ES).** Baleares es bilingüe (CA); parte del público objetivo (temporeros) habla inglés/italiano/rumano/árabe.
- **Autoría invisible.** Un observatorio de referencia tiene editor con nombre, método y política editorial pública.

Ser referente = que Diario de Ibiza te cite, que un regidor lea tu lunes, que un temporero reenvíe por WhatsApp. Nada de eso ocurre hoy.

---

## Fase 1 — Base imprescindible

Coste: 0 €. Duración estimada: 2-3 semanas.

1. **Dominio propio → diferido.** Se comprará cuando el proyecto tenga tracción (criterios sugeridos: >20 suscriptores al newsletter o una cita en prensa local). Mientras tanto, URL de GitHub Pages. Pérdida aceptada: imposible candidatarse a Google News, marca menos memorizable.
2. **Analítica privacy-friendly.** **GoatCounter** (gratis para sitios no comerciales, open-source, sin cookies) o **Cloudflare Web Analytics** (gratis ilimitado si el dominio pasa por CF, aplicable cuando haya dominio propio). Saber qué ediciones y propuestas se leen.
3. **Identidad editorial.** Página `/quien-edita` con nombre, método, sesgos reconocidos, política de correcciones. Firmar cada edición.
4. **Contacto + aportes.** **Formspree** gratis (50 env/mes) como opción principal; **Formsubmit.co** como fallback si se satura (gratis ilimitado con anti-spam básico). Formulario en `/contacto` y `/aportar-caso`. Email de contacto via alias Gmail hasta que haya dominio.
5. **Metodología pública.** Página `/metodologia`: cribado con Haiku, redacción con Opus, supervisión humana antes de publicar. Transparencia = credibilidad.
6. **Licencia Creative Commons (CC-BY)** en el footer. Invita a medios a reproducir citando.

## Fase 2 — Distribución activa

Coste: 0 €. Duración estimada: 3-4 semanas.

1. **Newsletter.** **Buttondown** (gratis <100 subs) o **Mailchimp** (gratis <500 subs, interfaz más pesada). Envío automático del lunes 10:00 CEST con la edición completa. Captura email en home y al final de cada edición. Cuando se aproxime el límite, reevaluar plan.
2. **Bot social.** Bluesky + Mastodon (gratis). GitHub Action publica un hilo los lunes con las señales + enlace. **No X**: ecosistema baleárico se ha movido a Bluesky y X obliga a pagar API.
3. **Envío directo.** Al publicar, email automático a lista curada (15-20 personas): periodistas de vivienda (Diario de Ibiza, Periódico, elDiario.es Baleares, Ara Balears), gabinetes Consell y ayuntamientos, Cáritas, GEN-GOB, sindicatos (CCOO, UGT, PIMEEF). Dos citas = referencia.
4. **SEO básico + multilingüe.** Meta OpenGraph, schema.org `NewsArticle`, sitemap.xml, robots.txt. Con el sitio trilingüe activo: `hreflang` por página en las 3 variantes, `og:locale` y `og:locale:alternate`, canonical por idioma, RSS feed separado por idioma (`feed.xml`, `feed.ca.xml`, `feed.en.xml`), title/description optimizados por idioma (no solo traducidos), `<html lang>` correcto. Google News verification queda bloqueada hasta que haya dominio propio; el resto del SEO sí se puede hacer ya. Ver detalle en sección *Bloque trilingüe — privacidad de costes — alertas*.

## Fase 3 — Contenido diferencial

Coste: 0 €. Duración estimada: 6-8 semanas. Aquí dejas de ser refrito y te vuelves fuente primaria.

1. **Observatorio de precios (ruta 0 €).** Dos vías complementarias en paralelo:

   **Vía A — Agregación de fuentes oficiales.** Script mensual que recoja datos de informes trimestrales públicos: Idealista (Informe de Precios), Fotocasa (Índice Inmobiliario), INE (ECV y EPA), IBESTAT, Ministerio de Vivienda (Observatorio del Alquiler). Publicar en `/precios` con gráfico de líneas, ficha por fuente con link al PDF original, y CSV descargable. Dato sólido, 0 € y 0 riesgo legal. Limitación: granularidad trimestral, mide vivienda general, no separa habitación.

   **Vía B — Crowd-sourcing ciudadano.** Formulario permanente en `/aportar-precio` (Formspree gratis <50/mes, Formsubmit gratis ilimitado como fallback) con campos:
   - Zona: dropdown con los 5 municipios de Ibiza (**toda la isla**).
   - Tipo: individual / compartida / cama en compartida / piso entero.
   - Precio mensual (€).
   - Duración: mensual / temporada / anual.
   - Suministros incluidos: sí / no / algunos.
   - ¿Trabajador de temporada?: sí / no.
   - Mes de inicio del contrato.
   - Email (opcional, no se publica).

   Política:
   - **Email: solo acuse automático.** No se responde personalmente salvo caso grave que Raúl decida escalar manualmente.
   - **Publicación anónima.** Cada respuesta se añade a `data/prices_crowd.csv` sin email ni metadatos personales; el CSV completo se publica como dato abierto descargable. Solo se publican agregados en la web (media, mediana, p25, p75 por zona y tipo).
   - **Umbral mínimo de publicación**: no publicar agregados de una zona/tipo hasta tener ≥10 respuestas en ese segmento, para evitar reidentificación.
   - **Sesgo muestral declarado** en `/metodologia`: muestra autoseleccionada, probablemente sesgada hacia quienes peor están. Triangular con Vía A.

   **Calendario:**
   - Semanas 1-4: montar Vía A, abrir formulario de Vía B (acumular sin publicar).
   - Junio-julio: empezar a publicar crowd-sourcing junto a oficial cuando ≥50 respuestas y ≥10 por zona.
   - Octubre: edición especial "Balance temporada" con dataset completo.

   El scraping directo de Idealista/Milanuncios queda descartado. Ver sección *Rutas descartadas*.
2. **Tracker de propuestas.** Cada edición genera 3-5 propuestas. Añadir columna `estado` (propuesta / recogida por medio / debatida en pleno / implementada / descartada). Página `/propuestas` con tabla filtrable. Convierte el informe en sistema de rendición de cuentas.
3. **BOIB watcher.** Scraping del BOIB diario filtrado por keywords (IBAVI, vivienda, alquiler, turístico). Alerta en la siguiente edición de normativa nueva. Alto valor, baja competencia. BOIB es publicación oficial pública, sin problema legal.
4. **Serie multi-semana.** Tag "Temporada 2026" agrupando ediciones mayo-octubre. Al cierre del verano, edición especial "Balance temporada": qué propusimos, qué pasó.
5. **Idioma.** *Desplazado a bloque prioritario propio, ver sección "Bloque trilingüe — privacidad de costes — alertas".* Decisión actualizada: las 3 versiones (ES/CA/EN) completas desde el día 1, no solo resumen.

## Fase 4 — Red y escala (opcional)

Coste: 0 €. Duración estimada: 3-6 meses.

1. **Consejo editorial honorífico.** 3-5 personas con credibilidad local (académico UIB, trabajador social de Cáritas, periodista senior, sindicalista). No pagan, no deciden contenido: prestan nombre y revisan una vez al trimestre. Multiplica credibilidad.
2. **Datos ciudadanos.** Formulario permanente para que temporeros reporten anonimizados precio/condiciones de su habitación. Mismo formulario que el del Observatorio de precios, se retroalimenta.
3. **Cobertura pitiusa.** Extender a Formentera. Mismo pipeline, fuentes adicionales.
4. **Evento anual de cierre de temporada.** Mesa redonda presencial en octubre, **co-organizada** con entidad local (UIB Ibiza, Cáritas, Ateneu, IBAVI o sindicatos): ellos ponen sala, tú pones contenido. Alternativa 100 % online (Meet/Jitsi) si no cuaja. Convierte proyecto digital en actor físico a coste 0.

---

## Mejoras técnicas puntuales

Sin relación con la estrategia pero deuda fácil. 1-2 días total. Todas 0 €.

- **Prompt caching en Opus** (`generate.py`): añadir `cache_control={"type": "ephemeral"}` al SYSTEM. Ahorro ~50 % del coste Opus (~1 €/mes). ROI inmediato.
- **Resiliencia en `classify.py`**: si Haiku devuelve menos items que el input, loguear y continuar con los válidos en vez de abortar.
- **Métricas de pipeline.** Al final de `report.py`, loguear en CSV: `n_feeds_ok`, `n_items_raw`, `n_housing`, `n_duplicates`. En 3 meses detectas degradación de fuentes.
- **Smoke test mínimo.** Mock de Anthropic + verificar que el pipeline end-to-end no se rompe al tocar algo.
- **Notificación de fallo.** Email si el cron falla. Hoy falla en silencio.

---

## Prioridades honestas (próximas 4 semanas)

4 cosas. Todas 0 € o coste marginal en API. El resto es deseable pero no crítico.

1. **Analítica (GoatCounter) + identidad editorial + metodología pública** (Fase 1.2, 1.3, 1.5). Desbloquea medición y credibilidad sin depender de nada externo.
2. **Newsletter + envío directo a periodistas** (Fase 2.1 + 2.3). La única vía realista a que te citen.
3. **Observatorio de precios por agregación + crowd-sourcing** (Fase 3.1). Lo único que te hace irremplazable; el formulario de precios se reutiliza en la Fase 4.2.
4. **Privacidad de costes + alertas Telegram + refactor `costs.py` a €** (sección "Bloque operativo inmediato" abajo). Saca la contabilidad del público, blinda el pipeline contra pérdidas por sobrecoste o fallo y expresa todo en euros. Coste marginal: 0 €. La parte trilingüe queda **diferida** con criterios de reactivación explícitos.

---

## Bloque operativo inmediato — privacidad de costes + alertas Telegram

Ejecución prioritaria, en paralelo a las Fases 1-2. Coste recurrente: 0 €.

### 1. Privacidad de costes

El CSV y el dashboard de costes salen de la carpeta pública:

- `data/costs.csv` se queda como está (repo público, no indexado porque no es HTML).
- `docs/costs.md` se elimina.
- Link "Costes" del nav del sitio se elimina.
- Dashboard regenerado por `src/costs.py` va a `private/costs.md` (carpeta excluida de Jekyll vía `_config.yml`).
- Consulta: Raúl abre el archivo desde su clon local o desde GitHub directamente. Sigue teniendo visibilidad completa, simplemente no está en la web pública.

### 2. Alertas Telegram + filosofía "no cortar editorial"

Cambio de diseño respecto al pipeline actual: **no se aborta en caso de sobrecoste blando**. El pipeline avisa y sigue publicando. Solo corta en caso extremo (tope duro = protección runaway).

**Capas de alerta:**

| Capa | Umbral gasto mes | Acción |
|---|---|---|
| Verde | < 4 € | Silencio |
| Amarilla | 4-6 € | Telegram FYI |
| Naranja | 6-8 € | Telegram atención |
| Roja blanda | 8-20 € | Telegram urgente + **sigue publicando** |
| Roja dura | > 20 € | **Corta** + Telegram crítico (protección runaway) |

**Qué notifica Telegram:**

- Resumen semanal tras publicar (OK / con avisos).
- Alerta de coste según capa.
- Excepciones no controladas del pipeline.
- API key inválida o sin créditos.
- (Cuando se active el trilingüe) fallo de validación de traducción.

**Infra:**

- Bot creado vía `@BotFather`. Token + `chat_id` personales como GitHub Secrets (`TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID`).
- Módulo `src/notify.py` con `send_telegram(message, level)`.
- **Fallback si Telegram falla:** crea issue en el propio repo (vía `gh` CLI) con la misma alerta. Doble red.
- Coste: 0 €. Telegram Bot API es gratis, GitHub issues es gratis.

### 3. Refactor `src/costs.py` a euros

- Migrar todo el cálculo interno a € (ahora en USD). Tipo de cambio fijo publicado en el propio módulo, revisable cada 3 meses.
- Topes: blando 8 €, duro 20 €.
- Cambio de filosofía: `assert_budget_available()` deja de lanzar excepción en tope blando; solo lanza en tope duro. En blando invoca `notify.send_telegram(...)` y devuelve `True` para seguir.
- Dashboard pasa a `private/costs.md`.

### 4. Coste actual en €

| Partida | Coste/mes |
|---|---|
| Clasificar noticias (Haiku) | 0,06 € |
| Generar informe ES (Opus 4.7) | 2,70 € |
| **Total actual** | **~2 €/mes** |
| **Tope blando** | 8 € |
| **Tope duro (corte)** | 20 € |

Margen del tope blando ≈ 4× el coste actual. Tope duro ≈ 10× el coste actual. Pensado para cubrir también el escenario trilingüe (~3,15 €/mes) sin tener que ajustar cuando se reactive.

### 5. Orden de ejecución

1. Crear bot de Telegram (Raúl) + configurar secrets (Claude).
2. Módulo `src/notify.py` con Telegram + fallback a issue.
3. Privatizar costes (mover `docs/costs.md` → `private/costs.md`, excluir de Jekyll, quitar enlace del nav).
4. Refactor `src/costs.py` a € + topes 8/20 + capas de alerta + filosofía no-corte-en-blando.
5. Integrar notificaciones en `report.py` (resumen semanal, excepciones).

---

## Trilingüe ES/CA/EN — **diferido**

Decisión 2026-04-20: no se monta ahora. Razones:

- El concepto editorial aún no está cerrado (identidad, metodología, newsletter, primera cita en prensa están pendientes). Montar trilingüe antes de tener audiencia es gastar tokens sin validar demanda.
- Mejor esperar a tener datos reales para decidir si CA y EN aportan.

**Criterios de reactivación** (basta con que se cumpla uno):

- Analítica muestra >10 % del tráfico llegando desde fuera de España durante 4 semanas consecutivas.
- 1 cita o mención en medio catalán (Ara Balears, Vilaweb, IB3) o anglófono.
- Newsletter supera 50 suscriptores y al menos 5 son de fuera de España o identificados como catalanohablantes.
- Raúl lo pide explícitamente porque el concepto está cerrado.

**Recordatorio activo:** en cada sesión en la que se cumpla alguno de los criterios de reactivación, Claude debe proponer explícitamente retomar este bloque. Límite: una sugerencia por sesión (respetando nivel de proactividad global).

### Decisiones ya tomadas para cuando se reactive

No repetir el análisis cuando toque ejecutar.

**Alcance:** chrome (nav, footer, home, /acerca, /ediciones) + ediciones semanales íntegras en ES/CA/EN desde el día 1 de la reactivación. Castellano = fuente de verdad. Sin versión EN reducida.

**Variante catalán: estándar IEC + glosario eivissenc (Opción A).** Justificación basada en estudio de medios locales:

- **IB3 Notícies Eivissa** (referencia pública) usa catalán estándar IEC desde 2015; abandonó el article salat en informativos.
- **Diario de Ibiza** y **Última Hora Ibiza** solo publican en castellano.
- **Periódico de Ibiza** y **NouDiari** reservan el balear con article salat para columnas de opinión y cultura popular, no para hard news.
- El catalán balear escrito en registro periodístico **casi no existe** como corpus. Riesgo de fallo del LLM traductor alto.

Variante = la del ARA, Vilaweb, IB3. Balear descartado.

**Glosario obligatorio** en el prompt del traductor:

| Término | Forma a usar |
|---|---|
| Ciudad | **Eivissa** (nunca "Ibiza" en texto catalán) |
| Municipios | **Sant Antoni de Portmany, Santa Eulària des Riu, Sant Josep de sa Talaia, Sant Joan de Labritja** (formas oficiales) |
| Microtopónimos | **Sa Penya, Dalt Vila, Ses Figueretes, Can Toni, es Cubells, s'Argentera, Cala Llonga** (literal desde el ES) |
| Gentilicio | **eivissenc/a** (nunca "ibicenc"); **pitiús/pitiüsa** para asuntos de ambas islas |
| Instituciones | **Consell d'Eivissa, IBAVI, GOIB, Govern Balear** (siglas literales) |
| Leyes y planes | Forma oficial catalana (*Llei d'habitatge de les Illes Balears*, *PTI d'Eivissa*) |

Regla dura adicional para el traductor: **nunca alterar palabras con mayúscula interior** (preserva topónimos insulares tipo "Can Toni", "Sa Penya" aunque coincidan con determinantes balear).

**Infra Jekyll sin plugins externos:** carpetas manuales `/ca/` y `/en/` + diccionario central `_data/i18n.yml` + `_includes/lang-switcher.html`. `polyglot` descartado (fuera de allowlist de GitHub Pages y la infra manual cubre lo necesario). El builder nativo de Pages sigue sirviendo el sitio; no se cambia la fuente de deploy.

**Estructura:**

- `/` → castellano (default).
- `/ca/` → catalán.
- `/en/` → inglés.
- Selector ES / CA / EN visible en todas las páginas.
- `<html lang>` correcto por idioma, `hreflang` por página apuntando a sus hermanas.

**Pipeline de generación y traducción:**

```
ingest → classify (Haiku) → generate ES (Opus) → translate CA (Sonnet) → translate EN (Sonnet) → validate → write 3 archivos .md
```

- Castellano = fuente de verdad. Opus genera solo en castellano.
- Traductor = Sonnet. Equilibrio calidad/coste. Haiku descartado para traducir por riesgo de aplanar el tono editorial.
- **Validador pre-publicación** protege contra alucinaciones:
  1. Mismo número de enlaces markdown que el ES.
  2. Mismas URLs (set igual).
  3. Mismas cifras (regex sobre `\d[\d.,]*\s*(€|%|m²|anys?/años?)`).
  4. Mismo número de bullets en "Señales" y propuestas.
  5. Si falla → publica solo ES + alerta Telegram. Nunca pierde editorial.

**Archivos:** `docs/_editions/YYYY-wWW.md` (ES), `docs/_editions/ca/YYYY-wWW.md` (CA), `docs/_editions/en/YYYY-wWW.md` (EN). Front-matter mantiene `date`, `week`, cifras y URLs; traduce `title` y `excerpt`. Permalinks: `/ediciones/YYYY-wWW/`, `/ca/edicions/YYYY-wWW/`, `/en/editions/YYYY-wWW/`.

**Coste esperado en modo trilingüe:** ~3,15 €/mes (+1,15 € sobre actual). Cubierto por los topes ya establecidos.

### SEO multilingüe (tarea separada, post-activación trilingüe)

Checklist para la sesión dedicada cuando el trilingüe esté montado:

- `hreflang` por página apuntando a sus hermanas ES/CA/EN (no solo home).
- URL canónica por idioma.
- Open Graph con `og:locale` y `og:locale:alternate` en `<head>`.
- Twitter Cards con locale correcto.
- JSON-LD `NewsArticle` por edición con `inLanguage`.
- Meta description única por página e idioma (alimentada del `excerpt` del front-matter).
- Sitemap XML con `<xhtml:link rel="alternate" hreflang="…">`.
- RSS separado por idioma: `feed.xml`, `feed.ca.xml`, `feed.en.xml`.
- `robots.txt` explícito: permitir todo excepto `/private/`.
- Internal linking: cada edición enlaza a las 2 anteriores y 2 siguientes del mismo idioma.
- Títulos y descripciones **optimizados** por idioma (no solo traducidos): EN enfatiza "Ibiza", "housing crisis", "seasonal workers"; CA enfatiza "Eivissa", "habitatge", "treballadors de temporada".

Coste API: 0 €. Tiempo estimado: ~2 h.

### Orden de ejecución cuando se reactive

1. Chrome trilingüe ES/CA/EN + selector + diccionario i18n.
2. Glosario eivissenc + prompt del traductor con Opción A.
3. Pipeline Python: generate ES + translate CA/EN + validador + escritura 3 archivos.
4. Integrar notificaciones de fallo de validación en Telegram.
5. Sesión dedicada de SEO multilingüe.

---

## Criterios para desbloquear gasto futuro

Cuando se cumpla al menos **uno** de estos criterios, revisar y considerar comprar dominio propio:

- >20 suscriptores reales al newsletter.
- 1 cita en prensa local (Diario de Ibiza, Periódico, elDiario.es Baleares, Ara Balears, etc.).
- 1 regidor, técnico municipal o sindicalista que se reconozca como lector habitual.
- 3 meses consecutivos con >200 lectores únicos mensuales según analítica.

Hasta entonces, GitHub Pages free tier.

---

## Lo que NO vamos a hacer

- **Instagram/TikTok.** Coste de producción alto, audiencia dispersa, no es el canal.
- **Podcast.** Consume horas, sin retorno para un observatorio de datos.
- **Monetización activa en 2026.** Foco en tracción. Solo canal pasivo de donaciones + `/financiacion` transparente. Ver sección *Monetización* para roadmap completo.
- **App nativa.** Sobre-ingeniería. Web responsive + newsletter cubre el 95 % del uso.
- **Ampliar a toda Baleares.** Diluye foco. Ibiza + Formentera primero; Mallorca/Menorca solo si la marca aguanta.
- **Scraping de Idealista/Milanuncios.** Descartado. Ver sección *Rutas descartadas*.

---

## Rutas descartadas con justificación

### Scraping directo de portales inmobiliarios (Idealista, Fotocasa, Milanuncios)

**Qué sería:** script que parsea listados públicos del portal y agrega estadísticas semanales por zona y tipo de habitación. Publicar solo agregados, nunca anuncios individuales.

**Por qué se descarta:**

1. **Contradicción reputacional.** Un proyecto que denuncia semanalmente el alquiler turístico ilegal no puede permitirse violar los TOS de un portal. Basta que un comentarista lo levante para inhabilitar la línea editorial.
2. **Riesgo legal real.** Idealista ha llevado a tribunales a terceros por scraping en España, con jurisprudencia favorable bajo competencia desleal (Ley 3/1991) y derecho *sui generis* del fabricante de bases de datos (arts. 133-137 LPI). No es empresa pasiva en defensa. Un cease-and-desist de sus abogados, aunque no llegue a juicio, mata el proyecto de precios.
3. **Coste real de consulta legal.** Un dictamen escrito de abogado especializado en propiedad intelectual ronda 500-1.500 €, no los 80 € que se estimaron en la primera versión del plan. Por debajo es apretón de manos sin valor probatorio.
4. **Valor marginal sobre Vía A + Vía B.** El scraping aporta granularidad semanal del precio de oferta, pero las vías limpias ya cubren lo esencial. Lo que más daña al mercado de temporeros es el circuito off-portal (Facebook Groups, WhatsApp, carteles), que el scraping **tampoco captura** — solo la Vía B llega ahí.
5. **Coste oculto de mantenimiento.** El DOM del portal cambia cada 3-6 meses; el scraper se rompe y hay que rehacerlo. Tiempo que Raúl no tiene.

**Ruta limpia de reserva — API oficial de partners.** Idealista y Fotocasa tienen programas de API para entidades sin ánimo de lucro. Requieren persona jurídica o proyecto con respaldo institucional (UIB, sindicato, ONG), solicitud justificada y aprobación manual. **Condiciones para reactivar esta línea:**

- Fase 4.1 cerrada: consejo editorial con al menos un miembro institucional.
- Solicitud de API aprobada por vía oficial.
- En ningún caso scraping contra TOS, ni aunque la API sea rechazada.

Si la API se rechaza tras cumplir las condiciones, se reevalúa — pero **nunca** reintroducir scraping directo.

---

## Monetización

Techo realista honesto si todo va bien en año 3-5: **5-20 k€/año combinados**. No es un proyecto que financie un salario. Puede complementar ingresos, cubrir dedicación parcial o costear infra/tiempo.

### Condicionantes que acotan todas las vías

- **Misión social explícita.** Cualquier ingreso de actores con intereses en el mercado de vivienda/turismo mata la credibilidad editorial. No es reversible.
- **Nicho geográfico pequeño.** Ibiza tiene ~150 k residentes + ~100 k temporeros. Mercado de pago limitado.
- **Público partido.** Los afectados (temporeros) no pagan; quienes pueden pagar (instituciones, académicos, periodistas) esperan acceso público por interés general.
- **Sin persona jurídica.** Hoy es repo personal. Sin asociación/cooperativa el techo de grants y convenios es bajo.

### Vías compatibles con la misión

| Vía | Realista año 1 | Realista año 3 | Esfuerzo | Riesgo misión |
|---|---|---|---|---|
| **Donaciones pasivas** (Ko-fi, GitHub Sponsors, Liberapay, Open Collective) | 50-300 € | 500-2.000 € | Mínimo | Nulo |
| **Grants periodísticos y de innovación social** (Google News Initiative, Meta Journalism, Caixa, Fundación Sa Nostra, Govern Balear, Institut d'Estudis Eivissencs, NextGenerationEU) | 0 € (sin persona jurídica no cualificas) | 5-25 k€ si ganas una sola | Alto (2-4 semanas por propuesta) | Bajo |
| **Consultoría a instituciones** (Consell, ayuntamientos, IBAVI, sindicatos) — Raúl factura aparte | 0 € | 3-10 k€ | Medio | Medio-alto (captura editorial) |
| **Partnership institucional** (cátedra UIB, convenio con Cáritas o sindicato) | 0 € | 2-5 k€ | Alto | Bajo |
| **Charlas y mesas redondas** | 0 € | 400-4 k€ | Bajo marginal | Bajo |
| **Libro/informe anual** (Amazon KDP o editorial local) | 0 € | 500-3 k€ | Alto | Bajo (valor real = posicionamiento, no €) |
| **Membership voluntario** (Substack/Buttondown paid tier con extras opcionales) | 0-200 € | 500-2 k€ | Medio | Medio (riesgo de paywall percibido) |
| **Licencia del dataset** (API premium, exports personalizados para medios/consultoras) | 0 € | 500-2 k€ | Medio | Bajo |
| **Servicios freelance derivados** (montar radares temáticos para otros) | 0 € | 3-9 k€ | Alto | Bajo (negocio separado) |

### Vías grises

- **Merchandising simbólico** (camiseta/tote con frase fuerte, impresión a demanda). 100-500 €/año. Más branding que ingreso. Tiene sentido en evento presencial de Fase 4.4.

### Líneas rojas (descartadas sin matices)

- **Publicidad o sponsored content** de cualquier actor con intereses en vivienda/turismo.
- **Affiliate** de plataformas inmobiliarias o de alquiler turístico.
- **Paywall total** del informe semanal principal.
- **Aceptar encargo** del mismo actor al que se está fiscalizando esa misma semana.
- **Ocultar** cualquier fuente de financiación.

### Transparencia radical

Publicar en `/financiacion` cada ingreso, origen, fecha e importe. Única forma de que la monetización no erosione la credibilidad editorial. Misma lógica que `/metodologia`: lo que no se hace público, pesa en contra.

### Roadmap de monetización

**2026 (año 1) — tracción, monetización cero activa.**
- Abrir Ko-fi o GitHub Sponsors como canal pasivo (10 min). Enlace discreto en footer y en `/quien-edita`. Sin push.
- Publicar `/financiacion` con situación real: "proyecto sostenido por tiempo voluntario del editor; coste directo actual ~2 €/mes de API Anthropic, costeado por Raúl Serrano".

**2027 (año 2) — institucionalización mínima.**
- Constituir asociación sin ánimo de lucro (60-300 €, requiere 3 personas — buscar aliados del consejo editorial Fase 4.1).
- Aplicar a 1-2 grants específicos.
- Aceptar primera charla o encargo institucional si aparece, con reglas de transparencia publicadas.
- Libro anual opcional si hay material.

**2028+ (año 3 en adelante) — diversificación si el proyecto pesa.**
- Grant ganado o consultoría consolidada como base.
- Partnership institucional con UIB o similar.
- Charlas regulares.
- Licencia de dataset si hay demanda profesional real.

---

## Riesgos reales

1. **Reputacional.** Una propuesta de Opus con cifra mal estimada erosiona credibilidad. Mitigación: página `/correcciones` pública + revisión humana obligatoria antes del commit del lunes.
2. **Sesgo IA.** Opus tiende a propuestas "progresistas". Mitigación: sesgo reconocido en `/metodologia` + consejo editorial mixto (Fase 4.1).
3. **Sesgo muestral del crowd-sourcing.** Los que responden son autoseleccionados (probablemente los que pagan más o están peor). Mitigación: avisarlo explícitamente y triangular con fuentes oficiales.
4. **Fatiga editor.** Revisar cada lunes cuesta ~30 min reales. Diseñar el proceso para aguantar sin Raúl 2 semanas al año.

---

## Seguimiento

Al cerrar cada punto, actualizar [`DIARIO.md`](DIARIO.md) con la entrada correspondiente y marcar aquí el estado.

| Fase | Punto | Estado |
|---|---|---|
| 1 | Dominio propio | diferido (hasta tracción) |
| 1 | Analítica (GoatCounter) | pendiente |
| 1 | Identidad editorial | pendiente |
| 1 | Contacto + aportes (Formspree) | pendiente |
| 1 | Metodología pública | pendiente |
| 1 | Licencia CC-BY | pendiente |
| 2 | Newsletter (Buttondown free) | pendiente |
| 2 | Bot social (Bluesky + Mastodon) | pendiente |
| 2 | Envío directo a periodistas | pendiente |
| 2 | SEO básico | pendiente |
| 3 | Observatorio de precios — Vía A (agregación oficial) | pendiente |
| 3 | Observatorio de precios — Vía B (crowd-sourcing, toda isla, acuse auto, CSV anónimo) | pendiente |
| 3 | Tracker de propuestas | pendiente |
| 3 | BOIB watcher | pendiente |
| 3 | Serie multi-semana | pendiente |
| Operativo | Privatizar costes (fuera de `docs/`) | ✅ hecho 20-abr-2026 |
| Operativo | Bot Telegram + alertas por capas | ✅ hecho 20-abr-2026 |
| Operativo | Fallback Telegram → issue GitHub | ✅ hecho 20-abr-2026 |
| Operativo | Refactor `costs.py` a €, tope blando 8 €, tope duro 20 € | ✅ hecho 20-abr-2026 |
| Operativo | Resumen semanal vía Telegram en `report.py` | ✅ hecho 20-abr-2026 |
| Trilingüe | Chrome ES/CA/EN + selector + diccionario i18n | **diferido** |
| Trilingüe | Glosario eivissenc + prompt Sonnet (Opción A) | **diferido** |
| Trilingüe | Pipeline 3 idiomas + validador de datos | **diferido** |
| Trilingüe | SEO multilingüe (hreflang, feeds por idioma, JSON-LD) | **diferido** |
| 4 | Consejo editorial | pendiente |
| 4 | Datos ciudadanos | pendiente |
| 4 | Cobertura Formentera | pendiente |
| 4 | Evento anual co-organizado | pendiente |
| Técnico | Prompt caching Opus | pendiente |
| Técnico | Resiliencia classify | pendiente |
| Técnico | Métricas de pipeline | pendiente |
| Técnico | Smoke test | pendiente |
| Técnico | Notificación de fallo | pendiente |
| Monetización | Ko-fi / GitHub Sponsors pasivo | pendiente (año 1) |
| Monetización | Página `/financiacion` transparente | pendiente (año 1) |
| Monetización | Constituir asociación sin ánimo de lucro | pendiente (año 2) |
| Monetización | Aplicar a primer grant | pendiente (año 2) |
