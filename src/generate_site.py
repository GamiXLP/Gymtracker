import shutil
from pathlib import Path

SOURCE_DIR = Path("studios")
DOCS_DIR = Path("docs")
PUBLIC_STUDIOS_DIR = DOCS_DIR / "studios"


def nice_name(value: str) -> str:
    return value.replace("ai-fitness-", "").replace("-", " ").title()


def nice_chart_name(value: str) -> str:
    value = value.replace(".png", "").replace("_", " ")

    replacements = {
        "weekday monday": "Montag",
        "weekday tuesday": "Dienstag",
        "weekday wednesday": "Mittwoch",
        "weekday thursday": "Donnerstag",
        "weekday friday": "Freitag",
        "weekday saturday": "Samstag",
        "weekday sunday": "Sonntag",
        "day": "Tagesverlauf",
    }

    for old, new in replacements.items():
        value = value.replace(old, new)

    return value.title()


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
  --bg: #070707;
  --panel: #111;
  --card: #181818;
  --text: #f5f5f5;
  --muted: #a7a7a7;
  --border: rgba(255,255,255,.08);
}}

body {{
  margin: 0;
  font-family: Inter, system-ui;
  background: radial-gradient(circle at top, rgba(227,6,19,.2), transparent 40%), var(--bg);
  color: var(--text);
}}

a {{ text-decoration: none; color: inherit; }}

