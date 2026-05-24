# 🏏 IPL Analytics Dashboard

An interactive, multi-page web application built with **Python** and **Streamlit** that provides comprehensive analysis of IPL matches from **2008 to 2025**, including team performance, player stats, match prediction using Machine Learning, and historical insights.

---

##  Live Demo
> Coming soon — deploying on Streamlit Cloud

---

##  Features

###  Team Analysis
- Season-wise win/loss breakdown with interactive charts
- Toss strategy analysis — bat vs field decisions and win impact
- Venue-wise performance — best and worst grounds for each team
- Drill down into any player from the selected team

###  Player Stats
- Complete batting profile — runs, average, strike rate, 4s, 6s, 50s, 100s
- Complete bowling profile — wickets, economy, average, strike rate
- Season-wise performance trend charts
- **Compare any two players** side by side across batting and bowling

###  Match Prediction
- Select two teams, toss winner, toss decision, and venue
- **Logistic Regression model** trained on 17 years of IPL data
- Win probability displayed as an interactive gauge chart
- Head-to-head historical record between the two teams

###  Hall of Fame
- All-time top 10 run scorers
- All-time top 10 wicket takers
- Most sixes hit in IPL history
- Best economy bowlers (minimum 50 overs)
- Most Player of the Match awards

###  Season Summary
- Pick any IPL season from 2008 to 2025
- Season-level stats — matches, runs, sixes, fours, wickets
- Champion reveal for that season
- Top run scorers and wicket takers of the season
- Player of the Match leaderboard

---

##  Tech Stack

| Tool | Purpose |
|---|---|
| Python | Core programming language |
| Streamlit | Web app framework |
| Pandas | Data manipulation and analysis |
| Plotly | Interactive charts and visualizations |
| Scikit-learn | Machine Learning (Logistic Regression) |
| NumPy | Numerical computations |
| Git & GitHub | Version control |

---

##  Project Structure

```
ipl-dashboard/
│
├── app.py                    # Home page
├── pages/
│   ├── 1_Team_Analysis.py    # Team stats & strategy
│   ├── 2_Player_Stats.py     # Player profile & comparison
│   ├── 3_Match_Prediction.py # ML-based win predictor
│   ├── 4_Hall_of_Fame.py     # All-time IPL records
│   └── 5_Season_Summary.py   # Season-wise breakdown
├── utils/
│   ├── data_loader.py        # Data loading & caching
│   └── style.py              # Navigation & styling
├── data/
│   └── IPL.csv               # Dataset (not tracked in git)
├── .gitignore
└── README.md
```

---

##  Run Locally

**1. Clone the repository**
```bash
git clone https://github.com/KkrishM/ipl-dashboard.git
cd ipl-dashboard
```

**2. Install dependencies**
```bash
pip install streamlit pandas numpy plotly scikit-learn
```

**3. Download the dataset**

Download the IPL dataset (2008–2025) from Kaggle:
👉 https://www.kaggle.com/datasets/chaitu20/ipl-dataset2008-2025

Place the file at `data/IPL.csv`

**4. Run the app**
```bash
streamlit run app.py
```

---

##  ML Model Details

- **Algorithm:** Logistic Regression
- **Features used:** Team A, Team B, Toss Winner, Toss Decision, Venue
- **Training data:** All IPL matches from 2008 to 2025
- **Output:** Win probability (%) for each team

---

##  Dataset

- **Source:** [Kaggle — IPL Dataset 2008–2025](https://www.kaggle.com/datasets/chaitu20/ipl-dataset2008-2025)
- **Size:** 278,000+ ball-by-ball records
- **Coverage:** IPL seasons 2008 to 2025 (18 seasons)

---

##  Author

**Krish M**
- GitHub: [@KkrishM](https://github.com/KkrishM)

---

## ⭐ Show Your Support

If you found this project helpful, please consider giving it a ⭐ on GitHub!