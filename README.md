# NBA Player Performance Analytics (2024-25 Season)

An end-to-end data analysis project using **Python (pandas, matplotlib)** and **SQL (SQLite)**.
It takes a raw NBA player statistics file, cleans it into one row per player, loads it into a
SQL database, and answers questions about scoring, rebounding, and playmaking.

---

## The Dataset

| | |
|---|---|
| **Source** | Basketball Reference — 2024-25 NBA regular season per-game player stats |
| **Raw file** | `data/raw/nba_player_stats_raw.csv` |
| **Raw size** | 735 rows × 30 columns |
| **After cleaning** | 569 rows (one per player) |

Every statistic in this dataset is a **per-game average**, not a season total. For example,
`PTS` is points *per game*. This is why the cleaning step renames the columns to names like
`Points_Per_Game` — it makes the numbers impossible to misread later.

---

## Cleaning Process

The raw file has more rows (735) than players (569). The difference comes from **players who
were traded mid-season**. Basketball Reference gives a traded player several rows:

- one combined row for the whole season, with the team listed as `2TM` (two teams) or `3TM`
- one row for each individual team they played on

For example, Luka Doncic has a `2TM` row for his full season plus separate rows for Dallas
and the Lakers. If you don't handle this, he gets counted three times, and his "season" is
whichever partial row happens to come first.

**The approach used here (`src/clean_data.py`):**

1. Flag every row whose team code looks like `2TM` or `3TM` using a regular expression.
2. Sort so those combined rows come first within each player.
3. Use `drop_duplicates(subset="Player", keep="first")` to keep exactly one row per player.

Because the combined rows were sorted first, each traded player keeps their **full-season**
line rather than a partial one. This takes 735 rows down to 569 — one per player.

4. Rename all 30 columns from abbreviations to readable names (`PTS` → `Points_Per_Game`).
5. Save the result to `data/processed/nba_players_clean.csv`.

The raw file is never modified. All cleaning happens on a copy.

### Why missing shooting percentages stay empty

Five columns have blanks in the raw data:

| Column | Blank rows |
|---|---|
| `3P%` (three-point %) | 45 |
| `FT%` (free throw %) | 42 |
| `2P%` (two-point %) | 11 |
| `FG%` (field goal %) | 4 |
| `eFG%` (effective FG %) | 4 |

A blank here means **the player never attempted that type of shot**, so the percentage is
*undefined* — not zero. Filling them with `0` would claim the player shot and missed every
single time, which would pull down any average calculated on that column.

Leaving them as `NaN` in pandas (and `NULL` in SQL) is the correct choice, because both tools
automatically **skip** missing values when averaging. In the database, `AVG(Three_Point_Percentage)`
correctly averages the 541 players who actually took a three, ignoring the 28 who never did.

### One known trade-off

Because traded players keep their combined row, their team is literally recorded as `"2TM"`.
That means they are **excluded from team-level analysis** (see query 8 in `sql/nba_analysis.sql`).
This is a deliberate trade-off: it keeps every player's season stats complete and accurate at
the cost of leaving traded players out of per-team averages.

---

## The 58-Game Filter

An NBA regular season is 82 games. In the cleaned dataset, **113 of 569 players appeared in
fewer than 20 games**, and 61 played fewer than 10.

Per-game averages from a tiny sample are unreliable. A player who scores well in 5 games can
outrank a star who played all season, even though there isn't enough evidence to say they're
actually better.

So `src/analyze_players.py` defines one constant:

```python
MIN_GAMES = 58   # roughly 70% of an 82-game season
```

This filter is applied to the **leaderboards, the position analysis, and the scatter plot**.
It reduces the pool from 569 players to **231 qualified players**. The full cleaned dataset and
the SQL database still contain all 569 players — nobody is deleted, they're just not ranked.

**This filter genuinely changed the results**, which is why it's worth calling out:

- *Top 10 rebounders:* Victor Wembanyama (46 games) and Isaiah Hartenstein (57) drop out;
  Alperen Sengun, Jalen Duren, and Nikola Vucevic take their places.
- *Top 10 assists:* Dejounte Murray, who played only **31 games**, drops out.
- *Scoring by position:* the ranking itself flipped. Unfiltered, power forwards ranked 2nd.
  With the filter, they fall to 4th and shooting guards move up to 2nd.

The unfiltered chart was partly measuring *"which position has more bench players"* rather
than *"which position scores most."* The filter fixes that.

---

## Python Analysis (`src/analyze_players.py`)

Produces three leaderboards and three charts, all using qualified players only:

