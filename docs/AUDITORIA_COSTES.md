# Auditoría histórica de costes — ibiza-housing-radar

**Fecha de cierre:** 2026-05-05
**Periodo cubierto:** 2026-04-20 → 2026-05-05 (15 días desde primer registro real).
**Periodo `no_data`:** anterior al 2026-04-20 (el proyecto no estaba en producción; sin actividad IA previa).
**Plantilla origen:** `panel/docs/AUDITORIA_TEMPLATE.md`.

---

## 1. Inventario de fuentes (Paso 1 plantilla)

Marca por fuente:

### Costes directos del proyecto

- [x] **IA medida (Anthropic API directa)** — Haiku 4.5 + Sonnet 4.6 + Opus 4.7. Todo registrado en `data/costs.csv`.
- [ ] IA via servicios externos
- [x] **Infra Cloudflare** — Workers + D1 + R2 + Cron Triggers. **Free tier**, coste 0 €.
- [ ] Base de datos pago
- [ ] **Dominio** — `radaribiza.com` candidato pendiente de compra. Hoy se sirve en `otundra.github.io/ibiza-housing-radar` (gratis, GitHub Pages).
- [ ] Email transaccional
- [x] **Storage R2** — backups de D1 (free tier 10 GB).
- [ ] CDN / monitoring
- [ ] Físicos
- [ ] Servicios humanos puntuales

### Costes compartidos imputables

- [x] **Claude Max** — reparto por coste imputable desde `~/.claude/projects/<folder>/*.jsonl`. Detalle abajo.
- [ ] Otras suscripciones del editor.

---

## 2. Trazado: dónde vive cada coste hoy (Paso 2)

| Fuente | Tracking actual | Histórico recuperable | Notas |
|---|---|---|---|
| Anthropic API directa | `data/costs.csv` (schema propio: `ts, edition, stage, model, input_tokens, output_tokens, cache_*, cost_usd`) | ✅ desde 2026-04-20, completo, 128 filas | Schema propio del proyecto, no se migra a `log_cost.{py,ts}` para no romper scripts |
| Cloudflare (Workers + D1 + R2) | Dashboard CF | hoy `0 €` (free tier) | Sin pago previsto |
| Dominio | manual | n/a | Candidato `radaribiza.com` no comprado |
| Suscripción Claude Max | `~/.claude/projects/` jsonl | ✅ recuperable, calculado | Ver §4 |

---

## 3. Histórico recuperado de Anthropic API directa (Paso 3)

Fuente: `data/costs.csv` (128 filas, 2026-04-20 → 2026-05-05).

| Mes | Calls | Coste USD | Coste EUR (FX 0,92) | Estado |
|---|---:|---:|---:|---|
| 2026-04 | 121 | $7,4611 | €6,8642 | ✅ frozen |
| 2026-05 | 7 | $0,6560 | €0,6035 | en curso |
| **Total** | **128** | **$8,1171** | **€7,4677** | |

Por modelo (todo el periodo):

| Modelo | Calls | Tokens in/out | Coste USD |
|---|---:|---:|---:|
| Opus 4.7 | (mayoría del coste) | — | $7,2394 |
| Sonnet 4.6 | — | — | $0,6278 |
| Haiku 4.5 | — | — | $0,2499 |

Topes definidos en `src/costs.py` v3:
- **Blando**: 12 USD/mes — solo avisa.
- **Duro**: 50 USD/mes — corta pipeline.

Hoy ambos meses están muy por debajo del tope blando.

---

## 4. Reparto Claude Max compartido (Paso 3)

Calculado por `panel/scripts/compute-claude-max-attribution.py` leyendo los `.jsonl` de las 7 carpetas de Claude Code asociadas a ibiza (raíz + 6 worktrees).

- **Coste imputable abr-may 2026**: $971,88 USD si se hubiera pagado por API directa.
- **Porcentaje del total Max**: 25,98 %.
- **Reparto del cargo Apple 140,92 € (con IVA)**: **36,61 €**.
- Periodo cubierto: 2026-04-08 (inicio Pro) → 2026-05-04.
- Detalle global y método en `panel/docs/costes/01_inventario.md` §1.1.ter.

---

## 5. Volcado a `data/costs.csv` (Paso 4)

**No se hace volcado adicional**: el csv del proyecto ya existe desde día 1 con schema propio que el panel sabe leer directamente. Migrar al schema homogéneo `log_cost.{py,ts}` (timestamp, amount, currency, category, recurrence, support, source_label, event_id, extra_json) rompería los scripts de pipeline (`src/extract.py`, `src/audit.py`, `src/costs.py`) que escriben con el formato actual.

**Si en futuro se quiere homogeneizar**: añadir helper `lib/costs/to_homogeneous.py` que convierte sobre la marcha al lectores externos pidan formato estándar. Decisión aplazada.

---

## 6. `costes.json` v2 generado (Paso 5)

Regenerado por este script. Contiene:
- `recurring_variable.current_month` — mayo 2026 con suma exacta hasta `as_of`.
- `recurring_variable.history` — abril 2026 cerrado y mayo en curso.
- `recurring_variable.ceiling` — tope blando 12 USD/mes (€11,04 con FX 0,92), `behavior: warn_only`.
- `shared_attribution.claude_max` — reparto 36,61 €/mes con IVA, 25,98 % del total imputable.
- `notes` — explicación del schema propio del csv y la conversión FX constante 0,92.

Sello `certainty: exact` para todas las cifras de Anthropic API (vienen de `data/costs.csv` que es append-only desde dentro del propio pipeline).
Sello `certainty: exact` para Claude Max share (cálculo determinista desde jsonl, no estimación).

---

## 7. Resumen final

**Periodo cubierto:** 2026-04-20 → 2026-05-05 con cifras `exact`.
**Periodo `no_data`:** anterior al 2026-04-20 — el proyecto no operaba.

### Fuentes recuperadas

- ✅ `csv:data/costs.csv` — desde 2026-04-20, 128 filas completas.
- ✅ `~/.claude/projects/` — reparto Max abr-may, calculado.

### Fuentes irrecuperables

- ❌ Coste de IA antes de 2026-04-20 — el proyecto no operaba con IA antes.

### Cambios en el sistema de captura desde hoy

- `data/costs.csv` sigue como fuente única del proyecto, escrito por `src/costs.py` desde el pipeline.
- `costes.json` v2 lo agrega el script de auditoría (este flujo) o el conector del panel cuando se construya en Fase 4b/5.
- Reparto Claude Max actualizado mensualmente vía `panel/scripts/compute-claude-max-attribution.py` ejecutado por el panel.

---

## 8. Verificación cruzada con el panel

Tras volcar `costes.json`:
1. Refrescar el panel (`localhost:3000` → "Actualizar").
2. Verificar que ibiza aparece con `current_month: €0,60` y `history` con abril cerrado.
3. Comparar el `claude_max.current_month_share_eur` con el dato global del panel — coincide con `26,99 €` calculado para wallapop, etc., suma 140,92 €.
