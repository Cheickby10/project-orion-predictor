"""
Project Orion Predictor
Statistiques des équipes
Version 0.1
"""

from collections import defaultdict


def calculate_team_stats(matches):
    teams = defaultdict(lambda: {
        "played": 0,
        "wins": 0,
        "draws": 0,
        "losses": 0,
        "goals_for": 0,
        "goals_against": 0
    })

    for match in matches:

        home = match["home_team"]
        away = match["away_team"]

        hg = match["home_goals"]
        ag = match["away_goals"]

        teams[home]["played"] += 1
        teams[away]["played"] += 1

        teams[home]["goals_for"] += hg
        teams[home]["goals_against"] += ag

        teams[away]["goals_for"] += ag
        teams[away]["goals_against"] += hg

        if hg > ag:
            teams[home]["wins"] += 1
            teams[away]["losses"] += 1

        elif hg < ag:
            teams[away]["wins"] += 1
            teams[home]["losses"] += 1

        else:
            teams[home]["draws"] += 1
            teams[away]["draws"] += 1

    return teams
