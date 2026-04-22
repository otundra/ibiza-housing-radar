// Variant C — Solar Low-Tech / brutalist-transparent
// Monospace on code-ish surfaces (status bar, paths, counters, listings).
// Headline + body respect the serif/sans toggle so the tweak is visible.
// Discreet dark-mode toggle lives in the top status bar.

const VariantC = ({ tw, setTw }) => {
  const d = window.RADAR_DATA;
  const t = d.transparency;
  const toggleDark = () => setTw && setTw("dark", !tw.dark);
  return (
    <div className="radar" data-heads={(tw && tw.heads) || "sans"} style={{ width: "100%", height: "100%", overflow: "hidden", fontFamily: "var(--ff-mono)", fontSize: "calc(var(--d-text) * 1.25)" }}>
      {/* TOP STATUS BAR — always visible, mono always */}
      <div style={{ background: "var(--ink)", color: "var(--paper)", padding: "7px 36px", fontSize: 11.5, letterSpacing: 0.04, display: "flex", gap: 22, alignItems: "center", fontFamily: "var(--ff-mono)" }}>
        <span style={{ display: "inline-flex", alignItems: "center", gap: 6 }}>
          <span style={{ width: 7, height: 7, borderRadius: "50%", background: "var(--alert-yellow)", display: "inline-block" }} />
          PIPELINE.OK · 4/4 jobs
        </span>
        <span style={{ opacity: .7 }}>│</span>
        <span>API_COST_MTD = <b className="tnum">{t.apiCost}</b></span>
        <span style={{ opacity: .7 }}>│</span>
        <span>ALERT.LAYER = 2/4 (yellow)</span>
        <span style={{ opacity: .7 }}>│</span>
        <span>LAST_EDIT = <span className="tnum">{t.lastEdit}</span></span>
        <span style={{ flex: 1 }} />
        <span>commit <b>a4f1c22</b></span>
        <span style={{ opacity: .7 }}>│</span>
        <span>build 00:08.2s</span>
        <span style={{ opacity: .7 }}>│</span>
        <button onClick={toggleDark} title="Modo oscuro"
          style={{ background: "transparent", border: "1px solid rgba(244,241,234,.25)", color: "var(--paper)", cursor: "pointer", padding: "2px 8px", fontFamily: "inherit", fontSize: 11, letterSpacing: 0.06, borderRadius: 2 }}>
          {tw && tw.dark ? "◐ dark" : "◑ light"}
        </button>
      </div>

      {/* HEADER */}
      <header style={{ padding: "22px 36px 16px", borderBottom: "2px solid var(--ink)" }}>
        <div className="row between mono" style={{ fontSize: 11.5, letterSpacing: 0.1, textTransform: "uppercase", color: "var(--ink-3)" }}>
          <span>/home/ibiza-housing-radar/</span>
          <span>edition_{String(d.edition.number).padStart(3, "0")}.md · {d.edition.label.toLowerCase()}</span>
        </div>
        <h1 style={{ fontSize: 52, lineHeight: 1, letterSpacing: -0.018, fontWeight: 600, marginTop: 16, fontFamily: "var(--ff-mono)" }}>
          ibiza_housing_radar <span style={{ color: "var(--ink-3)" }}>v.17</span>
        </h1>
        <p style={{ fontSize: 17, color: "var(--ink-2)", marginTop: 14, maxWidth: 760, lineHeight: 1.55, fontFamily: "var(--ff-mono)" }}>
          // Observatorio semanal de vivienda en Ibiza.<br/>
          // Mapeamos lo que se propone. No proponemos nosotros.<br/>
          // 5 reglas duras en <a href="politica-editorial.html">/politica-editorial/</a>. Balance público en <a href="balance.html">/balance/</a>.
        </p>
        <div className="mono" style={{ display: "flex", gap: 8, marginTop: 14, fontSize: 11.5, flexWrap: "wrap" }}>
          <a href="como-usarlo.html" style={{ padding: "6px 10px", border: "1px solid var(--ink)", textDecoration: "none", color: "var(--ink)" }}>[?] cómo usarlo</a>
          <a href="edicion.html" style={{ padding: "6px 10px", border: "1px solid var(--ink)", background: "var(--ink)", color: "var(--paper)", textDecoration: "none" }}>[→] última edición</a>
          <a href="ediciones.html" style={{ padding: "6px 10px", border: "1px solid var(--ink)", textDecoration: "none", color: "var(--ink)" }}>[□] archivo</a>
          <a href="propuesta.html" style={{ padding: "6px 10px", border: "1px solid var(--ink)", textDecoration: "none", color: "var(--ink)" }}>[◊] propuestas</a>
          <a href="actor.html" style={{ padding: "6px 10px", border: "1px solid var(--ink)", textDecoration: "none", color: "var(--ink)" }}>[△] actores</a>
          <a href="recursos.html" style={{ padding: "6px 10px", border: "1px solid var(--ink)", textDecoration: "none", color: "var(--ink)" }}>[≡] recursos</a>
          <a href="balance.html" style={{ padding: "6px 10px", border: "1px solid var(--ink)", textDecoration: "none", color: "var(--ink)" }}>[$] balance</a>
        </div>
      </header>

      {/* WEEK SUMMARY — counters */}
      <section style={{ padding: "16px 36px", borderBottom: "1px solid var(--ink)", background: "var(--paper-2)" }}>
        <div style={{ display: "grid", gridTemplateColumns: "auto 1fr auto auto auto", gap: 32, alignItems: "center", fontSize: 13 }}>
          <div>
            <div style={{ fontSize: 10.5, textTransform: "uppercase", letterSpacing: 0.12, color: "var(--ink-3)" }}>WEEK</div>
            <div style={{ fontSize: 22, fontWeight: 600 }} className="tnum">S-{d.edition.week}</div>
          </div>
          <div style={{ fontSize: 13.5, color: "var(--ink-2)", lineHeight: 1.5 }}>
            Govern retrasa decreto de tope · Patronal reabre suelo rústico · 1.400 temporeros sin alojamiento confirmado · TSJIB anula moratoria de Sant Josep.
          </div>
          {[
            { k: "signals", v: d.edition.signals },
            { k: "proposals", v: d.edition.proposals },
            { k: "omisiones", v: d.edition.omisiones },
          ].map((it) => (
            <div key={it.k} style={{ textAlign: "right", borderLeft: "1px solid var(--rule)", paddingLeft: 20 }}>
              <div style={{ fontSize: 10.5, textTransform: "uppercase", letterSpacing: 0.12, color: "var(--ink-3)" }}>{it.k}</div>
              <div style={{ fontSize: 22, fontWeight: 600 }} className="tnum">{String(it.v).padStart(2, "0")}</div>
            </div>
          ))}
        </div>
      </section>

      {/* SIGNALS — file-listing style */}
      <section style={{ padding: "18px 36px", borderBottom: "1px solid var(--ink)" }}>
        <div className="row between" style={{ marginBottom: 10 }}>
          <div style={{ fontSize: 11.5, letterSpacing: 0.1, textTransform: "uppercase", color: "var(--ink-3)" }}>## signals_of_the_week.md</div>
          <span className="small muted">{d.signals.length} registros · ordenar por fecha ↓</span>
        </div>
        <div style={{ fontFamily: "var(--ff-mono)", fontSize: 12.5, lineHeight: 1.5 }}>
          {d.signals.slice(0, 7).map((s, i) => (
            <div key={i} style={{ display: "grid", gridTemplateColumns: "32px 120px 1fr", gap: 16, padding: "6px 0", borderTop: i > 0 ? "0.5px dashed var(--rule)" : "0" }}>
              <span style={{ color: "var(--ink-4)" }}>{String(i + 1).padStart(3, "0")}</span>
              <span style={{ color: "var(--ink-3)" }}>{s.actor}</span>
              <span>
                <span style={{ color: "var(--ink)" }}>{s.text}</span>{" "}
                <a href={"https://" + s.url} style={{ color: "var(--ink-3)" }}>↗ {s.url}</a>
              </span>
            </div>
          ))}
        </div>
      </section>

      {/* 2 cols — positions & proposals preview */}
      <section style={{ padding: "18px 36px", borderBottom: "1px solid var(--ink)" }}>
        <div style={{ display: "grid", gridTemplateColumns: "1.1fr 1fr", gap: 36 }}>
          <div>
            <div style={{ fontSize: 11.5, letterSpacing: 0.1, textTransform: "uppercase", color: "var(--ink-3)", marginBottom: 10 }}>## positions_map.tsv</div>
            <PositionsTable />
            <div className="small muted" style={{ marginTop: 8, fontSize: 11 }}>
              ● yes · ○ no · ◐ amb · · nil // partidos en gris neutro por política editorial
            </div>
          </div>
          <div>
            <div style={{ fontSize: 11.5, letterSpacing: 0.1, textTransform: "uppercase", color: "var(--ink-3)", marginBottom: 10 }}>## proposals_feed.json (preview)</div>
            <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 20 }}>
              {d.proposals.slice(0, 4).map((p, i) => <ProposalCard key={i} p={p} compact />)}
            </div>
          </div>
        </div>
      </section>

      {/* Rescate · Omisiones · Vigilar */}
      <section style={{ padding: "18px 36px", borderBottom: "1px solid var(--ink)" }}>
        <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr 1fr", gap: 28 }}>
          {[
            { h: "## archive_rescue.md", list: d.rescate.map((r) => ({ a: r.year, b: r.text })) },
            { h: "## silences.md", list: d.omisiones.map((o) => ({ a: "—", b: o })) },
            { h: "## watchlist.md", list: d.vigilar.map((v) => ({ a: v.when, b: v.text })) },
          ].map((col, idx) => (
            <div key={idx}>
              <div style={{ fontSize: 11.5, letterSpacing: 0.1, textTransform: "uppercase", color: "var(--ink-3)", marginBottom: 10 }}>{col.h}</div>
              <div style={{ fontSize: 12.5, lineHeight: 1.5 }}>
                {col.list.map((it, i) => (
                  <div key={i} style={{ display: "grid", gridTemplateColumns: "auto 1fr", gap: 12, padding: "7px 0", borderTop: i > 0 ? "0.5px dashed var(--rule)" : "0" }}>
                    <span style={{ color: "var(--ink-4)", minWidth: 60 }}>{it.a}</span>
                    <span style={{ color: "var(--ink)" }}>{it.b}</span>
                  </div>
                ))}
              </div>
            </div>
          ))}
        </div>
      </section>

      {/* Archive list */}
      <section style={{ padding: "16px 36px 22px" }}>
        <div style={{ fontSize: 11.5, letterSpacing: 0.1, textTransform: "uppercase", color: "var(--ink-3)", marginBottom: 10 }}>## editions/ (ls -la, head -4)</div>
        <div style={{ fontSize: 12.5, lineHeight: 1.6 }}>
          {d.archive.map((a, i) => (
            <div key={i} style={{ display: "grid", gridTemplateColumns: "90px 180px 1fr auto", gap: 16, padding: "6px 0", borderTop: "0.5px dashed var(--rule)" }}>
              <span style={{ color: "var(--ink-4)" }}>ed_{String(a.n).padStart(3, "0")}.md</span>
              <span style={{ color: "var(--ink-3)" }}>{a.label}</span>
              <span>{a.headline}</span>
              <span className="muted small">{a.signals} s · {a.proposals} p</span>
            </div>
          ))}
        </div>
      </section>

      <TranspFooter pad="0 36px" />
    </div>
  );
};

window.VariantC = VariantC;
