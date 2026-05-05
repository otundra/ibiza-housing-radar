# AUDITORÍAS — Radar Vivienda Ibiza

Registro de **auditorías sistémicas del propio proyecto**: contradicciones entre reglas, redundancias, dimensiones y reglas zombi, presupuesto de complejidad. Decisión asociada: [D24](DECISIONES.md#d24--freno-al-pozo-de-modificación-infinita-auditoría-sistémica--termómetro--convención).

Las auditorías individuales viven en [`private/auditorias/`](private/auditorias/) (no servido por GitHub Pages). Este archivo raíz es índice + manual de uso.

---

## Para qué sirve

Sin auditoría humana periódica que mire el conjunto, las contradicciones, redundancias y zombis se enquistan invisibles. Cada decisión se revisa por su `Próxima revisión` individual, pero nadie lee las 25+ decisiones, las 17+ reglas del prompt del generador y las 6 dimensiones del revisor a la vez. La auditoría es ese momento.

## Cuándo se crea una auditoría

Disparada automáticamente por `decisions_watch.py` cada lunes vía Telegram cuando se cumple alguna de estas tres:

1. **≥90 días desde la última auditoría registrada.** Cuenta desde la fila más reciente de `data/auditorias.csv`.
2. **≥5 decisiones nuevas desde la última auditoría.** Cuenta el último ID `D{N}` registrado en `DECISIONES.md` y compara con el `last_decision_id` de la última fila del CSV.
3. **El editor lo pide.** Disparador manual; siempre prevalece.

El aviso por Telegram llega como bloque 🩺 dentro del mensaje semanal de `decisions_watch.py`. Mientras la auditoría no se registre como cerrada, el aviso reaparece cada lunes.

## Cómo lanzar una auditoría nueva

Cuando llegue el aviso (o cuando lo decidas tú), abre sesión con el asistente y ejecuta:

```
/cierre
```
o simplemente di *"toca auditoría sistémica, lánzala"*.

El asistente debe leer:

- `DECISIONES.md` completo
- Sección `REGLAS DURAS ADICIONALES` del SYSTEM en `src/generate.py`
- Sección `Devuelve JSON con` y dimensiones del SYSTEM en `src/self_review.py`
- Reglas fundacionales y reglas de gestión documental en `CLAUDE.md` del proyecto
- Apartado "Salud sistémica" del último `private/panel.md` regenerado
- Las dos auditorías anteriores (si existen) para detectar repeticiones

Y producir un informe con la **plantilla** de abajo. La sesión típica son 30-60 minutos en Opus + xhigh.

## Cómo cerrar una auditoría (registrar)

Cuando el informe esté escrito y guardado en `private/auditorias/YYYY-MM-DD-{slug}.md`, registrar el cierre con:

```bash
python -m src.decisions_watch --register-audit \
  --audit-note "una frase corta describiendo el estado al cierre"
```

Esto añade fila a `data/auditorias.csv` con la fecha de hoy, el último `D{N}` registrado y el conteo de decisiones vigentes. **Reinicia los dos contadores** (días y crecimiento de decisiones), y silencia el aviso por Telegram hasta el siguiente disparo.

Si te olvidas de registrar, el aviso seguirá saliendo cada lunes — es de diseño.

## Cómo silenciar manualmente sin auditar

Si por algún motivo necesitas silenciar el aviso sin haber hecho una auditoría real (ej. estás de viaje y la pospones), añade fila al CSV con `trigger=manual_silence` y nota explicando el motivo:

```bash
python -m src.decisions_watch --register-audit \
  --audit-note "silencio temporal — auditoría aplazada hasta YYYY-MM-DD por X razón"
```

El contador se reinicia igual; reaparecerá cuando vuelvan a cumplirse los disparadores. Honesto contigo: si abusas de esto, pierdes la red de seguridad.

## Plantilla de un archivo de auditoría

Cada archivo sigue esta estructura mínima:

```markdown
# Auditoría sistémica YYYY-MM-DD — {slug}

- **Fecha:** YYYY-MM-DD
- **Disparador:** ≥90 días / ≥5 decisiones nuevas / petición del editor
- **Modelo activo:** opus + xhigh (recomendado)
- **Sesgo declarado:** (si aplica)

## Línea base

Tabla con conteos actuales de cada subsistema.

## Contradicciones detectadas

Lista por número. Cada una con diagnóstico + acción propuesta.

## Redundancias detectadas

Lista por número. Cada una con diagnóstico + acción.

## Zombis detectados

Reglas/dimensiones/decisiones que no han generado señal en N semanas.

## Presupuesto de complejidad

Tabla con cuenta actual, umbral sugerido, margen.

## Acciones acordadas

Tabla con hallazgo + mecanismo de seguimiento + próxima cita.

## Veredicto

🟢/🟡/🔴 + frase resumen.

## Cierre

- Comando ejecutado para registrar.
- Próximo disparo previsto.
```

## Reglas

- **Una auditoría, un archivo.** Nombre `YYYY-MM-DD-{slug}.md`. El slug es libre (bootstrap, trimestral, decisiones-aceleradas…).
- **Append-only.** No editar auditorías cerradas. Si una decisión se reabre meses después, abrir nueva auditoría que cite la antigua.
- **Cierre con registro.** Sin la fila en `data/auditorias.csv`, la auditoría no cuenta como cerrada y el aviso sigue saliendo. Es de diseño.
- **Coste declarado.** Si la sesión cuesta >90 minutos del editor, anotarlo en el cierre. Es señal de que la plantilla pide simplificarse (criterio (b) de revocación de D24).

## Distinción con REVISIONES.md y APRENDIZAJES.md

|  | APRENDIZAJES | REVISIONES | AUDITORÍAS |
|---|---|---|---|
| Sujeto | sugerencias del revisor automático | edición publicada concreta | el propio sistema (reglas + dimensiones + decisiones) |
| Granularidad | una fila por sugerencia | un archivo por edición revisada | un archivo por auditoría |
| Frecuencia | cada lunes (continua) | cuando dispara alerta de revisor | cada 90 días o tras 5 decisiones nuevas |
| Tamaño típico | 1-3 líneas por entrada | 200-800 palabras por archivo | 400-1200 palabras por archivo |
| Rol | lección destilada | debate humano sobre la edición | mirada al conjunto del sistema |
| Estado | pendiente / aplicada / descartada | narrativa cerrada | informe cerrado + registro CSV |

## Índice

| Fecha | Slug | Disparador | Veredicto | Archivo |
|---|---|---|---|---|
| 2026-05-05 | bootstrap | petición del editor | 🟢 sistema controlado, sin acciones inmediatas | [`private/auditorias/2026-05-05-bootstrap.md`](private/auditorias/2026-05-05-bootstrap.md) |

---

*Última actualización: 2026-05-05.*
