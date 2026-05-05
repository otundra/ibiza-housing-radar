# Auditoría sistémica 2026-05-05 — bootstrap

- **Fecha:** 2026-05-05
- **Disparador:** petición explícita del editor (tercer disparador de [D24](../../DECISIONES.md#d24--freno-al-pozo-de-modificación-infinita-auditoría-sistémica--termómetro--convención)), tras abrir D22 + D23 + D24 en una sola sesión.
- **Modelo activo:** opus + xhigh
- **Sesgo declarado:** auditoría hecha en la misma sesión que abrió D24. Es bootstrap. La utilidad real del mecanismo se medirá en la segunda auditoría, cuando el sistema haya cambiado de forma genuina desde que se montó el freno.

## Línea base

| Subsistema | Cuenta |
|---|---|
| Reglas duras adicionales en prompt del generador | 17 |
| Dimensiones del revisor | 6 (reglas, rigor, balance, cobertura, claridad, trazabilidad) |
| Reglas fundacionales del observatorio | 5 + 1 complementaria |
| Reglas de gestión documental | 5 (regla 5 añadida hoy) |
| Decisiones registradas | 25 (D0–D24) |
| Decisiones vigentes | 22 (al cierre de la auditoría, con D24 ya en estado vigente) |

## Contradicciones detectadas

1. **Tensión `blocks_cited` — proponentes contra todos los actor_types citados.** La regla del prompt del generador limita `blocks_cited` a actor_types que PROPONEN (en `formal` o `en_movimiento`); el revisor de W19 pidió la lectura amplia (todos los actor_types citados en el cuerpo). Ya documentada hoy en el seguimiento de [`private/revisiones/2026-w19.md`](../revisiones/2026-w19.md). Estado: **vigilar W20**. Voto preformado para el caso de reapertura: alinear el prompt del revisor a la regla del generador, no al revés (la regla restrictiva sirve al cálculo del balance trimestral montado en `src/balance.py`).
2. **D21 supera parcialmente a D18 durante el rodaje.** No es contradicción activa — D21 lo declara explícitamente. Sin acción.
3. **D11 superada por D15** — explícitamente marcada. Sin acción.

**Veredicto:** una contradicción activa real (`blocks_cited`), ya en seguimiento desde antes de la auditoría.

## Redundancias detectadas

1. **Trazabilidad de fuente expresada en cuatro lugares distintos:**
   - Regla 1 fundacional (URL verificable).
   - Regla "DECLARA LA NATURALEZA DE CADA CIFRA" del prompt del generador.
   - Regla "FUENTE AGREGADA ETIQUETADA" del prompt del generador (añadida hoy).
   - Dimensión "trazabilidad" del revisor (D22, añadida hoy).

   **Diagnóstico:** son ángulos distintos del mismo concepto (fundacional / generación / evaluación), no duplicación. Se refuerzan, no chocan. **Vigilar** — si la dimensión trazabilidad da nota constante en W20–W23 sin warnings nuevos, retirarla y dejar las dos del generador como sustituto operativo.
2. **Lenguaje llano en chat — registrado en tres sitios** (CLAUDE.md proyecto + memoria del asistente + global). Justificado por feedback recurrente y disciplina que ha fallado cinco veces. Sin acción.

**Veredicto:** una redundancia tolerada con vigilancia, ninguna duplicación clara que toque retirar hoy.

## Zombis detectados

1. **Claridad como dimensión del revisor.** Tres semanas dando 9/10 sin warnings concretos. Ya en seguimiento. La heurística automática del termómetro empieza a funcionar en W21 (necesita cuatro ediciones). **Acción programada** — revisar tras W21.
2. **D14 efecto (f) — aviso de decisiones vencidas con pocas activaciones.** D14 misma reconoce que D15 dejó casi todas las decisiones en formato evento/hito (no fecha ISO), por lo que el aviso 1 dispara poco. El primer disparo real será D17 el 8 de junio. **Vigilar** ese momento como test de utilidad del aviso.
3. **Reglas duras del generador sin warning asociado.** No automatizable con la heurística actual del termómetro. Apuntar como mejora futura del termómetro.

**Veredicto:** un zombi pendiente confirmar (claridad), un zombi en observación condicional (D14 aviso 1), ninguno listo para retirar hoy.

## Presupuesto de complejidad

| Subsistema | Cuenta | Umbral sugerido | Margen |
|---|---|---|---|
| Reglas del generador | 17 | ≤20 | 🟢 holgado |
| Dimensiones del revisor | 6 | ≤6 con claridad como candidata | 🟡 en límite |
| Decisiones vigentes | 21 | ≤30 | 🟢 holgado |

🟡 sobre dimensiones: 6 es el techo natural. Hasta retirar claridad, no añadir más dimensiones del revisor.

## Acciones acordadas

Ninguna inmediata. Todos los hallazgos están en seguimiento natural por mecanismos ya existentes:

| Hallazgo | Mecanismo de seguimiento | Próxima cita |
|---|---|---|
| Tensión `blocks_cited` | seguimiento en revisión W19 | W20 (lunes 11 de mayo) |
| Claridad zombi | seguimiento en `APRENDIZAJES.md` + termómetro | W21 (lunes 18 de mayo) |
| Redundancia de trazabilidad | criterio de revocación de D22 | W23 (lunes 1 de junio) |
| D14 aviso 1 sin disparos | criterio (a) de D14 + revisión D17 | 8 de junio |
| Reglas del generador sin warning | mejora del termómetro | abierto |

## Veredicto bootstrap

🟢 **El sistema está controlado.** Las contradicciones detectadas ya están documentadas o en seguimiento. Las redundancias son por diseño (refuerzo en distintos planos). La única dimensión muerta (claridad) ya tiene plan. Los conteos están dentro de presupuesto.

**Aviso de calibración para la siguiente auditoría.** Si la próxima (cuando dispare por D29 o por 90 días desde hoy) tampoco encuentra problema enquistado, aplicar el criterio (a) de revocación de D24: bajar frecuencia a 6 meses o desmantelar.

## Cierre

- Auditoría registrada en `data/auditorias.csv` con trigger `manual` y la nota *"bootstrap — sistema controlado, sin acciones inmediatas"* el 2026-05-05.
- Próximo disparo automático del aviso por Telegram: cuando aparezca D29 o el 2026-08-03 (90 días), lo que ocurra antes.
- Este informe queda como referencia. Para abrir la siguiente auditoría: ver [`AUDITORIAS.md`](../../AUDITORIAS.md).
