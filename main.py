"""
Project Orion Predictor
Lancement du programme
Version 0.1
"""

from analysis.parser import parse_matches
from database.database import (
    save_matches,
    remove_duplicates
)


def main():

    with open(
        "data/matches.txt",
        "r",
        encoding="utf-8"
    ) as file:

        text = file.read()


    matches = parse_matches(text)

    matches = remove_duplicates(matches)

    save_matches(matches)


    print(
        "Project Orion Predictor lancé"
    )

    print(
        len(matches),
        "matchs chargés"
    )


if __name__ == "__main__":
    main()
