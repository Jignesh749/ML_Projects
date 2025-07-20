import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# Set Streamlit page config
st.set_page_config(page_title="Basketball Metrics Visualizer", layout="wide")

# Load player stats
df = pd.read_csv('data/player_stats_2024_cleaned.csv')

# ========== #
# 1. Metrics #
# ========== #

df['TS%'] = df['PTS'] / (2 * (df['FGA'] + 0.44 * df['FTA']))
df['TS%'] = df['TS%'].replace([np.inf, -np.inf], np.nan)

df['USG%'] = (df['FGA'] + 0.44 * df['FTA'] + df['TOV']) / df['MP']
df['USG%'] = df['USG%'].replace([np.inf, -np.inf], np.nan)

df['eFG%'] = (df['FG'] + 0.5 * df['3P']) / df['FGA']
df['eFG%'] = df['eFG%'].replace([np.inf, -np.inf], np.nan)

df = df[df['MP'] > 500]

# =========================== #
# 2. Full Team Name Mapping   #
# =========================== #

team_name_map = {
    "ATL": "Atlanta Hawks (ATL)",
    "BOS": "Boston Celtics (BOS)",
    "BRK": "Brooklyn Nets (BRK)",
    "CHI": "Chicago Bulls (CHI)",
    "CHO": "Charlotte Hornets (CHO)",
    "CLE": "Cleveland Cavaliers (CLE)",
    "DAL": "Dallas Mavericks (DAL)",
    "DEN": "Denver Nuggets (DEN)",
    "DET": "Detroit Pistons (DET)",
    "GSW": "Golden State Warriors (GSW)",
    "HOU": "Houston Rockets (HOU)",
    "IND": "Indiana Pacers (IND)",
    "LAC": "Los Angeles Clippers (LAC)",
    "LAL": "Los Angeles Lakers (LAL)",
    "MEM": "Memphis Grizzlies (MEM)",
    "MIA": "Miami Heat (MIA)",
    "MIL": "Milwaukee Bucks (MIL)",
    "MIN": "Minnesota Timberwolves (MIN)",
    "NOP": "New Orleans Pelicans (NOP)",
    "NYK": "New York Knicks (NYK)",
    "OKC": "Oklahoma City Thunder (OKC)",
    "ORL": "Orlando Magic (ORL)",
    "PHI": "Philadelphia 76ers (PHI)",
    "PHO": "Phoenix Suns (PHO)",
    "POR": "Portland Trail Blazers (POR)",
    "SAC": "Sacramento Kings (SAC)",
    "SAS": "San Antonio Spurs (SAS)",
    "TOR": "Toronto Raptors (TOR)",
    "UTA": "Utah Jazz (UTA)",
    "WAS": "Washington Wizards (WAS)"
}

# Add full team name column
df['TeamFull'] = df['Team'].map(team_name_map)

# ======================= #
# 3. Friendly Label Map   #
# ======================= #

metric_label_map = {
    'PTS': 'Points Per Season',
    'AST': 'Assists',
    'TRB': 'Rebounds',
    'MP': 'Minutes Played',
    'FG%': 'Field Goal %',
    'FT%': 'Free Throw %',
    '3P%': '3-Point %',
    'FGA': 'Field Goal Attempts',
    'FTA': 'Free Throw Attempts',
    'TOV': 'Turnovers',
    'TS%': 'True Shooting %',
    'USG%': 'Usage Rate (Proxy)',
    'eFG%': 'Effective FG %',
    'STL': 'Steals',
    'BLK': 'Blocks',
    'ORB': 'Offensive Rebounds',
    'DRB': 'Defensive Rebounds',
}
label_to_metric = {v: k for k, v in metric_label_map.items()}
friendly_labels = list(metric_label_map.values())

# ===================== #
# 4. Streamlit Interface#
# ===================== #

st.markdown("<h1 style='text-align: center; color: #1f77b4;'>🏀 NBA 2024 Basketball Metrics Visualizer</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Explore advanced and traditional player stats with interactive filtering and visuals.</p>", unsafe_allow_html=True)
st.markdown("---")

# Sidebar filters
st.sidebar.markdown("### 🔍 Filter Players")
team_options = sorted(df['TeamFull'].dropna().unique())
selected_teams = st.sidebar.multiselect("Teams", options=team_options, default=team_options)

positions = st.sidebar.multiselect("Positions", sorted(df['Pos'].unique()), default=sorted(df['Pos'].unique()))

# Filter based on full team names
df_filtered = df[df['TeamFull'].isin(selected_teams) & df['Pos'].isin(positions)]

# Sidebar metric selection
st.sidebar.markdown("### 📊 Metrics to Compare")
x_label = st.sidebar.selectbox("X-axis", options=friendly_labels, index=friendly_labels.index('Usage Rate (Proxy)'))
y_label = st.sidebar.selectbox("Y-axis", options=friendly_labels, index=friendly_labels.index('True Shooting %'))

x_axis = label_to_metric[x_label]
y_axis = label_to_metric[y_label]

# ================= #
# 5. Scatter Plot   #
# ================= #

st.subheader(f"📈 {y_label} vs {x_label}")

fig, ax = plt.subplots(figsize=(11, 6))
sns.set_style("whitegrid")
sns.scatterplot(
    data=df_filtered,
    x=x_axis,
    y=y_axis,
    hue='TeamFull',
    style='Pos',
    palette='tab10',
    s=90,
    alpha=0.75,
    ax=ax
)

plt.xlabel(x_label, fontsize=12)
plt.ylabel(y_label, fontsize=12)
plt.title(f"{y_label} vs {x_label} by Team and Position", fontsize=14, color='#333')
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize='small', title='Team')
st.pyplot(fig)

# =================== #
# 6. Data Table View  #
# =================== #

with st.expander("📋 Show Player Data Table"):
    st.dataframe(
        df_filtered[['Player', 'TeamFull', 'Pos', x_axis, y_axis]]
        .sort_values(by=y_axis, ascending=False)
        .reset_index(drop=True)
        .rename(columns={
            'TeamFull': 'Team',
            x_axis: x_label,
            y_axis: y_label
        })
    )

# Footer
st.markdown("---")
st.markdown("<small style='color:gray;'>Built with ❤️ using Python, Pandas, Seaborn & Streamlit. | Data from Basketball-Reference.com</small>", unsafe_allow_html=True)
