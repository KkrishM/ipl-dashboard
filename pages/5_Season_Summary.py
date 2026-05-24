import streamlit as st
import plotly.express as px
import pandas as pd
from utils.data_loader import load_data
from utils.style import show_nav

st.set_page_config(page_title="Season Summary", page_icon="📅", layout="wide")
show_nav()

df = load_data()

st.title("📅 Season Summary")
st.markdown("Explore any IPL season — top performers, results & the champion")
st.divider()

seasons = sorted(df['season'].unique(), reverse=True)
selected_season = st.selectbox("Select a Season", seasons)

season_df = df[df['season'] == selected_season].copy()
matches = season_df.drop_duplicates(subset='match_id')

st.divider()

# --- Season KPIs ---
total_matches = matches['match_id'].nunique()
total_runs = season_df['runs_batter'].sum()
total_sixes = (season_df['runs_batter'] == 6).sum()
total_fours = (season_df['runs_batter'] == 4).sum()
total_wickets = season_df['bowler_wicket'].sum()

k1, k2, k3, k4, k5 = st.columns(5)
k1.metric("🏏 Matches", total_matches)
k2.metric("🏃 Total Runs", int(total_runs))
k3.metric("💥 Sixes", int(total_sixes))
k4.metric("🔴 Fours", int(total_fours))
k5.metric("🎯 Wickets", int(total_wickets))

st.divider()

# --- Champion ---
final = matches[matches['stage'].str.contains('Final', na=False, case=False)]
if not final.empty:
    champion = final.iloc[-1]['match_won_by']
    st.success(f"🏆 **{selected_season} IPL Champion: {champion}**")
else:
    st.info("Champion data not available for this season")

st.divider()

# --- Team wins this season ---
st.markdown("### 📊 Team Performance This Season")
team_wins = matches['match_won_by'].value_counts().reset_index()
team_wins.columns = ['Team', 'Wins']

fig1 = px.bar(team_wins, x='Wins', y='Team', orientation='h',
              color='Wins', color_continuous_scale='teal',
              title=f"{selected_season} — Wins by Team")
fig1.update_layout(yaxis={'categoryorder': 'total ascending'})
st.plotly_chart(fig1, use_container_width=True)

st.divider()

# --- Top Batsmen this season ---
st.markdown("### 🏏 Top Run Scorers This Season")
top_bat = season_df.groupby('batter')['runs_batter'].sum().reset_index()
top_bat.columns = ['Player', 'Runs']
top_bat = top_bat.sort_values('Runs', ascending=False).head(10)

fig2 = px.bar(top_bat, x='Runs', y='Player', orientation='h',
              color='Runs', color_continuous_scale='oranges',
              title=f"Top 10 Run Scorers — {selected_season}")
fig2.update_layout(yaxis={'categoryorder': 'total ascending'})
st.plotly_chart(fig2, use_container_width=True)

st.divider()

# --- Top Bowlers this season ---
st.markdown("### 🎳 Top Wicket Takers This Season")
top_bowl = season_df[season_df['bowler_wicket'] == 1].groupby('bowler').size().reset_index()
top_bowl.columns = ['Player', 'Wickets']
top_bowl = top_bowl.sort_values('Wickets', ascending=False).head(10)

fig3 = px.bar(top_bowl, x='Wickets', y='Player', orientation='h',
              color='Wickets', color_continuous_scale='blues',
              title=f"Top 10 Wicket Takers — {selected_season}")
fig3.update_layout(yaxis={'categoryorder': 'total ascending'})
st.plotly_chart(fig3, use_container_width=True)

st.divider()

# --- Most Player of Match ---
st.markdown("### 🌟 Player of the Match Awards This Season")
potm = matches['player_of_match'].value_counts().head(5).reset_index()
potm.columns = ['Player', 'Awards']

fig4 = px.pie(potm, names='Player', values='Awards',
              title=f"Player of the Match — {selected_season}",
              color_discrete_sequence=px.colors.qualitative.Set2)
st.plotly_chart(fig4, use_container_width=True)
