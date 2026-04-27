import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "data" / "gymtracker.db"


def init_db() -> None:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS studio_load (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                studio_slug TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                load_percent INTEGER NOT NULL
            )
        """)


def insert_studio_load(studio_slug: str, timestamp: str, load_percent: int) -> None:
    init_db()

    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            INSERT INTO studio_load (studio_slug, timestamp, load_percent)
            VALUES (?, ?, ?)
        """, (studio_slug, timestamp, load_percent))
