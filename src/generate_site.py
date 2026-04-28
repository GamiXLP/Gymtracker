import os
from pathlib import Path

BASE_DIR = Path("docs")
DATA_DIR = Path("studios")


def write_page(path, title, content):
    path.parent.mkdir(parents=True, exist_ok=True)

    html = f"""
<!DOCTYPE html>
<html lang="de">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>

<style>
body {{
    font-family: 'Segoe UI', Arial, sans-serif;
    margin: 0;
    background: #0f0f0f;
    color: #f1f1f1;
}}

.container {{
    max-width: 1200px;
    margin: auto;
    padding: 30px;
}}

h1 {{
    font-size: 32px;
    margin-bottom: 20px;
}}

h2 {{
    margin-top: 30px;
    color: #e30613;
}}

a {{
    color: #e30613;
    text-decoration: none;
    font-weight: 500;
}}

a:hover {{
    text-decoration: underline;
}}

.back {{
    display: inline-block;
    margin-bottom: 20px;
    background: #e30613;
    color: white;
    padding: 8px 14px;
    border-radius: 8px;
    font-size: 14px;
}}

.back:hover {{
    background: #ff1f2f;
}}

.grid {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 15px;
}}

.card {{
    background: #1a1a1a;
    padding: 20px;
    border-radius: 14px;
    box-shadow: 0 0 20px rgba(0,0,0,0.4);
    transition: 0.2s;
}}

.card:hover {{
    transform: translateY(-4px);
    box-shadow: 0 0 30px rgba(227,6,19,0.2);
}}

img {{
    width: 100%;
    max-width: 1000px;
    border-radius: 12px;
    margin-top: 10px;
    border: 1px solid #333;
}}

.header {{
    background: linear-gradient(90deg, #e30613, #7a0000);
    padding: 25px;
    border-radius: 16px;
    margin-bottom: 30px;
}}
</style>
</head>

<body>
<div class="container">

<div class="header">
    <h1>🏋️ Gymtracker</h1>
    <p>Live Studio-Auslastung</p>
</div>

{content}

</div>
</body>
</html>
"""
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)


def generate():
    if not DATA_DIR.exists():
        print("Kein data/plots Ordner gefunden")
        return

    # -------- ROOT PAGE --------
    studios = sorted([d for d in DATA_DIR.iterdir() if d.is_dir()])

    items = []
    for studio in studios:
        link = f"{studio.name}/index.html"
        items.append(f"""
        <div class="card">
            <a href="{link}">{studio.name}</a>
        </div>
        """)

    write_page(
        BASE_DIR / "index.html",
        "Gymtracker",
        "<h2>Studios</h2><div class='grid'>" + "".join(items) + "</div>"
    )

    # -------- STUDIO PAGES --------
    for studio in studios:
        years = sorted([d for d in studio.iterdir() if d.is_dir()])

        items = []
        for year in years:
            link = f"{year.name}/index.html"
            items.append(f"""
            <div class="card">
                <a href="{link}">{year.name}</a>
            </div>
            """)

        write_page(
            BASE_DIR / studio.name / "index.html",
            studio.name,
            f"<a class='back' href='../index.html'>← Zurück</a>"
            f"<h2>{studio.name}</h2>"
            f"<div class='grid'>{''.join(items)}</div>"
        )

        # -------- YEAR --------
        for year in years:
            months = sorted([d for d in year.iterdir() if d.is_dir()])

            items = []
            for month in months:
                link = f"{month.name}/index.html"
                items.append(f"""
                <div class="card">
                    <a href="{link}">{month.name}</a>
                </div>
                """)

            write_page(
                BASE_DIR / studio.name / year.name / "index.html",
                year.name,
                f"<a class='back' href='../index.html'>← Zurück</a>"
                f"<h2>{studio.name} / {year.name}</h2>"
                f"<div class='grid'>{''.join(items)}</div>"
            )

            # -------- MONTH --------
            for month in months:
                files = list(month.glob("*.png"))

                days = []
                weekday = []

                for f in files:
                    if f.name.startswith("day_"):
                        days.append(f)
                    else:
                        weekday.append(f)

                day_links = []
                for d in sorted(days):
                    day_name = d.name.replace("day_", "").replace(".png", "")
                    link = f"{day_name}.html"

                    day_links.append(f"""
                    <div class="card">
                        <a href="{link}">{day_name}</a>
                    </div>
                    """)

                # Monatsdiagramme anzeigen
                weekday_html = []
                for w in sorted(weekday):
                    weekday_html.append(f"""
                    <div class="card">
                        <h3>{w.name}</h3>
                        <img src="{w.name}">
                    </div>
                    """)

                write_page(
                    BASE_DIR / studio.name / year.name / month.name / "index.html",
                    month.name,
                    f"<a class='back' href='../index.html'>← Zurück</a>"
                    f"<h2>{studio.name} / {year.name} / {month.name}</h2>"
                    f"<h2>Tage</h2>"
                    f"<div class='grid'>{''.join(day_links)}</div>"
                    f"<h2>Monatsdiagramme</h2>"
                    f"{''.join(weekday_html)}"
                )

                # -------- DAY --------
                for d in days:
                    day_name = d.name.replace("day_", "").replace(".png", "")

                    write_page(
                        BASE_DIR / studio.name / year.name / month.name / f"{day_name}.html",
                        day_name,
                        f"<a class='back' href='index.html'>← Zurück</a>"
                        f"<h2>{studio.name} / {year.name} / {month.name} / {day_name}</h2>"
                        f"<div class='card'>"
                        f"<img src='{d.name}'>"
                        f"</div>"
                    )


if __name__ == "__main__":
    generate()
