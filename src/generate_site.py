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
  --red-dark: #9b0009;
  --bg: #070707;
  --panel: #111;
  --card: #181818;
  --text: #f5f5f5;
  --muted: #a7a7a7;
  --border: rgba(255,255,255,.08);
}}

* {{
  box-sizing: border-box;
}}

body {{
  margin: 0;
  font-family: Inter, system-ui, sans-serif;
  color: var(--text);
  background:
    radial-gradient(circle at top left, rgba(227,6,19,.25), transparent 40%),
    var(--bg);
}}

a {{
  color: inherit;
  text-decoration: none;
}}

.hero {{
  min-height: 320px;
  padding: 40px 24px;
  background:
    linear-gradient(120deg, rgba(0,0,0,.4), rgba(0,0,0,.9)),
    linear-gradient(135deg, var(--red), var(--red-dark));
}}

.hero-inner {{
  max-width: 1100px;
  margin: auto;
}}

.logo {{
  display: inline-block;
  padding: 8px 14px;
  border-radius: 999px;
  background: rgba(255,255,255,.1);
  font-weight: bold;
}}

.hero h1 {{
  margin: 25px 0 10px;
  font-size: clamp(40px, 6vw, 70px);
}}

.hero p {{
  color: #ccc;
}}

.wrapper {{
  max-width: 1100px;
  margin: -80px auto 60px;
  padding: 0 20px;
}}

.shell {{
  background: rgba(20,20,20,.9);
  border-radius: 24px;
  border: 1px solid var(--border);
  overflow: hidden;
}}

.topbar {{
  padding: 20px;
  border-bottom: 1px solid var(--border);
  display: flex;
  justify-content: space-between;
  flex-wrap: wrap;
}}

.breadcrumbs {{
  font-size: 14px;
  color: var(--muted);
}}

.badge {{
  background: rgba(227,6,19,.2);
  padding: 6px 12px;
  border-radius: 999px;
  font-size: 12px;
}}

.content {{
  padding: 24px;
}}

.section-title {{
  display: flex;
  align-items: center;
  gap: 10px;
  margin: 20px 0;
}}

.section-title::before {{
  content: "";
  width: 5px;
  height: 24px;
  border-radius: 999px;
  background: linear-gradient(180deg, #ff0033, #ff3366);
  box-shadow: 0 0 10px rgba(255,0,50,0.6);
}}

.grid {{
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px,1fr));
  gap: 15px;
}}

.nav-card {{
  padding: 18px;
  border-radius: 16px;
  background: #1b1b1b;
  border: 1px solid var(--border);
  transition: 0.25s;
}}

.nav-card:hover {{
  transform: translateY(-4px);
  box-shadow: 0 20px 40px rgba(0,0,0,.6);
  border-color: rgba(255,255,255,.15);
}}

.chart-card {{
  padding: 20px;
  border-radius: 20px;
  background: #111;
  border: 1px solid var(--border);
  margin-bottom: 25px;
}}

.chart-card h3 {{
  margin-bottom: 15px;
}}

.chart-card img {{
  width: 100%;
  border-radius: 10px;
  filter: invert(1) hue-rotate(180deg) contrast(0.9);
}}

.btn {{
  padding: 10px 14px;
  border-radius: 999px;
  background: var(--red);
  color: white;
  font-weight: bold;
}}

.btn.secondary {{
  background: #222;
  border: 1px solid var(--border);
}}

.footer {{
  padding: 20px;
  font-size: 12px;
  color: #777;
  border-top: 1px solid var(--border);
}}
</style>
</head>

<body>

<header class="hero">
  <div class="hero-inner">
    <div class="logo">🏋️ Gymtracker</div>
    <h1>{title}</h1>
    <p>Studio-Auslastung automatisch gemessen und visualisiert.</p>
  </div>
</header>

<main class="wrapper">
  <section class="shell">
    <div class="topbar">
      <div class="breadcrumbs">{breadcrumbs}</div>
      <div class="badge">● LIVE</div>
    </div>

    <div class="content">
      {body}
    </div>

    <div class="footer">
      Automatisch generiert · AI Fitness Style
    </div>
  </section>
</main>

</body>
</html>
"""


def write(path: Path, title: str, body: str, breadcrumbs: str = ""):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(page(title, body, breadcrumbs), encoding="utf-8")


def copy_assets():
    if DOCS_DIR.exists():
        shutil.rmtree(DOCS_DIR)
    DOCS_DIR.mkdir(parents=True)
    shutil.copytree(SOURCE_DIR, PUBLIC_STUDIOS_DIR)


def build():
    if not SOURCE_DIR.exists():
        print("Kein studios/ Ordner gefunden")
        return

    copy_assets()

    studios = [p for p in PUBLIC_STUDIOS_DIR.iterdir() if p.is_dir()]

    # START
    cards = "".join(f"""
<a class="nav-card" href="studios/{s.name}/index.html">
  <strong>{nice_name(s.name)}</strong>
  <span>Studio öffnen →</span>
</a>""" for s in studios)

    write(DOCS_DIR / "index.html", "Gymtracker",
          f"<h2 class='section-title'>Studios</h2><div class='grid'>{cards}</div>",
          "Start")

    for s in studios:
        years = [p for p in s.iterdir() if p.is_dir()]

        cards = "".join(f"""
<a class="nav-card" href="{y.name}/index.html">
  <strong>{y.name}</strong>
  <span>Jahr anzeigen →</span>
</a>""" for y in years)

        write(s / "index.html", nice_name(s.name),
              f"<a class='btn secondary' href='../../index.html'>← Zurück</a><h2 class='section-title'>Jahre</h2><div class='grid'>{cards}</div>",
              f'<a href="../../index.html">Start</a> / {nice_name(s.name)}')

        for y in years:
            months = [p for p in y.iterdir() if p.is_dir()]
            charts = "".join(f"""
<div class="chart-card">
<h3>{nice_chart_name(p.name)}</h3>
<img src="{p.name}">
</div>""" for p in y.glob("*.png"))

            write(y / "index.html", f"{nice_name(s.name)} {y.name}",
                  f"<a class='btn secondary' href='../index.html'>← Zurück</a><h2 class='section-title'>Monate</h2><div class='grid'>{''.join(f'<a class=\"nav-card\" href=\"{m.name}/index.html\"><strong>{m.name}</strong></a>' for m in months)}</div><h2 class='section-title'>Jahr</h2>{charts}",
                  f'<a href="../../../index.html">Start</a> / <a href="../index.html">{nice_name(s.name)}</a> / {y.name}')

    print("🔥 Fertig!")


if __name__ == "__main__":
    build()
