# Protocolo interno — Cuando alguien avisa de un error

> Documento de uso interno. No servido por GitHub Pages.
> La página pública de este proceso vive en `/correcciones/`.

---

## Los dos casos que pueden llegar

### Caso A — Error claro de hecho

Ejemplos: enlace caído, nombre mal escrito, fecha equivocada, cita transcrita con error evidente.

**Cómo reconocerlo:** se puede verificar en 5 minutos mirando la fuente original. No depende de interpretación.

### Caso B — Reclamación de un actor

Ejemplos: "eso no lo dije", "el contexto era otro", "representáis mal nuestra posición".

**Cómo reconocerlo:** el actor discute el sentido o la interpretación, no un dato comprobable con un clic.

---

## Plazos

| Paso | Plazo | Qué haces |
|---|---|---|
| Acusar recibo | 24 horas | Contestas que lo has recibido y que lo revisas. Sin comprometerte a nada más. |
| Resolución | 72 horas desde el aviso | Decides y actúas. Si necesitas más tiempo, lo dices y das una nueva fecha. |

Los plazos corren desde que llega el aviso por cualquier canal (correo, formulario, issue de GitHub).

---

## Quién decide y con qué criterio

Decides tú, como editor. Nadie más.

El criterio único es: **¿el aviso señala un error de hecho verificable con la fuente original?**

- Si sí → se corrige (Caso A).
- Si no → no se toca el contenido. Se puede añadir nota de contexto si aporta algo al lector, pero la propuesta documentada no se retira ni se edita.

La presión del actor (importancia, volumen de mensajes, amenazas veladas de difusión) no es criterio. Lo que importa es si hay un error de hecho.

---

## Qué hacer en cada caso

### Caso A — Corregir

1. Verificar el error con la fuente original. Si el error existe, anotar: qué es, dónde está, cuál es la versión correcta.
2. Corregir el texto en la edición afectada.
3. Añadir nota de corrección visible en la página `/correcciones/` con: fecha, propuesta afectada, descripción del error y corrección aplicada.
4. Marcar la edición original como *corregida* con enlace a la nota.
5. Actualizar el campo de correcciones en el registro del auditor (`data/audit/`) si la propuesta afectada tiene entrada ahí.
6. Responder al que avisó con la plantilla A de abajo.

### Caso B — No corregir (pero responder)

1. Releer la propuesta documentada y la fuente original. Verificar que lo publicado refleja con exactitud lo que la fuente dice.
2. Si lo publicado es correcto: no tocar nada.
3. Si al releer detectas un matiz que, aunque no es un error, podría añadir contexto útil al lector: puedes añadir una nota breve al pie de la propuesta sin cambiar el texto original. Esto es opcional y solo si el matiz aporta algo real.
4. Responder al que avisó con la plantilla B de abajo.
5. No hay entrada en `/correcciones/` si no hubo corrección.

---

## Plantillas de respuesta

### Plantilla A — Corrección aplicada

> Hola [nombre o "estimado/a"],
>
> Gracias por avisar. Hemos revisado la propuesta que señalas y tienes razón: [descripción breve del error]. La hemos corregido.
>
> La corrección queda registrada en nuestra página de correcciones con fecha y detalle: [enlace].
>
> Un saludo,
> Radar Vivienda Ibiza

### Plantilla B — Sin corrección, con explicación

> Hola [nombre o "estimado/a"],
>
> Gracias por escribir. Hemos revisado la propuesta que mencionas y contrastado con la fuente original: [nombre del medio / URL].
>
> Lo publicado recoge con exactitud lo que aparece en esa fuente. El observatorio documenta lo que los actores formulan en público con fuente verificable; no podemos modificar ese registro basándonos en una interpretación posterior de lo dicho.
>
> Si hay un error de hecho concreto que podamos verificar, escríbenos de nuevo con el detalle y lo revisamos.
>
> Un saludo,
> Radar Vivienda Ibiza

### Plantilla de acuse de recibo (primeras 24 h)

> Hola [nombre o "estimado/a"],
>
> Recibido tu aviso sobre [tema breve]. Lo estamos revisando y te respondemos en las próximas 48-72 horas.
>
> Un saludo,
> Radar Vivienda Ibiza

---

## Qué NO hacer bajo ningún concepto

- **No editar el contenido en silencio.** Cualquier cambio deja rastro en `/correcciones/` y en git.
- **No retirar una propuesta porque al actor no le gusta.** La única razón para retirar es error de hecho verificado.
- **No ceder por presión.** Si el actor es un partido grande, una institución o alguien con mucho seguimiento, el criterio es el mismo que con un ciudadano desconocido.
- **No responder a disputas políticas o de interpretación como si fueran errores de hecho.** Son cosas distintas.
- **No ignorar un aviso.** Aunque decidas no corregir, siempre se responde dentro del plazo.

---

## Cuándo escalar

Si llega un aviso que menciona acciones legales, requerimiento notarial o abogado, no respondas tú directamente. Guarda el mensaje y consulta antes de actuar. Esto queda cubierto por el Hito 3 (resolución legal) antes del empuje público.

---

*Creado: 2026-04-29. Revisión: antes del empuje público (Hito 3).*
