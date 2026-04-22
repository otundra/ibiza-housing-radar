// Internal pages of Ibiza Housing Radar.
// Each page reads window.PAGE_ID to decide what to render.
// Keeps all internal pages in a single JSX file for brevity.

const D = window.RADAR_DATA;

// ---------- shared small atoms ----------
const Box = ({ children, style }) => (
  <div style={{ border: "1px solid var(--ink)", background: "var(--paper)", ...style }}>{children}</div>
);
const Label = ({ children, style }) => (
  <div style={{ fontFamily: "var(--ff-mono)", fontSize: 10.5, textTransform: "uppercase", letterSpacing: 0.12, color: "var(--ink-3)", ...style }}>{children}</div>
);
const Mono = ({ children, style, as = "span" }) => {
  const C = as;
  return <C style={{ fontFamily: "var(--ff-mono)", ...style }}>{children}</C>;
};
const H2 = ({ n, children }) => (
  <h2 style={{ fontFamily: "var(--ff-mono)", fontSize: 22, fontWeight: 600, letterSpacing: -0.01, margin: "0 0 14px", display: "flex", alignItems: "baseline", gap: 12 }}>
    <span style={{ color: "var(--ink-3)", fontSize: 13 }}># {String(n).padStart(2, "0")}</span>
    <span>{children}</span>
  </h2>
);
const Section = ({ children, style }) => (
  <section style={{ padding: "28px 36px", borderBottom: "1px solid var(--ink)", ...style }}>{children}</section>
);

// =====================================================================
// SIGNALS — 3 estrategias para que no quede hueco según nº de señales
// =====================================================================
const SignalsVariants = ({ signals }) => {
  const [v, setV] = React.useState("A");
  React.useEffect(() => {
    try { const s = localStorage.getItem("radar-signals-fill"); if (s) setV(s); } catch(e){}
  }, []);
  React.useEffect(() => {
    try { localStorage.setItem("radar-signals-fill", v); } catch(e){}
  }, [v]);

  const Switcher = () => (
    <div style={{ display: "flex", gap: 0, fontFamily: "var(--ff-mono)", fontSize: 11 }}>
      <Mono style={{ color: "var(--ink-3)", marginRight: 10, paddingTop: 4 }}>relleno:</Mono>
      {[
        ["A", "masonry + sistema"],
        ["B", "auto-densidad"],
        ["C", "titular + grid"],
      ].map(([k, label]) => (
        <button key={k} onClick={() => setV(k)}
          style={{
            border: "1px solid var(--ink)",
            borderLeft: k === "A" ? "1px solid var(--ink)" : "none",
            background: v === k ? "var(--ink)" : "transparent",
            color: v === k ? "var(--paper)" : "var(--ink)",
            fontFamily: "inherit", fontSize: 11, padding: "3px 10px",
            cursor: "pointer",
          }}>{k} · {label}</button>
      ))}
    </div>
  );

  return (
    <Section>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 16, flexWrap: "wrap", gap: 12 }}>
        <H2 n={1}>Señales de la semana</H2>
        <Switcher />
      </div>

      {v === "A" && <SignalsFillA signals={signals} />}
      {v === "B" && <SignalsFillB signals={signals} />}
      {v === "C" && <SignalsFillC signals={signals} />}
    </Section>
  );
};

// A — fichas B + tarjetas "de sistema" que rellenan cualquier hueco.
// Tarjetas: "+ sugerir señal", "→ archivo semana pasada", counter "+N señales no incluidas".
const SignalsFillA = ({ signals }) => {
  const items = [
    ...signals.map((s, i) => ({ kind: "signal", data: s, n: i })),
    { kind: "sys", title: "+ SUGERIR SEÑAL", body: "¿Se nos escapa algo? Envíanos fuente + URL.", cta: "radar.eiv/sugerir" },
    { kind: "sys", title: "→ ARCHIVO SEMANA 15", body: "19 señales la semana pasada. Revisa qué sigue vivo.", cta: "ediciones.html" },
    { kind: "stat", value: "41", unit: "señales descartadas", body: "No pasaron las 3 fuentes. Criterio en /politica-editorial/." },
  ];
  return (
    <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fill, minmax(260px, 1fr))", gap: 0, border: "1px solid var(--ink)" }}>
      {items.map((it, i) => {
        const base = { padding: "14px 16px 18px", borderRight: "1px solid var(--rule-soft)", borderBottom: "1px solid var(--rule-soft)" };
        if (it.kind === "signal") {
          const s = it.data;
          return (
            <article key={i} style={{ ...base, background: "var(--paper)" }}>
              <div style={{ display: "flex", justifyContent: "space-between", alignItems: "baseline", marginBottom: 8 }}>
                <Mono style={{ fontSize: 11, color: "var(--ink-3)" }}>#{String(it.n+1).padStart(2, "0")}</Mono>
                <Mono style={{ fontSize: 10.5, color: "var(--ink-3)", textTransform: "uppercase", letterSpacing: 0.08 }}>{s.type}</Mono>
              </div>
              <div style={{ fontFamily: "var(--ff-mono)", fontSize: 15, fontWeight: 600, marginBottom: 8 }}>{s.actor}</div>
              <div style={{ fontSize: 13.5, lineHeight: 1.5 }}>{s.text}</div>
              <div style={{ fontFamily: "var(--ff-mono)", fontSize: 10.5, color: "var(--ink-3)", marginTop: 10, overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap" }}>↗ {s.url}</div>
            </article>
          );
        }
        if (it.kind === "sys") {
          return (
            <article key={i} style={{ ...base, background: "var(--paper-2)", display: "flex", flexDirection: "column", justifyContent: "space-between" }}>
              <div>
                <Mono style={{ fontSize: 12, fontWeight: 600, color: "var(--ink)", display: "block", marginBottom: 10, letterSpacing: 0.05 }}>{it.title}</Mono>
                <div style={{ fontSize: 13, lineHeight: 1.5, color: "var(--ink-2)" }}>{it.body}</div>
              </div>
              <Mono style={{ fontSize: 10.5, color: "var(--ink-3)", marginTop: 14 }}>↗ {it.cta}</Mono>
            </article>
          );
        }
        // stat
        return (
          <article key={i} style={{ ...base, background: "var(--ink)", color: "var(--paper)", display: "flex", flexDirection: "column", justifyContent: "space-between" }}>
            <div>
              <Mono className="tnum" style={{ fontSize: 56, fontWeight: 600, lineHeight: 1, display: "block" }}>{it.value}</Mono>
              <Mono style={{ fontSize: 11, opacity: .7, textTransform: "uppercase", letterSpacing: 0.1 }}>{it.unit}</Mono>
            </div>
            <div style={{ fontSize: 12, lineHeight: 1.5, opacity: .8, marginTop: 14 }}>{it.body}</div>
          </article>
        );
      })}
    </div>
  );
};

// B — grid auto-densidad: el ancho de columna varía según nº señales
// Pocas (≤6) → columnas anchas (360px), tipografía mayor
// Medio (7–12) → 280px
// Muchas (13+) → 220px, compacto
const SignalsFillB = ({ signals }) => {
  const n = signals.length;
  const min = n <= 6 ? 360 : n <= 12 ? 280 : 220;
  const fs  = n <= 6 ? 15   : n <= 12 ? 13.5 : 12.5;
  const pad = n <= 6 ? "18px 20px 22px" : "14px 16px 18px";
  return (
    <div>
      <div style={{ fontFamily: "var(--ff-mono)", fontSize: 11, color: "var(--ink-3)", marginBottom: 8 }}>
        {n} señales · densidad {n <= 6 ? "amplia" : n <= 12 ? "media" : "compacta"}
      </div>
      <div style={{ display: "grid", gridTemplateColumns: `repeat(auto-fill, minmax(${min}px, 1fr))`, gap: 0, border: "1px solid var(--ink)" }}>
        {signals.map((s, i) => (
          <article key={i} style={{
            padding: pad, borderRight: "1px solid var(--rule-soft)",
            borderBottom: "1px solid var(--rule-soft)", background: "var(--paper)",
          }}>
            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "baseline", marginBottom: 8 }}>
              <Mono style={{ fontSize: 11, color: "var(--ink-3)" }}>#{String(i+1).padStart(2, "0")}</Mono>
              <Mono style={{ fontSize: 10.5, color: "var(--ink-3)", textTransform: "uppercase", letterSpacing: 0.08 }}>{s.type}</Mono>
            </div>
            <div style={{ fontFamily: "var(--ff-mono)", fontSize: fs + 1, fontWeight: 600, marginBottom: 8 }}>{s.actor}</div>
            <div style={{ fontSize: fs, lineHeight: 1.5 }}>{s.text}</div>
            <div style={{ fontFamily: "var(--ff-mono)", fontSize: 10.5, color: "var(--ink-3)", marginTop: 10, overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap" }}>↗ {s.url}</div>
          </article>
        ))}
      </div>
    </div>
  );
};

// C — titular + grid: primera señal a ancho completo como pieza destacada,
// resto en grid. Absorbe huecos cuando hay pocas.
const SignalsFillC = ({ signals }) => {
  const [head, ...rest] = signals;
  return (
    <div>
      {/* Titular */}
      <article style={{ padding: "24px 28px", background: "var(--ink)", color: "var(--paper)", border: "1px solid var(--ink)", display: "grid", gridTemplateColumns: "auto 1fr auto", gap: 28, alignItems: "center" }}>
        <Mono style={{ fontSize: 46, fontWeight: 600, lineHeight: 1, opacity: .6 }}>#01</Mono>
        <div>
          <Mono style={{ fontSize: 11, letterSpacing: 0.1, textTransform: "uppercase", opacity: .7 }}>SEÑAL DESTACADA · {head.actor}</Mono>
          <p style={{ margin: "6px 0 0", fontFamily: "var(--ff-mono)", fontSize: 22, fontWeight: 500, lineHeight: 1.3, letterSpacing: -0.005, textWrap: "pretty" }}>{head.text}</p>
        </div>
        <div style={{ textAlign: "right", fontFamily: "var(--ff-mono)", fontSize: 11, opacity: .7, maxWidth: 180 }}>↗ {head.url}</div>
      </article>
      {/* Resto en grid B estándar */}
      <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fill, minmax(260px, 1fr))", gap: 0, border: "1px solid var(--ink)", borderTop: "none" }}>
        {rest.map((s, i) => (
          <article key={i} style={{
            padding: "14px 16px 18px", borderRight: "1px solid var(--rule-soft)",
            borderBottom: "1px solid var(--rule-soft)", background: "var(--paper)",
          }}>
            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "baseline", marginBottom: 8 }}>
              <Mono style={{ fontSize: 11, color: "var(--ink-3)" }}>#{String(i+2).padStart(2, "0")}</Mono>
              <Mono style={{ fontSize: 10.5, color: "var(--ink-3)", textTransform: "uppercase", letterSpacing: 0.08 }}>{s.type}</Mono>
            </div>
            <div style={{ fontFamily: "var(--ff-mono)", fontSize: 15, fontWeight: 600, marginBottom: 8 }}>{s.actor}</div>
            <div style={{ fontSize: 13.5, lineHeight: 1.5 }}>{s.text}</div>
            <div style={{ fontFamily: "var(--ff-mono)", fontSize: 10.5, color: "var(--ink-3)", marginTop: 10, overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap" }}>↗ {s.url}</div>
          </article>
        ))}
      </div>
    </div>
  );
};

