import re
from datetime import datetime

from playwright.sync_api import sync_playwright

from db import insert_studio_load
from studios import STUDIOS


def fetch_studio_load(page, url: str) -> int | None:
    page.goto(url, wait_until="networkidle", timeout=60000)
    page.wait_for_timeout(3000)

    text = page.locator("body").inner_text()

    match = re.search(r"Aktuelle Auslastung.*?(\d{1,3})\s*%", text, re.DOTALL)

    if not match:
        match = re.search(r"(\d{1,3})\s*%", text)

    if not match:
        return None

    value = int(match.group(1))

    if value < 0 or value > 100:
        return None

    return value


def main() -> None:
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(user_agent="Mozilla/5.0")

        for studio in STUDIOS:
            slug = studio["slug"]
            name = studio["name"]
            url = studio["url"]

            try:
                load = fetch_studio_load(page, url)

                print(f"Studio: {name}")
                print(f"Zeit: {timestamp}")
                print(f"Auslastung: {load}")

                if load is not None:
                    insert_studio_load(
                        studio_slug=slug,
                        timestamp=timestamp,
                        load_percent=load,
                    )
                    print("Gespeichert in SQLite.")
                else:
                    print("Nicht gespeichert, weil keine Auslastung gefunden wurde.")

                print("-" * 40)

            except Exception as error:
                print(f"Fehler bei {name}: {error}")
                print("-" * 40)

        browser.close()


if __name__ == "__main__":
    main()
