"""
Project Orion Predictor
Analyseur de matchs
Version 0.1.1
"""


def parse_matches(text):
    """
    Transforme les matchs au format :

    Equipe A 3-2 Equipe B

    en données exploitables.
    """

    matches = []

    lines = text.strip().split("\n")

    for line in lines:

        line = line.strip()

        if not line:
            continue

        try:
            parts = line.split()

            score_index = None

            for i, part in enumerate(parts):
                if "-" in part and part[0].isdigit():
                    score_index = i
                    break

            if score_index is None:
                continue


            home_team = " ".join(
                parts[:score_index]
            )

            score = parts[score_index]

            away_team = " ".join(
                parts[score_index + 1:]
            )


            home_goals, away_goals = map(
                int,
                score.split("-")
            )


            matches.append(
                {
                    "home_team": home_team,
                    "away_team": away_team,
                    "home_goals": home_goals,
                    "away_goals": away_goals
                }
            )

        except Exception:
            continue


    return matches
