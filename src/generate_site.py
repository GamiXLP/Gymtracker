from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
STUDIOS_DIR = BASE_DIR / "studios"
DOCS_DIR = BASE_DIR / "docs"


def main() -> None:
    DOCS_DIR.mkdir(exist_ok=True)

    html = [
        "<!DOCTYPE html>",
        "<html lang='de'>",
        "<head>",
        "<meta charset='UTF-8'>",
        "<meta name='viewport' content='width=device-width, initial-scale=1.0'>",
        "<title>Gymtracker</title>",
        "<style>",
        "body { font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; color: #222; }",
        "h1 { margin-bottom: 10px; }",
        ".studio { background: white; padding: 24px; margin-bottom: 32px; border-radius: 12px; }",
        ".graph { margin: 24px 0; }",
        "img { max-width: 100%; border: 1px solid #ddd; border-radius: 8px; background: white; }",
        "a { color: #0066cc; }",
        "</style>",
        "</head>",
        "<body>",
        "<h1>Gymtracker</h1>",
        "<p>Automatisch generierte Studio-Auslastungsdiagramme.</p>",
    ]

    png_files = sorted(STUDIOS_DIR.glob("**/*.png"))

    if not png_files:
        html.append("<p>Keine Diagramme gefunden.</p>")

    current_studio = None

    for png in png_files:
        rel_path = png.relative_to(BASE_DIR)
        parts = rel_path.parts

        studio_slug = parts[1]

        if studio_slug != current_studio:
            current_studio = studio_slug
            html.append(f"<div class='studio'>")
            html.append(f"<h2>{studio_slug}</h2>")

        html.append("<div class='graph'>")
        html.append(f"<h3>{png.name}</h3>")
        html.append(f"<img src='../{rel_path.as_posix()}' alt='{png.name}'>")
        html.append("</div>")

    if current_studio is not None:
        html.append("</div>")

    html.extend([
        "</body>",
        "</html>",
    ])

    (DOCS_DIR / "index.html").write_text("\n".join(html), encoding="utf-8")
    print("Webseite erstellt: docs/index.html")


if __name__ == "__main__":
    main()
