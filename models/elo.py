"""
Project Orion Predictor
Système Elo amélioré
Version 0.4
"""

import math


# ============================================================
# CONFIGURATION
# ============================================================

INITIAL_RATING = 1500

# K de base
K_FACTOR = 32

# Avantage domicile Elo
HOME_ADVANTAGE = 35

# Limite de variation maximale sur un match
MAX_RATING_CHANGE = 60


class EloSystem:

    def __init__(self):

        self.ratings = {}

        # Nombre de matchs joués par équipe.
        # Sert à rendre le K-factor adaptatif.
        self.games_played = {}


    # ========================================================
    # RATING
    # ========================================================

    def get_rating(self, team):

        if team not in self.ratings:

            self.ratings[team] = INITIAL_RATING

        if team not in self.games_played:

            self.games_played[team] = 0

        return self.ratings[team]


    # ========================================================
    # K FACTOR ADAPTATIF
    # ========================================================

    def get_k_factor(self, team):

        games = self.games_played.get(
            team,
            0
        )

        # Équipe avec peu de données :
        # évolution plus rapide.
        if games < 10:

            return 40

        # Phase intermédiaire.
        elif games < 30:

            return 36

        # Équipe suffisamment connue.
        else:

            return K_FACTOR


    # ========================================================
    # SCORE ATTENDU
    # ========================================================

    def expected_score(
        self,
        rating_a,
        rating_b
    ):

        return 1 / (
            1
            +
            10 ** (
                (rating_b - rating_a)
                / 400
            )
        )


    # ========================================================
    # MARGE DE VICTOIRE
    # ========================================================

    def goal_margin_multiplier(
        self,
        goal_difference,
        winner_rating,
        loser_rating
    ):
        """
        Ajuste l'impact d'une victoire selon l'écart
        de buts.

        L'effet augmente avec la marge, mais reste
        volontairement limité.
        """

        margin = abs(
            goal_difference
        )

        if margin <= 1:

            return 1.00

        # Formule logarithmique :
        # évite qu'un énorme score fasse exploser Elo.
        multiplier = (
            math.log(
                margin + 1
            )
            + 0.50
        )

        # Petit ajustement lorsque le favori gagne.
        rating_difference = (
            winner_rating
            - loser_rating
        )

        if rating_difference > 0:

            multiplier *= 0.90

        else:

            multiplier *= 1.10

        return max(
            1.00,
            min(multiplier, 2.00)
        )


    # ========================================================
    # MISE À JOUR
    # ========================================================

    def update(
        self,
        home,
        away,
        home_goals,
        away_goals
    ):

        # ----------------------------------------------------
        # Ratings actuels
        # ----------------------------------------------------

        home_rating = self.get_rating(
            home
        )

        away_rating = self.get_rating(
            away
        )


        # ----------------------------------------------------
        # Avantage domicile
        # ----------------------------------------------------

        adjusted_home_rating = (
            home_rating
            +
            HOME_ADVANTAGE
        )


        # ----------------------------------------------------
        # Résultat attendu
        # ----------------------------------------------------

        expected_home = self.expected_score(
            adjusted_home_rating,
            away_rating
        )

        expected_away = (
            1
            -
            expected_home
        )


        # ----------------------------------------------------
        # Résultat réel
        # ----------------------------------------------------

        if home_goals > away_goals:

            actual_home = 1.0
            actual_away = 0.0

            winner_rating = home_rating
            loser_rating = away_rating

        elif home_goals < away_goals:

            actual_home = 0.0
            actual_away = 1.0

            winner_rating = away_rating
            loser_rating = home_rating

        else:

            actual_home = 0.5
            actual_away = 0.5

            winner_rating = home_rating
            loser_rating = away_rating


        # ----------------------------------------------------
        # Écart de buts
        # ----------------------------------------------------

        goal_difference = abs(
            home_goals
            -
            away_goals
        )


        if goal_difference > 0:

            margin_multiplier = (
                self.goal_margin_multiplier(
                    goal_difference,
                    winner_rating,
                    loser_rating
                )
            )

        else:

            margin_multiplier = 1.0


        # ----------------------------------------------------
        # K-factor
        # ----------------------------------------------------

        home_k = self.get_k_factor(
            home
        )

        away_k = self.get_k_factor(
            away
        )


        # ----------------------------------------------------
        # Variation Elo
        # ----------------------------------------------------

        home_change = (

            home_k
            *
            margin_multiplier
            *
            (
                actual_home
                -
                expected_home
            )
        )


        away_change = (

            away_k
            *
            margin_multiplier
            *
            (
                actual_away
                -
                expected_away
            )
        )


        # ----------------------------------------------------
        # Protection contre les variations extrêmes
        # ----------------------------------------------------

        home_change = max(
            -MAX_RATING_CHANGE,
            min(
                home_change,
                MAX_RATING_CHANGE
            )
        )

        away_change = max(
            -MAX_RATING_CHANGE,
            min(
                away_change,
                MAX_RATING_CHANGE
            )
        )


        # ----------------------------------------------------
        # Nouveau rating
        # ----------------------------------------------------

        self.ratings[home] = round(
            home_rating
            +
            home_change,
            2
        )

        self.ratings[away] = round(
            away_rating
            +
            away_change,
            2
        )


        # ----------------------------------------------------
        # Nombre de matchs
        # ----------------------------------------------------

        self.games_played[home] = (
            self.games_played.get(
                home,
                0
            )
            +
            1
        )

        self.games_played[away] = (
            self.games_played.get(
                away,
                0
            )
            +
            1
        )


    # ========================================================
    # TRAITEMENT DE LA BASE
    # ========================================================

    def process_matches(self, matches):

        """
        Les matchs sont fournis du plus récent
        au plus ancien.

        On les traite donc dans l'ordre inverse
        afin de reconstruire l'évolution Elo.
        """

        for match in reversed(matches):

            try:

                self.update(
                    match["home_team"],
                    match["away_team"],
                    int(match["home_goals"]),
                    int(match["away_goals"])
                )

            except (
                KeyError,
                TypeError,
                ValueError
            ):

                # Ignore proprement un match
                # mal formé.
                continue


        return self.ratings
