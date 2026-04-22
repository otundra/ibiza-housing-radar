// Shared PageShell for internal Ibiza Housing Radar pages.
// Mirrors variant C's top status bar + header nav language.
// Usage: <PageShell active="ediciones" title="Archivo de ediciones">{children}</PageShell>

const NAV = [
  ["home",            "Inicio",            "Ibiza Housing Radar.html"],
  ["edicion",         "Última edición",    "edicion.html"],
  ["ediciones",       "Ediciones",         "ediciones.html"],
  ["propuestas",      "Propuestas",        "propuesta.html"],
  ["actores",         "Actores",           "actor.html"],
  ["recursos",        "Recursos",          "recursos.html"],
  ["como-usarlo",     "Cómo usarlo",       "como-usarlo.html"],
  ["politica",        "Política editorial","politica-editorial.html"],
  ["balance",         "Balance",           "balance.html"],
];

const PageShell = ({ active, title, subtitle, path, children }) => {
  const [dark, setDark] = React.useState(false);
  React.useEffect(() => {
    try { setDark(localStorage.getItem("radar-dark") === "1"); } catch(e){}
  }, []);
  React.useEffect(() => {
    try { localStorage.setItem("radar-dark", dark ? "1" : "0"); } catch(e){}
  }, [dark]);
  const t = window.RADAR_DATA.transparency;

  return (
    <div className="radar" data-theme={dark ? "dark" : "light"}
      data-density="comfortable" data-palette="saturated" data-heads="sans"
      style={{ minHeight: "100vh", fontFamily: "var(--ff-mono)", fontSize: "calc(var(--d-text) * 1.25)" }}>

      {/* TOP STATUS BAR */}
      <div style={{ background: "var(--ink)", color: "var(--paper)", padding: "7px 36px", fontSize: 11.5, letterSpacing: 0.04, display: "flex", gap: 22, alignItems: "center", fontFamily: "var(--ff-mono)" }}>
        <span style={{ display: "inline-flex", alignItems: "center", gap: 6 }}>
          <span style={{ width: 7, height: 7, borderRadius: "50%", background: "var(--alert-yellow)" }} />
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
        <button onClick={() => setDark(!dark)} title="Modo oscuro"
          style={{ background: "transparent", border: "1px solid rgba(244,241,234,.25)", color: "var(--paper)", cursor: "pointer", padding: "2px 8px", fontFamily: "inherit", fontSize: 11, letterSpacing: 0.06, borderRadius: 2 }}>
          {dark ? "◐ dark" : "◑ light"}
        </button>
      </div>

      {/* HEADER NAV */}
      <header style={{ borderBottom: "2px solid var(--ink)", padding: "14px 36px 10px", background: "var(--paper)" }}>
        <div className="row between" style={{ alignItems: "center" }}>
          <a href="Ibiza Housing Radar.html" style={{ textDecoration: "none", color: "var(--ink)", fontFamily: "var(--ff-mono)", fontWeight: 600, fontSize: 14, letterSpacing: 0 }}>
            ibiza_housing_radar <span className="muted" style={{ fontWeight: 400 }}>v.17</span>
          </a>
          <nav style={{ display: "flex", gap: 14, fontSize: 12, fontFamily: "var(--ff-mono)", flexWrap: "wrap", justifyContent: "flex-end" }}>
            {NAV.filter(n => n[0] !== "home").map(([k, label, href]) => (
              <a key={k} href={href}
                style={{
                  textDecoration: "none",
                  color: k === active ? "var(--ink)" : "var(--ink-3)",
                  borderBottom: k === active ? "2px solid var(--ink)" : "2px solid transparent",
                  paddingBottom: 2,
                  fontWeight: k === active ? 600 : 400,
                }}>{label}</a>
            ))}
          </nav>
        </div>
      </header>

      {/* PAGE CRUMBS + TITLE */}
      <section style={{ padding: "18px 36px 22px", borderBottom: "1px solid var(--ink)" }}>
        <div className="mono" style={{ fontSize: 11.5, letterSpacing: 0.1, textTransform: "uppercase", color: "var(--ink-3)" }}>
          {path || `/${active}/`}
        </div>
        <h1 style={{ fontFamily: "var(--ff-mono)", fontSize: 42, lineHeight: 1.05, fontWeight: 600, marginTop: 10, letterSpacing: -0.015 }}>
          {title}
        </h1>
        {subtitle && <p style={{ fontFamily: "var(--ff-mono)", fontSize: 15, color: "var(--ink-2)", marginTop: 10, maxWidth: 780, lineHeight: 1.5 }}>{subtitle}</p>}
      </section>

      <main>{children}</main>

      <TranspFooter pad="0 36px" />
    </div>
  );
};

window.PageShell = PageShell;
window.RADAR_NAV = NAV;