// A — TABLA DENSA 3 COLUMNAS
// Aprovecha ancho distribuyendo señales en columnas de texto tipo periódico.
// Mantiene el # numerado a la izquierda, una sola línea por señal cuando es breve.
const SignalsA = ({ signals }) => (
  <ol style={{ listStyle: "none", padding: 0, margin: 0, columns: 3, columnGap: 36, columnRule: "1px solid var(--rule-soft)" }}>
    {signals.map((s, i) => (
      <li key={i} style={{ breakInside: "avoid", padding: "12px 0", borderTop: i < 3 ? "2px solid var(--ink)" : "1px solid var(--rule-soft)", display: "grid", gridTemplateColumns: "38px 1fr", gap: 10, alignItems: "baseline" }}>
        <Mono style={{ fontSize: 14, fontWeight: 600, color: "var(--ink)" }}>{String(i+1).padStart(2, "0")}</Mono>
        <div>
          <div style={{ fontSize: 14, lineHeight: 1.5 }}>{s.text}</div>
          <div style={{ display: "flex", justifyContent: "space-between", marginTop: 6, fontFamily: "var(--ff-mono)", fontSize: 10.5, color: "var(--ink-3)" }}>
            <span>→ {s.actor}</span>
            <span>{s.url}</span>
          </div>
        </div>
      </li>
    ))}
  </ol>
);

// B — FICHAS EN GRID 4·col (autofit)
// Cada señal es una fichita tipo archivero — actor como headline, texto debajo.
// Funciona como sala de fichas: escaneas rápido por actor.
const SignalsB = ({ signals }) => (
  <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fill, minmax(260px, 1fr))", gap: 0, border: "1px solid var(--ink)" }}>
    {signals.map((s, i) => (
      <article key={i} style={{
        padding: "14px 16px 18px",
        borderRight: "1px solid var(--rule-soft)",
        borderBottom: "1px solid var(--rule-soft)",
        background: "var(--paper)",
      }}>
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "baseline", marginBottom: 8 }}>
          <Mono style={{ fontSize: 11, color: "var(--ink-3)" }}>#{String(i+1).padStart(2, "0")}</Mono>
          <Mono style={{ fontSize: 10.5, color: "var(--ink-3)", textTransform: "uppercase", letterSpacing: 0.08 }}>{s.type}</Mono>
        </div>
        <div style={{ fontFamily: "var(--ff-mono)", fontSize: 15, fontWeight: 600, marginBottom: 8, letterSpacing: -0.005 }}>{s.actor}</div>
        <div style={{ fontSize: 13.5, lineHeight: 1.5 }}>{s.text}</div>
        <div style={{ fontFamily: "var(--ff-mono)", fontSize: 10.5, color: "var(--ink-3)", marginTop: 10, overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap" }}>↗ {s.url}</div>
      </article>
    ))}
  </div>
);

