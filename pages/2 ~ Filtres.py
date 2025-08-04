import streamlit as st
st.set_page_config(page_title="Module streamlit", layout="centered")
import pandas as pd
from imap_tools import MailBox, AND
import re
import os
import imaplib
import unicodedata
from datetime import datetime, timedelta

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

if 'compteur_1' not in st.session_state:
    st.session_state.compteur_1=0
if 'y_pred_real' not in st.session_state:
    st.session_state.y_pred_real=None
if 'base' not in st.session_state:
    st.session_state.base=pd.DataFrame()
if "exp_filter" not in st.session_state:
    st.session_state.exp_filter = ""
if "subject_filter" not in st.session_state:
    st.session_state.subject_filter = ""
if "autres_expediteurs" not in st.session_state:
    st.session_state.autres_expediteurs = []
if "choix_expediteurs" not in st.session_state:
    st.session_state.choix_expediteurs = []
if "mots_objet" not in st.session_state:
    st.session_state.mots_objet = []
if "periode_mail" not in st.session_state:
    st.session_state.periode_mail = 15
if "max_results" not in st.session_state:
    st.session_state.max_results = 20
if "enl_choix" not in st.session_state:
    st.session_state.enl_choix = []
if "compteur" not in st.session_state:
    st.session_state.compteur = 0
if "mail" not in st.session_state:
    st.session_state.mail = MailBox("imap.ionos.fr",993).login(username="tickets2025@servitel-cm.com",password="Ti@2025_$*2025")
if "vectoriseur" not in st.session_state:
    st.session_state.vectoriseur = None
if "encoder" not in st.session_state:
    st.session_state.encoder = None
if "model" not in st.session_state:
    st.session_state.model = None

from sklearn.feature_extraction.text import TfidfVectorizer
st.session_state.vectoriseur=TfidfVectorizer()

base_fictive = pd.read_excel("emails_fictifs_300_avec_apercu.xlsx")
base_fictive['texte_concat']=base_fictive['sujet']+" "+base_fictive['apercu']

vecteur_texte=st.session_state.vectoriseur.fit_transform(base_fictive["texte_concat"])

from sklearn.preprocessing import StandardScaler
scaler=StandardScaler()
X_num_scaled = scaler.fit_transform(base_fictive[['Heure_journee','Taille (caractères)','Nombre PJ']])

from sklearn.preprocessing import LabelEncoder
st.session_state.encoder = LabelEncoder()
Y = st.session_state.encoder.fit_transform(base_fictive['label'])

from scipy.sparse import hstack
X_final_fictif=hstack([vecteur_texte,X_num_scaled,base_fictive[['Jour_semaine','PJ_document', 'PJ_image', 'mot_cle_alerte']]])

from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

st.session_state.model=LogisticRegression(max_iter=1000)
X_train, X_test, y_train, y_test = train_test_split(X_final_fictif, Y, test_size=0.2, random_state=42)
st.session_state.model.fit(X_train,y_train)
Correspondance = {'group-activa.com': 'Activa Assurance',
 'areaassurances.com': 'Area Assurances',
 'afrilandfirstbank.com': 'Afriland',
 'africagoldenbank.com': 'AGB',
 'banqueatlantique.net': 'Banque Atlantique',
 'bgfi.com': 'BGFI Bank',
 'bicec.com': 'BICEC',
 'cca-bank.com': 'CCA',
 'groupecommercialbank.com': 'Commercial Bank Cameroon',
 'ecobank.com': 'Ecobank',
 'scbcameroun.com': 'SCB',
 'socgen.com': 'Société Générale Cameroun',
 'ubagroup.com': 'UBA',
 'unionbankcameroon.com': 'UBC',
 'doualagrandmall.com': 'Douala Grand Mall',
 'diageo.com': 'Guiness',
 'sourcedupays.com': 'Source du pays',
 'sparcameroon.com': 'Spar',
 'eneo.cm': 'Eneo',
 'mail.totalenergies.com': 'Total Energie',
 'tradexsa.com': 'Tradex',
 'camtel.cm': 'Camtel',
 'mtn.com': 'Mtn',
 'orange.com': 'Orange',
 'hotel-akwa-palace.com': 'Akwa Palace',
 'accor.com': 'Ibis Douala',
 'khoteldouala.com': 'K Hotel',
 'krystalpalacedouala.com': 'Krystal Palace',
 'hotellafalaisebonanjo.com': 'La Falaise Bonanjo',
 'lafalaisebonapriso.com': 'La Falaise Bonapriso',
 'lewathotel.com': 'Lewat Hotel',
 'cdc-cameroon.com': 'CDC',
 'dangote.com': 'Dangote',
 'gh.nestle.com': 'Nestlé',
 'castel-afrique.com': 'SABC',
 'barry-callebaut.com': 'SIC CACAOS',
 'socapalm.org': 'SOCAPALM',
 'sa-ucb.com': 'UCB',
 'ionos.fr': 'IONOS',
 'camnet.cm': 'Aéroport du Cameroun',
 'adcsa.aero': 'Aéroport du Cameroun',
 'camair-co.net': 'Camair-co',
 'camrail.net': 'CAMRAIL',
 'finexs-voyages.net': 'Finex Voyages',
 'maersk.com': 'Maersk',
 'pad.cm': 'Port autonome de Douala',
 'pak.cm': 'Port autonome de Kribi',
 'alizesgroup.com': 'Servitel',
 'servitel-cm.com': 'Servitel'}

