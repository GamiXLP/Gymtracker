import shutil
from pathlib import Path
from html import escape

SOURCE_DIR = Path("studios")
DOCS_DIR = Path("docs")
PUBLIC_STUDIOS_DIR = DOCS_DIR / "studios"


def nice_name(value: str) -> str:
    return value.replace("ai-fitness-", "").replace("-", " ").title()


def nice_chart_name(value: str) -> str:
    value = value.replace(".png", "").replace("_", " ").lower()

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


def sort_dirs(items):
    return sorted([p for p in items if p.is_dir()], key=lambda p: p.name)


def sort_pngs(path: Path):
    return sorted(path.glob("*.png"), key=lambda p: p.name)


def page(title: str, body: str, back_href: str | None = None, subtitle: str = "Studio-Auslastung automatisch gemessen und visualisiert.") -> str:
    back_button = ""
    if back_href:
        back_button = f'<a class="back-btn" href="{back_href}">← Zurück</a>'

    return f"""<!DOCTYPE html>
<html lang="de">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{escape(title)}</title>

<style>
:root {{
  --red: #e30613;
  --red-dark: #93000a;
  --bg: #070707;
  --panel: #121212;
  --panel-2: #181818;
  --text: #f4f4f4;
  --muted: #a6a6a6;
  --border: rgba(255,255,255,.10);
}}

* {{
  box-sizing: border-box;
}}

html {{
  scroll-behavior: smooth;
}}

body {{
  margin: 0;
  min-height: 100vh;
  font-family: Inter, Arial, system-ui, sans-serif;
  background:
    radial-gradient(circle at 20% 0%, rgba(227, 6, 19, .34), transparent 34%),
    radial-gradient(circle at 90% 10%, rgba(227, 6, 19, .16), transparent 30%),
    linear-gradient(180deg, #090909 0%, #050505 100%);
  color: var(--text);
}}

a {{
  color: inherit;
  text-decoration: none;
}}

.hero {{
  padding: 34px 18px 92px;
  background:
    linear-gradient(135deg, rgba(227,6,19,.96), rgba(110,0,8,.96)),
    linear-gradient(135deg, var(--red), var(--red-dark));
  border-bottom: 1px solid rgba(255,255,255,.12);
}}

.hero-inner {{
  width: min(1180px, 100%);
  margin: 0 auto;
}}

.top-nav {{
  min-height: 42px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 14px;
  margin-bottom: 34px;
}}

.back-btn {{
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 10px 15px;
  border-radius: 999px;
  background: rgba(0,0,0,.24);
  border: 1px solid rgba(255,255,255,.22);
  font-weight: 800;
  font-size: 14px;
  transition: .2s ease;
}}

.back-btn:hover {{
  background: rgba(0,0,0,.38);
  transform: translateY(-1px);
}}

.live-badge {{
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 9px 13px;
  border-radius: 999px;
  background: rgba(0,0,0,.24);
  border: 1px solid rgba(255,255,255,.22);
  font-weight: 900;
  font-size: 13px;
  letter-spacing: .04em;
}}

.live-dot {{
  width: 9px;
  height: 9px;
  border-radius: 999px;
  background: #31ff72;
  box-shadow: 0 0 16px rgba(49,255,114,.9);
}}

.hero h1 {{
  margin: 0;
  max-width: 980px;
  font-size: clamp(38px, 7vw, 92px);
  line-height: .9;
  letter-spacing: -0.06em;
  text-transform: uppercase;
}}

.hero p {{
  margin: 18px 0 0;
  max-width: 680px;
  color: rgba(255,255,255,.82);
  font-size: clamp(16px, 2vw, 20px);
  font-weight: 600;
}}

.wrapper {{
  width: min(1180px, 100%);
  margin: -58px auto 70px;
  padding: 0 18px;
}}

.shell {{
  background: rgba(18,18,18,.90);
  border: 1px solid var(--border);
  border-radius: 30px;
  box-shadow: 0 30px 90px rgba(0,0,0,.58);
  backdrop-filter: blur(18px);
  overflow: hidden;
}}

.content {{
  padding: clamp(18px, 3vw, 34px);
}}

.grid {{
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(210px, 1fr));
  gap: 16px;
}}

.nav-card {{
  position: relative;
  min-height: 118px;
  padding: 22px;
  border-radius: 24px;
  background:
    linear-gradient(145deg, rgba(255,255,255,.075), rgba(255,255,255,.025));
  border: 1px solid var(--border);
  overflow: hidden;
  transition: .22s ease;
}}

.nav-card::before {{
  content: "";
  position: absolute;
  inset: 0;
  background: radial-gradient(circle at 20% 0%, rgba(227,6,19,.32), transparent 38%);
  opacity: .7;
}}

.nav-card strong {{
  position: relative;
  z-index: 1;
  display: block;
  font-size: 23px;
  line-height: 1.05;
  letter-spacing: -0.03em;
}}

.nav-card span {{
  position: relative;
  z-index: 1;
  display: inline-block;
  margin-top: 14px;
  color: var(--muted);
  font-weight: 700;
}}

.nav-card:hover {{
  transform: translateY(-4px);
  border-color: rgba(227,6,19,.75);
  box-shadow: 0 18px 45px rgba(0,0,0,.35);
}}

.section-title {{
  margin: 6px 0 18px;
  font-size: 18px;
  color: var(--muted);
  font-weight: 900;
  text-transform: uppercase;
  letter-spacing: .10em;
}}

.chart-card {{
  margin-top: 22px;
  padding: clamp(14px, 2vw, 22px);
  border-radius: 26px;
  background:
    linear-gradient(145deg, rgba(255,255,255,.07), rgba(255,255,255,.025));
  border: 1px solid var(--border);
}}

.chart-card:first-child {{
  margin-top: 0;
}}

.chart-card h3 {{
  margin: 0 0 16px;
  font-size: clamp(20px, 3vw, 34px);
  letter-spacing: -0.04em;
}}

.chart-frame {{
  width: 100%;
  overflow-x: auto;
  border-radius: 18px;
  background: #fff;
}}

.chart-card img {{
  display: block;
  width: 100%;
  height: auto;
  min-width: 720px;
  border-radius: 18px;
}}

.empty {{
  padding: 28px;
  border-radius: 24px;
  border: 1px dashed var(--border);
  color: var(--muted);
  background: rgba(255,255,255,.03);
  font-weight: 700;
}}

.footer {{
  padding: 18px 24px;
  border-top: 1px solid var(--border);
  color: var(--muted);
  text-align: center;
  font-size: 13px;
  font-weight: 700;
}}

@media (max-width: 760px) {{
  .hero {{
    padding-bottom: 78px;
  }}

  .top-nav {{
    margin-bottom: 26px;
  }}

  .shell {{
    border-radius: 24px;
  }}

  .nav-card {{
    min-height: 98px;
  }}

  .chart-card img {{
    min-width: 620px;
  }}
}}
</style>
</head>

<body>

<header class="hero">
  <div class="hero-inner">
    <div class="top-nav">
      <div>{back_button}</div>
      <div class="live-badge"><span class="live-dot"></span> LIVE</div>
    </div>

    <h1>{escape(title)}</h1>
    <p>{escape(subtitle)}</p>
  </div>
</header>

<main class="wrapper">
  <div class="shell">
    <div class="content">
      {body}
    </div>

    <div class="footer">
      Gymtracker · AI Fitness Dashboard
    </div>
  </div>
</main>

</body>
</html>
"""