// C — MARGINALIA (ancho completo, measure cómoda)
// Columna central de lectura ~65ch + índice sticky a la izquierda + metadatos a la derecha.
// Aprovecha el ancho sin estirar líneas; los números # actúan como navegación.
const SignalsC = ({ signals }) => (
  <div style={{ display: "grid", gridTemplateColumns: "140px minmax(0, 65ch) 1fr", gap: 40 }}>
    <aside style={{ position: "sticky", top: 0, alignSelf: "start", fontFamily: "var(--ff-mono)", fontSize: 11 }}>
      <Label style={{ marginBottom: 10 }}>Índice</Label>
      {signals.map((s, i) => (
        <a key={i} href={`#sig-${i}`} style={{
          display: "block", padding: "3px 0",
          textDecoration: "none", color: "var(--ink-2)",
          borderBottom: "1px solid var(--rule-soft)",
          fontSize: 11,
        }}>
          <span style={{ color: "var(--ink-3)", marginRight: 8 }}>{String(i+1).padStart(2, "0")}</span>
          {s.actor}
        </a>
      ))}
    </aside>
    <ol style={{ listStyle: "none", padding: 0, margin: 0 }}>
      {signals.map((s, i) => (
        <li id={`sig-${i}`} key={i} style={{ padding: "18px 0", borderTop: i === 0 ? "2px solid var(--ink)" : "1px solid var(--rule-soft)", scrollMarginTop: 20 }}>
          <div style={{ display: "flex", alignItems: "baseline", gap: 12 }}>
            <Mono style={{ fontSize: 24, fontWeight: 600, color: "var(--ink-3)", lineHeight: 1 }}>{String(i+1).padStart(2, "0")}</Mono>
            <p style={{ margin: 0, fontSize: 16, lineHeight: 1.55, textWrap: "pretty" }}>{s.text}</p>
          </div>
        </li>
      ))}
    </ol>
    <aside style={{ fontFamily: "var(--ff-mono)", fontSize: 11 }}>
      <Label style={{ marginBottom: 10 }}>Fuentes</Label>
      {signals.map((s, i) => (
        <div key={i} style={{ padding: "18px 0", borderTop: i === 0 ? "2px solid var(--ink)" : "1px solid var(--rule-soft)" }}>
          <div style={{ color: "var(--ink)", fontWeight: 600 }}>{s.actor}</div>
          <div style={{ color: "var(--ink-3)", marginTop: 3, wordBreak: "break-all" }}>↗ {s.url}</div>
        </div>
      ))}
    </aside>
  </div>
);

// =====================================================================
// PROPUESTAS — 3 propuestas de layout
// =====================================================================
const barColor = (v) => v >= 65 ? "var(--alert-green)" : v >= 45 ? "var(--alert-yellow)" : "var(--alert-red)";

const ProposalsVariants = ({ proposals }) => (
  <Section>
    <H2 n={2}>Propuestas activas</H2>
    <div style={{ marginTop: 4 }}>
      <ProposalsC proposals={proposals} />
    </div>
  </Section>
);

