"""
Project Orion Predictor
Moteur central de prédiction
Version 0.3
"""

from models.poisson import (
    calculate_score_probabilities,
    calculate_result_probabilities,
    calculate_all_over_under,
    calculate_all_btts,
    most_likely_scores
)

from models.elo import EloSystem

from analysis.form import (
    get_team_form,
    calculate_h2h_stats
)


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
        form_games=10,
        over_under_lines=None
    ):

        if home_team not in self.stats:
            return None

        if away_team not in self.stats:
            return None


        home = self.stats[home_team]
        away = self.stats[away_team]


        # ==============================
        # FORME RÉCENTE
        # ==============================

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


        # ==============================
        # H2H
        # ==============================

        h2h = calculate_h2h_stats(
            self.matches,
            home_team,
            away_team,
            max_matches=10
        )


        # ==============================
        # ELO
        # ==============================

        home_elo = self.elo.get_rating(
            home_team
        )

        away_elo = self.elo.get_rating(
            away_team
        )

        elo_difference = (
            home_elo - away_elo
        )

        elo_home_probability = (
            1 /
            (
                1 +
                10 ** (
                    -elo_difference / 400
                )
            )
        )


        # ==============================
        # ATTAQUE
        # ==============================

        home_attack = (
            home["attack_average"] * 0.45
            +
            home_form["weighted_goals_for"] * 0.35
            +
            away["defense_average"] * 0.20
        )

        away_attack = (
            away["attack_average"] * 0.45
            +
            away_form["weighted_goals_for"] * 0.35
            +
            home["defense_average"] * 0.20
        )


        # ==============================
        # BUTS ATTENDUS
        # ==============================

        home_expected = (
            home_attack * 0.80
            +
            away_form["weighted_goals_against"] * 0.20
        )

        away_expected = (
            away_attack * 0.80
            +
            home_form["weighted_goals_against"] * 0.20
        )


        # ==============================
        # AJUSTEMENT ELO
        # ==============================

        elo_adjustment = (
            elo_home_probability - 0.5
        )

        home_expected *= (
            1 + elo_adjustment * 0.12
        )

        away_expected *= (
            1 - elo_adjustment * 0.12
        )


        # ==============================
        # AJUSTEMENT H2H
        # ==============================

        if h2h["matches"] >= 2:

            home_expected = (
                home_expected * 0.90
                +
                h2h["weighted_team_a_goals"] * 0.10
            )

            away_expected = (
                away_expected * 0.90
                +
                h2h["weighted_team_b_goals"] * 0.10
            )


        # ==============================
        # LIMITES
        # ==============================

        home_expected = max(
            0.10,
            min(home_expected, 10.0)
        )

        away_expected = max(
            0.10,
            min(away_expected, 10.0)
        )


        # ==============================
        # POISSON
        # ==============================

        probabilities = calculate_score_probabilities(
            home_expected,
            away_expected,
            max_goals=12
        )


        # ==============================
        # 1N2
        # ==============================

        result_probabilities = (
            calculate_result_probabilities(
                probabilities
            )
        )


        # ==============================
        # OVER / UNDER
        # ==============================

        if over_under_lines is None:

            over_under_lines = [
                3.5,
                4.5,
                5.5,
                6.5,
                7.5,
                8.5,
                9.5
            ]

        over_under = calculate_all_over_under(
            probabilities,
            over_under_lines
        )


        # ==============================
        # BTTS
        # ==============================

        btts = calculate_all_btts(
            probabilities
        )


        # ==============================
        # SCORES
        # ==============================

        likely_scores = most_likely_scores(
            probabilities,
            top=10
        )


        # ==============================
        # TOTAL BUTS
        # ==============================

        expected_total = (
            home_expected
            +
            away_expected
        )


        # ==============================
        # CONFIANCE
        # ==============================

        values = sorted(
            [
                result_probabilities["home_win"],
                result_probabilities["draw"],
                result_probabilities["away_win"]
            ],
            reverse=True
        )

        confidence = (
            values[0] - values[1]
        ) * 200

        confidence = max(
            0,
            min(confidence, 100)
        )


        # ==============================
        # RÉSULTAT
        # ==============================

        return {

            "home_team": home_team,

            "away_team": away_team,

            "home_rating": round(
                home_elo,
                2
            ),

            "away_rating": round(
                away_elo,
                2
            ),

            "elo_home_advantage": round(
                elo_home_probability * 100,
                2
            ),

            "home_form": home_form,

            "away_form": away_form,

            "h2h": h2h,

            "expected_goals": {

                "home": round(
                    home_expected,
                    2
                ),

                "away": round(
                    away_expected,
                    2
                ),

                "total": round(
                    expected_total,
                    2
                )
            },

            "result_probabilities":
                result_probabilities,

            "over_under":
                over_under,

            "btts":
                btts,

            "scores":
                likely_scores,

            "confidence":
                round(
                    confidence,
                    2
                )
        }
