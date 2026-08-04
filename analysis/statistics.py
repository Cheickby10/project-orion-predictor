"""
Project Orion Predictor
Calcul des statistiques des équipes
Version 0.1.1
"""


def calculate_team_stats(matches):
    """
    Calcule les statistiques de chaque équipe.
    """

    stats = {}


    for match in matches:

        home = match["home_team"]
        away = match["away_team"]

        home_goals = match["home_goals"]
        away_goals = match["away_goals"]


        if home not in stats:
            stats[home] = create_team_profile()


        if away not in stats:
            stats[away] = create_team_profile()


        # Matchs joués
        stats[home]["played"] += 1
        stats[away]["played"] += 1


        # Buts marqués
        stats[home]["goals_for"] += home_goals
        stats[away]["goals_for"] += away_goals


        # Buts encaissés
        stats[home]["goals_against"] += away_goals
        stats[away]["goals_against"] += home_goals


        # Résultats
        if home_goals > away_goals:

            stats[home]["wins"] += 1
            stats[away]["losses"] += 1

        elif home_goals < away_goals:

            stats[away]["wins"] += 1
            stats[home]["losses"] += 1

        else:

            stats[home]["draws"] += 1
            stats[away]["draws"] += 1


    return stats



def create_team_profile():

    return {
        "played": 0,
        "wins": 0,
        "draws": 0,
        "losses": 0,
        "goals_for": 0,
        "goals_against": 0
    }
