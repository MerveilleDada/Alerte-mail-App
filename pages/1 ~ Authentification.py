import streamlit as st
st.set_page_config(page_title="Alerte-mail-App", layout="centered",page_icon="📊")
import logging
import socket
import imaplib
from imap_tools import MailBox
import imap_tools
import pandas as pd
#Importations indispensables

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
    
    </style>
""", unsafe_allow_html=True)

if "compteur_ionos" not in st.session_state:
    st.session_state.compteur_ionos = 0
if 'base' not in st.session_state:
    st.session_state.base=pd.DataFrame()
if "connect_ionos" not in st.session_state:
    st.session_state.connect_ionos = 0

if "mail" not in st.session_state:
    st.session_state.mail = None
if "username" not in st.session_state:
    st.session_state.username = ""
if "password" not in st.session_state:
    st.session_state.password = ""
logging.getLogger("streamlit").setLevel(logging.ERROR)


if st.button("Se connecter",type="primary"):
    st.session_state.compteur_ionos = 1
    if st.session_state.connect_ionos == 1:
        st.info("Déjà authentifier. Déconnectez ce compte pour en authentifier un autre")


if st.session_state.compteur_ionos == 1:
    st.session_state.username = st.text_input("Adresse e-mail")
    st.session_state.password = st.text_input("Mot de passe")
    with st.spinner("Connexion..."):
        if st.button("OK",type="primary"):
            imap_server = "imap.ionos.fr"
            port = 993
            try:
                st.session_state.mail = MailBox(f"{imap_server}", port)
                st.session_state.mail.login(st.session_state.username, st.session_state.password)
                #st.session_state.mail.select("inbox")
                st.session_state.connect_ionos = 1
                st.success("Connexion réussie")
            except imaplib.IMAP4.error as e:
                st.error("Échec de connexion")
                st.code(e)
            except socket.gaierror as f:
                st.error("Hors ligne")
                st.code(f)
            except imap_tools.errors.MailboxLoginError as i:
                st.error("Échec de connexion")
                st.code(i)

if st.session_state.connect_ionos==1:
    if st.sidebar.button("🔒 Se déconnecter",type="primary"):
        try:
            st.session_state.mail.logout()
            st.session_state.connect_ionos = 0
            st.success("🔁 Déconnecté avec succès. Rechargez pour réinitialiser l'app.")
        except socket.gaierror as f:
            st.error("Hors ligne")
        except imaplib.IMAP4.abort as l:
            st.error("Délai de connexion dépassé")
            st.session_state.connect_ionos = 0
