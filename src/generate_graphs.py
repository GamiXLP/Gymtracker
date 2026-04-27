import sqlite3
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "data" / "gymtracker.db"

STUDIO_SLUG = "ai-fitness-friedrichshafen"
OUTPUT_BASE = BASE_DIR / "studios" / STUDIO_SLUG

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


def save_line_graph(
    x,
    y,
    title: str,
    xlabel: str,
    ylabel: str,
    output_file: Path,
    rotate_x: bool = False,
) -> None:
    output_file.parent.mkdir(parents=True, exist_ok=True)

    plt.figure(figsize=(14, 6))
    plt.plot(x, y, marker=".", linewidth=1)

    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.ylim(0, 100)
    plt.grid(True)

    if rotate_x:
        plt.xticks(rotation=45)

    plt.tight_layout()
    plt.savefig(output_file)
    plt.close()


def create_daily_graphs(df: pd.DataFrame, year: int, month: int) -> None:
    month_df = df[(df["year"] == year) & (df["month"] == month)]

    if month_df.empty:
        return

    for date, day_df in month_df.groupby("date"):
        day_df = day_df.sort_values("timestamp")

        day_str = str(date.day).zfill(2)
        output_dir = OUTPUT_BASE / str(year) / f"{month:02d}" / day_str

        output_file = output_dir / f"day_{date}.png"

        save_line_graph(
            x=day_df["time"],
            y=day_df["load_percent"],
            title=f"Tagesverlauf {date}",
            xlabel="Uhrzeit",
            ylabel="Auslastung (%)",
            output_file=output_file,
            rotate_x=True,
        )

def create_daily_csv_files(df: pd.DataFrame, year: int, month: int) -> None:
    month_df = df[(df["year"] == year) & (df["month"] == month)]

    if month_df.empty:
        return

    for date, day_df in month_df.groupby("date"):
        day_df = day_df.sort_values("timestamp")

        day_str = str(date.day).zfill(2)
        output_dir = OUTPUT_BASE / str(year) / f"{month:02d}" / day_str
        output_dir.mkdir(parents=True, exist_ok=True)

        export_df = day_df[["timestamp", "load_percent"]].copy()
        export_df["timestamp"] = export_df["timestamp"].dt.strftime("%Y-%m-%d %H:%M:%S")

        output_file = output_dir / f"day_{date}.csv"
        export_df.to_csv(output_file, index=False)

def create_monthly_weekday_average_graphs(df: pd.DataFrame, year: int, month: int) -> None:
    month_df = df[(df["year"] == year) & (df["month"] == month)]

    if month_df.empty:
        return

    output_dir = OUTPUT_BASE / str(year) / f"{month:02d}"

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

        output_file = output_dir / f"weekday_{weekday_name}_{year}-{month:02d}.png"

        save_line_graph(
            x=avg_df["time"],
            y=avg_df["load_percent"],
            title=f"Durchschnitt aller {weekday_name.capitalize()}e im {year}-{month:02d}",
            xlabel="Uhrzeit",
            ylabel="Durchschnittliche Auslastung (%)",
            output_file=output_file,
            rotate_x=True,
        )


def create_yearly_weekday_average_graphs(df: pd.DataFrame, year: int) -> None:
    year_df = df[df["year"] == year]

    if year_df.empty:
        return

    output_dir = OUTPUT_BASE / str(year)

    for weekday_number, weekday_name in WEEKDAY_NAMES.items():
        weekday_df = year_df[year_df["weekday"] == weekday_number]

        if weekday_df.empty:
            continue

        avg_df = (
            weekday_df
            .groupby("time", as_index=False)["load_percent"]
            .mean()
            .sort_values("time")
        )

        output_file = output_dir / f"weekday_{weekday_name}_{year}.png"

        save_line_graph(
            x=avg_df["time"],
            y=avg_df["load_percent"],
            title=f"Durchschnitt aller {weekday_name.capitalize()}e im Jahr {year}",
            xlabel="Uhrzeit",
            ylabel="Durchschnittliche Auslastung (%)",
            output_file=output_file,
            rotate_x=True,
        )


def main() -> None:
    df = load_data()

    if df.empty:
        print("Keine Daten vorhanden.")
        return

    latest = df["timestamp"].max()
    year = latest.year
    month = latest.month

    create_daily_graphs(df, year, month)
    create_daily_csv_files(df, year, month)
    create_monthly_weekday_average_graphs(df, year, month)
    create_yearly_weekday_average_graphs(df, year)

    print("Graphen wurden erstellt.")


if __name__ == "__main__":
    main()
