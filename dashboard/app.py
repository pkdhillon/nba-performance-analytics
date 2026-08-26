from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st


# -----------------------------------
# File paths
# -----------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_PATH = PROJECT_ROOT / "data" / "processed" / "nba_players_clean.csv"


# -----------------------------------
# Constants
# -----------------------------------

MIN_GAMES = 58
SEASON = "2024-25"


# -----------------------------------
# Page setup
# -----------------------------------

st.set_page_config(
    page_title="NBA Player Performance Dashboard",
    page_icon="🏀",
    layout="wide"
)

st.markdown(
    """
    <style>
        .block-container {
            padding-top: 1.5rem;
            padding-bottom: 2rem;
        }

        h1 {
            margin-bottom: 0rem;
        }

        .subtitle {
            color: #666;
            font-size: 1.05rem;
            margin-bottom: 1.5rem;
        }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("🏀 NBA Player Performance Dashboard")

st.markdown(
    f'<div class="subtitle">{SEASON} Regular Season</div>',
    unsafe_allow_html=True
)


# -----------------------------------
# Load data
# -----------------------------------

@st.cache_data
def load_data():
    return pd.read_csv(DATA_PATH)


df = load_data()

qualified_df = df[
    df["Games"] >= MIN_GAMES
].copy()


# -----------------------------------
# Sidebar filters
# -----------------------------------

st.sidebar.header("Filters")

teams = ["All"] + sorted(
    qualified_df["Team"]
    .dropna()
    .unique()
    .tolist()
)

positions = ["All"] + sorted(
    qualified_df["Position"]
    .dropna()
    .unique()
    .tolist()
)

selected_team = st.sidebar.selectbox(
    "Team",
    teams
)

selected_position = st.sidebar.selectbox(
    "Position",
    positions
)


# -----------------------------------
# Apply filters
# -----------------------------------

filtered_df = qualified_df.copy()

if selected_team != "All":
    filtered_df = filtered_df[
        filtered_df["Team"] == selected_team
    ]

if selected_position != "All":
    filtered_df = filtered_df[
        filtered_df["Position"] == selected_position
    ]


# -----------------------------------
# Empty filter check
# -----------------------------------

if filtered_df.empty:
    st.warning("No players match the selected filters.")
    st.stop()


# -----------------------------------
# KPI cards
# -----------------------------------

top_scorer = filtered_df.loc[
    filtered_df["Points_Per_Game"].idxmax()
]

assist_leader = filtered_df.loc[
    filtered_df["Assists_Per_Game"].idxmax()
]

rebound_leader = filtered_df.loc[
    filtered_df["Rebounds_Per_Game"].idxmax()
]

st.subheader("Season Overview")

kpi1, kpi2, kpi3, kpi4 = st.columns(4)

kpi1.metric(
    "Qualified Players",
    len(filtered_df)
)

kpi2.metric(
    "Top Scorer",
    top_scorer["Player"],
    f'{top_scorer["Points_Per_Game"]:.1f} PPG'
)

kpi3.metric(
    "Assist Leader",
    assist_leader["Player"],
    f'{assist_leader["Assists_Per_Game"]:.1f} APG'
)

kpi4.metric(
    "Rebound Leader",
    rebound_leader["Player"],
    f'{rebound_leader["Rebounds_Per_Game"]:.1f} RPG'
)

st.divider()


# -----------------------------------
# Top scorers
# -----------------------------------

top_scorers = (
    filtered_df
    .sort_values(
        "Points_Per_Game",
        ascending=False
    )
    .head(10)
    .sort_values(
        "Points_Per_Game",
        ascending=True
    )
)

fig_scorers = px.bar(
    top_scorers,
    x="Points_Per_Game",
    y="Player",
    orientation="h",
    title="Top 10 Scorers",
    labels={
        "Points_Per_Game": "Points Per Game",
        "Player": ""
    },
    hover_data={
        "Team": True,
        "Position": True,
        "Games": True,
        "Points_Per_Game": ":.1f"
    }
)

fig_scorers.update_layout(
    height=500,
    margin=dict(l=20, r=20, t=60, b=20)
)


# -----------------------------------
# Position scoring
# -----------------------------------

position_scoring = (
    filtered_df
    .groupby("Position", as_index=False)[
        "Points_Per_Game"
    ]
    .mean()
    .sort_values(
        "Points_Per_Game",
        ascending=False
    )
)

fig_position = px.bar(
    position_scoring,
    x="Position",
    y="Points_Per_Game",
    title="Average Scoring by Position",
    labels={
        "Position": "Position",
        "Points_Per_Game": "Average Points Per Game"
    }
)

fig_position.update_layout(
    height=500,
    margin=dict(l=20, r=20, t=60, b=20)
)


# -----------------------------------
# Place charts side by side
# -----------------------------------

chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    st.plotly_chart(
        fig_scorers,
        use_container_width=True
    )

with chart_col2:
    st.plotly_chart(
        fig_position,
        use_container_width=True
    )

st.divider()


# -----------------------------------
# Minutes vs scoring
# -----------------------------------

correlation = filtered_df[
    "Minutes_Per_Game"
].corr(
    filtered_df["Points_Per_Game"]
)

fig_scatter = px.scatter(
    filtered_df,
    x="Minutes_Per_Game",
    y="Points_Per_Game",
    hover_name="Player",
    hover_data={
        "Team": True,
        "Position": True,
        "Games": True,
        "Minutes_Per_Game": ":.1f",
        "Points_Per_Game": ":.1f",
        "Assists_Per_Game": ":.1f",
        "Rebounds_Per_Game": ":.1f"
    },
    title=(
        "Minutes Per Game vs Points Per Game "
        f"(Correlation: {correlation:.2f})"
    ),
    labels={
        "Minutes_Per_Game": "Minutes Per Game",
        "Points_Per_Game": "Points Per Game"
    }
)

fig_scatter.update_traces(
    marker=dict(size=9, opacity=0.7)
)

fig_scatter.update_layout(
    height=550,
    margin=dict(l=20, r=20, t=60, b=20)
)

st.plotly_chart(
    fig_scatter,
    use_container_width=True
)

st.caption(
    f"Among players meeting the {MIN_GAMES}-game threshold, "
    f"minutes per game and points per game have a correlation of "
    f"{correlation:.2f}, indicating a strong positive relationship."
)

st.divider()


# -----------------------------------
# Player comparison
# -----------------------------------

st.subheader("Player Comparison")

player_names = sorted(
    qualified_df["Player"]
    .unique()
    .tolist()
)

comparison_col1, comparison_col2 = st.columns(2)

player_1 = comparison_col1.selectbox(
    "Player 1",
    player_names,
    index=0
)

player_2 = comparison_col2.selectbox(
    "Player 2",
    player_names,
    index=1
)

player_1_data = qualified_df[
    qualified_df["Player"] == player_1
].iloc[0]

player_2_data = qualified_df[
    qualified_df["Player"] == player_2
].iloc[0]

comparison_df = pd.DataFrame({
    "Metric": [
        "Points Per Game",
        "Rebounds Per Game",
        "Assists Per Game"
    ],
    player_1: [
        player_1_data["Points_Per_Game"],
        player_1_data["Rebounds_Per_Game"],
        player_1_data["Assists_Per_Game"]
    ],
    player_2: [
        player_2_data["Points_Per_Game"],
        player_2_data["Rebounds_Per_Game"],
        player_2_data["Assists_Per_Game"]
    ]
})

comparison_long = comparison_df.melt(
    id_vars="Metric",
    var_name="Player",
    value_name="Value"
)

fig_compare = px.bar(
    comparison_long,
    x="Metric",
    y="Value",
    color="Player",
    barmode="group",
    title=f"{player_1} vs {player_2}"
)

fig_compare.update_layout(
    height=500,
    legend_title_text="Player",
    margin=dict(l=20, r=20, t=60, b=20)
)

st.plotly_chart(
    fig_compare,
    use_container_width=True
)


# -----------------------------------
# Comparison table
# -----------------------------------

with st.expander("View Player Comparison Data"):
    st.dataframe(
        comparison_df,
        use_container_width=True,
        hide_index=True
    )


# -----------------------------------
# Methodology
# -----------------------------------

st.divider()

with st.expander("Methodology"):
    st.write(
        f"""
        Performance comparisons include players who appeared in at least
        **{MIN_GAMES} games**, approximately 70% of the NBA's 82-game
        regular season.

        This threshold reduces the impact of small sample sizes when
        comparing per-game statistics.

        Players who changed teams during the season are represented by
        their combined multi-team statistics for player-level analysis.

        Missing shooting percentages are preserved as missing values when
        a player recorded no attempts, rather than incorrectly treating
        those values as 0%.
        """
    )