import streamlit as st

def show_nav():
    st.markdown("""
        <style>
            [data-testid="stSidebar"] {display: none;}
            [data-testid="collapsedControl"] {display: none;}
        </style>
    """, unsafe_allow_html=True)

    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        if st.button("🏠 Home", use_container_width=True):
            st.switch_page("app.py")
    with col2:
        if st.button("📊 Team Analysis", use_container_width=True):
            st.switch_page("pages/1_Team_Analysis.py")
    with col3:
        if st.button("🏏 Player Stats", use_container_width=True):
            st.switch_page("pages/2_Player_Stats.py")
    with col4:
        if st.button("🔮 Predict Match", use_container_width=True):
            st.switch_page("pages/3_Match_Prediction.py")
    with col5:
        if st.button("🏆 Hall of Fame", use_container_width=True):
            st.switch_page("pages/4_Hall_of_Fame.py")
    st.divider()
    