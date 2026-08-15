"""
Project Orion Predictor
Interface Streamlit
Version 0.3
"""

import os
import sys

# ============================================================
# CHEMIN RACINE DU PROJET
# ============================================================

ROOT_DIR = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        ".."
    )
)

if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)


import streamlit as st


from database.database import (
    load_matches,
    add_matches,
    delete_all_matches,
    delete_last_matches
)


from database.history import (
    load_history,
    get_import_count,
    get_total_imported_matches
)


from analysis.parser import parse_matches


from analysis.statistics import (
    calculate_team_stats
)


from analysis.form import (
    get_team_form
)


from models.predictor import (
    Predictor
)


# ============================================================
# CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Project Orion Predictor",
    page_icon="⚽",
    layout="wide"
)


# ============================================================
# STYLE
# ============================================================

st.markdown(
    """
    <style>

    .main-title {
        font-size: 36px;
        font-weight: 700;
        margin-bottom: 0;
    }

    .subtitle {
        color: #888888;
        font-size: 16px;
        margin-bottom: 25px;
    }

    .metric-card {
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #333333;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# CHARGEMENT DES DONNÉES
# ============================================================

matches = load_matches()

stats = calculate_team_stats(
    matches
)

teams = sorted(
    stats.keys()
)


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title(
    "⚽ Project Orion"
)

st.sidebar.caption(
    "FIFA FC 26 • 5v5"
)

page = st.sidebar.radio(
    "Navigation",
    [
        "🏠 Tableau de bord",
        "📥 Importer des matchs",
        "🎯 Nouvelle prédiction",
        "📊 Statistiques",
        "📚 Base de données"
    ]
)


# ============================================================
# TABLEAU DE BORD
# ============================================================

if page == "🏠 Tableau de bord":

    st.markdown(
        '<div class="main-title">'
        '⚽ Project Orion Predictor'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">'
        'FIFA FC 26 • 5v5'
        '</div>',
        unsafe_allow_html=True
    )


    col1, col2, col3 = st.columns(3)


    with col1:

        st.metric(
            "Matchs",
            len(matches)
        )


    with col2:

        st.metric(
            "Équipes",
            len(teams)
        )


    with col3:

        st.metric(
            "Importations",
            get_import_count()
        )


    st.divider()


    st.subheader(
        "État de la base"
    )


    if not matches:

        st.warning(
            "La base de données est vide."
        )

        st.info(
            "Va dans « Importer des matchs » "
            "pour ajouter tes premiers matchs."
        )

    else:

        st.success(
            f"{len(matches)} matchs disponibles."
        )

        st.write(
            f"Nombre total de matchs importés "
            f"depuis la création de la base : "
            f"{get_total_imported_matches()}"
        )

        st.subheader(
            "Équipes détectées"
        )

        st.write(
            ", ".join(teams)
        )


# ============================================================
# IMPORTATION
# ============================================================

elif page == "📥 Importer des matchs":

    st.title(
        "📥 Importer des matchs"
    )

    st.write(
        "Colle plusieurs matchs ci-dessous. "
        "Ils doivent être classés du plus récent "
        "au plus ancien."
    )


    text = st.text_area(
        "Matchs",
        height=300,
        placeholder=(
            "Galatasaray 5-2 Club Atlético de Madrid\n"
            "Napoli 1-3 Liverpool\n"
            "Real Madrid 5-1 Chelsea"
        )
    )


    if st.button(
        "📥 Importer les matchs",
        type="primary"
    ):

        if not text.strip():

            st.warning(
                "Aucun match n'a été saisi."
            )

        else:

            parsed_matches = parse_matches(
                text
            )


            if not parsed_matches:

                st.error(
                    "Aucun match valide n'a été détecté."
                )

            else:

                before = len(matches)

                total = add_matches(
                    parsed_matches
                )

                after = total

                added = after - before

                st.success(
                    f"Import terminé. "
                    f"Base actuelle : {after} matchs."
                )

                st.write(
                    f"Matchs détectés : "
                    f"{len(parsed_matches)}"
                )

                st.write(
                    f"Nouveaux matchs réellement ajoutés : "
                    f"{max(added, 0)}"
                )

                st.write(
                    f"Doublons ignorés : "
                    f"{max(len(parsed_matches) - added, 0)}"
                )

                st.rerun()


# ============================================================
# NOUVELLE PRÉDICTION
# ============================================================

elif page == "🎯 Nouvelle prédiction":

    st.title(
        "🎯 Nouvelle prédiction"
    )


    if len(teams) < 2:

        st.warning(
            "Il faut au moins deux équipes "
            "dans la base."
        )

        st.stop()


    # ========================================================
    # ÉQUIPES
    # ========================================================

    col1, col2 = st.columns(2)


    with col1:

        home_team = st.selectbox(
            "Équipe A",
            teams
        )


    with col2:

        away_options = [
            team
            for team in teams
            if team != home_team
        ]

        away_team = st.selectbox(
            "Équipe B",
            away_options
        )


    # ========================================================
    # PARAMÈTRES
    # ========================================================

    col1, col2 = st.columns(2)


    with col1:

        form_games = st.selectbox(
            "Forme récente",
            [5, 8, 10],
            index=2
        )


    with col2:

        st.selectbox(
            "Analyse Over/Under",
            [
                "Toutes les lignes"
            ],
            index=0
        )


    # ========================================================
    # ANALYSE
    # ========================================================

    if st.button(
        "🔎 Analyser le match",
        type="primary"
    ):

        predictor = Predictor(
            matches,
            stats
        )


        result = predictor.predict(
            home_team,
            away_team,
            form_games=form_games,
            over_under_lines=[
                3.5,
                4.5,
                5.5,
                6.5,
                7.5,
                8.5,
                9.5
            ]
        )


        if result is None:

            st.error(
                "Impossible de calculer la prédiction."
            )

        else:

            st.divider()


            st.subheader(
                f"{home_team} vs {away_team}"
            )


            # =================================================
            # 1N2
            # =================================================

            st.markdown(
                "### 🎯 Probabilités 1N2"
            )


            probabilities = (
                result["result_probabilities"]
            )


            col1, col2, col3 = st.columns(3)


            with col1:

                st.metric(
                    f"Victoire {home_team}",
                    f"{probabilities['home_win'] * 100:.1f}%"
                )


            with col2:

                st.metric(
                    "Nul",
                    f"{probabilities['draw'] * 100:.1f}%"
                )


            with col3:

                st.metric(
                    f"Victoire {away_team}",
                    f"{probabilities['away_win'] * 100:.1f}%"
                )


            # =================================================
            # ELO
            # =================================================

            st.markdown(
                "### 📊 Classement Elo"
            )


            col1, col2, col3 = st.columns(3)


            with col1:

                st.metric(
                    home_team,
                    result["home_rating"]
                )


            with col2:

                st.metric(
                    away_team,
                    result["away_rating"]
                )


            with col3:

                st.metric(
                    "Avantage Elo A",
                    f"{result['elo_home_advantage']:.1f}%"
                )


            # =================================================
            # BUTS ATTENDUS
            # =================================================

            st.markdown(
                "### ⚽ Buts attendus"
            )


            expected = result[
                "expected_goals"
            ]


            col1, col2, col3 = st.columns(3)


            with col1:

                st.metric(
                    home_team,
                    expected["home"]
                )


            with col2:

                st.metric(
                    away_team,
                    expected["away"]
                )


            with col3:

                st.metric(
                    "Total attendu",
                    expected["total"]
                )


            # =================================================
            # SCORES
            # =================================================

            st.markdown(
                "### 🎯 Scores les plus probables"
            )


            for score, probability in result["scores"]:

                st.write(
                    f"**{score[0]} - {score[1]}** "
                    f"→ {probability * 100:.2f}%"
                )


            # =================================================
            # BTTS
            # =================================================

            st.markdown(
                "### ⚽ BTTS"
            )


            btts = result["btts"]


            col1, col2, col3, col4 = st.columns(4)


            with col1:

                st.metric(
                    "BTTS 1+",
                    f"{btts['1']['yes'] * 100:.1f}%"
                )


            with col2:

                st.metric(
                    "BTTS 2+",
                    f"{btts['2']['yes'] * 100:.1f}%"
                )


            with col3:

                st.metric(
                    "BTTS 3+",
                    f"{btts['3']['yes'] * 100:.1f}%"
                )


            with col4:

                st.metric(
                    "BTTS 4+",
                    f"{btts['4']['yes'] * 100:.1f}%"
                )


            # =================================================
            # OVER / UNDER
            # =================================================

            st.markdown(
                "### 📊 Over / Under"
            )


            over_under = result[
                "over_under"
            ]


            for current_line in [
                3.5,
                4.5,
                5.5,
                6.5,
                7.5,
                8.5,
                9.5
            ]:

                line_data = over_under[
                    str(current_line)
                ]


                col1, col2, col3 = st.columns(3)


                with col1:

                    st.write(
                        f"**Ligne {current_line}**"
                    )


                with col2:

                    st.metric(
                        f"Over {current_line}",
                        f"{line_data['over'] * 100:.1f}%"
                    )


                with col3:

                    st.metric(
                        f"Under {current_line}",
                        f"{line_data['under'] * 100:.1f}%"
                    )


            # =================================================
            # FORME
            # =================================================

            st.markdown(
                f"### 📈 Forme — "
                f"{form_games} derniers matchs"
            )


            home_form = result[
                "home_form"
            ]

            away_form = result[
                "away_form"
            ]


            col1, col2 = st.columns(2)


            with col1:

                st.write(
                    f"**{home_team}**"
                )

                st.write(
                    f"Forme : "
                    f"{home_form['form_score']:.1f}%"
                )

                st.write(
                    f"Buts marqués/match : "
                    f"{home_form['average_goals_for']:.2f}"
                )

                st.write(
                    f"Buts encaissés/match : "
                    f"{home_form['average_goals_against']:.2f}"
                )


            with col2:

                st.write(
                    f"**{away_team}**"
                )

                st.write(
                    f"Forme : "
                    f"{away_form['form_score']:.1f}%"
                )

                st.write(
                    f"Buts marqués/match : "
                    f"{away_form['average_goals_for']:.2f}"
                )

                st.write(
                    f"Buts encaissés/match : "
                    f"{away_form['average_goals_against']:.2f}"
                )


            # =================================================
            # H2H
            # =================================================

            st.markdown(
                "### 🤝 H2H"
            )


            h2h = result["h2h"]


            if h2h["matches"] == 0:

                st.info(
                    "Aucun H2H disponible."
                )

            else:

                st.write(
                    f"Matchs H2H analysés : "
                    f"**{h2h['matches']}**"
                )

                st.write(
                    f"Buts pondérés {home_team} : "
                    f"**{h2h['weighted_team_a_goals']:.2f}**"
                )

                st.write(
                    f"Buts pondérés {away_team} : "
                    f"**{h2h['weighted_team_b_goals']:.2f}**"
                )


            # =================================================
            # CONFIANCE
            # =================================================

            st.markdown(
                "### 🧠 Indice de confiance"
            )


            st.metric(
                "Confiance du modèle",
                f"{result['confidence']:.1f}%"
            )


# ============================================================
# STATISTIQUES
# ============================================================

elif page == "📊 Statistiques":

    st.title(
        "📊 Statistiques des équipes"
    )


    if not teams:

        st.info(
            "Aucune équipe disponible."
        )

    else:

        selected_team = st.selectbox(
            "Choisir une équipe",
            teams
        )


        team = stats[
            selected_team
        ]


        st.subheader(
            selected_team
        )


        col1, col2, col3, col4 = st.columns(4)


        with col1:

            st.metric(
                "Matchs",
                team["played"]
            )


        with col2:

            st.metric(
                "Victoires",
                team["wins"]
            )


        with col3:

            st.metric(
                "Nuls",
                team["draws"]
            )


        with col4:

            st.metric(
                "Défaites",
                team["losses"]
            )


        col1, col2, col3 = st.columns(3)


        with col1:

            st.metric(
                "Buts marqués",
                team["goals_for"]
            )


        with col2:

            st.metric(
                "Buts encaissés",
                team["goals_against"]
            )


        with col3:

            st.metric(
                "Différence",
                team["goal_difference"]
            )


        st.write(
            f"Attaque moyenne : "
            f"**{team['attack_average']:.2f}**"
        )


        st.write(
            f"Défense moyenne : "
            f"**{team['defense_average']:.2f}**"
        )


        st.write(
            f"Taux de victoire : "
            f"**{team['win_rate']:.1f}%**"
        )


        st.subheader(
            "Forme récente"
        )


        form_games = st.selectbox(
            "Nombre de matchs",
            [5, 8, 10],
            key="stats_form_games"
        )


        form = get_team_form(
            matches,
            selected_team,
            form_games
        )


        st.write(
            f"Forme : "
            f"**{form['form_score']:.1f}%**"
        )


        st.write(
            f"Buts marqués/match : "
            f"**{form['average_goals_for']:.2f}**"
        )


        st.write(
            f"Buts encaissés/match : "
            f"**{form['average_goals_against']:.2f}**"
        )


# ============================================================
# BASE DE DONNÉES
# ============================================================

elif page == "📚 Base de données":

    st.title(
        "📚 Base de données"
    )


    st.metric(
        "Nombre de matchs",
        len(matches)
    )


    st.metric(
        "Nombre d'équipes",
        len(teams)
    )


    st.divider()


    # ========================================================
    # MATCHS
    # ========================================================

    if matches:

        st.subheader(
            "Matchs enregistrés"
        )


        display_matches = []


        for index, match in enumerate(
            matches
        ):

            display_matches.append(
                {
                    "N°": index + 1,

                    "Équipe A":
                        match["home_team"],

                    "Score":
                        f"{match['home_goals']}-"
                        f"{match['away_goals']}",

                    "Équipe B":
                        match["away_team"]
                }
            )


        st.dataframe(
            display_matches,
            use_container_width=True,
            hide_index=True
        )


    else:

        st.info(
            "La base est vide."
        )


    st.divider()


    # ========================================================
    # SUPPRESSION
    # ========================================================

    st.subheader(
        "🗑️ Gestion des données"
    )


    delete_number = st.number_input(
        "Nombre de matchs à supprimer "
        "depuis le début de la liste",
        min_value=1,
        max_value=max(len(matches), 1),
        value=min(
            10,
            max(len(matches), 1)
        ),
        step=1
    )


    if st.button(
        "🗑️ Supprimer les matchs sélectionnés"
    ):

        if not matches:

            st.warning(
                "La base est déjà vide."
            )

        else:

            delete_last_matches(
                int(delete_number)
            )

            st.success(
                f"{delete_number} matchs supprimés."
            )

            st.rerun()


    st.divider()


    # ========================================================
    # SUPPRESSION TOTALE
    # ========================================================

    st.subheader(
        "⚠️ Zone dangereuse"
    )


    confirm = st.checkbox(
        "Je confirme vouloir supprimer "
        "toute la base de données."
    )


    if st.button(
        "🗑️ Réinitialiser toute la base"
    ):

        if not confirm:

            st.warning(
                "Coche la case de confirmation."
            )

        else:

            delete_all_matches()

            st.success(
                "Base de données réinitialisée."
            )

            st.rerun()


    # ========================================================
    # HISTORIQUE
    # ========================================================

    st.divider()


    st.subheader(
        "📜 Historique des imports"
    )


    history = load_history()


    if not history:

        st.info(
            "Aucun import enregistré."
        )

    else:

        st.dataframe(
            history,
            use_container_width=True,
            hide_index=True
)