// A — MATRIZ DE VIABILIDAD (scatter jurídica × económica)
// Aprovecha el ancho con un solo diagrama. Cuadrantes etiquetados.
// Cada propuesta es un punto + etiqueta breve.
const ProposalsA = ({ proposals }) => {
  const H = 520, padX = 60, padY = 40;
  return (
    <div>
      <div style={{ display: "flex", justifyContent: "space-between", fontFamily: "var(--ff-mono)", fontSize: 11, color: "var(--ink-3)", marginBottom: 8 }}>
        <span>eje Y ↑ viabilidad jurídica</span>
        <span>eje X → viabilidad económica</span>
      </div>
      <div style={{ position: "relative", border: "1px solid var(--ink)", height: H, background: "var(--paper-2)" }}>
        {/* quadrants */}
        <div style={{ position: "absolute", inset: 0, borderRight: "1px dashed var(--ink-4)", width: "50%" }} />
        <div style={{ position: "absolute", inset: 0, borderBottom: "1px dashed var(--ink-4)", height: "50%" }} />
        {/* axis labels */}
        <span style={{ position: "absolute", top: 8, left: 12, fontFamily: "var(--ff-mono)", fontSize: 10.5, color: "var(--ink-3)" }}>BLOQUEO JURÍDICO / BARATO</span>
        <span style={{ position: "absolute", top: 8, right: 12, fontFamily: "var(--ff-mono)", fontSize: 10.5, color: "var(--ink-3)" }}>VIABLE / CARO</span>
        <span style={{ position: "absolute", bottom: 8, left: 12, fontFamily: "var(--ff-mono)", fontSize: 10.5, color: "var(--ink-3)" }}>INVIABLE</span>
        <span style={{ position: "absolute", bottom: 8, right: 12, fontFamily: "var(--ff-mono)", fontSize: 10.5, color: "var(--ink-3)" }}>VIABLE / RENTABLE ★</span>
        {/* points */}
        {proposals.map((p, i) => {
          const x = padX + (p.econ.v / 100) * (100 - 2 * (padX / H) * 100) * H / 100;
          // simpler: percent-based
          const left = `calc(${p.econ.v}% - 4px)`;
          const bottom = `calc(${p.legal.v}% - 4px)`;
          return (
            <a key={i} href="propuesta.html" style={{
              position: "absolute", left, bottom,
              textDecoration: "none", color: "var(--ink)",
              display: "flex", alignItems: "center", gap: 6,
            }}>
              <span style={{ width: 10, height: 10, background: "var(--ink)", border: "2px solid var(--paper)", borderRadius: "50%", boxShadow: "0 0 0 1px var(--ink)" }} />
              <span style={{
                fontFamily: "var(--ff-mono)", fontSize: 11,
                background: "var(--paper)", border: "1px solid var(--ink)",
                padding: "2px 6px", whiteSpace: "nowrap", maxWidth: 240,
                overflow: "hidden", textOverflow: "ellipsis",
              }}>
                <span style={{ color: "var(--ink-3)" }}>#{String(i+1).padStart(2, "0")}</span> {p.title.length > 40 ? p.title.slice(0, 38) + "…" : p.title}
              </span>
            </a>
          );
        })}
      </div>
      {/* legend */}
      <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(300px, 1fr))", gap: 8, marginTop: 16, fontFamily: "var(--ff-mono)", fontSize: 11.5 }}>
        {proposals.map((p, i) => (
          <a key={i} href="propuesta.html" style={{ textDecoration: "none", color: "var(--ink)", display: "grid", gridTemplateColumns: "30px 1fr auto auto", gap: 8, alignItems: "baseline", padding: "4px 0", borderTop: "1px solid var(--rule-soft)" }}>
            <span style={{ color: "var(--ink-3)" }}>{String(i+1).padStart(2, "0")}</span>
            <span style={{ overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap" }}>{p.title}</span>
            <span style={{ color: "var(--ink-3)" }}>jur {p.legal.v}</span>
            <span style={{ color: "var(--ink-3)" }}>eco {p.econ.v}</span>
          </a>
        ))}
      </div>
    </div>
  );
};

// B — TABLA COMPARATIVA DENSA
// Columna por atributo. Barras inline en viabilidad. Escaneable a una sola mirada.
const ProposalsB = ({ proposals }) => {
  const cols = "40px 2.4fr 0.9fr 0.9fr 0.6fr 1.1fr 1.1fr";
  const Hd = ({ children, align }) => (
    <div style={{ fontFamily: "var(--ff-mono)", fontSize: 10.5, textTransform: "uppercase", letterSpacing: 0.1, color: "var(--ink-3)", padding: "10px 8px", textAlign: align || "left" }}>{children}</div>
  );
  const Cell = ({ children, style }) => (
    <div style={{ padding: "14px 8px", borderTop: "1px solid var(--rule-soft)", fontSize: 13.5, ...style }}>{children}</div>
  );
  const Bar = ({ v }) => (
    <div style={{ display: "flex", alignItems: "center", gap: 8 }}>
      <div style={{ flex: 1, height: 5, background: "var(--rule-soft)", minWidth: 40 }}>
        <div style={{ height: "100%", width: `${v}%`, background: barColor(v) }} />
      </div>
      <Mono className="tnum" style={{ fontSize: 11, color: "var(--ink-3)", width: 22, textAlign: "right" }}>{v}</Mono>
    </div>
  );
  return (
    <div style={{ border: "1px solid var(--ink)" }}>
      <div style={{ display: "grid", gridTemplateColumns: cols, background: "var(--ink)", color: "var(--paper)" }}>
        <Hd>#</Hd><Hd>Propuesta</Hd><Hd>Actor</Hd><Hd>Estado</Hd><Hd>Horiz.</Hd><Hd>Viab. jur.</Hd><Hd>Viab. eco.</Hd>
      </div>
      {proposals.map((p, i) => (
        <a key={i} href="propuesta.html" style={{ textDecoration: "none", color: "var(--ink)", display: "grid", gridTemplateColumns: cols, alignItems: "center", background: i % 2 ? "var(--paper-2)" : "var(--paper)" }}>
          <Cell><Mono style={{ color: "var(--ink-3)" }}>{String(i+1).padStart(2, "0")}</Mono></Cell>
          <Cell style={{ fontWeight: 500, lineHeight: 1.35 }}>{p.title}</Cell>
          <Cell><Mono style={{ fontSize: 12 }}>{p.actor}</Mono><div style={{ fontSize: 10.5, color: "var(--ink-3)", textTransform: "uppercase", letterSpacing: 0.08 }}>{p.typeLabel}</div></Cell>
          <Cell><span style={{ fontFamily: "var(--ff-mono)", fontSize: 10.5, letterSpacing: 0.1, border: "1px solid var(--ink)", padding: "2px 7px", textTransform: "uppercase", display: "inline-block" }}>{p.stateLabel}</span></Cell>
          <Cell><Mono style={{ fontSize: 11.5, color: "var(--ink-2)" }}>{p.horizon}</Mono></Cell>
          <Cell><Bar v={p.legal.v} /></Cell>
          <Cell><Bar v={p.econ.v} /></Cell>
        </a>
      ))}
    </div>
  );
};

// C — LISTA EDITORIAL ANCHA (tipo sumario de periódico)
// Una propuesta por fila a ancho completo. Jerarquía tipográfica, barras inline.
const ProposalsC = ({ proposals }) => (
  <ol style={{ listStyle: "none", padding: 0, margin: 0 }}>
    {proposals.map((p, i) => (
      <li key={i} style={{ padding: "22px 0", borderTop: i === 0 ? "2px solid var(--ink)" : "1px solid var(--rule-soft)" }}>
        <a href="propuesta.html" style={{ textDecoration: "none", color: "var(--ink)", display: "grid", gridTemplateColumns: "70px minmax(0, 2fr) 1fr 1fr", gap: 28, alignItems: "start" }}>
          <Mono style={{ fontSize: 34, fontWeight: 600, color: "var(--ink-3)", lineHeight: 1 }}>{String(i+1).padStart(2, "0")}</Mono>
          <div>
            <div style={{ display: "flex", gap: 10, fontFamily: "var(--ff-mono)", fontSize: 10.5, textTransform: "uppercase", letterSpacing: 0.1, color: "var(--ink-3)", marginBottom: 6 }}>
              <span>{p.actor}</span><span>·</span><span>{p.typeLabel}</span><span>·</span><span>{p.horizon}</span>
            </div>
            <h3 style={{ margin: 0, fontFamily: "var(--ff-mono)", fontSize: 22, fontWeight: 600, lineHeight: 1.2, letterSpacing: -0.01 }}>{p.title}</h3>
            <div style={{ marginTop: 8, fontFamily: "var(--ff-mono)", fontSize: 11, color: "var(--ink-3)" }}>↗ {p.src}</div>
          </div>
          <div style={{ display: "grid", gap: 10 }}>
            {[["jurídica", p.legal.v], ["económica", p.econ.v]].map(([lbl, v]) => (
              <div key={lbl}>
                <div style={{ display: "flex", justifyContent: "space-between", fontFamily: "var(--ff-mono)", fontSize: 10.5, color: "var(--ink-3)", textTransform: "uppercase", letterSpacing: 0.08 }}>
                  <span>viab. {lbl}</span><Mono className="tnum">{v}/100</Mono>
                </div>
                <div style={{ height: 5, background: "var(--rule-soft)", marginTop: 3 }}>
                  <div style={{ height: "100%", width: `${v}%`, background: barColor(v) }} />
                </div>
              </div>
            ))}
          </div>
          <div style={{ textAlign: "right" }}>
            <span style={{ fontFamily: "var(--ff-mono)", fontSize: 11, letterSpacing: 0.1, border: "1px solid var(--ink)", padding: "3px 10px", textTransform: "uppercase", display: "inline-block" }}>{p.stateLabel}</span>
          </div>
        </a>
      </li>
    ))}
  </ol>
);

// =====================================================================
// 1) EDICIONES — archive
// =====================================================================
const Ediciones = () => {
  const all = [
    { n: 17, label: "Semana 16 · 13–19 abr 2026", headline: "Del retraso del decreto al convenio de temporeros: el tablero se divide.", signals: 23, proposals: 11, current: true },
    ...D.archive,
    { n: 12, label: "Semana 11 · 09–15 mar", headline: "Plan insular de 400 viviendas: del anuncio a la letra pequeña.", signals: 18, proposals: 9 },
    { n: 11, label: "Semana 10 · 02–08 mar", headline: "Primer choque patronal‑sindicato por módulos temporales.", signals: 15, proposals: 7 },
    { n: 10, label: "Semana 09 · 23 feb–01 mar", headline: "UIB publica el mapa de vivienda vacía. Nadie lo cita aún.", signals: 22, proposals: 8 },
    { n: 9, label: "Semana 08 · 16–22 feb", headline: "Vox abre debate sobre compradores no residentes.", signals: 14, proposals: 6 },
  ];
  return (
    <PageShell active="ediciones" path="/ediciones/"
      title="Archivo de ediciones"
      subtitle="// Todas las ediciones publicadas. Una por semana. Ninguna se edita después de publicarse; los errores van en /balance/.">
      <Section>
        <div style={{ display: "grid", gridTemplateColumns: "auto 1fr auto auto auto", gap: 16, alignItems: "center", fontFamily: "var(--ff-mono)", fontSize: 14 }}>
          <div style={{ display: "contents", color: "var(--ink-3)" }}>
            <Label>Edición</Label><Label>Titular</Label><Label>Señales</Label><Label>Propuestas</Label><Label>Estado</Label>
          </div>
          {all.map((e) => (
            <React.Fragment key={e.n}>
              <a href={e.current ? "edicion.html" : "#"} style={{ color: "var(--ink)", textDecoration: "none", borderTop: "1px solid var(--ink-4)", padding: "14px 0", fontWeight: 600 }}>
                #{String(e.n).padStart(3, "0")}
              </a>
              <a href={e.current ? "edicion.html" : "#"} style={{ color: "var(--ink)", textDecoration: "none", borderTop: "1px solid var(--ink-4)", padding: "14px 0" }}>
                <div style={{ fontSize: 11, color: "var(--ink-3)", textTransform: "uppercase", letterSpacing: 0.08 }}>{e.label}</div>
                <div style={{ fontSize: 15, marginTop: 2, lineHeight: 1.35 }}>{e.headline}</div>
              </a>
              <div style={{ borderTop: "1px solid var(--ink-4)", padding: "14px 0", textAlign: "right" }} className="tnum">{e.signals}</div>
              <div style={{ borderTop: "1px solid var(--ink-4)", padding: "14px 0", textAlign: "right" }} className="tnum">{e.proposals}</div>
              <div style={{ borderTop: "1px solid var(--ink-4)", padding: "14px 0", textAlign: "right" }}>
                {e.current
                  ? <span style={{ background: "var(--ink)", color: "var(--paper)", padding: "3px 8px", fontSize: 11 }}>ACTUAL</span>
                  : <span style={{ color: "var(--ink-3)", fontSize: 11 }}>archivo</span>}
              </div>
            </React.Fragment>
          ))}
        </div>
      </Section>
      <Section>
        <Label>Política</Label>
        <p style={{ fontSize: 14, lineHeight: 1.55, color: "var(--ink-2)", marginTop: 8, maxWidth: 760 }}>
          Una edición por semana, siempre en jueves. Nunca se edita retroactivamente.
          Las correcciones se publican en la edición siguiente y se listan en <a href="balance.html">/balance/</a>.
        </p>
      </Section>
    </PageShell>
  );
};

// =====================================================================
// 2) PROPUESTA (ficha individual)
// =====================================================================
const Propuesta = () => {
  const p = D.proposals[1]; // "Tope autonómico al precio del alquiler"
  const Bar = ({ label, v, cls }) => (
    <div>
      <div style={{ display: "flex", justifyContent: "space-between", fontFamily: "var(--ff-mono)", fontSize: 11, color: "var(--ink-3)" }}>
        <span>{label}</span><span className="tnum" style={{ color: "var(--ink)" }}>{v}/100</span>
      </div>
      <div style={{ height: 6, background: "var(--rule-soft)", marginTop: 4 }}>
        <div style={{ height: "100%", width: `${v}%`, background: cls === "ok" ? "var(--alert-green)" : cls === "mid" ? "var(--alert-yellow)" : "var(--alert-red)" }} />
      </div>
    </div>
  );

  const timeline = [
    { d: "2025-11-04", t: "PSIB‑PSOE registra la iniciativa en el Parlament." },
    { d: "2026-01-22", t: "Dictamen del Consell Consultiu: viable con matices competenciales." },
    { d: "2026-02-18", t: "Debate a la totalidad. Se aprueba tramitación (54 a favor · 39 en contra · 6 abs)." },
    { d: "2026-03-12", t: "Enmiendas parciales: PP propone excluir zonas con índice < 1,4 precio/renta." },
    { d: "2026-04-17", t: "Govern retrasa seis meses el decreto técnico que lo hace aplicable." },
  ];
  const actores = [
    { who: "PSIB‑PSOE", pos: "yes",  q: "Impulsor. Condiciona su apoyo al presupuesto." },
    { who: "PP",        pos: "no",   q: "Rechaza tope pero negocia umbrales por zona." },
    { who: "Vox",       pos: "no",   q: "Anuncia recurso ante el Constitucional si se aprueba." },
    { who: "Sumar",     pos: "yes",  q: "Pide extensión a zonas costeras sin índice." },
    { who: "PIMEEF",    pos: "no",   q: "Advierte de retirada de oferta privada." },
    { who: "USO Ibiza", pos: "yes",  q: "Lo vincula a protección de temporeros." },
    { who: "Cáritas",   pos: "yes",  q: "Insuficiente sin fondo de garantía paralelo." },
  ];
  const posColor = (x) => x === "yes" ? "var(--alert-green)" : x === "no" ? "var(--alert-red)" : "var(--alert-yellow)";
  const posLabel = (x) => x === "yes" ? "A FAVOR" : x === "no" ? "EN CONTRA" : "AMBIGUO";

  return (
    <PageShell active="propuestas" path={`/propuestas/${p.src.replace(/\W+/g,"-").slice(0,40)}/`}
      title={p.title}
      subtitle={`// Ficha individual. Actor original: ${p.actor}. Estado: ${p.stateLabel.toLowerCase()}. Horizonte: ${p.horizon}. Fuente: ${p.src}`}>

      {/* Viability + state */}
      <Section>
        <div style={{ display: "grid", gridTemplateColumns: "2fr 1fr 1fr", gap: 28 }}>
          <div>
            <Label>Resumen editorial</Label>
            <p style={{ fontSize: 16, lineHeight: 1.6, marginTop: 8, maxWidth: 620 }}>
              Iniciativa autonómica para fijar precio de referencia en los municipios
              declarados zona tensionada. Depende de un decreto técnico de desarrollo que
              el Govern ha retrasado esta semana <Mono style={{ color: "var(--ink-3)" }}>(ver señal #01)</Mono>.
              Dos terceras partes del Parlament apoyan el principio; el desacuerdo es
              el perímetro y el mecanismo de revisión.
            </p>
          </div>
          <div style={{ display: "grid", gap: 14, alignContent: "start" }}>
            <Bar label="Viab. jurídica" v={p.legal.v} cls={p.legal.cls} />
            <Bar label="Viab. económica" v={p.econ.v} cls={p.econ.cls} />
            <Bar label="Apoyo parlam."  v={66} cls="mid" />
          </div>
          <div style={{ display: "grid", gap: 10, alignContent: "start" }}>
            <Box style={{ padding: 12 }}>
              <Label>Estado</Label>
              <div style={{ fontFamily: "var(--ff-mono)", fontSize: 18, marginTop: 4 }}>{p.stateLabel}</div>
            </Box>
            <Box style={{ padding: 12 }}>
              <Label>Horizonte</Label>
              <div style={{ fontFamily: "var(--ff-mono)", fontSize: 18, marginTop: 4 }}>{p.horizon}</div>
            </Box>
            <Box style={{ padding: 12 }}>
              <Label>Capa alerta</Label>
              <div style={{ fontFamily: "var(--ff-mono)", fontSize: 18, marginTop: 4, color: "var(--alert-yellow)" }}>2 / 4 · yellow</div>
            </Box>
          </div>
        </div>
      </Section>

      {/* Timeline */}
      <Section>
        <H2 n={1}>Recorrido</H2>
        <ol style={{ listStyle: "none", padding: 0, margin: 0, borderLeft: "2px solid var(--ink)" }}>
          {timeline.map((x, i) => (
            <li key={i} style={{ padding: "10px 0 10px 18px", position: "relative", fontSize: 14, lineHeight: 1.5 }}>
              <span style={{ position: "absolute", left: -6, top: 16, width: 10, height: 10, background: "var(--paper)", border: "2px solid var(--ink)", borderRadius: "50%" }} />
              <Mono style={{ color: "var(--ink-3)", fontSize: 12 }}>{x.d}</Mono>
              <div>{x.t}</div>
            </li>
          ))}
        </ol>
      </Section>

      {/* Positions */}
      <Section>
        <H2 n={2}>Posiciones registradas</H2>
        <div style={{ display: "grid", gridTemplateColumns: "repeat(2, 1fr)", gap: 12 }}>
          {actores.map((a, i) => (
            <Box key={i} style={{ padding: 14 }}>
              <div style={{ display: "flex", justifyContent: "space-between", alignItems: "baseline" }}>
                <Mono style={{ fontWeight: 600, fontSize: 14 }}>{a.who}</Mono>
                <span style={{ fontFamily: "var(--ff-mono)", fontSize: 10.5, letterSpacing: 0.1, color: posColor(a.pos), border: `1px solid ${posColor(a.pos)}`, padding: "1px 6px" }}>{posLabel(a.pos)}</span>
              </div>
              <p style={{ margin: "8px 0 0", fontSize: 13.5, lineHeight: 1.5, color: "var(--ink-2)" }}>{a.q}</p>
            </Box>
          ))}
        </div>
      </Section>

      {/* Omisiones + next */}
      <Section>
        <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 28 }}>
          <div>
            <H2 n={3}>Lo que no se está diciendo</H2>
            <ul style={{ padding: 0, margin: 0, listStyle: "none" }}>
              <li style={{ padding: "8px 0", borderBottom: "1px solid var(--rule-soft)", fontSize: 14 }}>→ No se ha publicado el índice oficial de zona tensionada 2026.</li>
              <li style={{ padding: "8px 0", borderBottom: "1px solid var(--rule-soft)", fontSize: 14 }}>→ Ningún grupo plantea qué pasa con contratos vigentes.</li>
              <li style={{ padding: "8px 0", borderBottom: "1px solid var(--rule-soft)", fontSize: 14 }}>→ Sin mención a sanciones o mecanismo de inspección.</li>
            </ul>
          </div>
          <div>
            <H2 n={4}>A vigilar</H2>
            <ul style={{ padding: 0, margin: 0, listStyle: "none" }}>
              <li style={{ padding: "8px 0", borderBottom: "1px solid var(--rule-soft)", fontSize: 14 }}><Mono style={{ color: "var(--ink-3)" }}>22 abr</Mono> — Pleno del Parlament: debate umbrales.</li>
              <li style={{ padding: "8px 0", borderBottom: "1px solid var(--rule-soft)", fontSize: 14 }}><Mono style={{ color: "var(--ink-3)" }}>may</Mono> — Publicación del decreto técnico (BOE).</li>
            </ul>
          </div>
        </div>
      </Section>
    </PageShell>
  );
};

