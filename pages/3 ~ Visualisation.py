import streamlit as st
st.set_page_config(page_title="Module streamlit", layout="centered")
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
    elif st.session_state.base is None:
        st.info("Vous devez valider vos options de filtres.")
    elif st.session_state.base.empty:
        st.info("Base vide ou non existante.")
    else:
        try:
            st.title("Visualisation de la base")
            # vecteur_texte_vrai=st.session_state.vectoriseur.transform(st.session_state.base["texte_concat"])
            # from sklearn.preprocessing import StandardScaler
            # scaler=StandardScaler()
            # X_num_scaled_vrai = scaler.fit_transform(st.session_state.base[['Heure_journee','Taille (caractères)','Nombre PJ']])
            # st.session_state.base[['PJ_document', 'PJ_image', 'mot_cle_alerte']]=st.session_state.base[['PJ_document', 'PJ_image', 'mot_cle_alerte']].astype(int)
            # from scipy.sparse import hstack
            # X_final=hstack([vecteur_texte_vrai,X_num_scaled_vrai,st.session_state.base[['Jour_semaine','PJ_document', 'PJ_image', 'mot_cle_alerte']]])
            # y_pred_real = st.session_state.model.predict(X_final)
            # st.session_state.base["Label"] = st.session_state.encoder.inverse_transform(y_pred_real)
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
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"):
                st.info("Données sauvegardées dans 'base_mail.xlsx'")

           
            csv_data = df.to_csv(index=False).encode('utf-8')
            if st.download_button(
                label="Télécharger CSV",
                data=csv_data,
                file_name="base_mail.csv",
                mime="text/csv"):
                st.info("Données sauvegardées dans 'base_mail.csv'")
        except AttributeError as a:
            st.error("Base de données non existante")
            st.code(a)
except AttributeError as l:
    st.error("Connexion expirée.")
    st.code(l)
except socket.gaierror as f:
    st.error("Hors ligne")
# with st.spinner("Wait for it...", show_time=True):
#     time.sleep(60)