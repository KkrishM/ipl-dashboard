import streamlit as st
import plotly.express as px
from utils.data_loader import load_data
from utils.style import show_nav

st.set_page_config(page_title="Hall of Fame", page_icon="🏆", layout="wide")
show_nav()

df = load_data()

st.title("🏆 Hall of Fame")
st.markdown("The greatest performers in IPL history")
st.divider()

# --- Top Run Scorers ---
st.markdown("### 🏏 Top 10 Run Scorers (All Time)")
run_scorers = df.groupby('batter')['runs_batter'].sum().reset_index()
run_scorers.columns = ['Player', 'Total Runs']
run_scorers = run_scorers.sort_values('Total Runs', ascending=False).head(10)

fig1 = px.bar(run_scorers, x='Total Runs', y='Player', orientation='h',
              color='Total Runs', color_continuous_scale='oranges',
              title="Top 10 Run Scorers")
fig1.update_layout(yaxis={'categoryorder': 'total ascending'})
st.plotly_chart(fig1, use_container_width=True)

st.divider()

# --- Top Wicket Takers ---
st.markdown("### 🎳 Top 10 Wicket Takers (All Time)")
wicket_takers = df[df['bowler_wicket'] == 1].groupby('bowler').size().reset_index()
wicket_takers.columns = ['Player', 'Wickets']
wicket_takers = wicket_takers.sort_values('Wickets', ascending=False).head(10)

fig2 = px.bar(wicket_takers, x='Wickets', y='Player', orientation='h',
              color='Wickets', color_continuous_scale='blues',
              title="Top 10 Wicket Takers")
fig2.update_layout(yaxis={'categoryorder': 'total ascending'})
st.plotly_chart(fig2, use_container_width=True)

st.divider()

# --- Most Sixes ---
st.markdown("### 💥 Top 10 Six Hitters (All Time)")
sixes = df[df['runs_batter'] == 6].groupby('batter').size().reset_index()
sixes.columns = ['Player', 'Sixes']
sixes = sixes.sort_values('Sixes', ascending=False).head(10)

fig3 = px.bar(sixes, x='Sixes', y='Player', orientation='h',
              color='Sixes', color_continuous_scale='reds',
              title="Top 10 Six Hitters")
fig3.update_layout(yaxis={'categoryorder': 'total ascending'})
st.plotly_chart(fig3, use_container_width=True)

st.divider()

# --- Best Economy Bowlers (min 50 overs) ---
st.markdown("### 🎯 Best Economy Bowlers (min 50 overs)")
bowl_df = df.copy()
bowl_stats = bowl_df.groupby('bowler').agg(
    Balls=('valid_ball', 'sum'),
    Runs=('runs_bowler', 'sum')
).reset_index()
bowl_stats = bowl_stats[bowl_stats['Balls'] >= 300]
bowl_stats['Economy'] = round((bowl_stats['Runs'] / bowl_stats['Balls']) * 6, 2)
bowl_stats = bowl_stats.sort_values('Economy').head(10)
bowl_stats.columns = ['Player', 'Balls', 'Runs', 'Economy']

fig4 = px.bar(bowl_stats, x='Economy', y='Player', orientation='h',
              color='Economy', color_continuous_scale='greens',
              title="Best Economy Bowlers (min 50 overs)")
fig4.update_layout(yaxis={'categoryorder': 'total descending'})
st.plotly_chart(fig4, use_container_width=True)

st.divider()

# --- Most Player of the Match ---
st.markdown("### 🌟 Most Player of the Match Awards")
matches = df.drop_duplicates(subset='match_id')
potm = matches['player_of_match'].value_counts().head(10).reset_index()
potm.columns = ['Player', 'Awards']

fig5 = px.bar(potm, x='Awards', y='Player', orientation='h',
              color='Awards', color_continuous_scale='purples',
              title="Most Player of the Match Awards")
fig5.update_layout(yaxis={'categoryorder': 'total ascending'})
st.plotly_chart(fig5, use_container_width=True)