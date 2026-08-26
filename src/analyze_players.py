from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

# -----------------------------------
# Project paths
# -----------------------------------

# Build every path from the location of this file instead of the folder
# the script happens to be run from, so the project works from any
# working directory.
PROJECT_ROOT = Path(__file__).resolve().parent.parent
CLEAN_DATA_FILE = PROJECT_ROOT / "data" / "processed" / "nba_players_clean.csv"
SCREENSHOTS_DIR = PROJECT_ROOT / "screenshots"

# -----------------------------------
# Analysis settings
# -----------------------------------

SEASON = "2024-25"

# Minimum games played for a player to appear in the analysis below.
# 58 games is roughly 70% of the 82-game season.
# Per-game averages from a handful of games are unreliable: a player who
# scored well in 5 games can outrank a star who played all season.
# The full cleaned dataset still keeps every player - this filter is only
# applied to the leaderboards and charts.
MIN_GAMES = 58


def show_top_10(df, stat_column, title):
    """Print the 10 players with the highest value in stat_column.

    Returns the top 10 rows so they can also be used in a chart.
    """
    top_10 = df.sort_values(by=stat_column, ascending=False).head(10)

    print(f"\n{title}")
    print(
        top_10[
            [
                "Player",
                "Team",
                "Position",
                "Games",
                stat_column
            ]
        ].to_string(index=False)
    )

    return top_10


def main():
    # Create the screenshots folder if it does not exist yet
    SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)

    # Load cleaned player data
    df = pd.read_csv(CLEAN_DATA_FILE)

    # Keep the full cleaned dataset in df, and build a separate filtered
    # dataframe for the leaderboards and charts.
    qualified = df[df["Games"] >= MIN_GAMES]

    print(f"All players in cleaned dataset: {len(df)}")
    print(f"Players with at least {MIN_GAMES} games: {len(qualified)}")

    # -----------------------------------
    # Top 10 leaderboards
    # -----------------------------------

    top_scorers = show_top_10(
        qualified,
        "Points_Per_Game",
        f"Top 10 NBA Scorers - {SEASON} (min {MIN_GAMES} games)"
    )

    show_top_10(
        qualified,
        "Rebounds_Per_Game",
        f"Top 10 NBA Rebounders - {SEASON} (min {MIN_GAMES} games)"
    )

    show_top_10(
        qualified,
        "Assists_Per_Game",
        f"Top 10 NBA Assist Leaders - {SEASON} (min {MIN_GAMES} games)"
    )

    # -----------------------------------
    # Visualize Top 10 scorers
    # -----------------------------------

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
    plt.title(f"Top 10 NBA Scorers - {SEASON} Season (min {MIN_GAMES} games)")

    plt.tight_layout()

    # Save the chart for the GitHub project
    plt.savefig(
        SCREENSHOTS_DIR / "top_10_scorers.png",
        dpi=300,
        bbox_inches="tight"
    )
    plt.close()

    # -----------------------------------
    # Average points per game by position
    # -----------------------------------

    position_scoring = (
        qualified.groupby("Position")["Points_Per_Game"]
        .mean()
        .sort_values(ascending=False)
    )

    print(f"\nAverage Points Per Game by Position (min {MIN_GAMES} games)")
    print(position_scoring.round(2))

    plt.figure(figsize=(8, 5))

    plt.bar(
        position_scoring.index,
        position_scoring.values
    )

    plt.xlabel("Position")
    plt.ylabel("Average Points Per Game")
    plt.title(
        f"Average NBA Scoring by Position - {SEASON} (min {MIN_GAMES} games)"
    )

    plt.tight_layout()

    plt.savefig(
        SCREENSHOTS_DIR / "scoring_by_position.png",
        dpi=300,
        bbox_inches="tight"
    )
    plt.close()

    # -----------------------------------
    # Minutes played vs points per game
    # -----------------------------------

    # Correlation is a number between -1 and 1 that describes how closely
    # two columns move together. A value near 1 means players who play
    # more minutes almost always score more points.
    correlation = qualified["Minutes_Per_Game"].corr(
        qualified["Points_Per_Game"]
    )

    print(
        f"\nCorrelation between Minutes_Per_Game and Points_Per_Game "
        f"(min {MIN_GAMES} games): {correlation:.3f}"
    )

    plt.figure(figsize=(9, 6))

    plt.scatter(
        qualified["Minutes_Per_Game"],
        qualified["Points_Per_Game"],
        alpha=0.6
    )

    plt.xlabel("Minutes Per Game")
    plt.ylabel("Points Per Game")
    plt.title(
        f"Minutes Played vs Scoring - {SEASON} NBA Season "
        f"(min {MIN_GAMES} games, r = {correlation:.2f})"
    )

    plt.tight_layout()

    plt.savefig(
        SCREENSHOTS_DIR / "minutes_vs_scoring.png",
        dpi=300,
        bbox_inches="tight"
    )
    plt.close()

    print("\nCharts saved to the screenshots folder.")


if __name__ == "__main__":
    main()
