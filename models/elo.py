"""
Project Orion Predictor
Classement Elo
Version 0.1
"""

INITIAL_RATING = 1500
K_FACTOR = 32


def expected_score(rating_a, rating_b):
    return 1 / (1 + 10 ** ((rating_b - rating_a) / 400))


def update_elo(rating_a, rating_b, goals_a, goals_b):
    expected_a = expected_score(rating_a, rating_b)
    expected_b = expected_score(rating_b, rating_a)

    if goals_a > goals_b:
        score_a = 1
        score_b = 0
    elif goals_a < goals_b:
        score_a = 0
        score_b = 1
    else:
        score_a = 0.5
        score_b = 0.5

    new_rating_a = rating_a + K_FACTOR * (score_a - expected_a)
    new_rating_b = rating_b + K_FACTOR * (score_b - expected_b)

    return round(new_rating_a, 2), round(new_rating_b, 2)
