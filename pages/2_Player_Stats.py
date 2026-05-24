import streamlit as st
import plotly.express as px
import pandas as pd
from utils.data_loader import load_data, get_all_teams, get_team_players
from utils.style import show_nav

st.set_page_config(page_title="Player Stats", page_icon="🏏", layout="wide")
show_nav()

df = load_data()
teams = get_all_teams(df)

st.title("🏏 Player Stats")

col1, col2 = st.columns(2)
with col1:
    default_team = st.session_state.get('selected_team', teams[0])
    team = st.selectbox("Select Team", teams, index=list(teams).index(default_team))
with col2:
    players = get_team_players(df, team)
    default_player = st.session_state.get('selected_player', players[0])
    default_player = default_player if default_player in players else players[0]
    player = st.selectbox("Select Player", players, index=list(players).index(default_player))

st.divider()

# --- Batting Stats ---
bat_df = df[df['batter'] == player].copy()
bowl_df = df[df['bowler'] == player].copy()

if not bat_df.empty:
    st.markdown("### 🏏 Batting Stats")

    total_runs = bat_df['runs_batter'].sum()
    total_balls = bat_df['balls_faced'].sum()
    dismissals = df[df['player_out'] == player].shape[0]
    average = round(total_runs / dismissals, 2) if dismissals > 0 else total_runs
    strike_rate = round((total_runs / total_balls) * 100, 2) if total_balls > 0 else 0
    fours = bat_df[bat_df['runs_batter'] == 4].shape[0]
    sixes = bat_df[bat_df['runs_batter'] == 6].shape[0]
    fifties = bat_df.groupby('match_id')['runs_batter'].sum()
    fifty_count = fifties[(fifties >= 50) & (fifties < 100)].count()
    hundreds = fifties[fifties >= 100].count()

    k1, k2, k3, k4, k5, k6, k7 = st.columns(7)
    k1.metric("🏃 Total Runs", int(total_runs))
    k2.metric("🎯 Average", average)
    k3.metric("⚡ Strike Rate", strike_rate)
    k4.metric("🔴 4s", int(fours))
    k5.metric("💥 6s", int(sixes))
    k6.metric("🥈 50s", int(fifty_count))
    k7.metric("🥇 100s", int(hundreds))

    # Runs per season
    season_runs = bat_df.groupby('season')['runs_batter'].sum().reset_index()
    season_runs.columns = ['Season', 'Runs']
    season_runs = season_runs.sort_values('Season')

    fig1 = px.bar(season_runs, x='Season', y='Runs',
                  color='Runs', color_continuous_scale='oranges',
                  title=f"{player} — Runs per Season")
    st.plotly_chart(fig1, use_container_width=True)

st.divider()

# --- Bowling Stats ---
if not bowl_df.empty:
    st.markdown("### 🎳 Bowling Stats")

    valid_balls = bowl_df[bowl_df['valid_ball'] == 1].shape[0]
    overs_bowled = round(valid_balls / 6, 1)
    runs_given = bowl_df['runs_bowler'].sum()
    wickets = bowl_df[bowl_df['bowler_wicket'] == 1].shape[0]
    economy = round(runs_given / (valid_balls / 6), 2) if valid_balls > 0 else 0
    bowl_avg = round(runs_given / wickets, 2) if wickets > 0 else '-'
    sr = round(valid_balls / wickets, 2) if wickets > 0 else '-'

    k1, k2, k3, k4, k5 = st.columns(5)
    k1.metric("🎯 Wickets", int(wickets))
    k2.metric("📦 Overs", overs_bowled)
    k3.metric("💸 Economy", economy)
    k4.metric("📊 Average", bowl_avg)
    k5.metric("⚡ Strike Rate", sr)

    # Wickets per season
    season_wickets = bowl_df[bowl_df['bowler_wicket'] == 1].groupby('season').size().reset_index()
    season_wickets.columns = ['Season', 'Wickets']
    season_wickets = season_wickets.sort_values('Season')

    fig2 = px.bar(season_wickets, x='Season', y='Wickets',
                  color='Wickets', color_continuous_scale='blues',
                  title=f"{player} — Wickets per Season")
    st.plotly_chart(fig2, use_container_width=True)

st.divider()

# --- Compare Players ---
st.markdown("### ⚖️ Compare with Another Player")
compare_team = st.selectbox("Select team for comparison", teams, key='cmp_team')
compare_players = get_team_players(df, compare_team)
compare_player = st.selectbox("Select player to compare", compare_players, key='cmp_player')

if st.button("Compare Players"):
    p1_runs = df[df['batter'] == player]['runs_batter'].sum()
    p2_runs = df[df['batter'] == compare_player]['runs_batter'].sum()
    p1_wkts = df[(df['bowler'] == player) & (df['bowler_wicket'] == 1)].shape[0]
    p2_wkts = df[(df['bowler'] == compare_player) & (df['bowler_wicket'] == 1)].shape[0]

    cmp_df = pd.DataFrame({
        'Player': [player, compare_player],
        'Total Runs': [p1_runs, p2_runs],
        'Total Wickets': [p1_wkts, p2_wkts]
    })

    c1, c2 = st.columns(2)
    with c1:
        fig3 = px.bar(cmp_df, x='Player', y='Total Runs',
                      color='Player', title="Runs Comparison")
        st.plotly_chart(fig3, use_container_width=True)
    with c2:
        fig4 = px.bar(cmp_df, x='Player', y='Total Wickets',
                      color='Player', title="Wickets Comparison")
        st.plotly_chart(fig4, use_container_width=True)