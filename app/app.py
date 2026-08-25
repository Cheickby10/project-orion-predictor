"""
Project Orion Predictor
Interface Streamlit
Version 0.3.5
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
    Predictor )

from analysis.backtesting import ( Backtester )

# ============================================================
# CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Project Orion",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# STYLE
# ============================================================

st.markdown(
    """
    <style>

    /* =======================================================
       GLOBAL
       ======================================================= */

    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1400px;
    }

    /* =======================================================
       TITRES
       ======================================================= */

    .orion-title {
        font-size: 42px;
        font-weight: 800;
        letter-spacing: -1px;
        margin-bottom: 2px;
    }

    .orion-subtitle {
        font-size: 16px;
        color: #8b949e;
        margin-bottom: 25px;
    }

    .section-title {
        font-size: 24px;
        font-weight: 700;
        margin-top: 15px;
        margin-bottom: 12px;
    }

    /* =======================================================
       HERO
       ======================================================= */

    .hero {
        padding: 28px;
        border-radius: 18px;
        border: 1px solid rgba(255,255,255,0.08);
        background:
            linear-gradient(
                135deg,
                rgba(40,40,40,0.95),
                rgba(20,20,20,0.95)
            );
        margin-bottom: 25px;
    }

    .hero-title {
        font-size: 34px;
        font-weight: 800;
        margin-bottom: 4px;
    }

    .hero-subtitle {
        color: #9ca3af;
        font-size: 15px;
    }

    /* =======================================================
       MATCH HEADER
       ======================================================= */

    .match-card {
        padding: 25px;
        border-radius: 18px;
        border: 1px solid rgba(255,255,255,0.09);
        background: rgba(255,255,255,0.025);
        text-align: center;
        margin-bottom: 25px;
    }

    .team-name {
        font-size: 22px;
        font-weight: 700;
    }

    .vs-text {
        font-size: 15px;
        color: #888888;
        margin: 8px 0;
    }

    /* =======================================================
       RESULTAT
       ======================================================= */

    .result-card {
        padding: 20px;
        border-radius: 15px;
        border: 1px solid rgba(255,255,255,0.08);
        background: rgba(255,255,255,0.025);
        margin-bottom: 15px;
    }

    .result-title {
        font-size: 14px;
        color: #8b949e;
        margin-bottom: 6px;
    }

    .result-value {
        font-size: 30px;
        font-weight: 800;
    }

    /* =======================================================
       SCORE CARD
       ======================================================= */

    .score-card {
        padding: 14px;
        border-radius: 12px;
        border: 1px solid rgba(255,255,255,0.08);
        background: rgba(255,255,255,0.025);
        text-align: center;
        margin-bottom: 10px;
    }

    .score {
        font-size: 23px;
        font-weight: 800;
    }

    .score-prob {
        color: #9ca3af;
        font-size: 14px;
    }

    /* =======================================================
       INFO CARD
       ======================================================= */

    .info-card {
        padding: 18px;
        border-radius: 14px;
        border: 1px solid rgba(255,255,255,0.08);
        background: rgba(255,255,255,0.02);
        margin-bottom: 15px;
    }

    .info-label {
        color: #8b949e;
        font-size: 13px;
    }

    .info-value {
        font-size: 21px;
        font-weight: 700;
    }

    /* =======================================================
       BADGES
       ======================================================= */

    .badge {
        display: inline-block;
        padding: 5px 10px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 700;
        margin-right: 5px;
    }

    /* =======================================================
       SIDEBAR
       ======================================================= */

    section[data-testid="stSidebar"] {
        border-right: 1px solid rgba(255,255,255,0.07);
    }

    .sidebar-brand {
        font-size: 25px;
        font-weight: 800;
        margin-bottom: 0;
    }

    .sidebar-version {
        color: #8b949e;
        font-size: 13px;
        margin-bottom: 20px;
    }

    /* =======================================================
       MOBILE
       ======================================================= */

    @media (max-width: 768px) {

        .block-container {
            padding-left: 1rem;
            padding-right: 1rem;
        }

        .orion-title {
            font-size: 30px;
        }

        .hero-title {
            font-size: 27px;
        }

        .team-name {
            font-size: 18px;
        }

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

st.sidebar.markdown(
    '<div class="sidebar-brand">⚽ Project Orion</div>',
    unsafe_allow_html=True
)

st.sidebar.markdown(
    '<div class="sidebar-version">'
    'FIFA FC 26 • 5v5 • v0.3.5'
    '</div>',
    unsafe_allow_html=True
)

page = st.sidebar.radio(
    "Navigation",
    [
        "🏠 Tableau de bord",
        "📥 Importer des matchs",
        "🎯 Nouvelle prédiction",
        "📊 Statistiques",
        "📈 Backtesting",
        "📚 Base de données"
    ]
)


# ============================================================
# TABLEAU DE BORD
# ============================================================

if page == "🏠 Tableau de bord":

    st.markdown(
        """
        <div class="hero">
            <div class="hero-title">
                ⚽ Project Orion Predictor
            </div>
            <div class="hero-subtitle">
                Moteur d'analyse FIFA FC 26 • 5v5
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


    # ========================================================
    # CARTES PRINCIPALES
    # ========================================================

    col1, col2, col3, col4 = st.columns(4)


    with col1:

        st.metric(
            "⚽ Matchs",
            len(matches)
        )


    with col2:

        st.metric(
            "👥 Équipes",
            len(teams)
        )


    with col3:

        st.metric(
            "📥 Importations",
            get_import_count()
        )


    with col4:

        st.metric(
            "📚 Total importé",
            get_total_imported_matches()
        )


    st.divider()


    # ========================================================
    # ÉTAT
    # ========================================================

    st.markdown(
        '<div class="section-title">'
        '📡 État du système'
        '</div>',
        unsafe_allow_html=True
    )


    if not matches:

        st.warning(
            "La base de données est vide."
        )

        st.info(
            "Commence par importer des matchs "
            "dans la section « Importer des matchs »."
        )

    else:

        st.success(
            f"🟢 Système opérationnel — "
            f"{len(matches)} matchs disponibles."
        )


        # ====================================================
        # INFORMATIONS BASE
        # ====================================================

        col1, col2 = st.columns(2)


        with col1:

            st.markdown(
                '<div class="info-card">'
                '<div class="info-label">'
                'Matchs disponibles'
                '</div>'
                f'<div class="info-value">'
                f'{len(matches)}'
                '</div>'
                '</div>',
                unsafe_allow_html=True
            )


        with col2:

            st.markdown(
                '<div class="info-card">'
                '<div class="info-label">'
                'Équipes détectées'
                '</div>'
                f'<div class="info-value">'
                f'{len(teams)}'
                '</div>'
                '</div>',
                unsafe_allow_html=True
            )


        st.markdown(
            '<div class="section-title">'
            '👥 Équipes disponibles'
            '</div>',
            unsafe_allow_html=True
        )


        st.write(
            ", ".join(teams)
        )


# ============================================================
# IMPORTATION
# ============================================================

elif page == "📥 Importer des matchs":

    st.markdown(
        """
        <div class="hero">
            <div class="hero-title">
                📥 Importer des matchs
            </div>
            <div class="hero-subtitle">
                Alimente la base de données de Project Orion
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


    st.info(
        "Les matchs doivent être classés du plus récent "
        "au plus ancien."
    )


    text = st.text_area(
        "Colle tes matchs ici",
        height=300,
        placeholder=(
            "Galatasaray 5-2 Club Atlético de Madrid\n"
            "Napoli 1-3 Liverpool\n"
            "Real Madrid 5-1 Chelsea"
        )
    )


    st.caption(
        "💡 Tu peux importer plusieurs matchs en une seule fois."
    )


    if st.button(
        "📥 Importer les matchs",
        type="primary",
        use_container_width=True
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
                    f"Import terminé — base actuelle : "
                    f"{after} matchs."
                )


                col1, col2, col3 = st.columns(3)


                with col1:

                    st.metric(
                        "Matchs détectés",
                        len(parsed_matches)
                    )


                with col2:

                    st.metric(
                        "Nouveaux matchs",
                        max(added, 0)
                    )


                with col3:

                    st.metric(
                        "Doublons",
                        max(
                            len(parsed_matches) - added,
                            0
                        )
                    )


                st.rerun()


# ============================================================
# NOUVELLE PRÉDICTION
# ============================================================

elif page == "🎯 Nouvelle prédiction":

    st.markdown(
        """
        <div class="hero">
            <div class="hero-title">
                🎯 Nouvelle analyse
            </div>
            <div class="hero-subtitle">
                Analyse statistique complète du match
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


    if len(teams) < 2:

        st.warning(
            "Il faut au moins deux équipes "
            "dans la base pour lancer une analyse."
        )

        st.stop()


    # ========================================================
    # SÉLECTION DES ÉQUIPES
    # ========================================================

    col1, col2 = st.columns(2)


    with col1:

        home_team = st.selectbox(
            "🏠 Équipe A",
            teams
        )


    with col2:

        away_options = [
            team
            for team in teams
            if team != home_team
        ]


        away_team = st.selectbox(
            "✈️ Équipe B",
            away_options
        )


    # ========================================================
    # PARAMÈTRES
    # ========================================================

    col1, col2 = st.columns(2)


    with col1:

        form_games = st.selectbox(
            "📈 Forme récente",
            [5, 8, 10],
            index=2
        )


    with col2:

        st.selectbox(
            "📊 Analyse Over/Under",
            ["Toutes les lignes"],
            index=0
        )


    st.caption(
        "Le moteur analysera automatiquement "
        "les lignes Over/Under de 3.5 à 9.5."
    )


    # ========================================================
    # BOUTON
    # ========================================================

    if st.button(
        "🔎 ANALYSER LE MATCH",
        type="primary",
        use_container_width=True
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


            # =================================================
            # MATCH HEADER
            # =================================================

            st.markdown(
                f"""
                <div class="match-card">
                    <div class="team-name">
                        {home_team}
                    </div>
                    <div class="vs-text">
                        VS
                    </div>
                    <div class="team-name">
                        {away_team}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )


            # =================================================
            # SYNTHÈSE ORION
            # =================================================

            probabilities = (
                result["result_probabilities"]
            )


            expected = result[
                "expected_goals"
            ]


            btts = result[
                "btts"
            ]


            confidence = result[
                "confidence"
            ]


            best_result = max(
                [
                    (
                        probabilities["home_win"],
                        f"Victoire {home_team}"
                    ),
                    (
                        probabilities["draw"],
                        "Match nul"
                    ),
                    (
                        probabilities["away_win"],
                        f"Victoire {away_team}"
                    )
                ],
                key=lambda x: x[0]
            )


            st.markdown(
                '<div class="section-title">'
                '🧠 Synthèse Orion'
                '</div>',
                unsafe_allow_html=True
            )


            col1, col2, col3, col4 = st.columns(4)


            with col1:

                st.metric(
                    "Projection principale",
                    best_result[1],
                    f"{best_result[0] * 100:.1f}%"
                )


            with col2:

                st.metric(
                    "Buts attendus",
                    expected["total"]
                )


            with col3:

                st.metric(
                    "BTTS 1+",
                    f"{btts['1']['yes'] * 100:.1f}%"
                )


            with col4:

                st.metric(
                    "Confiance",
                    f"{confidence:.1f}%"
                )


            st.divider()


            # =================================================
            # 1N2
            # =================================================

            st.markdown(
                '<div class="section-title">'
                '🎯 Probabilités 1N2'
                '</div>',
                unsafe_allow_html=True
            )


            col1, col2, col3 = st.columns(3)


            with col1:

                st.metric(
                    f"🏠 {home_team}",
                    f"{probabilities['home_win'] * 100:.1f}%"
                )


            with col2:

                st.metric(
                    "⚪ Nul",
                    f"{probabilities['draw'] * 100:.1f}%"
                )


            with col3:

                st.metric(
                    f"✈️ {away_team}",
                    f"{probabilities['away_win'] * 100:.1f}%"
                )


            # =================================================
            # ELO
            # =================================================

            st.markdown(
                '<div class="section-title">'
                '📊 Classement Elo'
                '</div>',
                unsafe_allow_html=True
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
                '<div class="section-title">'
                '⚽ Buts attendus'
                '</div>',
                unsafe_allow_html=True
            )


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
                    "Total",
                    expected["total"]
                )


            # =================================================
            # SCORES
            # =================================================

            st.markdown(
                '<div class="section-title">'
                '🎯 Scores les plus probables'
                '</div>',
                unsafe_allow_html=True
            )


            scores = result[
                "scores"
            ]


            score_columns = st.columns(
                min(len(scores), 3)
            )


            for index, (
                score,
                probability
            ) in enumerate(scores):

                with score_columns[
                    index % len(score_columns)
                ]:

                    st.markdown(
                        f"""
                        <div class="score-card">
                            <div class="score">
                                {score[0]} - {score[1]}
                            </div>
                            <div class="score-prob">
                                {probability * 100:.2f}%
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )


            # =================================================
            # BTTS
            # =================================================

            st.markdown(
                '<div class="section-title">'
                '⚽ BTTS'
                '</div>',
                unsafe_allow_html=True
            )


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
                '<div class="section-title">'
                '📊 Over / Under'
                '</div>',
                unsafe_allow_html=True
            )


            over_under = result[
                "over_under"
            ]


            over_under_rows = []


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


                over_under_rows.append(
                    {
                        "Ligne": current_line,
                        "Over": (
                            f"{line_data['over'] * 100:.1f}%"
                        ),
                        "Under": (
                            f"{line_data['under'] * 100:.1f}%"
                        )
                    }
                )


            st.dataframe(
                over_under_rows,
                use_container_width=True,
                hide_index=True
            )


            # =================================================
            # FORME
            # =================================================

            st.markdown(
                f'<div class="section-title">'
                f'📈 Forme — {form_games} derniers matchs'
                f'</div>',
                unsafe_allow_html=True
            )


            home_form = result[
                "home_form"
            ]


            away_form = result[
                "away_form"
            ]


            col1, col2 = st.columns(2)


            with col1:

                st.markdown(
                    f"### 🏠 {home_team}"
                )

                st.metric(
                    "Forme",
                    f"{home_form['form_score']:.1f}%"
                )

                st.write(
                    f"⚽ Buts marqués/match : "
                    f"**{home_form['average_goals_for']:.2f}**"
                )

                st.write(
                    f"🛡️ Buts encaissés/match : "
                    f"**{home_form['average_goals_against']:.2f}**"
                )


            with col2:

                st.markdown(
                    f"### ✈️ {away_team}"
                )

                st.metric(
                    "Forme",
                    f"{away_form['form_score']:.1f}%"
                )

                st.write(
                    f"⚽ Buts marqués/match : "
                    f"**{away_form['average_goals_for']:.2f}**"
                )

                st.write(
                    f"🛡️ Buts encaissés/match : "
                    f"**{away_form['average_goals_against']:.2f}**"
                )


            # =================================================
            # H2H
            # =================================================

            st.markdown(
                '<div class="section-title">'
                '🤝 Face-à-face (H2H)'
                '</div>',
                unsafe_allow_html=True
            )


            h2h = result[
                "h2h"
            ]


            if h2h["matches"] == 0:

                st.info(
                    "Aucun historique H2H disponible "
                    "pour ces deux équipes."
                )

            else:

                col1, col2, col3 = st.columns(3)


                with col1:

                    st.metric(
                        "Matchs H2H",
                        h2h["matches"]
                    )


                with col2:

                    st.metric(
                        f"Buts {home_team}",
                        f"{h2h['weighted_team_a_goals']:.2f}"
                    )


                with col3:

                    st.metric(
                        f"Buts {away_team}",
                        f"{h2h['weighted_team_b_goals']:.2f}"
                    )


            # =================================================
            # CONFIANCE
            # =================================================

            st.markdown(
                '<div class="section-title">'
                '🧠 Fiabilité du modèle'
                '</div>',
                unsafe_allow_html=True
            )


            st.progress(
                max(
                    0.0,
                    min(
                        1.0,
                        confidence / 100
                    )
                )
            )


            st.metric(
                "Indice de confiance",
                f"{confidence:.1f}%"
            )


# ============================================================
# STATISTIQUES
# ============================================================

elif page == "📊 Statistiques":

    st.markdown(
        """
        <div class="hero">
            <div class="hero-title">
                📊 Statistiques
            </div>
            <div class="hero-subtitle">
                Analyse détaillée des équipes de la base
            </div>
        </div>
        """,
        unsafe_allow_html=True
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


        st.markdown(
            f"### ⚽ {selected_team}"
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
                "⚽ Buts marqués",
                team["goals_for"]
            )


        with col2:

            st.metric(
                "🛡️ Buts encaissés",
                team["goals_against"]
            )


        with col3:

            st.metric(
                "Différence",
                team["goal_difference"]
            )


        st.divider()


        col1, col2, col3 = st.columns(3)


        with col1:

            st.metric(
                "Attaque moyenne",
                f"{team['attack_average']:.2f}"
            )


        with col2:

            st.metric(
                "Défense moyenne",
                f"{team['defense_average']:.2f}"
            )


        with col3:

            st.metric(
                "Taux de victoire",
                f"{team['win_rate']:.1f}%"
            )


        st.divider()


        st.markdown(
            "### 📈 Forme récente"
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


        col1, col2, col3 = st.columns(3)


        with col1:

            st.metric(
                "Forme",
                f"{form['form_score']:.1f}%"
            )


        with col2:

            st.metric(
                "Buts marqués/match",
                f"{form['average_goals_for']:.2f}"
            )


        with col3:

            st.metric(
                "Buts encaissés/match",
                f"{form['average_goals_against']:.2f}"
            )
            # ============================================================
# BACKTESTING
# ============================================================

elif page == "📈 Backtesting":

    st.title("📈 Backtesting")

    st.write(
        "Évalue les performances de Project Orion "
        "sur des matchs historiques."
    )

    st.info(
        "Le modèle utilise uniquement les matchs disponibles "
        "avant chaque match testé afin d'éviter la fuite de données."
    )

    if len(matches) < 25:

        st.warning(
            f"Il faut idéalement au moins 25 matchs "
            f"pour lancer un backtest fiable. "
            f"Base actuelle : {len(matches)} matchs."
        )

    else:

        col1, col2 = st.columns(2)

        with col1:

            min_history = st.number_input(
                "Historique minimum",
                min_value=10,
                max_value=max(10, len(matches) - 1),
                value=min(
                    20,
                    max(10, len(matches) - 1)
                ),
                step=5
            )

        with col2:

            form_games_bt = st.selectbox(
                "Matchs utilisés pour la forme",
                [5, 8, 10],
                index=2,
                key="backtest_form_games"
            )


        if st.button(
            "🚀 Lancer le backtest",
            type="primary"
        ):

            with st.spinner(
                "Analyse des matchs historiques..."
            ):

                backtester = Backtester(
                    matches
                )

                results = backtester.run(
                    min_history=int(
                        min_history
                    ),
                    form_games=int(
                        form_games_bt
                    )
                )

                summary = (
                    backtester.summarize(
                        results
                    )
                )


            if not results:

                st.error(
                    "Aucun match n'a pu être testé."
                )

            else:

                st.success(
                    f"Backtest terminé : "
                    f"{len(results)} matchs analysés."
                )


                st.divider()


                # =================================================
                # RÉSUMÉ
                # =================================================

                st.subheader(
                    "📊 Résultats globaux"
                )


                col1, col2, col3 = st.columns(3)


                with col1:

                    st.metric(
                        "Matchs testés",
                        summary[
                            "matches_tested"
                        ]
                    )


                with col2:

                    st.metric(
                        "Précision 1N2",
                        f"{summary['accuracy_1x2']:.1f}%"
                    )


                with col3:

                    st.metric(
                        "Score exact",
                        f"{summary['exact_score_accuracy']:.1f}%"
                    )


                col1, col2, col3, col4 = st.columns(4)


                with col1:

                    st.metric(
                        "Over 3.5",
                        f"{summary['over_3_5_accuracy']:.1f}%"
                    )


                with col2:

                    st.metric(
                        "BTTS 1+",
                        f"{summary['btts_accuracy']:.1f}%"
                    )


                with col3:

                    st.metric(
                        "Erreur buts",
                        f"{summary['average_goal_error']:.2f}"
                    )


                with col4:

                    st.metric(
                        "Confiance moyenne",
                        f"{summary['average_confidence']:.1f}%"
                    )


                st.divider()


                # =================================================
                # TABLEAU
                # =================================================

                st.subheader(
                    "📋 Détail des prédictions"
                )


                display_results = []


                for item in results:

                    actual_score = (
                        f"{item['actual_score'][0]}"
                        f"-"
                        f"{item['actual_score'][1]}"
                    )


                    predicted_score = "-"


                    if item["top_score"]:

                        predicted_score = (
                            f"{item['top_score'][0]}"
                            f"-"
                            f"{item['top_score'][1]}"
                        )


                    display_results.append(
                        {
                            "Match":
                                f"{item['home_team']} "
                                f"vs "
                                f"{item['away_team']}",

                            "Réel":
                                actual_score,

                            "Score prédit":
                                predicted_score,

                            "1N2":
                                "✅"
                                if item["correct_1x2"]
                                else "❌",

                            "Score exact":
                                "✅"
                                if item["exact_score"]
                                else "❌",

                            "Over 3.5":
                                "✅"
                                if item[
                                    "over_3_5_correct"
                                ]
                                else "❌",

                            "BTTS 1+":
                                "✅"
                                if item[
                                    "btts_1_correct"
                                ]
                                else "❌",

                            "Confiance":
                                f"{item['confidence']:.1f}%"
                        }
                    )


                st.dataframe(
                    display_results,
                    use_container_width=True,
                    hide_index=True
            )


# ============================================================
# BASE DE DONNÉES
# ============================================================

elif page == "📚 Base de données":

    st.markdown(
        """
        <div class="hero">
            <div class="hero-title">
                📚 Base de données
            </div>
            <div class="hero-subtitle">
                Gestion des matchs et historique des imports
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


    col1, col2 = st.columns(2)


    with col1:

        st.metric(
            "⚽ Matchs",
            len(matches)
        )


    with col2:

        st.metric(
            "👥 Équipes",
            len(teams)
        )


    st.divider()


    # ========================================================
    # MATCHS
    # ========================================================

    if matches:

        st.markdown(
            "### 📋 Matchs enregistrés"
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

    st.markdown(
        "### 🗑️ Gestion des données"
    )


    delete_number = st.number_input(
        "Nombre de matchs à supprimer "
        "depuis le début de la liste",
        min_value=1,
        max_value=max(
            len(matches),
            1
        ),
        value=min(
            10,
            max(
                len(matches),
                1
            )
        ),
        step=1
    )


    if st.button(
        "🗑️ Supprimer les matchs sélectionnés",
        use_container_width=True
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

    st.markdown(
        "### ⚠️ Zone dangereuse"
    )


    confirm = st.checkbox(
        "Je confirme vouloir supprimer "
        "toute la base de données."
    )


    if st.button(
        "🗑️ Réinitialiser toute la base",
        use_container_width=True
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


    st.divider()


    # ========================================================
    # HISTORIQUE
    # ========================================================

    st.markdown(
        "### 📜 Historique des imports"
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
