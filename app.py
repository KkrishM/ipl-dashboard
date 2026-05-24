import streamlit as st
from utils.data_loader import load_data, get_all_teams
from utils.style import show_nav

st.set_page_config(
    page_title="IPL Analytics Dashboard",
    page_icon="🏏",
    layout="wide"
)
show_nav()
# Load data
df = load_data()
teams = get_all_teams(df)

# Header
st.title("🏏 IPL Analytics Dashboard")
st.markdown("##### Your one-stop destination for IPL stats, player analysis & match predictions")
st.divider()

# Section 1 - Team Explorer
st.markdown("### 📊 Explore a Team")
col1, col2 = st.columns([2, 1])
with col1:
    selected_team = st.selectbox("Select a team to explore", teams)
with col2:
    st.write("")
    st.write("")
    if st.button("View Team Analysis →", use_container_width=True):
        st.session_state['selected_team'] = selected_team
        st.switch_page("pages/1_Team_Analysis.py")

st.divider()

# Section 2 - Match Predictor
st.markdown("### 🔮 Predict a Match")
col3, col4, col5 = st.columns(3)
with col3:
    team_a = st.selectbox("Select Team A", teams, key='team_a')
with col4:
    team_b = st.selectbox("Select Team B", [t for t in teams if t != team_a], key='team_b')
with col5:
    st.write("")
    st.write("")
    if st.button("Predict Winner →", use_container_width=True):
        st.session_state['team_a'] = team_a
        st.session_state['team_b'] = team_b
        st.switch_page("pages/3_Match_Prediction.py")

st.divider()

# Section 3 - Quick Links
st.markdown("### 🏆 More to Explore")
col6, col7 = st.columns(2)
with col6:
    if st.button("🥇 Hall of Fame", use_container_width=True):
        st.switch_page("pages/4_Hall_of_Fame.py")
with col7:
    if st.button("📅 Season Summary", use_container_width=True):
        st.switch_page("pages/5_Season_Summary.py")