"""
Project Orion Predictor
Système Elo
Version 0.3
"""

INITIAL_RATING = 1500
K_FACTOR = 32


class EloSystem:

    def __init__(self):

        self.ratings = {}


    def get_rating(self, team):

        if team not in self.ratings:

            self.ratings[team] = INITIAL_RATING

        return self.ratings[team]


    def expected_score(
        self,
        rating_a,
        rating_b
    ):

        return 1 / (
            1 + 10 ** (
                (rating_b - rating_a) / 400
            )
        )


    def update(
        self,
        home,
        away,
        home_goals,
        away_goals
    ):

        home_rating = self.get_rating(
            home
        )

        away_rating = self.get_rating(
            away
        )


        expected_home = self.expected_score(
            home_rating,
            away_rating
        )

        expected_away = self.expected_score(
            away_rating,
            home_rating
        )


        if home_goals > away_goals:

            actual_home = 1
            actual_away = 0

        elif home_goals < away_goals:

            actual_home = 0
            actual_away = 1

        else:

            actual_home = 0.5
            actual_away = 0.5


        self.ratings[home] = round(
            home_rating
            + K_FACTOR
            * (
                actual_home
                - expected_home
            ),
            2
        )


        self.ratings[away] = round(
            away_rating
            + K_FACTOR
            * (
                actual_away
                - expected_away
            ),
            2
        )


    def process_matches(self, matches):

        """
        Les matchs sont fournis du plus récent
        au plus ancien.

        On les traite donc dans l'ordre inverse pour
        reconstruire l'évolution Elo.
        """

        for match in reversed(matches):

            self.update(
                match["home_team"],
                match["away_team"],
                match["home_goals"],
                match["away_goals"]
            )


        return self.ratings
