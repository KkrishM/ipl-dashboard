import streamlit as st
import plotly.express as px
import pandas as pd
from utils.data_loader import load_data, get_all_teams, get_team_players
from utils.style import show_nav
show_nav()
st.set_page_config(page_title="Team Analysis", page_icon="📊", layout="wide")

df = load_data()
teams = get_all_teams(df)

# Get selected team from home page or let user pick
if 'selected_team' in st.session_state:
    default_idx = list(teams).index(st.session_state['selected_team'])
else:
    default_idx = 0

st.title("📊 Team Analysis")
selected_team = st.selectbox("Select a team", teams, index=default_idx)

matches = df.drop_duplicates(subset='match_id').copy()
team_matches = matches[
    (matches['batting_team'] == selected_team) |
    (matches['bowling_team'] == selected_team)
].copy()

team_matches['won'] = team_matches['match_won_by'] == selected_team

st.divider()

# --- KPI Cards ---
total = len(team_matches)
wins = team_matches['won'].sum()
losses = total - wins
win_pct = round((wins / total) * 100, 1) if total > 0 else 0

k1, k2, k3, k4 = st.columns(4)
k1.metric("🏏 Matches Played", total)
k2.metric("✅ Wins", wins)
k3.metric("❌ Losses", losses)
k4.metric("🎯 Win %", f"{win_pct}%")

st.divider()

# --- Win/Loss by Season ---
st.markdown("### 📅 Season-wise Performance")
season_stats = team_matches.groupby('season').agg(
    Matches=('match_id', 'count'),
    Wins=('won', 'sum')
).reset_index()
season_stats['Losses'] = season_stats['Matches'] - season_stats['Wins']
season_stats = season_stats.sort_values('season')

fig1 = px.bar(
    season_stats, x='season', y=['Wins', 'Losses'],
    barmode='group',
    color_discrete_map={'Wins': '#00c853', 'Losses': '#d50000'},
    labels={'value': 'Matches', 'season': 'Season'},
    title=f"{selected_team} — Win/Loss by Season"
)
st.plotly_chart(fig1, use_container_width=True)

# --- Toss Analysis ---
st.markdown("### 🪙 Toss Strategy")
toss_data = team_matches[team_matches['toss_winner'] == selected_team]
toss_decision = toss_data['toss_decision'].value_counts().reset_index()
toss_decision.columns = ['Decision', 'Count']

col1, col2 = st.columns(2)
with col1:
    fig2 = px.pie(toss_decision, names='Decision', values='Count',
                  title="Toss Decision (when won toss)",
                  color_discrete_sequence=['#1565c0', '#f57f17'])
    st.plotly_chart(fig2, use_container_width=True)

with col2:
    # Win after winning toss
    toss_won_match = team_matches[team_matches['toss_winner'] == selected_team]
    toss_win_rate = round((toss_won_match['won'].sum() / len(toss_won_match)) * 100, 1) if len(toss_won_match) > 0 else 0
    toss_lost_match = team_matches[team_matches['toss_winner'] != selected_team]
    toss_loss_rate = round((toss_lost_match['won'].sum() / len(toss_lost_match)) * 100, 1) if len(toss_lost_match) > 0 else 0

    st.markdown("#### 🎯 Win Rate by Toss Outcome")
    st.metric("Won toss → Win %", f"{toss_win_rate}%")
    st.metric("Lost toss → Win %", f"{toss_loss_rate}%")

st.divider()

# --- Top Venues ---
st.markdown("### 🏟️ Venue Performance")
venue_stats = team_matches.groupby('venue').agg(
    Matches=('match_id', 'count'),
    Wins=('won', 'sum')
).reset_index()
venue_stats['Win %'] = round((venue_stats['Wins'] / venue_stats['Matches']) * 100, 1)
venue_stats = venue_stats[venue_stats['Matches'] >= 3].sort_values('Win %', ascending=False).head(10)

fig3 = px.bar(venue_stats, x='Win %', y='venue', orientation='h',
              color='Win %', color_continuous_scale='greens',
              title="Top Venues by Win %")
st.plotly_chart(fig3, use_container_width=True)

st.divider()

# --- Player Section ---
st.markdown("### 🏏 Explore a Player")
players = get_team_players(df, selected_team)
selected_player = st.selectbox("Select a player", players)

if st.button("View Player Stats →", use_container_width=False):
    st.session_state['selected_player'] = selected_player
    st.session_state['selected_team'] = selected_team
    st.switch_page("pages/2_Player_Stats.py")
