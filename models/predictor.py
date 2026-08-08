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
    ):

        if home_team not in self.stats:
            return None

        if away_team not in self.stats:
            return None

        home = self.stats[home_team]
        away = self.stats[away_team]

        # Statistiques générales
        home_attack = home["attack_average"]
        away_attack = away["attack_average"]

        home_defense = home["defense_average"]
        away_defense = away["defense_average"]

        # Forme récente
        home_form = get_team_form(
            self.matches,
            home_team,
            form_games
        )

        away_form = get_team_form(
            self.matches,
            away_team,
            form_games
        )

        # Moyenne offensive ajustée
        home_expected_goals = (
            home_attack
            + away_defense
        ) / 2

        away_expected_goals = (
            away_attack
            + home_defense
        ) / 2

        # Influence modérée de la forme récente
        home_expected_goals = (
            home_expected_goals * 0.75
            + home_form["average_goals_for"] * 0.25
        )

        away_expected_goals = (
            away_expected_goals * 0.75
            + away_form["average_goals_for"] * 0.25
        )

        home_expected_goals = max(
            home_expected_goals,
            0.1
        )

        away_expected_goals = max(
            away_expected_goals,
            0.1
        )

        probabilities = calculate_score_probabilities(
            home_expected_goals,
            away_expected_goals
        )

        results = calculate_result_probabilities(
            probabilities
        )

        over_under = calculate_over_under(
            probabilities,
            over_under_line
        )

        btts = calculate_btts(
            probabilities
        )

        scores = most_likely_scores(
            probabilities,
            top=5
        )

        return {
            "home_team": home_team,
            "away_team": away_team,

            "home_rating":
                self.elo.get_rating(home_team),

            "away_rating":
                self.elo.get_rating(away_team),

            "home_form":
                home_form,

            "away_form":
                away_form,

            "expected_goals": {
                "home":
                    round(home_expected_goals, 2),

                "away":
                    round(away_expected_goals, 2)
            },

            "result_probabilities": results,

            "over_under":
                over_under,

            "btts":
                btts,

            "scores":
                scores
        }
