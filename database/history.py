"""
Project Orion Predictor
Gestion de l'historique des imports
Version 0.2
"""

import json
import os


HISTORY_FILE = "data/imports_history.json"



def load_history():

    if not os.path.exists(HISTORY_FILE):
        return []

    with open(
        HISTORY_FILE,
        "r",
        encoding="utf-8"
    ) as file:

        return json.load(file)



def get_import_count():

    history = load_history()

    return len(history)



def get_total_imported_matches():

    history = load_history()

    total = 0

    for item in history:

        total += item.get(
            "matches_added",
            0
        )

    return total



def clear_history():

    with open(
        HISTORY_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            [],
            file
  )