def write(path: Path, title: str, body: str, back_href: str | None = None):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(page(title, body, back_href), encoding="utf-8")


def copy_assets():
    if DOCS_DIR.exists():
        shutil.rmtree(DOCS_DIR)

    DOCS_DIR.mkdir(parents=True, exist_ok=True)
    shutil.copytree(SOURCE_DIR, PUBLIC_STUDIOS_DIR)


def nav_card(href: str, title: str, label: str = "Öffnen") -> str:
    return f"""
<a class="nav-card" href="{escape(href)}">
  <strong>{escape(title)}</strong>
  <span>{escape(label)} →</span>
</a>
"""


def chart_card(png: Path) -> str:
    return f"""
<div class="chart-card">
  <h3>{escape(nice_chart_name(png.name))}</h3>
  <div class="chart-frame">
    <img src="{escape(png.name)}" alt="{escape(nice_chart_name(png.name))}">
  </div>
</div>
"""


def empty(text: str) -> str:
    return f'<div class="empty">{escape(text)}</div>'


def build():
    if not SOURCE_DIR.exists():
        print("Kein studios/ Ordner gefunden")
        return

    copy_assets()

    studios = sort_dirs(PUBLIC_STUDIOS_DIR.iterdir())

    cards = ""
    for s in studios:
        cards += nav_card(f"studios/{s.name}/index.html", nice_name(s.name), "Studio anzeigen")

    if not cards:
        cards = empty("Noch keine Studios gefunden.")

    write(
        DOCS_DIR / "index.html",
        "Gymtracker",
        f"<div class='section-title'>Studios</div><div class='grid'>{cards}</div>",
        None,
    )

    for s in studios:
        years = sort_dirs(s.iterdir())

        year_cards = ""
        for y in years:
            year_cards += nav_card(f"{y.name}/index.html", y.name, "Jahr anzeigen")

        if not year_cards:
            year_cards = empty("Für dieses Studio wurden noch keine Jahre gefunden.")

        write(
            s / "index.html",
            nice_name(s.name),
            f"<div class='section-title'>Jahre</div><div class='grid'>{year_cards}</div>",
            "../../index.html",
        )

        for y in years:
            months = sort_dirs(y.iterdir())

            month_cards = ""
            for m in months:
                month_cards += nav_card(f"{m.name}/index.html", m.name, "Monat anzeigen")

            charts = ""
            for png in sort_pngs(y):
                charts += chart_card(png)

            body = ""
            if month_cards:
                body += f"<div class='section-title'>Monate</div><div class='grid'>{month_cards}</div>"
            if charts:
                body += f"<div class='section-title' style='margin-top:32px;'>Jahresauswertung</div>{charts}"
            if not body:
                body = empty("Für dieses Jahr wurden noch keine Daten gefunden.")

            write(
                y / "index.html",
                f"{nice_name(s.name)} {y.name}",
                body,
                "../index.html",
            )

            for m in months:
                days = sort_dirs(m.iterdir())

                day_cards = ""
                for d in days:
                    day_cards += nav_card(f"{d.name}/index.html", d.name, "Tag anzeigen")

                charts = ""
                for png in sort_pngs(m):
                    charts += chart_card(png)

                body = ""
                if day_cards:
                    body += f"<div class='section-title'>Tage</div><div class='grid'>{day_cards}</div>"
                if charts:
                    body += f"<div class='section-title' style='margin-top:32px;'>Monatsauswertung</div>{charts}"
                if not body:
                    body = empty("Für diesen Monat wurden noch keine Daten gefunden.")

                write(
                    m / "index.html",
                    f"{nice_name(s.name)} {y.name}/{m.name}",
                    body,
                    "../index.html",
                )

                for d in days:
                    charts = ""
                    for png in sort_pngs(d):
                        charts += chart_card(png)

                    if not charts:
                        charts = empty("Für diesen Tag wurden noch keine Diagramme gefunden.")

                    write(
                        d / "index.html",
                        f"{nice_name(s.name)} {y.name}/{m.name}/{d.name}",
                        charts,
                        "../index.html",
                    )

    print("✅ Dashboard erstellt!")


if __name__ == "__main__":
    build()
