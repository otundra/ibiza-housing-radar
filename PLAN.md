# Plan de mejora — Ibiza Housing Radar

Estrategia para convertir el proyecto en un observatorio de referencia sobre vivienda de trabajadores en Ibiza. Registro vivo: actualizar al cerrar cada fase.

Última revisión: 2026-04-20.

## Diagnóstico

**Lo que funciona.** Pipeline limpio, control de costes sólido, theme profesional, calidad editorial de la W17 alta (propuestas accionables, precedentes verificables, tono directo). La parte técnica está casi terminada.

**El problema real no es técnico, es de impacto.** Un observatorio que nadie lee no cambia nada. Estado actual:

- **0 distribución.** URL `otundra.github.io/ibiza-housing-radar` sin dominio propio. No memorizable ni citable en prensa.
- **0 tracking.** Sin analítica. Decisiones a ciegas.
- **0 feedback.** Vía de un solo sentido. Nadie puede contactar, corregir o aportar datos.
- **0 red.** Cáritas, IBAVI, sindicatos y periodistas aparecen en los informes pero no saben que existes.
- **Fuente secundaria pura.** Solo noticias refritas. Ningún dato original. Eso te deja como "blog más".
- **Monolingüe (ES).** Baleares es bilingüe (CA); parte del público objetivo (temporeros) habla inglés/italiano/rumano/árabe.
- **Autoría invisible.** Un observatorio de referencia tiene editor con nombre, método y política editorial pública.

Ser referente = que Diario de Ibiza te cite, que un regidor lea tu lunes, que un temporero reenvíe por WhatsApp. Nada de eso ocurre hoy.

---

## Fase 1 — Base imprescindible

Sin esto, el resto da igual. Coste one-shot ≈ 20 €. Duración estimada: 2-3 semanas.

1. **Dominio propio.** `radaribiza.org` o similar (~12 €/año). Apuntar a GitHub Pages vía `CNAME`. Marca memorable, citable, permanente.
2. **Analítica privacy-friendly.** Plausible (~9 €/mes) o Umami self-hosted (0 €). Saber qué ediciones y propuestas se leen.
3. **Identidad editorial.** Página `/quien-edita` con nombre, método, sesgos reconocidos, política de correcciones. Firmar cada edición.
4. **Contacto + aportes.** Formspree gratis (50 env/mes). Formulario en `/contacto` y `/aportar-caso`. Email `radar@<dominio>`.
5. **Metodología pública.** Página `/metodologia`: cribado con Haiku, redacción con Opus, supervisión humana antes de publicar. Transparencia = credibilidad.
6. **Licencia Creative Commons (CC-BY)** en el footer. Invita a medios a reproducir citando.

## Fase 2 — Distribución activa

Coste ≈ 5 €/mes. Duración estimada: 3-4 semanas.

1. **Newsletter.** Buttondown (<100 subs gratis, 9 $/mes después). Envío automático del lunes 10:00 CEST con la edición completa. Captura email en home y al final de cada edición.
2. **Bot social.** Bluesky + Mastodon (gratis). GitHub Action publica un hilo los lunes con las señales + enlace. **No X**: ecosistema baleárico se ha movido a Bluesky y X obliga a pagar API.
3. **Envío directo.** Al publicar, email automático a lista curada (15-20 personas): periodistas de vivienda (Diario de Ibiza, Periódico, elDiario.es Baleares, Ara Balears), gabinetes Consell y ayuntamientos, Cáritas, GEN-GOB, sindicatos (CCOO, UGT, PIMEEF). Dos citas = referencia.
4. **SEO básico.** Meta OpenGraph, schema.org `NewsArticle`, sitemap.xml, robots.txt. Google News verification (requiere dominio ≥30 días + política editorial publicada → por eso la Fase 1 primero).

## Fase 3 — Contenido diferencial

Duración estimada: 6-8 semanas. Aquí dejas de ser refrito y te vuelves fuente primaria.

1. **Observatorio de precios.** Scraping ético (respetando robots.txt y rate-limit) de Idealista y Milanuncios filtrado por "habitación Ibiza". Guardar precio medio/mediana semanal en CSV. En 3 meses tienes serie temporal que nadie más tiene. Datos agregados públicos, sin reproducir anuncios individuales. Consulta legal previa (~80 €).
2. **Tracker de propuestas.** Cada edición genera 3-5 propuestas. Añadir columna `estado` (propuesta / recogida por medio / debatida en pleno / implementada / descartada). Página `/propuestas` con tabla filtrable. Convierte el informe en sistema de rendición de cuentas.
3. **BOIB watcher.** Scraping del BOIB diario filtrado por keywords (IBAVI, vivienda, alquiler, turístico). Alerta en la siguiente edición de normativa nueva. Alto valor, baja competencia.
4. **Serie multi-semana.** Tag "Temporada 2026" agrupando ediciones mayo-octubre. Al cierre del verano, edición especial "Balance temporada": qué propusimos, qué pasó.
5. **Idioma.** Versión CA automatizada (Claude traduce, coste marginal) y resumen EN de 200 palabras por edición para temporeros internacionales. No traducir todo, solo resumen + propuestas.

