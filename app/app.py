import os
import sys

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, ROOT_DIR)

import streamlit as st

from database.database import load_matches
from analysis.statistics import calculate_team_stats
from models.predictor import Predictor

st.set_page_config(
    page_title="Project Orion Predictor",
    page_icon="⚽",
    layout="wide"
)

st.title("⚽ Project Orion Predictor")
st.write("FIFA FC 26 5v5")

matches = load_matches()

if len(matches) == 0:
    st.warning("Aucun match trouvé.")
    st.stop()

stats = calculate_team_stats(matches)

teams = sorted(stats.keys())

team1 = st.selectbox("Équipe A", teams)

team2 = st.selectbox("Équipe B", teams)

if st.button("Analyser"):

    predictor = Predictor(matches, stats)

    result = predictor.predict(team1, team2)

    if result is None:
        st.error("Impossible de générer une prédiction.")
    else:

        st.success("Analyse terminée")

        st.subheader("Classement Elo")

        st.write(
            f"{team1} : {result['home_rating']}"
        )

        st.write(
            f"{team2} : {result['away_rating']}"
        )

        st.subheader("Scores les plus probables")

        for score, probability in result["scores"]:

            st.write(
                f"{score[0]} - {score[1]} : {probability*100:.2f}%"
)
