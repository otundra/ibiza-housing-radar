---
layout: page
title: Método
permalink: /metodo/
---

Cómo funciona el observatorio por dentro: cómo se captura la información cada semana, qué hace el sistema automático con ella, qué criterios aplica, qué actores reconoce, qué sesgos declaramos y qué no hace este proyecto. Si algo aquí no cuadra con lo que ves en las ediciones, es un error — [avísanos](/correcciones/).

---

## Cómo se captura la información

Cada lunes a primera hora, el sistema lee automáticamente los titulares de prensa local de la semana anterior: Google News, Diario de Ibiza y Periódico de Ibiza. Filtra por palabras clave relacionadas con vivienda, alquiler y temporada, descarta duplicados y verifica que cada noticia tenga enlace accesible.

Solo entra lo que ya ha sido publicado por un medio. No hacemos scraping de redes sociales, no procesamos comunicados no publicados, no escuchamos fuentes de confianza.

Los criterios exactos de qué noticias se convierten en propuestas documentadas y cuáles no están en [/que-documentamos/](/que-documentamos/).

---

## Qué hace el sistema con cada noticia

El proceso tiene ocho pasos automáticos que corren en secuencia:

1. **Lectura y filtrado.** Recoge los titulares, quita duplicados y deja solo lo publicado en los últimos 10 días.
2. **Clasificación.** Un modelo de IA ligero revisa cada titular y decide si está relacionado con vivienda y si hay una propuesta formal detrás. Lo hace en una sola pasada para los 15-30 titulares típicos de cada semana.
3. **Extracción de la ficha.** Para cada noticia con propuesta, un modelo más potente extrae la información estructurada: quién propone, qué propone exactamente, qué palanca (oferta de vivienda, regulación, ayudas…), en qué horizonte temporal, con qué viabilidad declarada. Si la extracción resulta contradictoria, un tercer modelo actúa como árbitro.
4. **Rescate de propuestas anteriores.** Busca en el histórico propuestas de semanas previas que siguen vigentes pero no han aparecido en 4 semanas. Las incorpora a la edición con una marca visible para no perder el hilo.
5. **Redacción de la edición.** El modelo de mayor calidad redacta el informe semanal completo en 7 secciones. No genera propuestas nuevas: solo ordena y resume las documentadas.
6. **Verificación.** Comprueba que todos los enlaces citados responden. Si un enlace no carga, la propuesta queda marcada como *fuente caída* y no se publica hasta recuperación. También aplica una lista de verbos prohibidos para detectar si el sistema ha colado alguna opinión propia.
7. **Actualización del balance.** Recalcula la distribución de citas por tipo de actor y actualiza [/balance/](/balance/).
8. **Autoevaluación.** Un modelo diferente al que escribió la edición la puntúa en cinco dimensiones: cumplimiento de las reglas, rigor de las fuentes, equilibrio de actores, cobertura y claridad. Si alguna puntuación es baja, llega un aviso al editor.

