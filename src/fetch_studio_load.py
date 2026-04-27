import re
from db import insert_studio_load
from datetime import datetime
from playwright.sync_api import sync_playwright

URL = "https://www.ai-fitness.de/studios/friedrichshafen-bodenseecenter"


def fetch_studio_load() -> int | None:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(
            user_agent="Mozilla/5.0"
        )

        page.goto(URL, wait_until="networkidle", timeout=60000)

        # Kurz warten, damit das Widget sicher fertig rendert
        page.wait_for_timeout(3000)

        text = page.locator("body").inner_text()

        browser.close()

    # Erst gezielt nach Auslastungsbereich suchen
    match = re.search(r"Aktuelle Auslastung.*?(\d{1,3})\s*%", text, re.DOTALL)

    if not match:
        # Fallback: irgendeinen Prozentwert suchen
        match = re.search(r"(\d{1,3})\s*%", text)

    if not match:
        return None

    value = int(match.group(1))

    if value < 0 or value > 100:
        return None

    return value


if __name__ == "__main__":
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    load = fetch_studio_load()

    print("Zeit:", timestamp)
    print("Auslastung:", load)

    if load is not None:
        insert_studio_load(
            studio_slug="ai-fitness-friedrichshafen",
            timestamp=timestamp,
            load_percent=load,
        )
        print("Gespeichert in SQLite.")
    else:
        print("Nicht gespeichert, weil keine Auslastung gefunden wurde.")
