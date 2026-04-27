import requests
from bs4 import BeautifulSoup

URL = "https://www.ai-fitness.de/studios/friedrichshafen-bodenseecenter"

headers = {
    "User-Agent": "Mozilla/5.0"
}

response = requests.get(URL, headers=headers, timeout=20)
response.raise_for_status()

html = response.text

print("Status:", response.status_code)
print("HTML-Länge:", len(html))

search_terms = [
    "Auslastung",
    "auslastung",
    "capacity",
    "occupancy",
    "busy",
    "besucht",
    "Besucher",
    "current",
]

print("\nGefundene Suchbegriffe:")
for term in search_terms:
    if term in html:
        print("-", term)

soup = BeautifulSoup(html, "html.parser")

print("\nSeitentitel:")
print(soup.title.string if soup.title else "Kein Titel gefunden")

with open("data/page_dump.html", "w", encoding="utf-8") as file:
    file.write(html)

print("\nHTML wurde gespeichert unter: data/page_dump.html")
