"""
Project Orion Predictor
Parser amélioré des matchs
Version 0.2
"""


def parse_matches(text):
    """
    Transforme un texte de matchs en données exploitables.

    Format accepté :

    Real Madrid 5-1 Chelsea
    Liverpool 3-2 Juventus

    """

    matches = []

    lines = text.strip().split("\n")

    for line in lines:

        line = line.strip()

        if not line:
            continue

        try:

            parts = line.split()

            score_position = None

            for index, part in enumerate(parts):

                if "-" in part:

                    left, right = part.split("-")

                    if left.isdigit() and right.isdigit():

                        score_position = index
                        break


            if score_position is None:
                continue


            home_team = " ".join(
                parts[:score_position]
            )

            away_team = " ".join(
                parts[score_position + 1:]
            )


            score = parts[score_position]

            home_goals, away_goals = map(
                int,
                score.split("-")
            )


            matches.append(
                {
                    "home_team": home_team.strip(),
                    "away_team": away_team.strip(),
                    "home_goals": home_goals,
                    "away_goals": away_goals
                }
            )


        except Exception:

            continue


    return matches
