"""
Project Orion Predictor
Moteur central de prédiction
Version 0.4
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

        # ----------------------------------------------
        # Système Elo
        # ----------------------------------------------

        self.elo = EloSystem()
        self.elo.process_matches(matches)


    # ==================================================
    # OUTILS INTERNES
    # ==================================================

    @staticmethod
    def _clamp(value, minimum, maximum):

        return max(
            minimum,
            min(float(value), maximum)
        )


    @staticmethod
    def _safe_value(data, key, default=0.0):

        try:
            value = float(
                data.get(key, default)
            )

            return value

        except (
            TypeError,
            ValueError,
            AttributeError
        ):

            return float(default)


    # ==================================================
    # PRÉDICTION
    # ==================================================

    def predict(
        self,
        home_team,
        away_team,
        form_games=10,
        over_under_lines=None
    ):

        # ----------------------------------------------
        # Vérification des équipes
        # ----------------------------------------------

        if home_team not in self.stats:

            return None

        if away_team not in self.stats:

            return None

        if home_team == away_team:

            return None


        home = self.stats[home_team]
        away = self.stats[away_team]


        # ==================================================
        # 1. FORME RÉCENTE
        # ==================================================

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


        # ==================================================
        # 2. H2H
        # ==================================================

        h2h = calculate_h2h_stats(
            self.matches,
            home_team,
            away_team,
            max_matches=10
        )

        if not isinstance(h2h, dict):

            h2h = {
                "matches": 0,
                "weighted_team_a_goals": 0.0,
                "weighted_team_b_goals": 0.0
            }


        h2h_matches = int(
            self._safe_value(
                h2h,
                "matches",
                0
            )
        )


        # ==================================================
        # 3. ELO
        # ==================================================

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


        # ==================================================
        # 4. STATISTIQUES DE BASE
        # ==================================================

        home_attack_average = self._safe_value(
            home,
            "attack_average"
        )

        away_attack_average = self._safe_value(
            away,
            "attack_average"
        )

        home_defense_average = self._safe_value(
            home,
            "defense_average"
        )

        away_defense_average = self._safe_value(
            away,
            "defense_average"
        )


        # Forme récente

        home_form_goals_for = self._safe_value(
            home_form,
            "weighted_goals_for",
            home_attack_average
        )

        away_form_goals_for = self._safe_value(
            away_form,
            "weighted_goals_for",
            away_attack_average
        )

        home_form_goals_against = self._safe_value(
            home_form,
            "weighted_goals_against",
            home_defense_average
        )

        away_form_goals_against = self._safe_value(
            away_form,
            "weighted_goals_against",
            away_defense_average
        )


        # ==================================================
        # 5. PROJECTION OFFENSIVE
        # ==================================================

        # Équipe à domicile :
        #
        # attaque historique
        # + forme récente
        # + faiblesse défensive adverse

        home_attack = (

            home_attack_average * 0.40

            +

            home_form_goals_for * 0.35

            +

            away_defense_average * 0.15

            +

            away_form_goals_against * 0.10
        )


        # Équipe à l'extérieur

        away_attack = (

            away_attack_average * 0.40

            +

            away_form_goals_for * 0.35

            +

            home_defense_average * 0.15

            +

            home_form_goals_against * 0.10
        )


        # ==================================================
        # 6. BUTS ATTENDUS INITIAUX
        # ==================================================

        home_expected = (

            home_attack * 0.80

            +

            away_form_goals_against * 0.20
        )


        away_expected = (

            away_attack * 0.80

            +

            home_form_goals_against * 0.20
        )


        # ==================================================
        # 7. AVANTAGE DOMICILE
        # ==================================================

        # Petit bonus afin de ne pas laisser l'avantage
        # domicile dominer le reste du modèle.

        home_expected *= 1.04

        away_expected *= 0.98


        # ==================================================
        # 8. AJUSTEMENT ELO
        # ==================================================

        elo_adjustment = (
            elo_home_probability - 0.5
        )


        # Maximum d'influence volontairement limité.

        home_elo_factor = (
            1 +
            elo_adjustment * 0.14
        )

        away_elo_factor = (
            1 -
            elo_adjustment * 0.10
        )


        home_expected *= home_elo_factor

        away_expected *= away_elo_factor


        # ==================================================
        # 9. AJUSTEMENT H2H
        # ==================================================

        if h2h_matches >= 2:

            h2h_home_goals = self._safe_value(
                h2h,
                "weighted_team_a_goals"
            )

            h2h_away_goals = self._safe_value(
                h2h,
                "weighted_team_b_goals"
            )


            # On limite l'influence du H2H.
            #
            # Le H2H ne doit pas remplacer la forme
            # et les statistiques actuelles.

            h2h_weight = 0.10


            home_expected = (

                home_expected
                * (1 - h2h_weight)

                +

                h2h_home_goals
                * h2h_weight
            )


            away_expected = (

                away_expected
                * (1 - h2h_weight)

                +

                h2h_away_goals
                * h2h_weight
            )


        # ==================================================
        # 10. LIMITATION DES BUTS ATTENDUS
        # ==================================================

        home_expected = self._clamp(
            home_expected,
            0.10,
            10.0
        )

        away_expected = self._clamp(
            away_expected,
            0.10,
            10.0
        )


        # ==================================================
        # 11. POISSON
        # ==================================================

        probabilities = calculate_score_probabilities(
            home_expected,
            away_expected,
            max_goals=12
        )


        if not probabilities:

            return None


        # ==================================================
        # 12. PROBABILITÉS 1N2
        # ==================================================

        result_probabilities = (
            calculate_result_probabilities(
                probabilities
            )
        )


        # ==================================================
        # 13. OVER / UNDER
        # ==================================================

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


        # ==================================================
        # 14. BTTS
        # ==================================================

        btts = calculate_all_btts(
            probabilities
        )


        # ==================================================
        # 15. SCORES LES PLUS PROBABLES
        # ==================================================

        likely_scores = most_likely_scores(
            probabilities,
            top=10
        )


        # ==================================================
        # 16. BUTS TOTAUX ATTENDUS
        # ==================================================

        expected_total = (
            home_expected
            +
            away_expected
        )


        # ==================================================
        # 17. INDICE DE CONFIANCE
        # ==================================================

        result_values = [

            result_probabilities.get(
                "home_win",
                0.0
            ),

            result_probabilities.get(
                "draw",
                0.0
            ),

            result_probabilities.get(
                "away_win",
                0.0
            )
        ]


        result_values.sort(
            reverse=True
        )


        # Écart entre le premier et le deuxième
        # résultat.

        probability_gap = (
            result_values[0]
            -
            result_values[1]
        )


        # Transforme l'écart en score 0-100.

        result_confidence = (
            probability_gap * 200
        )


        # --------------------------------------------------
        # Fiabilité des données
        # --------------------------------------------------

        total_matches = len(
            self.matches
        )


        if total_matches >= 100:

            data_reliability = 1.00

        elif total_matches >= 50:

            data_reliability = 0.90

        elif total_matches >= 25:

            data_reliability = 0.80

        elif total_matches >= 10:

            data_reliability = 0.65

        else:

            data_reliability = 0.50


        # H2H supplémentaire

        if h2h_matches >= 5:

            h2h_reliability = 1.00

        elif h2h_matches >= 3:

            h2h_reliability = 0.90

        elif h2h_matches >= 2:

            h2h_reliability = 0.75

        else:

            h2h_reliability = 0.50


        # Confiance finale

        confidence = (

            result_confidence
            * 0.75
            +

            data_reliability
            * 100
            * 0.15

            +

            h2h_reliability
            * 100
            * 0.10
        )


        confidence = self._clamp(
            confidence,
            0.0,
            100.0
        )


        # ==================================================
        # 18. RÉSULTAT FINAL
        # ==================================================

        return {

            "home_team":
                home_team,

            "away_team":
                away_team,


            # ----------------------------------------------
            # ELO
            # ----------------------------------------------

            "home_rating":
                round(
                    home_elo,
                    2
                ),

            "away_rating":
                round(
                    away_elo,
                    2
                ),

            "elo_home_advantage":
                round(
                    elo_home_probability * 100,
                    2
                ),


            # ----------------------------------------------
            # FORME
            # ----------------------------------------------

            "home_form":
                home_form,

            "away_form":
                away_form,


            # ----------------------------------------------
            # H2H
            # ----------------------------------------------

            "h2h":
                h2h,


            # ----------------------------------------------
            # BUTS ATTENDUS
            # ----------------------------------------------

            "expected_goals": {

                "home":
                    round(
                        home_expected,
                        2
                    ),

                "away":
                    round(
                        away_expected,
                        2
                    ),

                "total":
                    round(
                        expected_total,
                        2
                    )
            },


            # ----------------------------------------------
            # 1N2
            # ----------------------------------------------

            "result_probabilities":
                result_probabilities,


            # ----------------------------------------------
            # OVER / UNDER
            # ----------------------------------------------

            "over_under":
                over_under,


            # ----------------------------------------------
            # BTTS
            # ----------------------------------------------

            "btts":
                btts,


            # ----------------------------------------------
            # SCORES
            # ----------------------------------------------

            "scores":
                likely_scores,


            # ----------------------------------------------
            # CONFIANCE
            # ----------------------------------------------

            "confidence":
                round(
                    confidence,
                    2
                )
        }
