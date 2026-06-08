# Tablero interno — monitorización del proyecto

*Archivo privado. No se publica en la web. Última actualización: 2026-06-08 09:26 UTC.*

Agrega las señales que otros módulos ya producen: gasto del mes, autoevaluación, verificación, decisiones con revisión pendiente, última edición. No genera datos propios. Ver decisión D14.

## Costes del mes

- **Gasto actual:** 1.92 € (blando 12 € / duro 50 €) — 🟢 Verde (<6 €) — silencio
- **Dashboard detallado:** [`costs.md`](costs.md)

## Decisiones con revisión pendiente

### ⚠️ Próximas (≤7 días)

- **Ritual de aprendizaje semanal + temperature=0 en self-review** (D17) — vence el 2026-06-08 (hoy)

## Última edición publicada

- `2026-w24`

## Histórico de propuestas

- **Total acumulado:** 22

## Verificación (última ejecución)

- **Resultado:** ✅ sin fallos bloqueantes
- **URLs comprobadas:** 34, caídas: 0
- **Actores comprobados:** 0, no trazables: 0
- **Avisos blandos:** 2

## Autoevaluación (último corte)

## 2026-W23 · 2026-06-01 10:25 UTC
- Scores bajos: rigor=5
- Detalle: [2026-w23.md](private/self-review/2026-w23.md)

## Salud sistémica (termómetro de complejidad)

Termómetro orientativo para detectar pozo de modificación infinita. Disparador de auditoría sistémica (D24) cuando los conteos crezcan más rápido que la utilidad real.

- **Reglas duras adicionales en el prompt del generador:** 19
- **Dimensiones del revisor (self-review):** 6
- **Decisiones vigentes en `DECISIONES.md`:** 42
- **Candidatas a retirar** (dimensiones con nota constante en últimas 4 ediciones):
    - claridad (constante en 9/10 durante 4 ediciones)

---

Fuente de datos: `DECISIONES.md`, `data/costs.csv` (vía `src.costs`), `data/verification_report.json`, `data/proposals_history.json`, `private/self-review-log.md`, `docs/_editions/`. Regenerado por `src.panel`.
