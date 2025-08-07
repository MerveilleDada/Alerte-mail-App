import streamlit as st
st.set_page_config(page_title="Alerte-mail-App", layout="centered",page_icon="📊")
import io
import pandas as pd
import pickle
import os
import socket

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
if 'compte_d' not in st.session_state:
    st.session_state.compte_d=0
if os.path.exists("base_sauvegardee_{st.session_state.username}.pkl"):
    with open("base_sauvegardee_{st.session_state.username}.pkl", "rb") as f:
        if 'base_passee' not in st.session_state:
            st.session_state.base_passee = pickle.load(f)
else:
    if 'base_passee' not in st.session_state:
        st.session_state.base_passee = pd.DataFrame()


def style_statut(val):
    if val == "RAS":
        return 'background-color: #e6f4ea; color: #2e7d32'  # vert doux
    elif val == "Alerte":
        return 'background-color: #fdecea; color: #c62828'  # rouge doux
    return ''
try:
    if st.session_state.connect_ionos == 0:
        st.info("Vous devez vous connecter préalablement!")
    elif st.session_state.base.empty:
        with st.sidebar:
            if "charger_base_1" not in st.session_state:
                choix = st.radio("Base", ["Dernière session"], index=None)
                if choix:  
                    st.session_state.charger_base_1 = choix
            else:
                st.radio("Base", ["Dernière session"], index=0, key="charger_base_1")

        if st.session_state.charger_base_1=="Dernière session":
            st.session_state.compte_d=1
            st.title("Visualisation de la base")
            st.session_state.base = st.session_state.base_passee
            clients_2 = st.multiselect("Clients",list(st.session_state.base.Client.unique()),[list(st.session_state.base.Client.unique())[0]])
            label_2 = st.multiselect("Label",list(st.session_state.base.Label.unique()),list(st.session_state.base.Label.unique()))
            df=st.session_state.base[['Client', 'Activité', 'Date', 'Expéditeur', 'Sujet','Nombre PJ', 'PJ_image', 'PJ_document','PJ_Excel','Label']][st.session_state.base["Client"].isin(clients_2) & st.session_state.base["Label"].isin(label_2)]
            styled_df = df.style.applymap(style_statut, subset=['Label'])
            st.dataframe(styled_df)
            st.session_state.base=pd.DataFrame()
        else:
            st.session_state.compte_d=0
            st.info("Base vide ou non existante.")
    elif st.session_state.base is None:
        st.info('Base non existante')
    else:
        try:
            st.title("Visualisation de la base")
            with st.sidebar:
                charger_base = st.radio("Base",["Session courante","Dernière session"],index=0)
            if charger_base=="Session courante":
                st.session_state.base=st.session_state.base_temp
                st.session_state.base.sort_values(by="Date", ascending=False, inplace=True)
                st.session_state.base[['PJ_document', 'PJ_image']]=st.session_state.base[['PJ_document', 'PJ_image']].astype(bool)
                clients = st.multiselect("Clients",list(st.session_state.base.Client.unique()),[list(st.session_state.base.Client.unique())[0]])
                label = st.multiselect("Label",list(st.session_state.base.Label.unique()),list(st.session_state.base.Label.unique()))
                df=st.session_state.base[['Client', 'Activité', 'Date', 'Expéditeur', 'Sujet','Nombre PJ', 'PJ_image', 'PJ_document','PJ_Excel','Label']][st.session_state.base["Client"].isin(clients) & st.session_state.base["Label"].isin(label)]
                styled_df = df.style.applymap(style_statut, subset=['Label'])
                st.dataframe(styled_df)

                def to_excel(df):
                    output = io.BytesIO()
                    with pd.ExcelWriter(output, engine='openpyxl') as writer:
                        df.to_excel(writer, index=False)
                    return output.getvalue()
                
                excel_data = to_excel(df)
                if st.download_button(
                    label="Télécharger Excel",
                    data=excel_data,
                    file_name="base_mail.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",type="primary"):
                    st.info("Données sauvegardées dans 'base_mail.xlsx'")

            
                csv_data = df.to_csv(index=False).encode('utf-8')
                if st.download_button(
                    label="Télécharger CSV",
                    data=csv_data,
                    file_name="base_mail.csv",
                    mime="text/csv",type="primary"):
                    st.info("Données sauvegardées dans 'base_mail.csv'")

                if st.button("Sauvegarder la session",type="primary"):
                    with open("base_sauvegardee_{st.session_state.username}.pkl", "wb") as f:
                        pickle.dump(st.session_state.base_temp, f)
                    st.success("Base sauvegardée avec succès.")

            if charger_base=="Dernière session":
                if not st.session_state.base_passee.empty:
                    st.session_state.base = st.session_state.base_passee
                    clients_2 = st.multiselect("Clients",list(st.session_state.base.Client.unique()),[list(st.session_state.base.Client.unique())[0]])
                    label_2 = st.multiselect("Label",list(st.session_state.base.Label.unique()),list(st.session_state.base.Label.unique()))
                    df=st.session_state.base[['Client', 'Activité', 'Date', 'Expéditeur', 'Sujet','Nombre PJ', 'PJ_image', 'PJ_document','PJ_Excel','Label']][st.session_state.base["Client"].isin(clients_2) & st.session_state.base["Label"].isin(label_2)]
                    styled_df = df.style.applymap(style_statut, subset=['Label'])
                    st.dataframe(styled_df)
                else:
                    st.info("Base non existante")      
        except AttributeError as a:
            st.warning("Connexion expirée")
except socket.gaierror as f:
    st.error("Hors ligne")

except AttributeError as a:
        st.info("Base non existante")