"""
Project Orion Predictor
Moteur principal
Version 0.1
"""

from analysis.parser import parse_matches
from analysis.statistics import calculate_team_stats


def analyze(text):
    """
    Analyse une liste de matchs
    """

    matches = parse_matches(text)
    stats = calculate_team_stats(matches)

    return stats
