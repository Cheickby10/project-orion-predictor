"""
Project Orion Predictor
Classement Elo
Version 0.1.1
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

    def expected_score(self, rating_a, rating_b):

        return 1 / (
            1 + 10 ** ((rating_b - rating_a) / 400)
        )

    def update(self, home, away, home_goals, away_goals):

        rating_home = self.get_rating(home)
        rating_away = self.get_rating(away)

        expected_home = self.expected_score(
            rating_home,
            rating_away
        )

        expected_away = self.expected_score(
            rating_away,
            rating_home
        )

        if home_goals > away_goals:
            score_home = 1
            score_away = 0

        elif home_goals < away_goals:
            score_home = 0
            score_away = 1

        else:
            score_home = 0.5
            score_away = 0.5

        rating_home += K_FACTOR * (
            score_home - expected_home
        )

        rating_away += K_FACTOR * (
            score_away - expected_away
        )

        self.ratings[home] = round(
            rating_home,
            2
        )

        self.ratings[away] = round(
            rating_away,
            2
        )

    def process_matches(self, matches):

        for match in reversed(matches):

            self.update(
                match["home_team"],
                match["away_team"],
                match["home_goals"],
                match["away_goals"]
            )

        return self.ratings
