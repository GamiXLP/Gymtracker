import sqlite3
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "data" / "gymtracker.db"

STUDIO_SLUG = "ai-fitness-friedrichshafen"
OUTPUT_BASE = BASE_DIR / "output" / STUDIO_SLUG

WEEKDAY_NAMES = {
    0: "monday",
    1: "tuesday",
    2: "wednesday",
    3: "thursday",
    4: "friday",
    5: "saturday",
    6: "sunday",
}


def load_data() -> pd.DataFrame:
    with sqlite3.connect(DB_PATH) as conn:
        df = pd.read_sql_query(
            """
            SELECT timestamp, load_percent
            FROM studio_load
            WHERE studio_slug = ?
            ORDER BY timestamp
            """,
            conn,
            params=(STUDIO_SLUG,),
        )

    if df.empty:
        return df

    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["date"] = df["timestamp"].dt.date
    df["year"] = df["timestamp"].dt.year
    df["month"] = df["timestamp"].dt.month
    df["weekday"] = df["timestamp"].dt.weekday
    df["time"] = df["timestamp"].dt.strftime("%H:%M")

    return df


def create_month_graph(df: pd.DataFrame, year: int, month: int, output_dir: Path) -> None:
    month_df = df[(df["year"] == year) & (df["month"] == month)]

    if month_df.empty:
        return

    plt.figure(figsize=(14, 6))
    plt.plot(month_df["timestamp"], month_df["load_percent"], marker=".", linewidth=1)

    plt.title(f"Studioauslastung {year}-{month:02d}")
    plt.xlabel("Datum")
    plt.ylabel("Auslastung (%)")
    plt.ylim(0, 100)
    plt.grid(True)
    plt.tight_layout()

    output_file = output_dir / f"month_{year}-{month:02d}.png"
    plt.savefig(output_file)
    plt.close()


def create_weekday_graphs(df: pd.DataFrame, year: int, month: int, output_dir: Path) -> None:
    month_df = df[(df["year"] == year) & (df["month"] == month)]

    if month_df.empty:
        return

    for weekday_number, weekday_name in WEEKDAY_NAMES.items():
        weekday_df = month_df[month_df["weekday"] == weekday_number]

        if weekday_df.empty:
            continue

        avg_df = (
            weekday_df
            .groupby("time", as_index=False)["load_percent"]
            .mean()
            .sort_values("time")
        )

        plt.figure(figsize=(14, 6))
        plt.plot(avg_df["time"], avg_df["load_percent"], marker=".", linewidth=1)

        plt.title(f"Durchschnittliche Auslastung: {weekday_name.capitalize()} {year}-{month:02d}")
        plt.xlabel("Uhrzeit")
        plt.ylabel("Durchschnittliche Auslastung (%)")
        plt.ylim(0, 100)
        plt.grid(True)
        plt.xticks(rotation=45)
        plt.tight_layout()

        output_file = output_dir / f"weekday_{weekday_name}.png"
        plt.savefig(output_file)
        plt.close()


def main() -> None:
    df = load_data()

    if df.empty:
        print("Keine Daten vorhanden.")
        return

    latest = df["timestamp"].max()
    year = latest.year
    month = latest.month

    output_dir = OUTPUT_BASE / str(year) / f"{month:02d}"
    output_dir.mkdir(parents=True, exist_ok=True)

    create_month_graph(df, year, month, output_dir)
    create_weekday_graphs(df, year, month, output_dir)

    print(f"Graphen erstellt unter: {output_dir}")


if __name__ == "__main__":
    main()
