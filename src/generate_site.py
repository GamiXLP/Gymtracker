import shutil
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
SOURCE_STUDIOS_DIR = BASE_DIR / "studios"
DOCS_DIR = BASE_DIR / "docs"
PUBLIC_STUDIOS_DIR = DOCS_DIR / "studios"


def write_page(path: Path, title: str, items: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)

    html = f"""<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 40px;
            background: #f4f4f4;
            color: #111;
        }}
        .container {{
            background: white;
            padding: 28px;
            border-radius: 14px;
            max-width: 1200px;
            margin: auto;
        }}
        a {{
            color: #0057b8;
            text-decoration: none;
            font-weight: bold;
        }}
        a:hover {{
            text-decoration: underline;
        }}
        ul {{
            line-height: 2;
        }}
        img {{
            width: 100%;
            max-width: 1100px;
            border: 1px solid #ddd;
            border-radius: 10px;
            margin: 12px 0 32px 0;
            background: white;
        }}
        .back {{
            margin-bottom: 24px;
            display: inline-block;
        }}
    </style>
</head>
<body>
<div class="container">
<h1>{title}</h1>
{''.join(items)}
</div>
</body>
</html>
"""
    path.write_text(html, encoding="utf-8")


def relative_link(from_file: Path, to_file: Path) -> str:
    return to_file.relative_to(from_file.parent).as_posix()


def build_pages() -> None:
    if DOCS_DIR.exists():
        shutil.rmtree(DOCS_DIR)

    DOCS_DIR.mkdir(parents=True, exist_ok=True)

    if PUBLIC_STUDIOS_DIR.exists():
        shutil.rmtree(PUBLIC_STUDIOS_DIR)

    shutil.copytree(SOURCE_STUDIOS_DIR, PUBLIC_STUDIOS_DIR)

    # Startseite: Studios
    studio_dirs = sorted([p for p in PUBLIC_STUDIOS_DIR.iterdir() if p.is_dir()])

    index_items = [
        "<p>Automatisch generierte Studio-Auslastungsdiagramme.</p>",
        "<ul>",
    ]

    for studio_dir in studio_dirs:
        studio_index = studio_dir / "index.html"
        index_items.append(
            f"<li><a href='{relative_link(DOCS_DIR / 'index.html', studio_index)}'>{studio_dir.name}</a></li>"
        )

    index_items.append("</ul>")
    write_page(DOCS_DIR / "index.html", "Gymtracker", index_items)

    # Studio -> Jahre
    for studio_dir in studio_dirs:
        year_dirs = sorted([p for p in studio_dir.iterdir() if p.is_dir()])

        items = [
            "<a class='back' href='../../index.html'>← Zurück zu allen Studios</a>",
            "<ul>",
        ]

        for year_dir in year_dirs:
            year_index = year_dir / "index.html"
            items.append(
                f"<li><a href='{relative_link(studio_dir / 'index.html', year_index)}'>{year_dir.name}</a></li>"
            )

        items.append("</ul>")
        write_page(studio_dir / "index.html", studio_dir.name, items)

        # Jahr -> Monatsordner + Jahresdiagramme
        for year_dir in year_dirs:
            month_dirs = sorted([p for p in year_dir.iterdir() if p.is_dir()])
            png_files = sorted(year_dir.glob("*.png"))

            items = [
                "<a class='back' href='../index.html'>← Zurück zum Studio</a>",
                "<h2>Monate</h2>",
                "<ul>",
            ]

            for month_dir in month_dirs:
                month_index = month_dir / "index.html"
                items.append(
                    f"<li><a href='{relative_link(year_dir / 'index.html', month_index)}'>{month_dir.name}</a></li>"
                )

            items.append("</ul>")

            if png_files:
                items.append("<h2>Jahresdiagramme</h2>")
                for png in png_files:
                    items.append(f"<h3>{png.name}</h3>")
                    items.append(f"<img src='{png.name}' alt='{png.name}'>")

            write_page(year_dir / "index.html", f"{studio_dir.name} / {year_dir.name}", items)

            # Monat -> Tage + Monatsdiagramme
            for month_dir in month_dirs:
                day_dirs = sorted([p for p in month_dir.iterdir() if p.is_dir()])
                png_files = sorted(month_dir.glob("*.png"))

                items = [
                    "<a class='back' href='../index.html'>← Zurück zum Jahr</a>",
                    "<h2>Tage</h2>",
                    "<ul>",
                ]

                for day_dir in day_dirs:
                    day_index = day_dir / "index.html"
                    items.append(
                        f"<li><a href='{relative_link(month_dir / 'index.html', day_index)}'>{day_dir.name}</a></li>"
                    )

                items.append("</ul>")

                if png_files:
                    items.append("<h2>Monatsdiagramme</h2>")
                    for png in png_files:
                        items.append(f"<h3>{png.name}</h3>")
                        items.append(f"<img src='{png.name}' alt='{png.name}'>")

                write_page(
                    month_dir / "index.html",
                    f"{studio_dir.name} / {year_dir.name} / {month_dir.name}",
                    items,
                )

                # Tag -> Tagesdiagramm + CSV
                for day_dir in day_dirs:
                    png_files = sorted(day_dir.glob("*.png"))
                    csv_files = sorted(day_dir.glob("*.csv"))

                    items = [
                        "<a class='back' href='../index.html'>← Zurück zum Monat</a>",
                    ]

                    for png in png_files:
                        items.append(f"<h2>{png.name}</h2>")
                        items.append(f"<img src='{png.name}' alt='{png.name}'>")

                    if csv_files:
                        items.append("<h2>Tabellen</h2>")
                        items.append("<ul>")
                        for csv in csv_files:
                            items.append(f"<li><a href='{csv.name}'>{csv.name}</a></li>")
                        items.append("</ul>")

                    write_page(
                        day_dir / "index.html",
                        f"{studio_dir.name} / {year_dir.name} / {month_dir.name} / {day_dir.name}",
                        items,
                    )


def main() -> None:
    build_pages()
    print("Webseite erstellt unter docs/")


if __name__ == "__main__":
    main()