## Fase 4 — Red y escala (opcional)

Duración estimada: 3-6 meses.

1. **Consejo editorial honorífico.** 3-5 personas con credibilidad local (académico UIB, trabajador social de Cáritas, periodista senior, sindicalista). No pagan, no deciden contenido: prestan nombre y revisan una vez al trimestre. Multiplica credibilidad.
2. **Datos ciudadanos.** Formulario permanente para que temporeros reporten anonimizados precio/condiciones de su habitación. En 1 temporada, dataset que ni INE ni IBAVI tienen.
3. **Cobertura pitiusa.** Extender a Formentera. Mismo pipeline, fuentes adicionales.
4. **Eventos anuales.** Mesa redonda presencial en octubre cerrando temporada. Convierte proyecto digital en actor físico.

---

## Mejoras técnicas puntuales

Sin relación con la estrategia pero deuda fácil. 1-2 días total.

- **Prompt caching en Opus** (`generate.py`): añadir `cache_control={"type": "ephemeral"}` al SYSTEM. Ahorro ~50 % del coste Opus (~1 €/mes). ROI inmediato.
- **Resiliencia en `classify.py`**: si Haiku devuelve menos items que el input, loguear y continuar con los válidos en vez de abortar.
- **Métricas de pipeline.** Al final de `report.py`, loguear en CSV: `n_feeds_ok`, `n_items_raw`, `n_housing`, `n_duplicates`. En 3 meses detectas degradación de fuentes.
- **Smoke test mínimo.** Mock de Anthropic + verificar que el pipeline end-to-end no se rompe al tocar algo.
- **Notificación de fallo.** Email si el cron falla. Hoy falla en silencio.

---

## Prioridades honestas (próximas 4 semanas)

Solo 3 cosas. El resto es deseable pero no crítico.

1. **Dominio propio + analítica** (Fase 1.1 + 1.2). Sin esto, no hay métrica de nada.
2. **Newsletter + envío directo a periodistas** (Fase 2.1 + 2.3). La única vía realista a que te citen.
3. **Observatorio de precios** (Fase 3.1). Lo único que te hace irremplazable.

---

## Lo que NO vamos a hacer

- **Instagram/TikTok.** Coste de producción alto, audiencia dispersa, no es el canal.
- **Podcast.** Consume horas, sin retorno para un observatorio de datos.
- **Monetización en 2026.** Matar credibilidad por 20 €/mes de publicidad es mal trade. Mantén gratis y CC-BY al menos el primer año.
- **App nativa.** Sobre-ingeniería. Web responsive + newsletter cubre el 95 % del uso.
- **Ampliar a toda Baleares.** Diluye foco. Ibiza + Formentera primero; Mallorca/Menorca solo si la marca aguanta.

---

## Riesgos reales

1. **Legal (scraping Idealista).** Operar con datos agregados, sin reproducir anuncios. Consulta de 1 h con abogado antes de lanzar el observatorio de precios (~80 €).
2. **Reputacional.** Una propuesta de Opus con cifra mal estimada erosiona credibilidad. Mitigación: página `/correcciones` pública + revisión humana obligatoria antes del commit del lunes.
3. **Sesgo IA.** Opus tiende a propuestas "progresistas". Mitigación: sesgo reconocido en `/metodologia` + consejo editorial mixto (Fase 4.1).
4. **Fatiga editor.** Revisar cada lunes cuesta ~30 min reales. Diseñar el proceso para aguantar sin Raúl 2 semanas al año.

---

## Seguimiento

Al cerrar cada punto, actualizar [`DIARIO.md`](DIARIO.md) con la entrada correspondiente y marcar aquí el estado.

| Fase | Punto | Estado |
|---|---|---|
| 1 | Dominio propio | pendiente |
| 1 | Analítica | pendiente |
| 1 | Identidad editorial | pendiente |
| 1 | Contacto + aportes | pendiente |
| 1 | Metodología pública | pendiente |
| 1 | Licencia CC-BY | pendiente |
| 2 | Newsletter | pendiente |
| 2 | Bot social | pendiente |
| 2 | Envío directo a periodistas | pendiente |
| 2 | SEO básico | pendiente |
| 3 | Observatorio de precios | pendiente |
| 3 | Tracker de propuestas | pendiente |
| 3 | BOIB watcher | pendiente |
| 3 | Serie multi-semana | pendiente |
| 3 | Idioma CA + resumen EN | pendiente |
| 4 | Consejo editorial | pendiente |
| 4 | Datos ciudadanos | pendiente |
| 4 | Cobertura Formentera | pendiente |
| 4 | Evento anual | pendiente |
| Técnico | Prompt caching Opus | pendiente |
| Técnico | Resiliencia classify | pendiente |
| Técnico | Métricas de pipeline | pendiente |
| Técnico | Smoke test | pendiente |
| Técnico | Notificación de fallo | pendiente |
