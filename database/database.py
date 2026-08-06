"""
Project Orion Predictor
Gestion avancée de la base de données
Version 0.2
"""

import json
import os
from datetime import datetime


DATA_FOLDER = "data"

MATCHES_FILE = os.path.join(
    DATA_FOLDER,
    "matches.json"
)


HISTORY_FILE = os.path.join(
    DATA_FOLDER,
    "imports_history.json"
)



def ensure_folder():

    os.makedirs(
        DATA_FOLDER,
        exist_ok=True
    )



def load_matches():

    ensure_folder()

    if not os.path.exists(MATCHES_FILE):
        return []

    with open(
        MATCHES_FILE,
        "r",
        encoding="utf-8"
    ) as file:

        return json.load(file)



def save_matches(matches):

    ensure_folder()

    with open(
        MATCHES_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            matches,
            file,
            indent=4,
            ensure_ascii=False
        )



def remove_duplicates(matches):

    unique = []

    for match in matches:

        if match not in unique:
            unique.append(match)

    return unique



def add_matches(new_matches):

    old_matches = load_matches()

    all_matches = (
        old_matches
        +
        new_matches
    )


    all_matches = remove_duplicates(
        all_matches
    )


    save_matches(
        all_matches
    )


    save_import_history(
        len(new_matches)
    )


    return len(all_matches)



def delete_all_matches():

    save_matches([])



def delete_last_matches(number):

    matches = load_matches()


    if number >= len(matches):

        save_matches([])

    else:

        matches = matches[number:]

        save_matches(matches)



def save_import_history(quantity):

    ensure_folder()


    history = []


    if os.path.exists(HISTORY_FILE):

        with open(
            HISTORY_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            history = json.load(file)



    history.append(
        {
            "date":
            datetime.now().strftime(
                "%d/%m/%Y %H:%M"
            ),

            "matches_added":
            quantity
        }
    )


    with open(
        HISTORY_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            history,
            file,
            indent=4,
            ensure_ascii=False
    )