Da={'Activa Assurance': 'Assurance',
 'Area Assurances': 'Assurance',
 'Afriland': 'Banque',
 'AGB': 'Banque',
 'Banque Atlantique': 'Banque',
 'BGFI Bank': 'Banque',
 'BICEC': 'Banque',
 'CCA': 'Banque',
 'Commercial Bank Cameroon': 'Banque',
 'Ecobank': 'Banque',
 'SCB': 'Banque',
 'Société Générale Cameroun': 'Banque',
 'UBA': 'Banque',
 'UBC': 'Banque',
 'Douala Grand Mall': 'Commerce',
 'Guiness': 'Commerce',
 'Source du pays': 'Commerce',
 'Spar': 'Commerce',
 'Eneo': 'Energie',
 'Total Energie': 'Energie',
 'Tradex': 'Energie',
 'Camtel': 'FAI',
 'Mtn': 'FAI',
 'Orange': 'FAI',
 'Akwa Palace': 'Hôtel',
 'Ibis Douala': 'Hôtel',
 'K Hotel': 'Hôtel',
 'Krystal Palace': 'Hôtel',
 'La Falaise Bonanjo': 'Hôtel',
 'La Falaise Bonapriso': 'Hôtel',
 'Lewat Hotel': 'Hôtel',
 'CDC': 'Industrie',
 'Dangote': 'Industrie',
 'Nestlé': 'Industrie',
 'SABC': 'Industrie',
 'SIC CACAOS': 'Industrie',
 'SOCAPALM': 'Industrie',
 'UCB': 'Industrie',
 'IONOS': 'Service Internet',
 'Aéroport du Cameroun': 'Transport',
 'Camair-co': 'Transport',
 'CAMRAIL': 'Transport',
 'Finex Voyages': 'Transport',
 'Maersk': 'Transport',
 'Port autonome de Douala': 'Transport',
 'Port autonome de Kribi': 'Transport',
 'Servitel': 'Intégrateur'}
def retirer_accents(texte):
    if not isinstance(texte, str):
        return ""
    texte = unicodedata.normalize('NFD', texte)
    return ''.join(c for c in texte if unicodedata.category(c) != 'Mn')

def contient_mot_alerte(texte, mots_alerte):
    texte = retirer_accents(texte.lower())
    return any(mot in texte for mot in mots_alerte)

def nbre_mot_alerte(texte, mots_alerte):
    texte = retirer_accents(texte.lower())
    i=0
    for mot in mots_alerte:
        if mot in texte:
            i+=1
    return i

mots_alerte = [
    "panne", "defaut", "erreur", "incident", "intrusion", "alarme", "anomalie", "defaillance",
    "probleme", "coupure", "surcharge", "surchauffe", "sabotage", "rupture", "court-circuit",
    "fuite", "batterie faible", "perte de signal", "hors service", "signal perdu",
    "hors ligne", "non fonctionnel", "non operationnel", "redemarrage", "surveillance interrompue",
    "connectivite perdue", "connexion echouee", "camera injoignable", "capteur deconnecte", "zone non couverte",
    "protection desactivee", "risque detecte", "incident critique", "securite compromise", "piratage",
    "breche", "alarme declenchee", "mouvement detecte", "anormal", "dereglement","situation critique"
    "configuration erronee", "incident materiel", "tension faible", "detection echouee", "probleme technique",
    "maintenance urgente", "plantage", "deconnexion", "detection impossible","signal", "dysfonctionnement","souci","camera desorientee",
    "risque","signalons", "signaler","urgence","urgence"
]

# def extract_mails_imap(
#     sender_filter=None,
#     subject_filter=None,
#     since_days=None,
#     max_results=20
# ):
    

