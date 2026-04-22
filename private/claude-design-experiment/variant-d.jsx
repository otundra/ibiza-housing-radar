// Variant D — Minimal all-serif, NYT Opinion calm
// Generous whitespace, serif throughout, real Tufte sidenotes column on
// the right. Single-column reading feel. Authority without density.

const VariantD = () => {
  const d = window.RADAR_DATA;
  return (
    <div className="radar" data-heads="serif" style={{ width: "100%", height: "100%", overflow: "hidden", fontFamily: "var(--ff-serif)" }}>
      {/* NAV */}
      <div style={{ padding: "16px 72px", borderBottom: "0.5px solid var(--rule)", display: "flex", alignItems: "baseline", gap: 22, fontSize: 13, fontFamily: "var(--ff-sans)" }}>
        <span style={{ fontFamily: "var(--ff-serif)", fontSize: 15, fontWeight: 500, letterSpacing: -0.01 }}>Ibiza Housing Radar</span>
        <span className="mono small muted" style={{ fontSize: 11 }}>Núm. {d.edition.number}</span>
        <span style={{ flex: 1 }} />
        <a href="#" style={{ textDecoration: "none", color: "var(--ink-2)" }}>Ediciones</a>
        <a href="#" style={{ textDecoration: "none", color: "var(--ink-2)" }}>Propuestas</a>
        <a href="#" style={{ textDecoration: "none", color: "var(--ink-2)" }}>Actores</a>
        <a href="#" style={{ textDecoration: "none", color: "var(--ink-2)" }}>Recursos</a>
        <a href="#" style={{ textDecoration: "none", color: "var(--ink-2)", fontStyle: "italic" }}>Suscribir</a>
      </div>

      {/* HERO — minimal */}
      <section style={{ padding: "56px 72px 42px" }}>
        <div style={{ display: "grid", gridTemplateColumns: "minmax(0, 780px) 280px", gap: 60 }}>
          <div>
            <div className="eyebrow" style={{ marginBottom: 14 }}>{d.edition.label}</div>
            <h1 style={{ fontSize: 72, lineHeight: 1, letterSpacing: -0.025, fontWeight: 400, fontFamily: "var(--ff-serif)" }}>
              <span style={{ fontStyle: "italic" }}>Ibiza</span> Housing Radar
            </h1>
            <p style={{ marginTop: 24, fontSize: 22, lineHeight: 1.4, color: "var(--ink-2)", fontFamily: "var(--ff-serif)", maxWidth: 620, textWrap: "balance" }}>
              Observatorio semanal de vivienda en Ibiza. Mapeamos lo que se propone,
              <em style={{ color: "var(--ink)" }}> no proponemos nosotros</em>.
            </p>
            <div className="row" style={{ marginTop: 28, gap: 24, fontFamily: "var(--ff-sans)", fontSize: 13.5 }}>
              <a href="#" style={{ color: "var(--ink)", textDecorationThickness: 1 }}>¿Primera vez? Cómo usarlo →</a>
              <a href="#" style={{ color: "var(--ink)", textDecorationThickness: 1, fontWeight: 500 }}>Última edición →</a>
            </div>
          </div>
          <aside style={{ paddingTop: 38 }}>
            <Sidenote n={1}>
              Esta es la edición <b>nº {d.edition.number}</b>. Publicamos cada lunes a las 09:00
              CET desde febrero de 2026. El archivo completo es descargable en
              TSV y Markdown.
            </Sidenote>
            <div style={{ height: 20 }} />
            <Sidenote n={2}>
              No recibimos financiación pública ni privada. El coste operacional
              mensual aparece al pie, en euros exactos.
            </Sidenote>
          </aside>
        </div>
      </section>

      <hr className="rule" style={{ margin: "0 72px" }} />

      {/* WEEK SUMMARY — narrative */}
      <section style={{ padding: "32px 72px 28px" }}>
        <div style={{ display: "grid", gridTemplateColumns: "minmax(0, 780px) 280px", gap: 60 }}>
          <div>
            <div className="kicker" style={{ marginBottom: 10, fontFamily: "var(--ff-sans)" }}>Resumen de la semana</div>
            <p style={{ fontSize: 19, lineHeight: 1.5, color: "var(--ink)", fontFamily: "var(--ff-serif)", textWrap: "pretty" }}>
              El Govern balear <b>retrasa seis meses</b> la aprobación del decreto de tope al alquiler
              turístico en zonas tensionadas y cita «ajustes técnicos». La patronal PIMEEF
              <em> reabre el debate</em> del suelo rústico para módulos temporales, una propuesta ya
              formulada en 2023. El sindicato USO cifra en <b>1.400 temporeros</b> los firmantes de
              contrato sin alojamiento confirmado. El TSJIB anula la moratoria municipal de
              Sant Josep por defectos de motivación.
            </p>
            <div className="row" style={{ marginTop: 20, gap: 36, fontFamily: "var(--ff-sans)" }}>
              {[
                { k: "señales", v: d.edition.signals },
                { k: "propuestas activas", v: d.edition.proposals },
                { k: "omisiones", v: d.edition.omisiones },
              ].map((it) => (
                <div key={it.k}>
                  <div style={{ fontSize: 36, fontWeight: 400, fontFamily: "var(--ff-serif)", lineHeight: 1 }} className="tnum">{it.v}</div>
                  <div className="small muted" style={{ marginTop: 6 }}>{it.k}</div>
                </div>
              ))}
            </div>
          </div>
          <aside style={{ paddingTop: 26 }}>
            <Sidenote n={3}>
              <em>Omisión</em>: lo que los actores podrían abordar y sistemáticamente no abordan.
              No es opinión editorial; se detecta cuando un asunto citado en el archivo
              reciente desaparece sin cierre.
            </Sidenote>
          </aside>
        </div>
      </section>

      <hr className="rule" style={{ margin: "0 72px" }} />

      {/* SIGNALS */}
      <section style={{ padding: "32px 72px" }}>
        <div style={{ display: "grid", gridTemplateColumns: "minmax(0, 780px) 280px", gap: 60 }}>
          <div>
            <div className="kicker" style={{ marginBottom: 12, fontFamily: "var(--ff-sans)" }}>I · Señales</div>
            <SignalList items={d.signals} limit={6} />
          </div>
          <aside style={{ paddingTop: 26 }}>
            <Sidenote n={4}>
              Una <em>señal</em> es una declaración pública con fuente verificable (URL).
              No incluimos rumores ni filtraciones off-the-record.
            </Sidenote>
            <div style={{ height: 20 }} />
            <Sidenote n={5}>
              Partidos políticos aparecen siempre en <b>gris neutro</b>, sin su color de marca.
              Regla editorial dura · nº 3.
            </Sidenote>
          </aside>
        </div>
      </section>

      <hr className="rule" style={{ margin: "0 72px" }} />

      {/* POSITIONS */}
      <section style={{ padding: "32px 72px" }}>
        <div style={{ display: "grid", gridTemplateColumns: "minmax(0, 780px) 280px", gap: 60 }}>
          <div>
            <div className="kicker" style={{ marginBottom: 12, fontFamily: "var(--ff-sans)" }}>II · Mapa de posiciones</div>
            <PositionsTable />
            <div className="mono small muted" style={{ marginTop: 10 }}>
              ● apoya · ○ rechaza · ◐ ambiguo · · sin pronunciamiento público.
            </div>
          </div>
          <aside style={{ paddingTop: 26 }}>
            <Sidenote n={6}>
              Las posiciones se extraen solo de declaraciones <em>públicas</em>
              (notas de prensa, intervenciones en pleno, redes oficiales).
            </Sidenote>
          </aside>
        </div>
      </section>

      <hr className="rule" style={{ margin: "0 72px" }} />

      {/* PROPOSALS */}
      <section style={{ padding: "32px 72px" }}>
        <div className="kicker" style={{ marginBottom: 16, fontFamily: "var(--ff-sans)" }}>III · Propuestas activas</div>
        <div className="grid-4">
          {d.proposals.slice(0, 4).map((p, i) => <ProposalCard key={i} p={p} />)}
        </div>
      </section>

      <hr className="rule" style={{ margin: "0 72px" }} />

      {/* RESCATE · OMISIONES · VIGILAR */}
      <section style={{ padding: "32px 72px" }}>
        <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr 1fr", gap: 40 }}>
          {[
            { h: "IV · Rescate", list: d.rescate.map((r) => ({ a: r.year, b: r.text })) },
            { h: "V · Omisiones", list: d.omisiones.map((o) => ({ a: "—", b: o })) },
            { h: "VI · A vigilar", list: d.vigilar.map((v) => ({ a: v.when, b: v.text })) },
          ].map((col, idx) => (
            <div key={idx}>
              <div className="kicker" style={{ marginBottom: 10, fontFamily: "var(--ff-sans)" }}>{col.h}</div>
              <ul className="signals" style={{ fontSize: 14.5 }}>
                {col.list.map((it, i) => (
                  <li key={i} style={{ gridTemplateColumns: "auto 1fr" }}>
                    <span className="n mono">{it.a}</span>
                    <span>{it.b}</span>
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </div>
      </section>

      <hr className="rule" style={{ margin: "0 72px" }} />

      {/* ARCHIVE */}
      <section style={{ padding: "28px 72px 36px" }}>
        <div className="kicker" style={{ marginBottom: 12, fontFamily: "var(--ff-sans)" }}>Archivo · últimas ediciones</div>
        <ul style={{ listStyle: "none", padding: 0, margin: 0 }}>
          {d.archive.map((a, i) => (
            <li key={i} style={{ display: "grid", gridTemplateColumns: "80px 1fr auto", gap: 24, padding: "14px 0", borderTop: "0.5px solid var(--rule-soft)", alignItems: "baseline" }}>
              <span className="mono small muted">Nº {a.n}</span>
              <span>
                <div style={{ fontSize: 16, fontFamily: "var(--ff-serif)", lineHeight: 1.35 }}>{a.headline}</div>
                <div className="mono small muted" style={{ marginTop: 2 }}>{a.label}</div>
              </span>
              <span className="mono small muted">{a.signals} señales · {a.proposals} propuestas</span>
            </li>
          ))}
        </ul>
      </section>

      <TranspFooter pad="0 72px" />
    </div>
  );
};

window.VariantD = VariantD;
