"""
Project Orion Predictor
Système de Backtesting
Version 0.5
"""

from models.predictor import Predictor
from analysis.statistics import calculate_team_stats


class Backtester:

    def __init__(self, matches):

        self.matches = matches


    def run(
        self,
        min_history=20,
        form_games=10
    ):
        """
        Teste le moteur sur les anciens matchs.

        Pour chaque match testé, le modèle utilise uniquement
        les matchs précédents afin d'éviter le data leakage.
        """

        results = []

        total_matches = len(self.matches)

        if total_matches <= min_history:

            return results


        # Les matchs sont normalement stockés
        # du plus récent au plus ancien.
        #
        # On travaille donc depuis l'ancien vers
        # le récent pour reproduire le déroulement
        # historique.

        chronological_matches = list(
            reversed(self.matches)
        )


        for index in range(
            min_history,
            total_matches
        ):

            historical_matches = (
                chronological_matches[:index]
            )

            target_match = (
                chronological_matches[index]
            )


            # ---------------------------------------------
            # Vérification du match
            # ---------------------------------------------

            try:

                home_team = target_match[
                    "home_team"
                ]

                away_team = target_match[
                    "away_team"
                ]

                home_goals = int(
                    target_match["home_goals"]
                )

                away_goals = int(
                    target_match["away_goals"]
                )

            except (
                KeyError,
                TypeError,
                ValueError
            ):

                continue


            # ---------------------------------------------
            # Statistiques historiques
            # ---------------------------------------------

            stats = calculate_team_stats(
                historical_matches
            )


            if home_team not in stats:
                continue

            if away_team not in stats:
                continue


            # ---------------------------------------------
            # Création du modèle
            # ---------------------------------------------

            predictor = Predictor(
                historical_matches,
                stats
            )


            # ---------------------------------------------
            # Prédiction
            # ---------------------------------------------

            prediction = predictor.predict(
                home_team,
                away_team,
                form_games=form_games
            )


            if prediction is None:
                continue


            probabilities = prediction[
                "result_probabilities"
            ]


            # ---------------------------------------------
            # Résultat réel
            # ---------------------------------------------

            if home_goals > away_goals:

                actual_result = "home"

            elif home_goals < away_goals:

                actual_result = "away"

            else:

                actual_result = "draw"


            # ---------------------------------------------
            # Résultat prédit
            # ---------------------------------------------

            predicted_result = max(
                probabilities,
                key=probabilities.get
            )


            result_mapping = {
                "home_win": "home",
                "draw": "draw",
                "away_win": "away"
            }


            predicted_result = (
                result_mapping[
                    predicted_result
                ]
            )


            # ---------------------------------------------
            # Précision 1N2
            # ---------------------------------------------

            correct_1x2 = (
                predicted_result
                ==
                actual_result
            )


            # ---------------------------------------------
            # Score prédit
            # ---------------------------------------------

            scores = prediction.get(
                "scores",
                []
            )


            top_score = None

            if scores:

                top_score = scores[0][0]


            exact_score = False

            if top_score is not None:

                exact_score = (
                    top_score[0] == home_goals
                    and
                    top_score[1] == away_goals
                )


            # ---------------------------------------------
            # Over / Under 3.5
            # ---------------------------------------------

            total_goals = (
                home_goals
                +
                away_goals
            )


            over_under = prediction.get(
                "over_under",
                {}
            )


            line_35 = over_under.get(
                "3.5"
            )


            over_35_prediction = None

            correct_over_35 = False


            if line_35:

                over_35_prediction = (
                    "over"
                    if line_35["over"]
                    >=
                    line_35["under"]
                    else
                    "under"
                )


                actual_over_35 = (
                    "over"
                    if total_goals > 3.5
                    else
                    "under"
                )


                correct_over_35 = (
                    over_35_prediction
                    ==
                    actual_over_35
                )


            # ---------------------------------------------
            # BTTS 1+
            # ---------------------------------------------

            btts = prediction.get(
                "btts",
                {}
            )


            btts_1 = btts.get(
                "1",
                {}
            )


            btts_prediction = None
            correct_btts = False


            if btts_1:

                btts_prediction = (
                    "yes"
                    if btts_1["yes"]
                    >=
                    btts_1["no"]
                    else
                    "no"
                )


                actual_btts = (
                    "yes"
                    if (
                        home_goals >= 1
                        and
                        away_goals >= 1
                    )
                    else
                    "no"
                )


                correct_btts = (
                    btts_prediction
                    ==
                    actual_btts
                )


            # ---------------------------------------------
            # Erreur sur les buts attendus
            # ---------------------------------------------

            expected_goals = prediction[
                "expected_goals"
            ]


            expected_total = (
                expected_goals["total"]
            )


            goal_error = abs(
                expected_total
                -
                total_goals
            )


            # ---------------------------------------------
            # Enregistrement
            # ---------------------------------------------

            results.append({

                "match_index": index,

                "home_team": home_team,

                "away_team": away_team,

                "actual_score": (
                    home_goals,
                    away_goals
                ),

                "actual_result":
                    actual_result,

                "predicted_result":
                    predicted_result,

                "correct_1x2":
                    correct_1x2,

                "top_score":
                    top_score,

                "exact_score":
                    exact_score,

                "over_3_5_correct":
                    correct_over_35,

                "btts_1_correct":
                    correct_btts,

                "expected_total":
                    round(
                        expected_total,
                        2
                    ),

                "actual_total":
                    total_goals,

                "goal_error":
                    round(
                        goal_error,
                        2
                    ),

                "confidence":
                    prediction.get(
                        "confidence",
                        0
                    )
            })


        return results


    # ========================================================
    # RAPPORT
    # ========================================================

    def summarize(
        self,
        results
    ):

        total = len(results)


        if total == 0:

            return {
                "matches_tested": 0,
                "accuracy_1x2": 0,
                "exact_score_accuracy": 0,
                "over_3_5_accuracy": 0,
                "btts_accuracy": 0,
                "average_goal_error": 0,
                "average_confidence": 0
            }


        correct_1x2 = sum(
            result["correct_1x2"]
            for result in results
        )


        exact_scores = sum(
            result["exact_score"]
            for result in results
        )


        over_35 = sum(
            result["over_3_5_correct"]
            for result in results
        )


        btts = sum(
            result["btts_1_correct"]
            for result in results
        )


        goal_error = sum(
            result["goal_error"]
            for result in results
        )


        confidence = sum(
            result["confidence"]
            for result in results
        )


        return {

            "matches_tested":
                total,

            "accuracy_1x2":
                round(
                    correct_1x2
                    /
                    total
                    *
                    100,
                    2
                ),

            "exact_score_accuracy":
                round(
                    exact_scores
                    /
                    total
                    *
                    100,
                    2
                ),

            "over_3_5_accuracy":
                round(
                    over_35
                    /
                    total
                    *
                    100,
                    2
                ),

            "btts_accuracy":
                round(
                    btts
                    /
                    total
                    *
                    100,
                    2
                ),

            "average_goal_error":
                round(
                    goal_error
                    /
                    total,
                    2
                ),

            "average_confidence":
                round(
                    confidence
                    /
                    total,
                    2
                )
      }
