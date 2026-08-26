import sqlite3
from pathlib import Path

import pandas as pd

# -----------------------------------
# Project paths
# -----------------------------------

# Build every path from the location of this file instead of the folder
# the script happens to be run from, so the project works from any
# working directory.
PROJECT_ROOT = Path(__file__).resolve().parent.parent
CLEAN_DATA_FILE = PROJECT_ROOT / "data" / "processed" / "nba_players_clean.csv"
DATABASE_FILE = PROJECT_ROOT / "data" / "nba_stats.db"


def main():
    # Load cleaned NBA data
    df = pd.read_csv(CLEAN_DATA_FILE)

    # Create SQLite database
    connection = sqlite3.connect(DATABASE_FILE)

    # Add the dataframe as a SQL table
    # Missing shooting percentages stay as NULL in SQL for the same reason
    # they stay as NaN in pandas: the player never attempted that shot, so
    # SQL's AVG() should skip them rather than treat them as 0%.
    df.to_sql(
        "players",
        connection,
        if_exists="replace",
        index=False
    )

    connection.close()

    print("NBA database created successfully.")


if __name__ == "__main__":
    main()
