import pandas as pd

# -----------------------------------
# Load raw NBA player dataset
# -----------------------------------

df = pd.read_csv("data/raw/nba_player_stats_raw.csv")

print("Dataset shape:", df.shape)

print("\nMissing values by column:")
print(df.isnull().sum())

print("\nDuplicate rows:")
print(df.duplicated().sum())

print("\nUnique players:")
print(df["Player"].nunique())


# -----------------------------------
# Inspect players with multiple rows
# -----------------------------------

player_counts = df["Player"].value_counts()

print("\nPlayers appearing more than once:")
print(player_counts[player_counts > 1].head(20))


# Identify combined multi-team rows such as 2TM or 3TM
multi_team_rows = df[df["Team"].str.match(r"\d+TM")]

print("\nMulti-team player rows:")
print(
    multi_team_rows[
        ["Player", "Team", "G", "PTS"]
    ].head(20)
)


# -----------------------------------
# Create player-level analysis dataset
# -----------------------------------

# Make a copy so the raw dataframe remains unchanged
player_df = df.copy()

# Mark rows that represent combined statistics
# for players who played on multiple teams
player_df["MultiTeam"] = player_df["Team"].str.match(r"\d+TM")

# Sort so combined 2TM / 3TM rows appear first
player_df = player_df.sort_values(
    by=["Player", "MultiTeam"],
    ascending=[True, False]
)

# Keep one row per player
# For traded players, this keeps the combined multi-team row
player_df = player_df.drop_duplicates(
    subset="Player",
    keep="first"
)

# Remove helper column
player_df = player_df.drop(columns=["MultiTeam"])


# -----------------------------------
# Rename columns for easier analysis
# -----------------------------------

player_df = player_df.rename(columns={
    "Rk": "Rank",
    "Player": "Player",
    "Age": "Age",
    "Team": "Team",
    "Pos": "Position",
    "G": "Games",
    "GS": "Games_Started",
    "MP": "Minutes_Per_Game",
    "FG": "Field_Goals_Per_Game",
    "FGA": "Field_Goal_Attempts_Per_Game",
    "FG%": "Field_Goal_Percentage",
    "3P": "Three_Pointers_Per_Game",
    "3PA": "Three_Point_Attempts_Per_Game",
    "3P%": "Three_Point_Percentage",
    "2P": "Two_Pointers_Per_Game",
    "2PA": "Two_Point_Attempts_Per_Game",
    "2P%": "Two_Point_Percentage",
    "eFG%": "Effective_Field_Goal_Percentage",
    "FT": "Free_Throws_Per_Game",
    "FTA": "Free_Throw_Attempts_Per_Game",
    "FT%": "Free_Throw_Percentage",
    "ORB": "Offensive_Rebounds_Per_Game",
    "DRB": "Defensive_Rebounds_Per_Game",
    "TRB": "Rebounds_Per_Game",
    "AST": "Assists_Per_Game",
    "STL": "Steals_Per_Game",
    "BLK": "Blocks_Per_Game",
    "TOV": "Turnovers_Per_Game",
    "PF": "Personal_Fouls_Per_Game",
    "PTS": "Points_Per_Game"
})


# -----------------------------------
# Check cleaned results
# -----------------------------------

print("\nClean player dataset shape:")
print(player_df.shape)

print("\nUnique players after cleaning:")
print(player_df["Player"].nunique())

print("\nLuka Doncic after cleaning:")
print(
    player_df[player_df["Player"] == "Luka Doncic"][
        [
            "Player",
            "Team",
            "Games",
            "Points_Per_Game",
            "Assists_Per_Game",
            "Rebounds_Per_Game"
        ]
    ]
)

print("\nCleaned columns:")
print(player_df.columns.tolist())

print("\nFirst 5 cleaned rows:")
print(player_df.head())


# -----------------------------------
# Save cleaned dataset
# -----------------------------------

player_df.to_csv(
    "data/processed/nba_players_clean.csv",
    index=False
)

print("\nClean player dataset saved successfully.")