Todo el código es público: [github.com/otundra/ibiza-housing-radar](https://github.com/otundra/ibiza-housing-radar).

---

## Modelos de IA usados

Usamos tres modelos de Anthropic, cada uno en la fase donde aporta la mejor relación calidad/coste:

| Tarea | Modelo | Por qué |
|---|---|---|
| Clasificar titulares | Haiku (el más ligero) | Los titulares son cortos. El modelo barato basta y reduce costes 20 veces respecto al siguiente. |
| Extraer fichas estructuradas | Sonnet (intermedio) | Las fichas son largas y exigen precisión en los campos. |
| Árbitro en extracciones dudosas | Opus (el más potente) | Solo interviene en ~5% de los casos donde Sonnet detecta contradicción. |
| Redactar la edición | Opus | La calidad del informe final sí importa. |
| Autoevaluación | Sonnet | Que el texto lo revise un modelo distinto al que lo escribió reduce la tendencia a auto-confirmarse. |

Coste típico por edición: entre 0,50 y 1,50 €. Mes completo: ~6-7 €. Los topes automáticos cortan si el gasto se dispara por encima de 20 € al mes.

No mezclamos modelos a mitad de una misma ejecución: cambiar rompe la memoria compartida del sistema y sube el coste sin mejorar el resultado.

---

## Taxonomía de actores

El sistema reconoce 8 tipos de actor. La lista está cerrada: añadir un tipo nuevo requiere decisión editorial formal. Los casos en la frontera se asimilan al tipo más cercano con una nota.

- **Institucional público** — Consell d'Eivissa, Govern Balear, ayuntamientos, IBAVI. Organismos con competencia administrativa directa.
- **Partido político** — PP, PSOE, Vox, Sumar, MÉS, Proposta per les Illes. Regla visual dura: siempre en gris neutro, nunca en el color del partido.
- **Patronal** — CAEB, PIMEEF, Fecoei, Ashome, COAPI. Asociaciones empresariales.
- **Sindicato** — CCOO, UGT, CSIF, USO. Representación laboral organizada.
- **Tercer sector** — Cáritas, Cruz Roja, GEN-GOB. ONG y entidades sin ánimo de lucro con programa público.
- **Académico** — UIB, IBESTAT, consultoras, colegios profesionales. Función técnico-consultiva.
- **Judicial** — TSJIB, juzgados, Fiscalía, Síndic de Greuges. Intervención vía resoluciones o declaraciones institucionales.
- **Colectivo ciudadano** — PAH Pitiüses, Ens Plantem, asambleas de temporeros. Plataformas sin personalidad jurídica rígida. El sistema los capta peor porque comunican más por redes sociales que por prensa escrita.

---

## Sesgos declarados

Ningún observatorio es neutral. Enumeramos los sesgos conocidos. Si detectas uno no listado, [escríbenos](/correcciones/).

- **Sesgo de fuente:** solo leemos prensa escrita (RSS). Lo que se dice en televisión, radio, podcast, redes sociales o en conversación privada no entra hasta que un diario lo recoge.
- **Sesgo de cobertura mediática:** los diarios cubren más a las instituciones que a los colectivos ciudadanos. El balance de [/balance/](/balance/) lo refleja semana a semana.
- **Sesgo del sistema de IA:** los modelos que usamos están entrenados globalmente y pueden tener tendencias favorables a la retórica institucional o al castellano frente al catalán. Contamos con una verificación cruzada entre dos modelos distintos en los casos dudosos.
- **Sesgo idiomático:** más del 90% del corpus está en castellano. El contenido en catalán se procesa correctamente pero representa menos del 10% del volumen total.
- **Sesgo del editor:** un solo editor decide qué fuentes se leen y qué palabras clave se usan como filtro. La auditoría trimestral de balance es la principal vacuna.
- **Sesgo de horizonte temporal:** el observatorio empieza a documentar en la semana del 3 al 9 de febrero de 2026. Las propuestas anteriores a esa fecha no están cubiertas, aunque sean relevantes o se repitan hoy. Cuando una propuesta aparece como *"primera vez documentada"*, significa siempre primera vez en este observatorio — no en la historia del debate.

---

## Qué NO hace este observatorio

- **No genera propuestas propias.** No inferimos, no completamos, no sintetizamos propuestas que nadie haya formulado.
- **No evalúa viabilidad jurídica o económica** salvo cuando la fuente lo declare explícitamente.
- **No hace scraping de portales inmobiliarios** ni medios de pago. Los datos de precio vendrán de fuentes oficiales (INE, IBESTAT, ministerio) en una fase futura.
- **No recibe financiación de actores que documenta** — instituciones, partidos, patronales, sindicatos, promotoras. El modelo sostenible a futuro es donaciones, becas periodísticas y consultoría con transparencia total sobre los ingresos.
- **No publica sin fuente verificable.** Si el enlace no responde, la propuesta no se publica.
- **No edita en silencio.** Cada cambio post-publicación pasa por [/correcciones/](/correcciones/).

---

## Transparencia

No pedimos confianza — ofrecemos lo que se puede verificar:

- **Código fuente completo:** [github.com/otundra/ibiza-housing-radar](https://github.com/otundra/ibiza-housing-radar) — licencia MIT.
- **Contenido:** Creative Commons CC BY 4.0. Reutilizable citando la fuente.
- **Balance de actores en vivo:** [/balance/](/balance/).
- **Registro de correcciones:** [/correcciones/](/correcciones/).
- **Registro de decisiones del proyecto** y costes reales: disponibles en el repositorio público.