- **Top 10 scorers**, rebounders, and assist leaders — all three use a single reusable
  function, `show_top_10(df, stat_column, title)`, instead of three copies of the same code.
- **Average points per game by position** — grouped with `groupby()`.
- **Minutes played vs points scored** — a scatter plot, plus the correlation between the two.

### Correlation finding

The correlation between `Minutes_Per_Game` and `Points_Per_Game` among qualified players is
**r = 0.837**.

Correlation runs from -1 to 1, and a value this close to 1 means the two move together very
closely: playing time explains most of the difference in scoring. Put simply, **most of what
separates a 25-point scorer from a 6-point scorer is how long the coach leaves them on the
floor.** This is a good argument for looking at *per-minute* efficiency stats if you want to
find genuinely underused players.

---

## SQL Analysis (`sql/nba_analysis.sql`)

`src/create_database.py` loads the cleaned CSV into a SQLite table called `players`
(569 rows, 30 columns) at `data/nba_stats.db`. The query file covers:

| # | Query | Concept demonstrated |
|---|---|---|
| 1 | Preview the first 10 players | `SELECT`, `LIMIT` |
| 2-4 | Top 10 scorers / rebounders / assist leaders | `ORDER BY`, `LIMIT` |
| 5 | Average scoring by position | `GROUP BY`, `AVG`, `ROUND` |
| 6 | Players averaging 20+ points | `WHERE` |
| 7 | Players with 20+ points **and** 5+ assists | `WHERE` with `AND` |
| 8 | Average player scoring by team | `GROUP BY` with a filter to exclude `2TM`/`3TM` |

Sample results: **50 players** averaged 20+ points per game, and **26 players** managed both
20+ points and 5+ assists — the two-way offensive threats.

Note that the SQL queries run against all 569 players, so they are not filtered by `MIN_GAMES`.

---

## Key Findings

1. **Shai Gilgeous-Alexander led the league in scoring** at 32.7 points per game, ahead of
   Giannis Antetokounmpo (30.4) and Nikola Jokic (29.6).
2. **Nikola Jokic appears in the top 10 for scoring, rebounding, and assists** — the only
   player to do so, and a clear statistical case for his MVP-level season.
3. **Point guards score the most on average** (14.1 PPG), and centers the least (11.2 PPG)
   among qualified players.
4. **Playing time drives scoring** (r = 0.837). Minutes explain most of the variation in
   points per game.
5. **26 players averaged both 20+ points and 5+ assists**, showing how many modern guards and
   forwards carry a dual scoring-and-playmaking role.

---

## How to Run

**Requirements:** Python 3.8 or newer.

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Clean the raw data  ->  data/processed/nba_players_clean.csv
python src/clean_data.py

# 3. Build the SQL database  ->  data/nba_stats.db
python src/create_database.py

# 4. Run the analysis and generate charts  ->  screenshots/
python src/analyze_players.py
```

Run the scripts **in that order** — each one uses the output of the previous step.

All file paths are built relative to the project folder, so the scripts work no matter which
directory you run them from. The `data/processed/` and `screenshots/` folders are created
automatically if they don't exist.

To explore the database directly:

```bash
sqlite3 data/nba_stats.db
sqlite> SELECT Player, Points_Per_Game FROM players ORDER BY Points_Per_Game DESC LIMIT 10;
```

---

## Project Structure

```
nba-performance-analytics/
├── data/
│   ├── raw/
│   │   └── nba_player_stats_raw.csv     # Original data, never modified
│   ├── processed/                       # Created by clean_data.py (not in git)
│   │   └── nba_players_clean.csv        # One row per player, readable columns
│   └── nba_stats.db                     # SQLite database, built from the clean CSV
├── src/
│   ├── clean_data.py                    # Step 1: clean and de-duplicate
│   ├── create_database.py               # Step 2: load into SQLite
│   └── analyze_players.py               # Step 3: analysis and charts
├── sql/
│   └── nba_analysis.sql                 # 8 analysis queries
├── screenshots/                         # Charts saved by analyze_players.py
│   ├── top_10_scorers.png
│   ├── scoring_by_position.png
│   └── minutes_vs_scoring.png
├── requirements.txt
└── README.md
```

---

## Charts

| Chart | What it shows |
|---|---|
| `screenshots/top_10_scorers.png` | Horizontal bar chart of the 10 highest scorers |
| `screenshots/scoring_by_position.png` | Average points per game for each of the 5 positions |
| `screenshots/minutes_vs_scoring.png` | Scatter plot of minutes vs points, with correlation |