// =====================================================================
// 3) ACTOR (ficha individual)
// =====================================================================
const Actor = () => {
  const name = "PIMEEF";
  const role = "Patronal · Pequeña y Mediana Empresa de Eivissa y Formentera";
  const stats = [
    ["Propuestas 2026", "7"],
    ["Aprobadas", "1"],
    ["Rechazadas", "2"],
    ["En debate", "4"],
    ["Última aparición", "16 abr 2026"],
    ["Frecuencia", "casi semanal"],
  ];
  const prop = D.proposals.filter(p => p.actor === "PIMEEF").concat([
    { title: "Convenio con formación profesional para temporadas cortas", state: "debate", stateLabel: "En debate", horizon: "≤ 6 meses" },
    { title: "Exención fiscal para empresas que alojan personal propio", state: "propuesta", stateLabel: "Propuesta", horizon: "12 meses" },
  ]);
  const positions = [
    ["Tope al alquiler",           "no"],
    ["Moratoria licencias",        "no"],
    ["Plan insular 400 viv.",      "amb"],
    ["Observatorio vivienda vacía","no"],
    ["Módulos temporales",         "yes"],
  ];
  const posColor = (x) => x === "yes" ? "var(--alert-green)" : x === "no" ? "var(--alert-red)" : "var(--alert-yellow)";
  const posMark = (x) => x === "yes" ? "A FAVOR" : x === "no" ? "EN CONTRA" : "AMBIGUO";

  return (
    <PageShell active="actores" path={`/actores/${name.toLowerCase()}/`}
      title={name}
      subtitle={`// ${role}. Ficha. Todas las propuestas registradas bajo este actor en ediciones recientes.`}>
      <Section>
        <div style={{ display: "grid", gridTemplateColumns: "2fr 1fr", gap: 28 }}>
          <div>
            <Label>Perfil editorial</Label>
            <p style={{ fontSize: 16, lineHeight: 1.6, marginTop: 8, maxWidth: 640 }}>
              Patronal con presencia editorial alta esta temporada. Coherente en defensa
              de soluciones de oferta privada para alojamiento temporal; hostil a
              mecanismos de control de precio. Voz fuerte en medios insulares, menor
              en Palma.
            </p>
            <p style={{ fontSize: 13, color: "var(--ink-3)", marginTop: 10, maxWidth: 640, lineHeight: 1.5, fontFamily: "var(--ff-mono)" }}>
              // esta ficha es descriptiva, no opinativa.<br/>
              // si detectas un sesgo, escríbenos: balance@housingradar.eiv
            </p>
          </div>
          <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 10, alignContent: "start" }}>
            {stats.map(([k, v], i) => (
              <Box key={i} style={{ padding: 12 }}>
                <Label>{k}</Label>
                <div className="tnum" style={{ fontFamily: "var(--ff-mono)", fontSize: 22, fontWeight: 600, marginTop: 4 }}>{v}</div>
              </Box>
            ))}
          </div>
        </div>
      </Section>

      <Section>
        <H2 n={1}>Propuestas registradas</H2>
        <div style={{ display: "grid", gap: 0 }}>
          {prop.map((p, i) => (
            <a key={i} href="propuesta.html" style={{ textDecoration: "none", color: "var(--ink)", display: "grid", gridTemplateColumns: "1fr auto auto", gap: 16, padding: "14px 0", borderTop: "1px solid var(--rule-soft)", alignItems: "center" }}>
              <div style={{ fontSize: 15, lineHeight: 1.4 }}>{p.title}</div>
              <Mono style={{ fontSize: 11, color: "var(--ink-3)" }}>{p.horizon}</Mono>
              <span style={{ fontFamily: "var(--ff-mono)", fontSize: 10.5, letterSpacing: 0.1, border: "1px solid var(--ink)", padding: "2px 8px" }}>{p.stateLabel}</span>
            </a>
          ))}
        </div>
      </Section>

      <Section>
        <H2 n={2}>Posiciones en propuestas ajenas</H2>
        <div style={{ display: "grid", gap: 0 }}>
          {positions.map(([p, v], i) => (
            <div key={i} style={{ display: "grid", gridTemplateColumns: "1fr auto", padding: "10px 0", borderTop: "1px solid var(--rule-soft)", alignItems: "center" }}>
              <div style={{ fontSize: 14 }}>{p}</div>
              <span style={{ fontFamily: "var(--ff-mono)", fontSize: 10.5, letterSpacing: 0.1, color: posColor(v), border: `1px solid ${posColor(v)}`, padding: "2px 8px" }}>{posMark(v)}</span>
            </div>
          ))}
        </div>
      </Section>
    </PageShell>
  );
};

