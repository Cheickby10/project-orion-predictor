"""
Project Orion Predictor
Modèle de Poisson avancé
Version 0.3
"""

import math


def poisson_probability(goals, average):
    """Probabilité d'obtenir exactement 'goals' buts."""

    average = max(float(average), 0.01)

    return (
        math.exp(-average)
        * (average ** goals)
        / math.factorial(goals)
    )


def calculate_score_probabilities(
    home_average,
    away_average,
    max_goals=12
):
    """
    Génère les probabilités de tous les scores
    de 0-0 jusqu'à max_goals-max_goals.
    """

    probabilities = {}

    for home_goals in range(max_goals + 1):

        home_probability = poisson_probability(
            home_goals,
            home_average
        )

        for away_goals in range(max_goals + 1):

            away_probability = poisson_probability(
                away_goals,
                away_average
            )

            probabilities[
                (home_goals, away_goals)
            ] = (
                home_probability
                * away_probability
            )

    return probabilities


def calculate_result_probabilities(probabilities):
    """Calcule les probabilités Victoire A / Nul / Victoire B."""

    home_win = 0.0
    draw = 0.0
    away_win = 0.0

    for (
        home_goals,
        away_goals
    ), probability in probabilities.items():

        if home_goals > away_goals:
            home_win += probability

        elif home_goals == away_goals:
            draw += probability

        else:
            away_win += probability

    total = home_win + draw + away_win

    if total <= 0:
        return {
            "home_win": 0.0,
            "draw": 0.0,
            "away_win": 0.0
        }

    return {
        "home_win": home_win / total,
        "draw": draw / total,
        "away_win": away_win / total
    }


def calculate_over_under(
    probabilities,
    line
):
    """
    Calcule Over/Under pour une ligne donnée.

    Exemple :
    line = 6.5
    Over = total de buts >= 7
    Under = total de buts <= 6
    """

    over = 0.0
    under = 0.0

    for (
        home_goals,
        away_goals
    ), probability in probabilities.items():

        total_goals = (
            home_goals
            + away_goals
        )

        if total_goals > line:
            over += probability

        else:
            under += probability

    total = over + under

    if total <= 0:
        return {
            "over": 0.0,
            "under": 0.0
        }

    return {
        "over": over / total,
        "under": under / total
    }


def calculate_all_over_under(
    probabilities,
    lines=None
):
    """
    Calcule plusieurs lignes Over/Under.
    """

    if lines is None:

        lines = [
            3.5,
            4.5,
            5.5,
            6.5,
            7.5,
            8.5,
            9.5
        ]

    results = {}

    for line in lines:

        results[str(line)] = (
            calculate_over_under(
                probabilities,
                line
            )
        )

    return results


def calculate_btts_threshold(
    probabilities,
    minimum_goals
):
    """
    Calcule la probabilité que les deux équipes
    marquent au moins 'minimum_goals' buts.

    minimum_goals = 1 -> BTTS 1+
    minimum_goals = 2 -> BTTS 2+
    minimum_goals = 3 -> BTTS 3+
    minimum_goals = 4 -> BTTS 4+
    """

    yes = 0.0
    no = 0.0

    for (
        home_goals,
        away_goals
    ), probability in probabilities.items():

        if (
            home_goals >= minimum_goals
            and
            away_goals >= minimum_goals
        ):

            yes += probability

        else:

            no += probability

    total = yes + no

    if total <= 0:
        return {
            "yes": 0.0,
            "no": 0.0
        }

    return {
        "yes": yes / total,
        "no": no / total
    }


def calculate_all_btts(probabilities):
    """
    Calcule BTTS 1+, 2+, 3+ et 4+.
    """

    results = {}

    for minimum_goals in [1, 2, 3, 4]:

        results[
            str(minimum_goals)
        ] = calculate_btts_threshold(
            probabilities,
            minimum_goals
        )

    return results


def most_likely_scores(
    probabilities,
    top=10
):
    """Retourne les scores les plus probables."""

    ordered = sorted(
        probabilities.items(),
        key=lambda item: item[1],
        reverse=True
    )

    return ordered[:top]
