"""
Project Orion Predictor
Gestion de la base de données
Version 0.1
"""

import json
import os


FILE = "data/matches.json"


def save_matches(matches):
    os.makedirs("data", exist_ok=True)

    with open(FILE, "w", encoding="utf-8") as f:
        json.dump(matches, f, indent=4, ensure_ascii=False)


def load_matches():

    if not os.path.exists(FILE):
        return []

    with open(FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def remove_duplicates(matches):

    unique = []

    for match in matches:
        if match not in unique:
            unique.append(match)

    return unique


def get_team_matches(matches, team):

    result = []

    for match in matches:

        if (
            match["home_team"] == team
            or match["away_team"] == team
        ):
            result.append(match)

    return result
