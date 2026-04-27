import asyncio
import re
from datetime import datetime, time

from playwright.async_api import async_playwright

from db import insert_studio_load
from studios import STUDIOS


MAX_CONCURRENT = 5

OPENING_HOURS = {
    0: (time(6, 0), time(0, 0)),   # Montag
    1: (time(6, 0), time(0, 0)),   # Dienstag
    2: (time(6, 0), time(0, 0)),   # Mittwoch
    3: (time(6, 0), time(0, 0)),   # Donnerstag
    4: (time(7, 0), time(22, 0)),  # Freitag
    5: (time(7, 0), time(22, 0)),  # Samstag
    6: (time(7, 0), time(22, 0)),  # Sonntag
}


def is_currently_open(now: datetime) -> bool:
    start, end = OPENING_HOURS[now.weekday()]
    current = now.time()

    if end == time(0, 0):
        return current >= start

    return start <= current <= end


def extract_load_from_text(text: str) -> int | None:
    match = re.search(r"Aktuelle Auslastung.*?(\d{1,3})\s*%", text, re.DOTALL)

    if not match:
        match = re.search(r"(\d{1,3})\s*%", text)

    if not match:
        return None

    value = int(match.group(1))
    return value if 0 <= value <= 100 else None


async def fetch_one_studio(browser, studio: dict, timestamp: str, semaphore: asyncio.Semaphore):
    async with semaphore:
        slug = studio["slug"]
        name = studio["name"]
        url = studio["url"]

        page = await browser.new_page(user_agent="Mozilla/5.0")

        try:
            await page.goto(url, wait_until="domcontentloaded", timeout=45000)
            await page.wait_for_timeout(4000)

            text = await page.locator("body").inner_text(timeout=10000)
            load = extract_load_from_text(text)

            if load is not None:
                insert_studio_load(
                    studio_slug=slug,
                    timestamp=timestamp,
                    load_percent=load,
                )
                print(f"{slug}: {load}% gespeichert.")
                return True

            print(f"Keine Auslastung gefunden für {slug}.")
            return False

        except Exception as error:
            print(f"Fehler bei {name} ({slug}): {error}")
            return False

        finally:
            await page.close()


async def main_async() -> None:
    now = datetime.now()

    if not is_currently_open(now):
        print("Studio ist aktuell geschlossen. Es werden keine Daten gesammelt.")
        return

    timestamp = now.strftime("%Y-%m-%d %H:%M:%S")

    studios_to_fetch = [studio for studio in STUDIOS if studio["url"]]

    semaphore = asyncio.Semaphore(MAX_CONCURRENT)

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)

        tasks = [
            fetch_one_studio(browser, studio, timestamp, semaphore)
            for studio in studios_to_fetch
        ]

        results = await asyncio.gather(*tasks)

        await browser.close()

    saved_count = sum(1 for result in results if result)

    print("-" * 40)
    print(f"Fertig. Gespeichert: {saved_count}/{len(studios_to_fetch)}")


def main() -> None:
    asyncio.run(main_async())


if __name__ == "__main__":
    main()
