import streamlit as st
st.set_page_config(page_title="Alerte-mail-App", layout="centered",page_icon="📊")
import logging


if "connect_ionos" not in st.session_state:
    st.session_state.connect_ionos = 0


logging.getLogger("streamlit").setLevel(logging.ERROR)




st.markdown("""
    <style>
    [data-testid="stSidebar"] {
    background: linear-gradient(-45deg, #3b5998, #192f6a, #4c669f, #1c1c2e);
    background-blend-mode: overlay;
    color: white;
    border-right: 1px solid rgba(255, 255, 255, 0.2);
    }
    [data-testid="stSidebar"] * {
        color: white !important;
    }
    .stApp {
        background: linear-gradient(-45deg, #3b5998, #192f6a, #4c669f, #1c1c2e);
        background-blend-mode: overlay;
        color: white;
    }
    @keyframes gradientBG {{
        0% {{background-position: 0% 50%;}}
        50% {{background-position: 100% 50%;}}
        100% {{background-position: 0% 50%;}}
    }}
    .stApp::before {{
        content: "";
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        backdrop-filter: blur(6px);
        z-index: 0;
    }}
    .block-container {{
        position: relative;
        z-index: 1;
    }}
    </style>
""", unsafe_allow_html=True)

st.markdown("""
<h1 style='text-align: center; color: white; font-size: 40px;'>
    Alerte Dashboard
</h1>
<h2 style='text-align:left; color: white; font-size: 30px;'>
    Analyse intelligente de vos e-mails avec filtres personnalisés et tableaux de bord
</h2>
""", unsafe_allow_html=True)

st.markdown("""
Bienvenue dans votre espace de visualisation d'e-mails d'alerte.

Cette application vous permet de :
- 🔐 **Vous authentifier** avec votre compte héberger par IONOS.
- 🔎 **Filtrer les e-mails** selon des critères avancés (expéditeur, date, pièce jointe...).
- 📂 **Visualiser et explorer la base** extraite.
- 📊 **Analyser les alertes** et obtenir des statistiques claires.

Utilisez le menu à gauche pour naviguer entre les différentes sections.
""")
if st.session_state.connect_ionos == 0:
    st.info("🔐 Veuillez vous authentifier via la page 'Authentification' pour commencer.")
else:
    st.success("✅ Vous êtes connecté. Vous pouvez accéder aux filtres.")



