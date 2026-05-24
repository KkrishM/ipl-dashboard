import pandas as pd

df = pd.read_csv('data/IPL.csv', low_memory=False)

print("Shape:", df.shape)
print("\nSeasons:", sorted(df['season'].astype(str).unique()))
print("\nTeams:", sorted(df['batting_team'].unique()))