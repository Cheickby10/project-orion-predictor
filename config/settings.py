"""
Configuration de Project Orion Predictor
Version 0.1
"""

# Elo
INITIAL_RATING = 1500
K_FACTOR = 32

# Poisson
MAX_GOALS = 15

# Pondération des matchs
LAST_5_MATCHS_WEIGHT = 0.60
OLDER_MATCHS_WEIGHT = 0.40

# Paramètres futurs
HOME_ADVANTAGE = 0.0
USE_XG = False
USE_MONTE_CARLO = False
