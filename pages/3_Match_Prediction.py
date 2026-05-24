import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import LabelEncoder
from utils.data_loader import load_data, get_all_teams
from utils.style import show_nav

st.set_page_config(page_title="Match Prediction", page_icon="🔮", layout="wide")
show_nav()

df = load_data()
teams = get_all_teams(df)
matches = df.drop_duplicates(subset='match_id').copy()

st.title("🔮 Match Prediction")
st.markdown("Select two teams and toss details to predict the winner")
st.divider()

# --- Train Model ---
@st.cache_resource
def train_model(matches):
    model_df = matches[['batting_team', 'bowling_team', 'toss_winner',
                         'toss_decision', 'venue', 'match_won_by']].dropna().copy()
    model_df = model_df[model_df['match_won_by'].isin(model_df['batting_team'].unique())]

    le_team = LabelEncoder()
    le_toss = LabelEncoder()
    le_decision = LabelEncoder()
    le_venue = LabelEncoder()

    all_teams = pd.concat([model_df['batting_team'], model_df['bowling_team'],
                           model_df['toss_winner'], model_df['match_won_by']]).unique()
    le_team.fit(all_teams)

    model_df['team1_enc'] = le_team.transform(model_df['batting_team'])
    model_df['team2_enc'] = le_team.transform(model_df['bowling_team'])
    model_df['toss_enc'] = le_team.transform(model_df['toss_winner'])
    model_df['decision_enc'] = le_decision.fit_transform(model_df['toss_decision'])
    model_df['venue_enc'] = le_venue.fit_transform(model_df['venue'])
    model_df['won'] = (model_df['match_won_by'] == model_df['batting_team']).astype(int)

    X = model_df[['team1_enc', 'team2_enc', 'toss_enc', 'decision_enc', 'venue_enc']]
    y = model_df['won']

    model = LogisticRegression(max_iter=1000)
    model.fit(X, y)

    return model, le_team, le_decision, le_venue

model, le_team, le_decision, le_venue = train_model(matches)

# --- Inputs ---
col1, col2 = st.columns(2)
with col1:
    default_a = st.session_state.get('team_a', teams[0])
    team_a = st.selectbox("🏏 Select Team A", teams, index=list(teams).index(default_a))
with col2:
    remaining = [t for t in teams if t != team_a]
    default_b = st.session_state.get('team_b', remaining[0])
    default_b = default_b if default_b in remaining else remaining[0]
    team_b = st.selectbox("🏏 Select Team B", remaining, index=remaining.index(default_b))

col3, col4 = st.columns(2)
with col3:
    toss_winner = st.selectbox("🪙 Who won the toss?", [team_a, team_b])
with col4:
    toss_decision = st.selectbox("📋 Toss decision", ["bat", "field"])

venues = sorted(matches['venue'].dropna().unique())
venue = st.selectbox("🏟️ Venue", venues)

st.divider()

if st.button("⚡ Predict Winner", use_container_width=True):

    try:
        t1_enc = le_team.transform([team_a])[0]
        t2_enc = le_team.transform([team_b])[0]
        toss_enc = le_team.transform([toss_winner])[0]
        dec_enc = le_decision.transform([toss_decision])[0]
        ven_enc = le_venue.transform([venue])[0]

        prob = model.predict_proba([[t1_enc, t2_enc, toss_enc, dec_enc, ven_enc]])[0]
        team_a_prob = round(prob[1] * 100, 1)
        team_b_prob = round(100 - team_a_prob, 1)

        winner = team_a if team_a_prob > team_b_prob else team_b

        st.success(f"🏆 Predicted Winner: **{winner}**")

        # Gauge chart
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=team_a_prob,
            title={'text': f"{team_a} Win Probability (%)"},
            gauge={
                'axis': {'range': [0, 100]},
                'bar': {'color': "#1565c0"},
                'steps': [
                    {'range': [0, 40], 'color': '#ffcdd2'},
                    {'range': [40, 60], 'color': '#fff9c4'},
                    {'range': [60, 100], 'color': '#c8e6c9'}
                ]
            }
        ))
        st.plotly_chart(fig, use_container_width=True)

        # Bar comparison
        fig2 = px.bar(
            x=[team_a, team_b],
            y=[team_a_prob, team_b_prob],
            color=[team_a, team_b],
            labels={'x': 'Team', 'y': 'Win Probability (%)'},
            title="Win Probability Comparison",
            text=[f"{team_a_prob}%", f"{team_b_prob}%"]
        )
        fig2.update_traces(textposition='outside')
        st.plotly_chart(fig2, use_container_width=True)

    except Exception as e:
        st.error(f"Prediction failed: {e}. Try a different venue or team combination.")

st.divider()

# --- Head to Head ---
st.markdown("### 🤝 Head to Head History")
h2h = matches[
    ((matches['batting_team'] == team_a) & (matches['bowling_team'] == team_b)) |
    ((matches['batting_team'] == team_b) & (matches['bowling_team'] == team_a))
].copy()

if not h2h.empty:
    a_wins = h2h[h2h['match_won_by'] == team_a].shape[0]
    b_wins = h2h[h2h['match_won_by'] == team_b].shape[0]
    total_h2h = len(h2h)

    h1, h2, h3 = st.columns(3)
    h1.metric("🏏 Total Matches", total_h2h)
    h2.metric(f"✅ {team_a} Wins", a_wins)
    h3.metric(f"✅ {team_b} Wins", b_wins)

    fig3 = px.pie(
        names=[team_a, team_b],
        values=[a_wins, b_wins],
        title="Head to Head Win Share",
        color_discrete_sequence=['#1565c0', '#d50000']
    )
    st.plotly_chart(fig3, use_container_width=True)
else:
    st.info("No head to head data found for this combination.")