#     criteria = ["ALL"]
#     if since_days:
#         date_since = (datetime.now() - timedelta(days=since_days)).strftime("%d-%b-%Y")
#         criteria = ["SINCE", date_since]
#     result, data = st.session_state.mail.search(None, *criteria)

#     mail_ids = data[0].split()
#     mail_ids = mail_ids[-max_results:]  # Limiter les résultats

#     rows = []

#     for mail_id in reversed(mail_ids):
#         result, msg_data = st.session_state.mail.fetch(mail_id, "(RFC822)")
#         if result != "OK":
#             continue

#         raw_email = msg_data[0][1]
#         msg = email.message_from_bytes(raw_email)

#         # Sujet
#         subject, encoding = decode_header(msg["Subject"])[0]
#         if isinstance(subject, bytes):
#             try:
#                 subject = subject.decode(encoding or "utf-8")
#             except:
#                 subject = subject.decode("utf-8", errors="ignore")
#         subject = subject or ""

#         # Expéditeur
#         from_ = msg.get("From", "")
#         from_email = email.utils.parseaddr(from_)[1]
#         domain = from_email.split("@")[-1] if "@" in from_email else ""

#         # Date
#         try:
#             date_tuple = email.utils.parsedate_tz(msg.get("Date"))
#             date = datetime.fromtimestamp(email.utils.mktime_tz(date_tuple))
#         except:
#             date = None

#         # Aperçu (premiers caractères du corps)
#         body = ""
#         if msg.is_multipart():
#             for part in msg.walk():
#                 content_type = part.get_content_type()
#                 if content_type == "text/plain":
#                     try:
#                         body = part.get_payload(decode=True).decode("utf-8", errors="ignore")
#                     except:
#                         pass
#                     break
#         else:
#             body = msg.get_payload(decode=True).decode("utf-8", errors="ignore")

#         preview = body.strip().replace("\r", "").replace("\n", " ")[:100]

#         # Filtrage
#         if sender_filter and not any(s.lower() in from_email.lower() for s in sender_filter):
#             continue
#         if subject_filter and not any(s.lower() in subject.lower() for s in subject_filter):
#             continue

#         rows.append({
#             "Date": date,
#             "Expéditeur": from_email,
#             "Domaine": domain,
#             "Sujet": subject,
#             "Aperçu": preview
#         })


#     df = pd.DataFrame(rows)
#     st.session_state.base = df.sort_values("Date", ascending=False)

#     if st.session_state.base.empty:
#         st.warning("Aucun mail correspondant trouvé.")
#     else:
#         st.success(f"✅ {len(st.session_state.base)} mails trouvés")
  
def extract_mails_imap_tools_ml_ready(
    sender_filter: list[str] = None,
    subject_filter: list[str] = None,
    period_days: int = 30,
    max_results: int = 100
):
    
    since_date = (datetime.now() - timedelta(days=period_days)).date()

    filters = AND(date_gte=since_date)

    mails_data = []
    count = 0

    with st.session_state.mail as mailbox:
        for msg in mailbox.fetch(filters, bulk=True, limit=max_results):
            if sender_filter and not any(s.lower() in msg.from_.lower() for s in sender_filter):
                continue
            if subject_filter and not any(s.lower() in msg.subject.lower() for s in subject_filter):
                continue

            # Aperçu (100 premiers caractères du texte)
            preview = msg.text.strip().replace('\n', ' ').replace('\r', '')[:300]

            # Domaine expéditeur
            match = re.search(r"@([\w\.-]+)", msg.from_)
            domain = match.group(1) if match else ""
            if domain not in Correspondance.keys():
                nom_eprise = domain
            else:
                nom_eprise = Correspondance[domain]

            # Pièces jointes
            has_attachments = bool(msg.attachments)
            attachment_types = [os.path.splitext(att.filename)[1].lower() for att in msg.attachments] if has_attachments else []
            nb_pj = len(attachment_types)

            mails_data.append({
                "Client": nom_eprise,
                "Activité":Da[nom_eprise],
                "Date": msg.date,
                "Expéditeur": msg.from_,
                "Sujet": msg.subject,
                "Aperçu": preview,
                "Taille (caractères)": len(msg.text.strip()),
                "Nombre PJ": nb_pj,
                "PJ_image":any(x in ['.png','.jpg','.jpeg'] for x in attachment_types),
                "PJ_document":any(x in ['.pdf','.docx','.doc'] for x in attachment_types),
                "PJ_Excel": any(x in ['.xlsx','.csv','.xls'] for x in attachment_types)
            })

            count += 1
            if count >= max_results:
                break
    df=pd.DataFrame(mails_data)
    df['Date'] = df['Date'].apply(lambda dt: dt.astimezone(tz=None)) 
    df['Date'] = df['Date'].dt.tz_localize(None)
    df["Jour_semaine"]=df["Date"].apply(lambda x: x.isoweekday())
    df["Heure_journee"]=df["Date"].apply(lambda x: x.hour)
    df["texte_concat"] = df["Sujet"].fillna("") + " " + df["Aperçu"].fillna("")
    df["mot_cle_alerte"] = df["texte_concat"].apply(lambda x: contient_mot_alerte(x, mots_alerte))
    df["Nombre_mot_alerte"]=df["texte_concat"].apply(lambda x: nbre_mot_alerte(x,mots_alerte))


    st.session_state.base = df

    if st.session_state.base.empty:
        st.warning("Aucun mail correspondant trouvé.")
    else:
        st.success(f"✅ {len(st.session_state.base)} mails trouvés")

