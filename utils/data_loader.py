import pandas as pd
import streamlit as st

TEAM_NAME_MAP = {
    'Delhi Daredevils': 'Delhi Capitals',
    'Kings XI Punjab': 'Punjab Kings',
    'Royal Challengers Bangalore': 'Royal Challengers Bengaluru',
    'Rising Pune Supergiants': 'Rising Pune Supergiant',
    'Deccan Chargers': 'Sunrisers Hyderabad',
}

VALID_SEASONS = [
    '2007/08', '2009', '2009/10', '2011', '2012', '2013',
    '2014', '2015', '2016', '2017', '2018', '2019', '2020/21',
    '2021', '2022', '2023', '2024', '2025'
]

@st.cache_data
def load_data():
    df = pd.read_csv('data/IPL.csv', low_memory=False)

    # Fix team names
    for col in ['batting_team', 'bowling_team', 'toss_winner', 'match_won_by']:
        if col in df.columns:
            df[col] = df[col].replace(TEAM_NAME_MAP)

    # Fix season column & remove bad data
    df['season'] = df['season'].astype(str)
    df = df[df['season'].isin(VALID_SEASONS)]

    return df

def get_all_teams(df):
    teams = pd.concat([df['batting_team'], df['bowling_team']]).unique()
    return sorted(teams)

def get_team_players(df, team):
    batsmen = df[df['batting_team'] == team]['batter'].unique()
    bowlers = df[df['bowling_team'] == team]['bowler'].unique()
    return sorted(set(batsmen) | set(bowlers))

def get_team_matches(df, team):
    return df[(df['batting_team'] == team) | (df['bowling_team'] == team)]

def get_match_results(df):
    # One row per match
    return df.drop_duplicates(subset='match_id')[
        ['match_id', 'date', 'season', 'batting_team', 'bowling_team',
         'toss_winner', 'toss_decision', 'match_won_by', 'win_outcome',
         'venue', 'city', 'player_of_match', 'stage']
    ].copy()