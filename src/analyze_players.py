import pandas as pd

# Load cleaned player data
df = pd.read_csv("data/processed/nba_players_clean.csv")


# -----------------------------------
# Top 10 scorers
# -----------------------------------

top_scorers = df.sort_values(
    by="Points_Per_Game",
    ascending=False
).head(10)

print("\nTop 10 NBA Scorers - 2024-25")
print(
    top_scorers[
        [
            "Player",
            "Team",
            "Position",
            "Games",
            "Points_Per_Game"
        ]
    ].to_string(index=False)
)


# -----------------------------------
# Top 10 rebounders
# -----------------------------------

top_rebounders = df.sort_values(
    by="Rebounds_Per_Game",
    ascending=False
).head(10)

print("\nTop 10 NBA Rebounders - 2024-25")
print(
    top_rebounders[
        [
            "Player",
            "Team",
            "Position",
            "Games",
            "Rebounds_Per_Game"
        ]
    ].to_string(index=False)
)


# -----------------------------------
# Top 10 assist leaders
# -----------------------------------

top_assists = df.sort_values(
    by="Assists_Per_Game",
    ascending=False
).head(10)

print("\nTop 10 NBA Assist Leaders - 2024-25")
print(
    top_assists[
        [
            "Player",
            "Team",
            "Position",
            "Games",
            "Assists_Per_Game"
        ]
    ].to_string(index=False)
)

# -----------------------------------
# Visualize Top 10 scorers
# -----------------------------------

import matplotlib.pyplot as plt

# Reverse the order so the highest scorer appears at the top
scorers_chart = top_scorers.sort_values(
    by="Points_Per_Game",
    ascending=True
)

plt.figure(figsize=(10, 6))

plt.barh(
    scorers_chart["Player"],
    scorers_chart["Points_Per_Game"]
)

plt.xlabel("Points Per Game")
plt.ylabel("Player")
plt.title("Top 10 NBA Scorers - 2024-25 Season")

plt.tight_layout()

# Save the chart for the GitHub project
plt.savefig(
    "screenshots/top_10_scorers.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()

# -----------------------------------
# Average points per game by position
# -----------------------------------

position_scoring = (
    df.groupby("Position")["Points_Per_Game"]
    .mean()
    .sort_values(ascending=False)
)

print("\nAverage Points Per Game by Position")
print(position_scoring.round(2))

plt.figure(figsize=(8, 5))

plt.bar(
    position_scoring.index,
    position_scoring.values
)

plt.xlabel("Position")
plt.ylabel("Average Points Per Game")
plt.title("Average NBA Scoring by Position - 2024-25")

plt.tight_layout()

plt.savefig(
    "screenshots/scoring_by_position.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()

# -----------------------------------
# Minutes played vs points per game
# -----------------------------------

plt.figure(figsize=(9, 6))

plt.scatter(
    df["Minutes_Per_Game"],
    df["Points_Per_Game"],
    alpha=0.6
)

plt.xlabel("Minutes Per Game")
plt.ylabel("Points Per Game")
plt.title("Minutes Played vs Scoring - 2024-25 NBA Season")

plt.tight_layout()

plt.savefig(
    "screenshots/minutes_vs_scoring.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()