expediteurs_de_base=[
    "@servitel-cm.com",
    "@alizesgroup.com",
    "@ionos.fr",
    "@socgen.com",
]
try:
    if st.session_state.connect_ionos == 0:
        st.info("Vous devez vous connecter préalablement!")
    else:
        try:
            #result, data = st.session_state.mail.search(None, "ALL") 
            # Filtre expéditeurs
            with st.expander("Options de filtre", expanded=True):
            # ⏬ Expander pour masquer/afficher le filtre d'expéditeurs
                with st.expander("📬 Filtrer par expéditeurs", expanded=False):
                    cols1, cols2 = st.columns([3, 1])

                    with cols2:
                        tout_selectionner = st.checkbox("✅ Tout sélectionner")

                    with cols1:
                        if tout_selectionner:
                            expediteurs_selectionnes = expediteurs_de_base
                        else:
                            expediteurs_selectionnes = st.multiselect(
                                "Sélectionnez les expéditeurs souhaités :",
                                options=expediteurs_de_base
                            )
                    cs1,cs2,cs3 = st.columns([4,1,1])
                    with cs1:
                        nouveau_mail = st.text_input("➕ Ajouter un expéditeur non prédéfini (email exact)")
                    with cs2:
                        ajouter = st.button("Ajouter")
                    with cs3:
                        enlever = st.button("Enlever")

                    if ajouter and nouveau_mail:
                        if nouveau_mail not in st.session_state.autres_expediteurs:
                            st.session_state.autres_expediteurs.append(nouveau_mail)
                    enl_choix=[]
                    if enlever:
                        st.session_state.compteur = 1
                    if st.session_state.compteur == 1:
                        enl = st.multiselect("Enlever un expéditeur",options=st.session_state.autres_expediteurs)
                        st.session_state.enl_choix=enl.copy()
                    if st.session_state.enl_choix:
                        for i in st.session_state.enl_choix:
                            st.session_state.autres_expediteurs.remove(i)

                    valider_expediteurs = st.button("✅ Valider le filtre d'expéditeurs",type = "primary")

                if valider_expediteurs:
                    try:
                        st.session_state.choix_expediteurs = expediteurs_selectionnes.copy()
                        if "autres_expediteurs" in st.session_state:
                            st.session_state.choix_expediteurs += st.session_state.autres_expediteurs

                        st.session_state.choix_expediteurs = list(set(st.session_state.choix_expediteurs))  # suppression doublons
                    except:
                        st.session_state.choix_expediteurs = []

                    if st.session_state.choix_expediteurs:
                        c1,c2 = st.columns([1,3])
                        with c1:
                            st.success("📩 Expéditeurs sélectionnés :")
                        with c2:
                            with st.expander("Votre sélection"):
                                contenu_html = """
                                <style>
                                    .scrollable {
                                        height: 100px;
                                        overflow-y: scroll;
                                        border: 1px solid #ccc;
                                        border-radius: 8px;
                                        padding: 10px;
                                        background-color: #f9f9f9;
                                        color: blue;
                                    }
                                </style>
                                <div class="scrollable">
                                <ul>
                                """
                                for i in st.session_state.choix_expediteurs:
                                    contenu_html += f"<li>{i}</li>"
                                contenu_html += "</ul></div>"

                                st.markdown(contenu_html, unsafe_allow_html=True)
                                st.write(" ")
                    else:
                        st.warning("⚠️ Aucun expéditeur sélectionné.")
                    
                
                #Filtre objet
                with st.expander("🏷️ Filtre objet", expanded=False):
                    c1,c2,c3 = st.columns([1,1,1])
                    with c1:
                        cle1 = st.text_input("Mot-clé 1")
                    with c2:
                        cle2 = st.text_input("Mot-clé 2")
                    with c3:
                        cle3 = st.text_input("Mot-clé 3")
                    valider_objets = st.button("Valider les clés de recherche",type="primary")

                if valider_objets:
                    try:
                        if cle1:
                            st.session_state.mots_objet.append(cle1)
                        if cle2:
                            st.session_state.mots_objet.append(cle2)
                        if cle3:
                            st.session_state.mots_objet.append(cle3)
                    except:
                        st.session_state.mots_objet=[]

                    if st.session_state.mots_objet:
                        st.success("Clés de recherche:")
                        for i in st.session_state.mots_objet:
                            st.code(f"subject:{i}")
                    else:
                        st.warning("⚠️ Aucune clé entrée.")



                #Filtre période
                with st.expander("⏳ Filtrer par période (reçus dans les x derniers jours/semaines/mois)",expanded=False):
                    col1, col2 = st.columns([1, 2])

                    # Choix de l’unité (d, w, m)
                    with col1:
                        unite = st.radio("Unité :", ["Jour(s)", "Semaine(s)", "Mois","Année(s)"], index=2)

                    # Choix du nombre
                    with col2:
                        nombre = st.number_input("Nombre :", min_value=1, max_value=365, step=1, value=7)

                    match unite:
                        case "Jour(s)":
                            st.session_state.periode_mail = nombre
                        case "Semaines(s)":
                            st.session_state.periode_mail = nombre*7
                        case "Mois":
                            st.session_state.periode_mail = nombre*30
                        case "Année(s)":
                            st.session_state.periode_mail = nombre*365
                    

                    if st.button("✅ Valider la période",type="primary"):
                        st.success(f"📅 Filtre appliqué : `Mails datant de moins de {nombre} {unite}`")

                #Limite de récupération
                with st.expander("📋 Limite de récupération"):
                    st.session_state.max_results = st.selectbox(
                        "Choisir le nombre maximum de mails à récupérer :",
                        options=[10, 20, 50, 100, 200,300],
                        index=1
                    )
            if st.button("OK", type ="primary"):
                extract_mails_imap_tools_ml_ready(sender_filter=st.session_state.choix_expediteurs,subject_filter=st.session_state.mots_objet,period_days=st.session_state.periode_mail,max_results=st.session_state.max_results)
                st.session_state.mots_objet=[]
                st.session_state.choix_expediteurs=[]
                st.session_state.periode_mail=20
                st.session_state.mail = MailBox("imap.ionos.fr",993).login(st.session_state.username,st.session_state.password)
                st.session_state.compteur_1=2

            if st.session_state.compteur_1==2:
                st.session_state.base[['PJ_document', 'PJ_image']]=st.session_state.base[['PJ_document', 'PJ_image']].astype(int)
                vecteur_texte_vrai=st.session_state.vectoriseur.transform(st.session_state.base["texte_concat"])
                from sklearn.preprocessing import StandardScaler
                scaler=StandardScaler()
                X_num_scaled_vrai = scaler.fit_transform(st.session_state.base[['Heure_journee','Taille (caractères)','Nombre PJ']])
                st.session_state.base[['PJ_document', 'PJ_image', 'mot_cle_alerte']]=st.session_state.base[['PJ_document', 'PJ_image', 'mot_cle_alerte']].astype(int)
                from scipy.sparse import hstack
                X_final=hstack([vecteur_texte_vrai,X_num_scaled_vrai,st.session_state.base[['Jour_semaine','PJ_document', 'PJ_image', 'mot_cle_alerte']]])
                st.session_state.y_pred_real = st.session_state.model.predict(X_final)
                st.session_state.base["Label"] = st.session_state.encoder.inverse_transform(st.session_state.y_pred_real)
                dico={1:'Lundi',2:'Mardi',3:'Mercredi',4:'Jeudi',5:'Vendredi',6:'Samedi',7:'Dimanche'}
                st.session_state.base.Jour_semaine=st.session_state.base.Jour_semaine.map(dico)
                st.session_state.compteur_1=1

        except imaplib.IMAP4.error as e:
            st.error("Délai de connexion dépassé")
            #st.session_state.mail = MailBox("imap.ionos.fr",993).login(st.session_state.username,st.session_state.password)
            #extract_mails_imap_tools_ml_ready(sender_filter=st.session_state.choix_expediteurs,subject_filter=st.session_state.mots_objet,period_days=st.session_state.periode_mail,max_results=st.session_state.max_results)

except AttributeError as a:
    st.error("Connexion expirée.")
    st.code(a)
