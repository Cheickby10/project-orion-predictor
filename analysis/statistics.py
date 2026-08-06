"""
Project Orion Predictor
Statistiques avancées des équipes
Version 0.2
"""


def create_profile():

    return {
        "played": 0,
        "wins": 0,
        "draws": 0,
        "losses": 0,

        "goals_for": 0,
        "goals_against": 0,

        "attack_average": 0,
        "defense_average": 0,
        "win_rate": 0
    }



def calculate_team_stats(matches):

    stats = {}


    for match in matches:

        home = match["home_team"]
        away = match["away_team"]

        hg = match["home_goals"]
        ag = match["away_goals"]


        if home not in stats:
            stats[home] = create_profile()


        if away not in stats:
            stats[away] = create_profile()



        # Matchs joués

        stats[home]["played"] += 1
        stats[away]["played"] += 1


        # Buts

        stats[home]["goals_for"] += hg
        stats[home]["goals_against"] += ag

        stats[away]["goals_for"] += ag
        stats[away]["goals_against"] += hg



        # Résultats

        if hg > ag:

            stats[home]["wins"] += 1
            stats[away]["losses"] += 1


        elif hg < ag:

            stats[away]["wins"] += 1
            stats[home]["losses"] += 1


        else:

            stats[home]["draws"] += 1
            stats[away]["draws"] += 1



    # Calcul des moyennes

    for team, data in stats.items():

        games = max(data["played"], 1)


        data["attack_average"] = round(
            data["goals_for"] / games,
            2
        )


        data["defense_average"] = round(
            data["goals_against"] / games,
            2
        )


        data["win_rate"] = round(
            (data["wins"] / games) * 100,
            2
        )


        data["goal_difference"] = (
            data["goals_for"]
            -
            data["goals_against"]
        )


    return stats
