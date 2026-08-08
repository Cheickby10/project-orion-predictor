"""
Project Orion Predictor
Modèle de Poisson
Version 0.2
"""

import math


def poisson_probability(goals, average):

    average = max(float(average), 0.01)

    return (
        math.exp(-average)
        * average ** goals
        / math.factorial(goals)
    )


def calculate_score_probabilities(
    home_average,
    away_average,
    max_goals=10
):

    probabilities = {}

    for home_goals in range(max_goals + 1):

        for away_goals in range(max_goals + 1):

            home_probability = poisson_probability(
                home_goals,
                home_average
            )

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

    home_win = 0
    draw = 0
    away_win = 0

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
            "home_win": 0,
            "draw": 0,
            "away_win": 0
        }

    return {
        "home_win": home_win / total,
        "draw": draw / total,
        "away_win": away_win / total
    }


def calculate_over_under(probabilities, line):

    over = 0
    under = 0

    for (
        home_goals,
        away_goals
    ), probability in probabilities.items():

        total_goals = home_goals + away_goals

        if total_goals > line:
            over += probability

        else:
            under += probability

    total = over + under

    if total <= 0:
        return {
            "over": 0,
            "under": 0
        }

    return {
        "over": over / total,
        "under": under / total
    }


def calculate_btts(probabilities):

    yes = 0
    no = 0

    for (
        home_goals,
        away_goals
    ), probability in probabilities.items():

        if home_goals >= 1 and away_goals >= 1:
            yes += probability

        else:
            no += probability

    total = yes + no

    if total <= 0:
        return {
            "yes": 0,
            "no": 0
        }

    return {
        "yes": yes / total,
        "no": no / total
    }


def most_likely_scores(
    probabilities,
    top=5
):

    ordered = sorted(
        probabilities.items(),
        key=lambda item: item[1],
        reverse=True
    )

    return ordered[:top]
