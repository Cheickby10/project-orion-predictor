"""
Project Orion Predictor
Modèle de Poisson
Version 0.1.1
"""

import math


def poisson_probability(goals, average):
    """
    Probabilité qu'une équipe marque 'goals' buts
    avec une moyenne 'average'.
    """

    if average <= 0:
        average = 0.01

    return (
        math.exp(-average)
        * (average ** goals)
        / math.factorial(goals)
    )


def calculate_score_probabilities(
    home_average,
    away_average,
    max_goals=10
):
    """
    Calcule les probabilités des scores.
    """

    probabilities = {}

    for home_goals in range(max_goals + 1):

        for away_goals in range(max_goals + 1):

            p_home = poisson_probability(
                home_goals,
                home_average
            )

            p_away = poisson_probability(
                away_goals,
                away_average
            )

            probabilities[
                (home_goals, away_goals)
            ] = p_home * p_away

    return probabilities


def most_likely_scores(
    probabilities,
    top=5
):
    """
    Retourne les scores les plus probables.
    """

    ordered = sorted(
        probabilities.items(),
        key=lambda item: item[1],
        reverse=True
    )

    return ordered[:top]
