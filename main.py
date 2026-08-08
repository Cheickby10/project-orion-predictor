"""
Project Orion Predictor
Point d'entrée principal
Version 0.2
"""

import subprocess
import sys


if __name__ == "__main__":

    subprocess.run(
        [
            sys.executable,
            "-m",
            "streamlit",
            "run",
            "app/app.py"
        ]
    )
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

    print(f"{len(matches)} matchs enregistrés.")


if __name__ == "__main__":
    main()
