"""
Project Orion Predictor
Analyse de la forme récente
Version 0.2
"""


def get_team_form(matches, team, last_games=5):
    """
    Retourne la forme récente d'une équipe.

    Les matchs doivent être classés
    du plus récent au plus ancien.
    """

    team_matches = []


    for match in matches:

        if (
            match["home_team"] == team
            or match["away_team"] == team
        ):

            team_matches.append(match)


        if len(team_matches) >= last_games:
            break



    wins = 0
    draws = 0
    losses = 0

    goals_for = 0
    goals_against = 0


    for match in team_matches:


        if match["home_team"] == team:

            scored = match["home_goals"]
            conceded = match["away_goals"]

        else:

            scored = match["away_goals"]
            conceded = match["home_goals"]



        goals_for += scored
        goals_against += conceded


        if scored > conceded:

            wins += 1

        elif scored < conceded:

            losses += 1

        else:

            draws += 1



    games = max(len(team_matches), 1)


    form_score = (
        (wins * 3)
        +
        (draws * 1)
    ) / (games * 3) * 100



    return {

        "games": len(team_matches),

        "wins": wins,

        "draws": draws,

        "losses": losses,

        "goals_for": goals_for,

        "goals_against": goals_against,

        "average_goals_for": round(
            goals_for / games,
            2
        ),

        "average_goals_against": round(
            goals_against / games,
            2
        ),

        "form_score": round(
            form_score,
            2
        )
  }
