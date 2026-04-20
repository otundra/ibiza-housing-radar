# Plan de mejora — Ibiza Housing Radar

Estrategia para convertir el proyecto en un observatorio de referencia sobre vivienda de trabajadores en Ibiza. Registro vivo: actualizar al cerrar cada fase.

Última revisión: 2026-04-20.

## Principio económico

**Coste-cero salvo IA.** Único gasto aceptado: llamadas a la API de Anthropic (~2 €/mes, tope duro 5 €/mes en `src/costs.py`). Toda herramienta externa debe tener alternativa 0 € o quedar diferida hasta que el proyecto demuestre tracción.

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
4. **SEO básico.** Meta OpenGraph, schema.org `NewsArticle`, sitemap.xml, robots.txt. Google News verification queda bloqueada hasta que haya dominio propio; el resto del SEO sí se puede hacer ya.

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
5. **Idioma.** Versión CA automatizada (Claude traduce, coste marginal IA) y resumen EN de 200 palabras por edición para temporeros internacionales. No traducir todo, solo resumen + propuestas.

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

Solo 3 cosas. Todas 0 €. El resto es deseable pero no crítico.

1. **Analítica (GoatCounter) + identidad editorial + metodología pública** (Fase 1.2, 1.3, 1.5). Desbloquea medición y credibilidad sin depender de nada externo.
2. **Newsletter + envío directo a periodistas** (Fase 2.1 + 2.3). La única vía realista a que te citen.
3. **Observatorio de precios por agregación + crowd-sourcing** (Fase 3.1). Lo único que te hace irremplazable; el formulario de precios se reutiliza en la Fase 4.2.

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
- **Monetización en 2026.** Matar credibilidad por 20 €/mes de publicidad es mal trade. Mantén gratis y CC-BY al menos el primer año.
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
| 3 | Idioma CA + resumen EN | pendiente |
| 4 | Consejo editorial | pendiente |
| 4 | Datos ciudadanos | pendiente |
| 4 | Cobertura Formentera | pendiente |
| 4 | Evento anual co-organizado | pendiente |
| Técnico | Prompt caching Opus | pendiente |
| Técnico | Resiliencia classify | pendiente |
| Técnico | Métricas de pipeline | pendiente |
| Técnico | Smoke test | pendiente |
| Técnico | Notificación de fallo | pendiente |
