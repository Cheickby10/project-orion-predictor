"""
Project Orion Predictor
Moteur principal de prédiction
Version 0.1
"""

from models.poisson import (
    calculate_score_probabilities,
    most_likely_scores
)


def predict(
    home_team,
    away_team,
    stats
):

    home = stats[home_team]
    away = stats[away_team]


    home_attack = (
        home["goals_for"] /
        max(home["played"], 1)
    )

    away_attack = (
        away["goals_for"] /
        max(away["played"], 1)
    )


    probabilities = calculate_score_probabilities(
        home_attack,
        away_attack
    )


    scores = most_likely_scores(
        probabilities
    )


    result = {
        "home_team": home_team,
        "away_team": away_team,
        "scores": scores
    }


    return result
