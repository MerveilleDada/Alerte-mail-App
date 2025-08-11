import streamlit as st
st.set_page_config(page_title="Alerte-mail-App", layout="centered",page_icon="📊")
import logging
import socket
import imaplib
from imap_tools import MailBox
import imap_tools
import pandas as pd
#Importations indispensables
imaplib.IMAP4._encoding = 'utf-8'
imaplib.IMAP4_SSL._encoding = 'utf-8'

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
if "champs_1" not in st.session_state:
    st.session_state.champs_1 = st.empty()
# if "champs_0" not in st.session_state:
#     st.session_state.champs_0 = st.empty()
if "mail" not in st.session_state:
    st.session_state.mail = None
if "username" not in st.session_state:
    st.session_state.username = ""
if "password" not in st.session_state:
    st.session_state.password = ""
logging.getLogger("streamlit").setLevel(logging.ERROR)


st.session_state.champs_0 = st.empty()
if st.session_state.compteur_ionos == 0:
    with st.session_state.champs_0:
        if st.button("Se connecter",type="primary"):
            st.session_state.compteur_ionos = 1
            # if st.session_state.connect_ionos == 1:
            #     st.info("Déjà authentifier. Déconnectez ce compte pour en authentifier un autre")
        
if st.session_state.compteur_ionos == 1:
    if st.session_state.connect_ionos == 1:
        st.info("Connecté.")
    elif st.session_state.connect_ionos == 0:
        st.session_state.champs_0.empty()
        champs = st.empty()
        with champs:
            col1, col2 = st.columns([3,1])
            with col1:
                st.session_state.username = st.text_input("Adresse e-mail")
                st.session_state.password = st.text_input("Mot de passe",type="password")
        with st.spinner("Connexion..."):
            st.session_state.champs_1 = st.empty()
            with st.session_state.champs_1:
                if st.button("OK",type="primary"):
                    imap_server = "imap.ionos.fr"
                    port = 993
                    try:
                        st.session_state.mail = MailBox(f"{imap_server}", port)
                        st.session_state.mail.login(st.session_state.username, st.session_state.password)
                        #st.session_state.mail.select("inbox")
                        st.session_state.connect_ionos = 1
                        champs.empty()
                        st.session_state.champs_1.empty()
                        st.info("Connecté.")
                        
                    except imaplib.IMAP4.error as e:
                        st.error("Échec de connexion")
                    except socket.gaierror as f:
                        st.error("Hors ligne")
                    except imap_tools.errors.MailboxLoginError as i:
                        st.error("Échec de connexion")
                    except UnicodeEncodeError:
                        st.error("Mot de passe ou adresse invalide")

with st.sidebar:
    bouton_container = st.empty()

    if st.session_state.connect_ionos == 1:
        #time.sleep(0.5)
        with bouton_container:
            if st.button("🔒 Se déconnecter", type="primary"):
                try:
                    st.session_state.mail.logout()
                    st.session_state.compteur_ionos = 0
                    st.session_state.username = ""
                    st.session_state.password = ""
                    bouton_container.empty()
                    st.session_state.connect_ionos = 0
                    st.success("Déconnecté !")
                    st.rerun()
                except socket.gaierror as f:
                    st.error("Hors ligne")
                except imaplib.IMAP4.abort as l:
                    st.error("Délai de connexion dépassé")
                    st.session_state.connect_ionos = 0
                    st.session_state.compteur_ionos = 0
            


