"""
Project Orion Predictor
Gestion des données
Version 0.1.1
"""

import json
import os


DATA_FOLDER = "data"
MATCHES_FILE = os.path.join(DATA_FOLDER, "matches.json")


def save_matches(matches):
    """
    Sauvegarde les matchs dans un fichier JSON.
    """

    os.makedirs(DATA_FOLDER, exist_ok=True)

    with open(MATCHES_FILE, "w", encoding="utf-8") as file:
        json.dump(matches, file, indent=4, ensure_ascii=False)


def load_matches():
    """
    Charge les matchs sauvegardés.
    """

    if not os.path.exists(MATCHES_FILE):
        return []

    with open(MATCHES_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def remove_duplicates(matches):
    """
    Supprime les doublons.
    """

    unique = []

    for match in matches:
        if match not in unique:
            unique.append(match)

    return unique


def get_team_matches(matches, team):
    """
    Retourne tous les matchs d'une équipe.
    """

    result = []

    for match in matches:

        if (
            match["home_team"] == team
            or match["away_team"] == team
        ):
            result.append(match)

    return result


def save_text_matches(text):
    """
    Lit un texte de matchs, enlève les doublons
    puis sauvegarde le résultat.
    """

    from analysis.parser import parse_matches

    matches = parse_matches(text)

    matches = remove_duplicates(matches)

    save_matches(matches)

    return len(matches)