// =====================================================================
// 4) RECURSOS
// =====================================================================
const Recursos = () => {
  const cats = [
    { t: "Datos abiertos", items: [
      ["IBESTAT — precio medio alquiler por municipio", "ibestat.caib.es/habitatge"],
      ["Catastro — parque residencial Ibiza", "sedecatastro.gob.es/07"],
      ["Registro Turístico Balear — plazas activas", "caib.es/turisme/registre"],
      ["Observatori UIB‑Eivissa (Q1 2026)", "uib.cat/observatori"],
    ]},
    { t: "Marco legal vigente", items: [
      ["Ley estatal 12/2023 por el derecho a la vivienda", "boe.es/leyes/12-2023"],
      ["Decreto Ley autonómico 3/2020 de vivienda turística", "caib.es/dl-3-2020"],
      ["Ordenanzas municipales de alquiler turístico (5 muni.)", "cnsl.eiv/ordenances"],
    ]},
    { t: "Actores con ficha abierta", items: [
      ["Govern Balear",        "actor.html"],
      ["Consell d'Eivissa",    "actor.html"],
      ["PIMEEF",               "actor.html"],
      ["USO Ibiza",            "actor.html"],
      ["Prou!",                "actor.html"],
      ["Cáritas Ibiza",        "actor.html"],
    ]},
    { t: "Descargas", items: [
      ["Edición 017 — PDF imprimible", "radar.eiv/edicions/017.pdf"],
      ["Archivo completo señales 2026 — CSV", "radar.eiv/data/senyals-2026.csv"],
      ["Archivo completo propuestas — JSON", "radar.eiv/data/propostes.json"],
    ]},
  ];
  return (
    <PageShell active="recursos" path="/recursos/"
      title="Recursos"
      subtitle="// Lo que usamos para verificar cada edición. Sin publicidad. Sin afiliación.">
      <Section>
        <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 28 }}>
          {cats.map((c, i) => (
            <div key={i}>
              <H2 n={i+1}>{c.t}</H2>
              <ul style={{ listStyle: "none", padding: 0, margin: 0 }}>
                {c.items.map(([label, href], j) => (
                  <li key={j} style={{ borderTop: "1px solid var(--rule-soft)", padding: "10px 0", display: "flex", justifyContent: "space-between", alignItems: "baseline", gap: 12 }}>
                    <a href={href.startsWith("actor") ? href : "#"} style={{ textDecoration: "none", color: "var(--ink)", fontSize: 14, lineHeight: 1.4 }}>→ {label}</a>
                    <Mono style={{ fontSize: 11, color: "var(--ink-3)" }}>{href}</Mono>
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </div>
      </Section>
    </PageShell>
  );
};

// =====================================================================
// 5) POLÍTICA EDITORIAL — 5 reglas duras
// =====================================================================
const Politica = () => {
  const reglas = [
    {
      t: "Mapeamos. No proponemos.",
      body: "Este observatorio no firma propuestas propias. Documentamos lo que proponen actores públicos, privados, sindicales y sociales. Cualquier lector debería poder detectar el sesgo editorial leyendo cómo elegimos las señales — no qué opinamos.",
    },
    {
      t: "Una edición por semana. Siempre en jueves.",
      body: "Ni una más, ni una menos. No publicamos \"números especiales\". Si hay urgencia, va en la edición siguiente. Esto protege al observatorio de convertirse en noticiario.",
    },
    {
      t: "Ninguna edición se edita después de publicarse.",
      body: "Las correcciones salen en la edición siguiente y se listan públicamente en /balance/. No reescribimos el pasado — ni siquiera un dato erróneo. La señal de un error es, en sí misma, editorialmente relevante.",
    },
    {
      t: "Tres fuentes o cita pública verificable.",
      body: "Cada señal requiere tres fuentes independientes o una cita pública con URL y fecha. Los rumores, off‑the‑record y \"fuentes del sector\" no entran, aunque sean ciertos.",
    },
    {
      t: "Balance público y coste editorial publicado.",
      body: "Coste de infraestructura, IA y edición publicado cada mes en /balance/. Si alguien nos paga, también. No hay publicidad; no hay suscripción premium; no hay paywall.",
    },
  ];
  return (
    <PageShell active="politica" path="/politica-editorial/"
      title="Política editorial"
      subtitle="// Cinco reglas duras. No son recomendaciones. Si una se rompe, lo decimos en /balance/ en la edición siguiente.">
      <Section>
        <ol style={{ listStyle: "none", padding: 0, margin: 0, counterReset: "r" }}>
          {reglas.map((r, i) => (
            <li key={i} style={{ display: "grid", gridTemplateColumns: "80px 1fr", gap: 24, padding: "22px 0", borderBottom: i === reglas.length - 1 ? "none" : "1px solid var(--ink-4)" }}>
              <div style={{ fontFamily: "var(--ff-mono)", fontSize: 48, fontWeight: 600, lineHeight: 1, color: "var(--ink-3)" }}>
                {String(i+1).padStart(2, "0")}
              </div>
              <div>
                <h3 style={{ fontFamily: "var(--ff-mono)", fontSize: 22, fontWeight: 600, margin: 0, letterSpacing: -0.005 }}>{r.t}</h3>
                <p style={{ fontSize: 16, lineHeight: 1.6, marginTop: 10, maxWidth: 680, color: "var(--ink-2)" }}>{r.body}</p>
              </div>
            </li>
          ))}
        </ol>
      </Section>

      <Section>
        <Label>Última revisión de estas reglas</Label>
        <Mono style={{ display: "block", fontSize: 13, marginTop: 6 }}>2026-03-02 — sin cambios desde edición 001.</Mono>
      </Section>
    </PageShell>
  );
};

// =====================================================================
// 6) BALANCE — transparencia financiera
// =====================================================================
const Balance = () => {
  const finance = [
    ["Infraestructura (hosting, dominios)",   "14,20 €"],
    ["IA (API calls, verificación señales)",  "28,60 €"],
    ["Honorarios editoriales (2 personas)",   "900,00 €"],
    ["Acceso a datos (IBESTAT premium)",      "18,00 €"],
    ["Total mes",                             "960,80 €"],
  ];
  const income = [
    ["Suscripciones voluntarias (87 pers.)",  "870,00 €"],
    ["Microgrants (Fundació Pita)",           "250,00 €"],
    ["Venta edición impresa (28 ud.)",         "56,00 €"],
    ["Total mes",                            "1 176,00 €"],
  ];
  const corr = [
    { d: "edic. 016", t: "Cifra de temporeros sin alojar: publicamos 1.600; la cifra confirmada es 1.400. Corregido en edición 017." },
    { d: "edic. 014", t: "Atribuimos una propuesta a Sumar cuando era de Més per Mallorca. Corregido." },
    { d: "edic. 011", t: "Error tipográfico en URL del Consell. Arreglado en edición siguiente." },
  ];
  const principles = [
    "Todos los números son verificables. Los libros están en un repositorio abierto.",
    "Si recibimos dinero de una institución, lo publicamos ese mes — nombre, importe, concepto.",
    "No hay publicidad. No hay afiliación. No hay suscripción premium.",
    "Si este balance deja de cuadrar tres meses seguidos, cerramos. No levantamos ronda.",
  ];
  return (
    <PageShell active="balance" path="/balance/"
      title="Balance"
      subtitle="// Mes: abril 2026. Cifras revisadas el 2026-04-19. Todas las correcciones editoriales también van aquí.">
      <Section>
        <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 32 }}>
          <div>
            <H2 n={1}>Costes</H2>
            <div style={{ display: "grid" }}>
              {finance.map(([k, v], i) => (
                <div key={i} style={{ display: "grid", gridTemplateColumns: "1fr auto", padding: "10px 0", borderTop: "1px solid var(--rule-soft)", fontSize: 14, fontWeight: i === finance.length - 1 ? 600 : 400, borderBottom: i === finance.length - 1 ? "2px solid var(--ink)" : undefined }}>
                  <span>{k}</span>
                  <span className="tnum" style={{ fontFamily: "var(--ff-mono)" }}>{v}</span>
                </div>
              ))}
            </div>
          </div>
          <div>
            <H2 n={2}>Ingresos</H2>
            <div style={{ display: "grid" }}>
              {income.map(([k, v], i) => (
                <div key={i} style={{ display: "grid", gridTemplateColumns: "1fr auto", padding: "10px 0", borderTop: "1px solid var(--rule-soft)", fontSize: 14, fontWeight: i === income.length - 1 ? 600 : 400, borderBottom: i === income.length - 1 ? "2px solid var(--ink)" : undefined }}>
                  <span>{k}</span>
                  <span className="tnum" style={{ fontFamily: "var(--ff-mono)" }}>{v}</span>
                </div>
              ))}
            </div>
          </div>
        </div>
        <div style={{ marginTop: 24, padding: 14, background: "var(--paper-2)", border: "1px solid var(--ink-4)", display: "flex", justifyContent: "space-between", alignItems: "baseline" }}>
          <Mono style={{ fontSize: 13, color: "var(--ink-3)" }}>BALANCE DEL MES</Mono>
          <Mono style={{ fontSize: 22, fontWeight: 600, color: "var(--alert-green)" }} className="tnum">+215,20 €</Mono>
        </div>
      </Section>

      <Section>
        <H2 n={3}>Correcciones editoriales recientes</H2>
        <ul style={{ listStyle: "none", padding: 0, margin: 0 }}>
          {corr.map((c, i) => (
            <li key={i} style={{ padding: "12px 0", borderTop: "1px solid var(--rule-soft)", display: "grid", gridTemplateColumns: "100px 1fr", gap: 16, fontSize: 14, lineHeight: 1.5 }}>
              <Mono style={{ color: "var(--ink-3)", fontSize: 12, paddingTop: 2 }}>{c.d}</Mono>
              <div>{c.t}</div>
            </li>
          ))}
        </ul>
      </Section>

      <Section>
        <H2 n={4}>Principios</H2>
        <ul style={{ listStyle: "none", padding: 0, margin: 0, maxWidth: 720 }}>
          {principles.map((p, i) => (
            <li key={i} style={{ padding: "10px 0", borderTop: "1px solid var(--rule-soft)", fontSize: 15, lineHeight: 1.55 }}>→ {p}</li>
          ))}
        </ul>
      </Section>
    </PageShell>
  );
};

// =====================================================================
// 7) CÓMO USARLO
// =====================================================================
const ComoUsarlo = () => {
  const steps = [
    { t: "Abre la última edición", body: "Cada jueves publicamos una. Empieza por ahí. Si no tienes tiempo, lee solo los bloques \"Nuevas propuestas\" y \"Lo que no se está diciendo\"." },
    { t: "Decide el horizonte que te interesa", body: "Cada propuesta tiene un horizonte declarado (≤6m, 12m, 12–24m, 24–36m). Si eres ciudadano, el útil suele ser ≤12m. Si eres planificador, mira ≥24m." },
    { t: "Sigue un actor, no un tema", body: "El tema se repite; el actor revela patrón. Abre una ficha de actor y mira su trayectoria. Si aparece cada semana, vigila; si aparece una vez, contrasta." },
    { t: "Usa /balance/ para auditarnos", body: "Publicamos costes, ingresos y correcciones todos los meses. Si ves una contradicción entre lo que decimos y lo que publicamos en balance, escríbenos." },
  ];
  const faqs = [
    ["¿Tienen una opinión?",       "No firmada. El sesgo está en qué señal elegimos. Si crees que lo tenemos, dilo en /balance/."],
    ["¿Suscripción?",              "Voluntaria. Sin paywall, sin \"premium\". Si no puedes pagar, leer es igual."],
    ["¿Puedo reutilizar los datos?", "Sí. Los archivos CSV y JSON están en /recursos/. Licencia CC BY 4.0."],
    ["¿Qué no hacen?",             "No hacemos activismo. No recomendamos voto. No aceptamos publicidad institucional ni privada."],
  ];
  return (
    <PageShell active="como-usarlo" path="/como-usarlo/"
      title="Cómo usarlo"
      subtitle="// Lectura honesta: qué es, qué no, y cómo sacarle provecho en menos de cinco minutos por semana.">
      <Section>
        <ol style={{ listStyle: "none", padding: 0, margin: 0 }}>
          {steps.map((s, i) => (
            <li key={i} style={{ display: "grid", gridTemplateColumns: "50px 1fr", gap: 16, padding: "18px 0", borderBottom: i === steps.length - 1 ? "none" : "1px solid var(--rule-soft)" }}>
              <Mono style={{ fontSize: 28, fontWeight: 600, color: "var(--ink-3)", lineHeight: 1 }}>{String(i+1).padStart(2, "0")}</Mono>
              <div>
                <h3 style={{ fontFamily: "var(--ff-mono)", fontSize: 19, fontWeight: 600, margin: 0 }}>{s.t}</h3>
                <p style={{ fontSize: 15, lineHeight: 1.6, marginTop: 6, color: "var(--ink-2)", maxWidth: 680 }}>{s.body}</p>
              </div>
            </li>
          ))}
        </ol>
      </Section>
      <Section>
        <H2 n={5}>Preguntas frecuentes</H2>
        {faqs.map(([q, a], i) => (
          <div key={i} style={{ padding: "14px 0", borderTop: "1px solid var(--rule-soft)", display: "grid", gridTemplateColumns: "1fr 2fr", gap: 16, alignItems: "start" }}>
            <Mono style={{ fontSize: 15, fontWeight: 600 }}>{q}</Mono>
            <div style={{ fontSize: 14.5, lineHeight: 1.55, color: "var(--ink-2)" }}>{a}</div>
          </div>
        ))}
      </Section>
      <Section>
        <Box style={{ padding: 20, background: "var(--ink)", color: "var(--paper)" }}>
          <Label style={{ color: "rgba(244,241,234,.6)" }}>Siguiente paso</Label>
          <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginTop: 10, gap: 14 }}>
            <Mono style={{ fontSize: 20, color: "var(--paper)" }}>→ Abrir la edición 017 (Sem. 16).</Mono>
            <a href="edicion.html" style={{ color: "var(--paper)", border: "1px solid var(--paper)", padding: "8px 14px", textDecoration: "none", fontFamily: "var(--ff-mono)", fontSize: 12, letterSpacing: 0.1 }}>leer ahora</a>
          </div>
        </Box>
      </Section>
    </PageShell>
  );
};

