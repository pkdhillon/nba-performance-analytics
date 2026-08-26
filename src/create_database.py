import pandas as pd
import sqlite3

# Load cleaned NBA data
df = pd.read_csv("data/processed/nba_players_clean.csv")

# Create SQLite database
connection = sqlite3.connect("data/nba_stats.db")

# Add the dataframe as a SQL table
df.to_sql(
    "players",
    connection,
    if_exists="replace",
    index=False
)

connection.close()

print("NBA database created successfully.")