import pandas as pd
import streamlit as st
import os
import requests

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

def download_from_gdrive(file_id, dest_path):
    session = requests.Session()
    url = "https://drive.google.com/uc?export=download"
    
    # First request to get confirmation token
    response = session.get(url, params={"id": file_id}, stream=True)
    
    # Find confirmation token
    token = None
    for key, value in response.cookies.items():
        if key.startswith("download_warning"):
            token = value
    
    # If token found, use it; otherwise try new Google Drive format
    if token:
        response = session.get(url, params={"id": file_id, "confirm": token}, stream=True)
    else:
        # Try newer Google Drive download format
        response = session.get(
            f"https://drive.usercontent.google.com/download?id={file_id}&export=download&confirm=t",
            stream=True
        )

    with open(dest_path, "wb") as f:
        for chunk in response.iter_content(chunk_size=32768):
            if chunk:
                f.write(chunk)

@st.cache_data
def load_data():
    local_path = 'data/IPL.csv'

    if not os.path.exists(local_path):
        os.makedirs('data', exist_ok=True)
        file_id = "1y8mb8_Mb_3X5iB6ds1X_fjZb1RSql0K0"
        download_from_gdrive(file_id, local_path)

    df = pd.read_csv(local_path, low_memory=False)

    for col in ['batting_team', 'bowling_team', 'toss_winner', 'match_won_by']:
        if col in df.columns:
            df[col] = df[col].replace(TEAM_NAME_MAP)

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
    return df.drop_duplicates(subset='match_id')[
        ['match_id', 'date', 'season', 'batting_team', 'bowling_team',
         'toss_winner', 'toss_decision', 'match_won_by', 'win_outcome',
         'venue', 'city', 'player_of_match', 'stage']
    ].copy()