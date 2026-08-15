"""
Project Orion Predictor
Analyse de forme pondérée par récence
Version 0.3
"""


def get_recency_weight(index, decay=0.85):
    """
    Calcule le poids d'un match.

    index = 0 -> match le plus récent
    index = 1 -> deuxième plus récent
    etc.

    Plus le match est ancien, plus son poids diminue.
    """

    return decay ** index


def get_team_form(
    matches,
    team,
    last_games=5,
    decay=0.85
):
    """
    Analyse la forme récente avec pondération temporelle.
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

    weighted_goals_for = 0.0
    weighted_goals_against = 0.0

    weighted_points = 0.0
    total_weight = 0.0


    for index, match in enumerate(team_matches):

        weight = get_recency_weight(
            index,
            decay
        )

        total_weight += weight


        if match["home_team"] == team:

            scored = match["home_goals"]
            conceded = match["away_goals"]

        else:

            scored = match["away_goals"]
            conceded = match["home_goals"]


        goals_for += scored
        goals_against += conceded


        weighted_goals_for += (
            scored * weight
        )

        weighted_goals_against += (
            conceded * weight
        )


        if scored > conceded:

            wins += 1
            weighted_points += 3 * weight

        elif scored == conceded:

            draws += 1
            weighted_points += 1 * weight

        else:

            losses += 1


    if total_weight <= 0:

        total_weight = 1


    weighted_attack = (
        weighted_goals_for
        /
        total_weight
    )

    weighted_defense = (
        weighted_goals_against
        /
        total_weight
    )

    weighted_form_score = (
        weighted_points
        /
        (total_weight * 3)
    ) * 100


    games = len(team_matches)


    normal_games = max(
        games,
        1
    )


    return {

        "games": games,

        "wins": wins,

        "draws": draws,

        "losses": losses,

        "goals_for": goals_for,

        "goals_against": goals_against,

        "average_goals_for": round(
            goals_for / normal_games,
            2
        ),

        "average_goals_against": round(
            goals_against / normal_games,
            2
        ),

        "weighted_goals_for": round(
            weighted_attack,
            2
        ),

        "weighted_goals_against": round(
            weighted_defense,
            2
        ),

        "form_score": round(
            weighted_form_score,
            2
        ),

        "recency_decay": decay
    }


def get_h2h(
    matches,
    team_a,
    team_b,
    max_matches=10
):
    """
    Retourne les confrontations directes récentes
    entre deux équipes.

    Les matchs doivent être classés du plus récent
    au plus ancien.
    """

    h2h = []


    for match in matches:

        is_h2h = (
            (
                match["home_team"] == team_a
                and
                match["away_team"] == team_b
            )
            or
            (
                match["home_team"] == team_b
                and
                match["away_team"] == team_a
            )
        )


        if is_h2h:

            h2h.append(match)


        if len(h2h) >= max_matches:
            break


    return h2h


def calculate_h2h_stats(
    matches,
    team_a,
    team_b,
    max_matches=10,
    decay=0.85
):
    """
    Analyse les H2H avec pondération de récence.
    """

    h2h = get_h2h(
        matches,
        team_a,
        team_b,
        max_matches
    )


    if not h2h:

        return {

            "matches": 0,

            "team_a_wins": 0,

            "draws": 0,

            "team_b_wins": 0,

            "team_a_goals": 0,

            "team_b_goals": 0,

            "weighted_team_a_goals": 0.0,

            "weighted_team_b_goals": 0.0,

            "weighted_team_a_win_rate": 0.0,

            "weighted_team_b_win_rate": 0.0,

            "weighted_draw_rate": 0.0
        }


    team_a_wins = 0
    team_b_wins = 0
    draws = 0

    team_a_goals = 0
    team_b_goals = 0

    weighted_a_goals = 0.0
    weighted_b_goals = 0.0

    weighted_a_wins = 0.0
    weighted_b_wins = 0.0
    weighted_draws = 0.0

    total_weight = 0.0


    for index, match in enumerate(h2h):

        weight = get_recency_weight(
            index,
            decay
        )

        total_weight += weight


        if match["home_team"] == team_a:

            a_goals = match["home_goals"]
            b_goals = match["away_goals"]

        else:

            a_goals = match["away_goals"]
            b_goals = match["home_goals"]


        team_a_goals += a_goals
        team_b_goals += b_goals


        weighted_a_goals += (
            a_goals * weight
        )

        weighted_b_goals += (
            b_goals * weight
        )


        if a_goals > b_goals:

            team_a_wins += 1
            weighted_a_wins += weight

        elif a_goals < b_goals:

            team_b_wins += 1
            weighted_b_wins += weight

        else:

            draws += 1
            weighted_draws += weight


    if total_weight <= 0:

        total_weight = 1


    return {

        "matches": len(h2h),

        "team_a_wins": team_a_wins,

        "draws": draws,

        "team_b_wins": team_b_wins,

        "team_a_goals": team_a_goals,

        "team_b_goals": team_b_goals,

        "weighted_team_a_goals": round(
            weighted_a_goals / total_weight,
            2
        ),

        "weighted_team_b_goals": round(
            weighted_b_goals / total_weight,
            2
        ),

        "weighted_team_a_win_rate": round(
            weighted_a_wins
            / total_weight
            * 100,
            2
        ),

        "weighted_team_b_win_rate": round(
            weighted_b_wins
            / total_weight
            * 100,
            2
        ),

        "weighted_draw_rate": round(
            weighted_draws
            / total_weight
            * 100,
            2
        )
        }
