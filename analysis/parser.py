"""
Project Orion Predictor
Parser des matchs FIFA FC 26 5v5
Version 0.1
"""

import re


def parse_matches(text):
    """
    Transforme une liste de matchs texte en données exploitables.
    Format attendu :
    Equipe A 3-2 Equipe B
    """

    matches = []

    lines = text.strip().split("\n")

    for line in lines:
        line = line.strip()

        if not line:
            continue

        # Recherche du score
        score = re.search(r"(.+?)\s+(\d+)-(\d+)\s+(.+)", line)

        if score:
            home_team = score.group(1).strip()
            home_goals = int(score.group(2))
            away_goals = int(score.group(3))
            away_team = score.group(4).strip()

            matches.append({
                "home_team": home_team,
                "home_goals": home_goals,
                "away_goals": away_goals,
                "away_team": away_team
            })

    return matches


# Test rapide
if __name__ == "__main__":

    data = """
    Galatasaray 5-2 Club Atlético de Madrid
    Napoli 1-3 Liverpool
    Real Madrid 5-1 Chelsea
    """

    result = parse_matches(data)

    for match in result:
        print(match)
