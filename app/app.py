"""
Project Orion Predictor
Interface utilisateur
Version 0.1
"""

import streamlit as st

from database.database import load_matches
from analysis.statistics import calculate_team_stats
from models.predictor import predict


st.title("🚀 Project Orion Predictor")
st.subheader("FIFA FC 26 5v5")


matches = load_matches()


if not matches:
    st.warning(
        "Aucun match chargé"
    )

else:

    stats = calculate_team_stats(matches)

    teams = list(stats.keys())


    team1 = st.selectbox(
        "Équipe A",
        teams
    )


    team2 = st.selectbox(
        "Équipe B",
        teams
    )


    if st.button("Analyser"):

        result = predict(
            team1,
            team2,
            stats
        )


        st.success(
            "Analyse terminée"
        )


        st.write(
            "Scores les plus probables :"
        )


        for score, probability in result["scores"]:
            st.write(
                score,
                round(probability*100,2),
                "%"
  )
