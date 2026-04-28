import shutil
from pathlib import Path

SOURCE_DIR = Path("studios")
DOCS_DIR = Path("docs")
PUBLIC_STUDIOS_DIR = DOCS_DIR / "studios"


def nice_name(value: str) -> str:
    return value.replace("ai-fitness-", "").replace("-", " ").title()


def page(title: str, body: str, breadcrumbs: str = "") -> str:
    return f"""<!DOCTYPE html>
<html lang="de">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<style>
:root {{
  --red: #e30613;
  --red-dark: #9b0009;
  --bg: #070707;
  --panel: #111;
  --card: #181818;
  --card-soft: #202020;
  --text: #f5f5f5;
  --muted: #a7a7a7;
  --border: rgba(255,255,255,.08);
}}

* {{
  box-sizing: border-box;
}}

body {{
  margin: 0;
  font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Arial, sans-serif;
  color: var(--text);
  background:
    radial-gradient(circle at top left, rgba(227,6,19,.24), transparent 35%),
    radial-gradient(circle at top right, rgba(227,6,19,.12), transparent 35%),
    var(--bg);
}}

a {{
  color: inherit;
  text-decoration: none;
}}

.hero {{
  min-height: 260px;
  padding: 42px 28px;
  background:
    linear-gradient(120deg, rgba(0,0,0,.35), rgba(0,0,0,.88)),
    linear-gradient(135deg, var(--red), var(--red-dark));
  border-bottom: 1px solid rgba(255,255,255,.1);
}}

.hero-inner {{
  max-width: 1180px;
  margin: 0 auto;
}}

.logo {{
  display: inline-flex;
  gap: 12px;
  align-items: center;
  padding: 9px 14px;
  border-radius: 999px;
  background: rgba(255,255,255,.1);
  border: 1px solid rgba(255,255,255,.18);
  font-weight: 800;
  letter-spacing: .3px;
}}

.hero h1 {{
  max-width: 900px;
  margin: 28px 0 12px;
  font-size: clamp(38px, 7vw, 76px);
  line-height: .92;
  text-transform: uppercase;
  letter-spacing: -2px;
}}

.hero p {{
  max-width: 720px;
  margin: 0;
  color: rgba(255,255,255,.82);
  font-size: 18px;
}}

.wrapper {{
  max-width: 1180px;
  margin: -56px auto 80px;
  padding: 0 20px;
}}

.shell {{
  background: rgba(17,17,17,.86);
  backdrop-filter: blur(18px);
  border: 1px solid var(--border);
  border-radius: 28px;
  box-shadow: 0 28px 80px rgba(0,0,0,.45);
  overflow: hidden;
}}

.topbar {{
  padding: 22px 26px;
  border-bottom: 1px solid var(--border);
  display: flex;
  justify-content: space-between;
  gap: 16px;
  align-items: center;
  flex-wrap: wrap;
}}

.breadcrumbs {{
  color: var(--muted);
  font-size: 14px;
}}

.breadcrumbs a {{
  color: white;
}}

.badge {{
  color: white;
  background: rgba(227,6,19,.16);
  border: 1px solid rgba(227,6,19,.45);
  padding: 8px 12px;
  border-radius: 999px;
  font-size: 13px;
  font-weight: 700;
}}

.content {{
  padding: 28px;
}}

.section-title {{
  display: flex;
  align-items: center;
  gap: 12px;
  margin: 6px 0 18px;
  font-size: 24px;
}}

.section-title::before {{
  content: "";
  width: 6px;
  height: 30px;
  border-radius: 99px;
  background: var(--red);
}}

.grid {{
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(190px, 1fr));
  gap: 16px;
  margin-bottom: 34px;
}}

.nav-card {{
  min-height: 92px;
  padding: 20px;
  border-radius: 20px;
  background:
    linear-gradient(145deg, rgba(255,255,255,.06), rgba(255,255,255,.02)),
    var(--card);
  border: 1px solid var(--border);
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  transition: .2s ease;
}}

.nav-card:hover {{
  transform: translateY(-4px);
  border-color: rgba(227,6,19,.75);
  box-shadow: 0 18px 40px rgba(227,6,19,.16);
}}

.nav-card strong {{
  font-size: 18px;
}}

.nav-card span {{
  color: var(--muted);
  font-size: 13px;
}}

.chart-card {{
  padding: 18px;
  margin-bottom: 26px;
  border-radius: 24px;
  background: #f8f8f8;
  color: #111;
  border: 1px solid rgba(255,255,255,.1);
  box-shadow: 0 18px 50px rgba(0,0,0,.32);
}}

.chart-card h3 {{
  margin: 0 0 14px;
  color: #111;
  font-size: 18px;
}}

.chart-card img {{
  width: 100%;
  display: block;
  border-radius: 16px;
  border: 1px solid #ddd;
  background: white;
}}

.action-row {{
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
  margin-bottom: 24px;
}}

.btn {{
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 11px 15px;
  border-radius: 999px;
  background: var(--red);
  color: white;
  font-weight: 800;
  box-shadow: 0 12px 28px rgba(227,6,19,.22);
}}

.btn.secondary {{
  background: var(--card-soft);
  color: var(--text);
  border: 1px solid var(--border);
  box-shadow: none;
}}

.table-list {{
  display: grid;
  gap: 12px;
}}

.footer {{
  padding: 22px 26px;
  color: var(--muted);
  border-top: 1px solid var(--border);
  font-size: 13px;
}}

@media (max-width: 700px) {{
  .content, .topbar {{
    padding: 20px;
  }}

  .wrapper {{
    margin-top: -36px;
  }}

  .hero {{
    min-height: 220px;
  }}
}}
</style>
</head>
<body>
<header class="hero">
  <div class="hero-inner">
    <div class="logo">🏋️ Gymtracker</div>
    <h1>{title}</h1>
    <p>Moderne Auslastungsanalyse für dein AI Fitness Studio. Automatisch gesammelt, visualisiert und täglich aktualisiert.</p>
  </div>
</header>

<main class="wrapper">
  <section class="shell">
    <div class="topbar">
      <div class="breadcrumbs">{breadcrumbs}</div>
      <div class="badge">● LIVE DASHBOARD</div>
    </div>
    <div class="content">
      {body}
    </div>
    <div class="footer">
      Automatisch generiert · AI Fitness Farben · GitHub Pages
    </div>
  </section>
</main>
</body>
</html>
"""