// =====================================================================
// 8) EDICIÓN — última edición (vista full)
// =====================================================================
const Edicion = () => {
  const d = D;
  return (
    <PageShell active="edicion" path={`/ediciones/${d.edition.number.toString().padStart(3,"0")}/`}
      title={`Edición ${String(d.edition.number).padStart(3, "0")} · ${d.edition.label}`}
      subtitle="// Del retraso del decreto al convenio de temporeros: el tablero se divide.">

      {/* Counters strip */}
      <Section style={{ background: "var(--paper-2)" }}>
        <div style={{ display: "grid", gridTemplateColumns: "repeat(4, 1fr)", gap: 32 }}>
          {[
            ["SEÑALES", d.edition.signals],
            ["PROPUESTAS ACTIVAS", d.edition.proposals],
            ["OMISIONES", d.edition.omisiones],
            ["A VIGILAR", d.vigilar.length],
          ].map(([k, v]) => (
            <div key={k}>
              <Label>{k}</Label>
              <Mono className="tnum" style={{ fontSize: 44, fontWeight: 600, lineHeight: 1.05, marginTop: 6, display: "block" }}>{v}</Mono>
            </div>
          ))}
        </div>
      </Section>

      {/* Señales — 3 variantes alternables */}
      <SignalsVariants signals={d.signals} />

      {/* Propuestas activas — 3 variantes alternables */}
      <ProposalsVariants proposals={d.proposals} />

      {/* Omisiones + vigilar */}
      <Section>
        <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 32 }}>
          <div>
            <H2 n={3}>Lo que no se está diciendo</H2>
            <ul style={{ listStyle: "none", padding: 0, margin: 0 }}>
              {d.omisiones.map((o, i) => (
                <li key={i} style={{ padding: "10px 0", borderTop: "1px solid var(--rule-soft)", fontSize: 14.5, lineHeight: 1.55 }}>→ {o}</li>
              ))}
            </ul>
          </div>
          <div>
            <H2 n={4}>A vigilar</H2>
            <ul style={{ listStyle: "none", padding: 0, margin: 0 }}>
              {d.vigilar.map((v, i) => (
                <li key={i} style={{ padding: "10px 0", borderTop: "1px solid var(--rule-soft)", fontSize: 14.5, lineHeight: 1.55, display: "grid", gridTemplateColumns: "80px 1fr", gap: 10 }}>
                  <Mono style={{ color: "var(--ink-3)", fontSize: 12 }}>{v.when}</Mono>
                  <span>{v.text}</span>
                </li>
              ))}
            </ul>
          </div>
        </div>
      </Section>

      {/* Rescate */}
      <Section>
        <H2 n={5}>Rescate del archivo</H2>
        <ul style={{ listStyle: "none", padding: 0, margin: 0 }}>
          {d.rescate.map((r, i) => (
            <li key={i} style={{ padding: "10px 0", borderTop: "1px solid var(--rule-soft)", display: "grid", gridTemplateColumns: "120px 1fr", gap: 10, fontSize: 14.5, lineHeight: 1.55 }}>
              <Mono style={{ color: "var(--ink-3)", fontSize: 12 }}>{r.year}</Mono>
              <span>{r.text}</span>
            </li>
          ))}
        </ul>
      </Section>
    </PageShell>
  );
};

// ---------- dispatch ----------
const PAGES = {
  ediciones: Ediciones,
  propuesta: Propuesta,
  actor: Actor,
  recursos: Recursos,
  politica: Politica,
  balance: Balance,
  "como-usarlo": ComoUsarlo,
  edicion: Edicion,
};
const Page = PAGES[window.PAGE_ID] || (() => <div style={{ padding: 36 }}>Page not found.</div>);
ReactDOM.createRoot(document.getElementById("app")).render(<Page />);