.hero {{
  padding: 40px;
  background: linear-gradient(135deg, #e30613, #8a0008);
}}

.hero h1 {{
  font-size: 60px;
  margin: 20px 0;
}}

.wrapper {{
  max-width: 1100px;
  margin: -60px auto 80px;
  padding: 0 20px;
}}

.shell {{
  background: #111;
  border-radius: 20px;
  overflow: hidden;
  border: 1px solid var(--border);
}}

.topbar {{
  padding: 20px;
  display: flex;
  justify-content: space-between;
  border-bottom: 1px solid var(--border);
}}

.content {{
  padding: 25px;
}}

.section-title {{
  margin: 20px 0;
  font-size: 22px;
}}

.grid {{
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: 15px;
}}

.nav-card {{
  background: var(--card);
  padding: 18px;
  border-radius: 14px;
  border: 1px solid var(--border);
  transition: 0.2s;
}}

.nav-card:hover {{
  transform: translateY(-4px);
  border-color: var(--red);
}}

.chart-card {{
  padding: 18px;
  margin-bottom: 26px;
  border-radius: 24px;
  background: linear-gradient(145deg, #1a1a1a, #111);
  border: 1px solid rgba(255,255,255,0.06);
  box-shadow: 0 20px 50px rgba(0,0,0,0.6);
}}

.chart-card img {{
  background: #0a0a0a;
  border-radius: 14px;
}}

.btn {{
  display: inline-block;
  padding: 10px 14px;
  border-radius: 999px;
  background: #222;
}}

.footer {{
  padding: 20px;
  text-align: center;
  color: var(--muted);
  border-top: 1px solid var(--border);
}}
</style>
</head>

<body>

<div class="hero">
  <h1>{title}</h1>
</div>

<div class="wrapper">
  <div class="shell">
    <div class="topbar">
      <div>{breadcrumbs}</div>
      <div>● LIVE</div>
    </div>

    <div class="content">
      {body}
    </div>

    <div class="footer">
      Gymtracker · AI Fitness Style
    </div>
  </div>
</div>

</body>
</html>
"""


def write(path: Path, title: str, body: str, breadcrumbs: str = ""):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(page(title, body, breadcrumbs), encoding="utf-8")


def copy_assets():
    if DOCS_DIR.exists():
        shutil.rmtree(DOCS_DIR)

    DOCS_DIR.mkdir()
    shutil.copytree(SOURCE_DIR, PUBLIC_STUDIOS_DIR)


def build():
    if not SOURCE_DIR.exists():
        print("Kein studios/ Ordner gefunden")
        return

    copy_assets()

    studios = [p for p in PUBLIC_STUDIOS_DIR.iterdir() if p.is_dir()]

    # HOME
    write(
        DOCS_DIR / "index.html",
        "Gymtracker",
        f"""
<h2 class="section-title">Studios</h2>
<div class="grid">
{''.join(f'<a class="nav-card" href="studios/{s.name}/index.html"><strong>{nice_name(s.name)}</strong></a>' for s in studios)}
</div>
""",
        "Start"
    )

    # STUDIOS
    for s in studios:
        years = [p for p in s.iterdir() if p.is_dir()]

        write(
            s / "index.html",
            nice_name(s.name),
            f"""
<a class="btn" href="../../index.html">← Zurück</a>

<h2 class="section-title">Jahre</h2>
<div class="grid">
{''.join(f'<a class="nav-card" href="{y.name}/index.html"><strong>{y.name}</strong></a>' for y in years)}
</div>
""",
            f'<a href="../../index.html">Start</a> / {nice_name(s.name)}'
        )

        # YEARS
        for y in years:
            months = [p for p in y.iterdir() if p.is_dir()]
            yearly_pngs = list(y.glob("*.png"))

            write(
                y / "index.html",
                f"{nice_name(s.name)} {y.name}",
                f"""
<a class="btn" href="../index.html">← Zurück</a>

<h2 class="section-title">Monate</h2>
<div class="grid">
{''.join(f'<a class="nav-card" href="{m.name}/index.html"><strong>{m.name}</strong></a>' for m in months)}
</div>

<h2 class="section-title">Jahresdiagramme</h2>
{''.join(f'<div class="chart-card"><h3>{nice_chart_name(p.name)}</h3><img src="{p.name}"></div>' for p in yearly_pngs)}
""",
                f'<a href="../../../index.html">Start</a> / <a href="../index.html">{nice_name(s.name)}</a> / {y.name}'
            )

            # MONTHS
            for m in months:
                days = [p for p in m.iterdir() if p.is_dir()]
                monthly_pngs = list(m.glob("*.png"))

                write(
                    m / "index.html",
                    f"{nice_name(s.name)} {y.name}/{m.name}",
                    f"""
<a class="btn" href="../index.html">← Zurück</a>

<h2 class="section-title">Tage</h2>
<div class="grid">
{''.join(f'<a class="nav-card" href="{d.name}/index.html"><strong>{d.name}</strong></a>' for d in days)}
</div>

<h2 class="section-title">Monatsdiagramme</h2>
{''.join(f'<div class="chart-card"><h3>{nice_chart_name(p.name)}</h3><img src="{p.name}"></div>' for p in monthly_pngs)}
""",
                    f'<a href="../../../../index.html">Start</a> / <a href="../../index.html">{nice_name(s.name)}</a> / <a href="../index.html">{y.name}</a> / {m.name}'
                )

                # DAYS
                for d in days:
                    day_pngs = list(d.glob("*.png"))
                    csvs = list(d.glob("*.csv"))

                    write(
                        d / "index.html",
                        f"{nice_name(s.name)} {y.name}/{m.name}/{d.name}",
                        f"""
<a class="btn" href="../index.html">← Zurück</a>

<h2 class="section-title">Tagesdiagramme</h2>
{''.join(f'<div class="chart-card"><h3>{nice_chart_name(p.name)}</h3><img src="{p.name}"></div>' for p in day_pngs)}

<h2 class="section-title">Tabellen</h2>
<div class="grid">
{''.join(f'<a class="nav-card" href="{c.name}"><strong>{c.name}</strong></a>' for c in csvs)}
</div>
""",
                        f'<a href="../../../../../index.html">Start</a> / <a href="../../../index.html">{nice_name(s.name)}</a> / <a href="../../index.html">{y.name}</a> / <a href="../index.html">{m.name}</a> / {d.name}'
                    )

    print("✅ Fertig! Site unter docs/ generiert.")


if __name__ == "__main__":
    build()