def write(path: Path, title: str, body: str, breadcrumbs: str = "") -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(page(title, body, breadcrumbs), encoding="utf-8")


def copy_assets() -> None:
    if DOCS_DIR.exists():
        shutil.rmtree(DOCS_DIR)

    DOCS_DIR.mkdir(parents=True, exist_ok=True)
    shutil.copytree(SOURCE_DIR, PUBLIC_STUDIOS_DIR)


def build() -> None:
    if not SOURCE_DIR.exists():
        print("Kein studios/ Ordner gefunden")
        return

    copy_assets()

    studio_dirs = sorted([p for p in PUBLIC_STUDIOS_DIR.iterdir() if p.is_dir()])

    cards = ""
    for studio in studio_dirs:
        cards += f"""
<a class="nav-card" href="studios/{studio.name}/index.html">
  <strong>{nice_name(studio.name)}</strong>
  <span>Studio öffnen →</span>
</a>
"""

    write(
        DOCS_DIR / "index.html",
        "Gymtracker",
        f"""
<h2 class="section-title">Studios</h2>
<div class="grid">{cards}</div>
""",
        "Startseite",
    )

    for studio in studio_dirs:
        years = sorted([p for p in studio.iterdir() if p.is_dir()])

        cards = ""
        for year in years:
            cards += f"""
<a class="nav-card" href="{year.name}/index.html">
  <strong>{year.name}</strong>
  <span>Jahr anzeigen →</span>
</a>
"""

        write(
            studio / "index.html",
            nice_name(studio.name),
            f"""
<div class="action-row">
  <a class="btn secondary" href="../../index.html">← Alle Studios</a>
</div>
<h2 class="section-title">Jahre</h2>
<div class="grid">{cards}</div>
""",
            f'<a href="../../index.html">Start</a> / {nice_name(studio.name)}',
        )

        for year in years:
            months = sorted([p for p in year.iterdir() if p.is_dir()])
            yearly_pngs = sorted(year.glob("*.png"))

            month_cards = ""
            for month in months:
                month_cards += f"""
<a class="nav-card" href="{month.name}/index.html">
  <strong>{month.name}</strong>
  <span>Monat anzeigen →</span>
</a>
"""

            charts = ""
            for png in yearly_pngs:
                charts += f"""
<div class="chart-card">
  <h3>{png.stem.replace("_", " ").title()}</h3>
  <img src="{png.name}" alt="{png.name}">
</div>
"""

            write(
                year / "index.html",
                f"{nice_name(studio.name)} · {year.name}",
                f"""
<div class="action-row">
  <a class="btn secondary" href="../index.html">← Zurück zum Studio</a>
</div>
<h2 class="section-title">Monate</h2>
<div class="grid">{month_cards}</div>
<h2 class="section-title">Jahresdiagramme</h2>
{charts if charts else "<p>Keine Jahresdiagramme vorhanden.</p>"}
""",
                f'<a href="../../../index.html">Start</a> / <a href="../index.html">{nice_name(studio.name)}</a> / {year.name}',
            )

            for month in months:
                days = sorted([p for p in month.iterdir() if p.is_dir()])
                monthly_pngs = sorted(month.glob("*.png"))

                day_cards = ""
                for day in days:
                    day_cards += f"""
<a class="nav-card" href="{day.name}/index.html">
  <strong>{day.name}</strong>
  <span>Tagesverlauf anzeigen →</span>
</a>
"""

                charts = ""
                for png in monthly_pngs:
                    charts += f"""
<div class="chart-card">
  <h3>{png.stem.replace("_", " ").title()}</h3>
  <img src="{png.name}" alt="{png.name}">
</div>
"""

                write(
                    month / "index.html",
                    f"{nice_name(studio.name)} · {year.name}/{month.name}",
                    f"""
<div class="action-row">
  <a class="btn secondary" href="../index.html">← Zurück zum Jahr</a>
</div>
<h2 class="section-title">Tage</h2>
<div class="grid">{day_cards}</div>
<h2 class="section-title">Monatsdiagramme</h2>
{charts if charts else "<p>Keine Monatsdiagramme vorhanden.</p>"}
""",
                    f'<a href="../../../../index.html">Start</a> / <a href="../../index.html">{nice_name(studio.name)}</a> / <a href="../index.html">{year.name}</a> / {month.name}',
                )

                for day in days:
                    day_pngs = sorted(day.glob("*.png"))
                    csvs = sorted(day.glob("*.csv"))

                    charts = ""
                    for png in day_pngs:
                        charts += f"""
<div class="chart-card">
  <h3>{png.stem.replace("_", " ").title()}</h3>
  <img src="{png.name}" alt="{png.name}">
</div>
"""

                    tables = ""
                    for csv in csvs:
                        tables += f"""
<a class="nav-card" href="{csv.name}">
  <strong>{csv.name}</strong>
  <span>CSV öffnen →</span>
</a>
"""

                    write(
                        day / "index.html",
                        f"{nice_name(studio.name)} · {year.name}/{month.name}/{day.name}",
                        f"""
<div class="action-row">
  <a class="btn secondary" href="../index.html">← Zurück zum Monat</a>
</div>
<h2 class="section-title">Tagesdiagramme</h2>
{charts if charts else "<p>Keine Tagesdiagramme vorhanden.</p>"}
<h2 class="section-title">Tabellen</h2>
<div class="grid">{tables}</div>
""",
                        f'<a href="../../../../../index.html">Start</a> / <a href="../../../index.html">{nice_name(studio.name)}</a> / <a href="../../index.html">{year.name}</a> / <a href="../index.html">{month.name}</a> / {day.name}',
                    )

    print("Schönes Dashboard wurde unter docs/ erstellt.")


if __name__ == "__main__":
    build()
