"""
Project Orion Predictor
Moteur de prédiction
Version 0.1.1
"""

from models.poisson import (
    calculate_score_probabilities,
    most_likely_scores
)

from models.elo import EloSystem


class Predictor:

    def __init__(self, matches, stats):

        self.matches = matches
        self.stats = stats

        self.elo = EloSystem()
        self.elo.process_matches(matches)

    def predict(self, home_team, away_team):

        if home_team not in self.stats:
            return None

        if away_team not in self.stats:
            return None

        home = self.stats[home_team]
        away = self.stats[away_team]

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
            away_attack,
            max_goals=10
        )

        scores = most_likely_scores(
            probabilities,
            top=5
        )

        return {
            "home_team": home_team,
            "away_team": away_team,
            "home_rating": self.elo.get_rating(home_team),
            "away_rating": self.elo.get_rating(away_team),
            "scores": scores
        }
