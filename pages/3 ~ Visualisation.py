import streamlit as st
st.set_page_config(page_title="Alerte-mail-App", layout="centered",page_icon="📊")
import io
import pandas as pd
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
        st.info("Base vide ou non existante.")
    elif st.session_state.base is None:
        st.info('Base non existante')
    else:
        try:
            st.title("Visualisation de la base")
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

        except AttributeError as a:
            st.warning("Connexion expirée ou base non existante") #A revoir
        
except socket.gaierror as f:
    st.error("Hors ligne")

except AttributeError as a:
        st.info("Connexion expirée ou base non existante") #A revoir