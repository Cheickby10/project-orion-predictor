"""
Project Orion Predictor
Moteur central de prédiction
Version 0.2
"""

from models.poisson import (
    calculate_score_probabilities,
    calculate_result_probabilities,
    calculate_over_under,
    calculate_btts,
    most_likely_scores
)

from models.elo import EloSystem

from analysis.form import get_team_form


class Predictor:

    def __init__(self, matches, stats):

        self.matches = matches
        self.stats = stats

        self.elo = EloSystem()

        self.elo.process_matches(matches)

    def predict(
        self,
        home_team,
        away_team,
        form_games=5,
        over_under_line=5.5
