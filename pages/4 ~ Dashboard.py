import streamlit as st
st.set_page_config(page_title="Module streamlit", layout="wide")
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px


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
try:
    if st.session_state.connect_ionos == 0:
        st.info("Vous devez vous connecter préalablement!")
    elif st.session_state.base is None:
        st.info("Vous devez valider vos options de filtres.")
    elif st.session_state.base.empty:
        st.info("Base vide ou non existante.")
    else:
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
                background: linear-gradient(rgb(68,60,108),rgb(23,30,68));
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
            .block-container {
                padding-top: 2rem;
                padding-bottom: 2rem;
            }
            .custom-box {
                background-color: rgba(0, 0, 0, 0.65);
                padding: 25px;
                border-radius: 20px;
                box-shadow: 0px 4px 12px rgba(0,0,0,0.25);
                color: white;
            }
            </style>
        """, unsafe_allow_html=True)

        # st.markdown("""
        # <h1 style='text-align: center; color: white; font-size: 30px;'>
        #     Configurez votre adresse e-mail
        # </h1>
        # """, unsafe_allow_html=True)

        st.session_state.base.sort_values(by="Date", ascending=False, inplace=True)
        c1,c2,c3 = st.columns([1,1,1])

        with c1:
            fig = go.Figure(
                data=go.Pie(
                    labels=st.session_state.base["Label"].value_counts().index,
                    values=st.session_state.base["Label"].value_counts().values,hole=0.7,marker=dict(colors=px.colors.sequential.Blues)))
            
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(family="Segoe UI", size=14, color="white"),
                legend=dict(
                font=dict(color="#FFFFFF")
            ))

            st.plotly_chart(fig, use_container_width=True)
                

        with c2:
            heure_counts = st.session_state.base[st.session_state.base["Label"]=="Alerte"].Heure_journee.value_counts().sort_index()
            df_heure = heure_counts.reset_index()
            df_heure.columns = ['Heure', 'Nb']

            fig2=px.bar(df_heure,x='Heure',y='Nb',color_discrete_sequence=["#CCE4FF"])
            fig2.update_yaxes(title_text="Nombre d'occurrences")
            fig2.update_xaxes(title_text='Heure')
            fig2.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(family="Segoe UI", size=14, color="white"),
                bargap=0.1,
                xaxis=dict(title_font=dict(color="white"), tickfont=dict(color="white")),
                yaxis=dict(title_font=dict(color="white"), tickfont=dict(color="white")),
                legend=dict(
                font=dict(color="#FFFFFF")
            ))
            st.plotly_chart(fig2,use_container_width=True)
        with c3:
            # fig3=px.histogram(y=st.session_state.base.Jour_semaine.value_counts().sort_values(ascending=True).index.tolist(),x=st.session_state.base.Jour_semaine.value_counts().sort_values(ascending=True).values.tolist(),color_discrete_sequence=["#61B0FF"],orientation='h')
            # fig3.update_xaxes(title_text="Nombre d'occurrences")
            # fig3.update_yaxes(title_text='Jour')
            # fig3.update_layout(bargap=0.1)
            # st.plotly_chart(fig3,use_container_width=True)

            jour_counts = st.session_state.base[st.session_state.base["Label"]=="Alerte"].Jour_semaine.value_counts().sort_values(ascending=True)

            # Créer un DataFrame temporaire
            df_jour = jour_counts.reset_index()
            df_jour.columns = ['Jour', 'Nb']

            # Tracer avec Plotly Express
            fig3 = px.bar(
                df_jour,
                x='Nb',
                y='Jour',
                orientation='h',
                color_discrete_sequence=px.colors.sequential.Blues # palette plus sobre et dégradée
        )

            fig3.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(family="Segoe UI", size=14, color="white"),
                bargap=0.15,
                xaxis=dict(title='Nombre d’occurrences',title_font=dict(color="white"), tickfont=dict(color="white")),
                yaxis=dict(title='Jour',title_font=dict(color="white"), tickfont=dict(color="white")),
            )

            fig3.update_traces(
                marker=dict(opacity=0.85, line=dict(width=1, color='rgba(255,255,255,0.2)')),
                hoverlabel=dict(bgcolor="black", font_size=13, font_family="Segoe UI")
            )
            
            st.plotly_chart(fig3, use_container_width=True)

        df_alertes = st.session_state.base[st.session_state.base["Label"] == "Alerte"]
        df_grouped = df_alertes.groupby(["Jour_semaine", "Heure_journee"]).size().reset_index(name="Nb_alertes")


        ordre_jours = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]
        df_grouped["Jour_semaine"] = pd.Categorical(df_grouped["Jour_semaine"], categories=ordre_jours, ordered=True)
        fig4 = px.area(
        df_grouped,
        x='Heure_journee',
        y='Nb_alertes',
        color='Jour_semaine',
        line_group='Jour_semaine',
        markers=True,
        color_discrete_sequence=px.colors.sequential.Reds
        )

        fig4.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(family="Segoe UI", size=14,color="#FFFFFF"),
            xaxis=dict(title_font=dict(color="white"), tickfont=dict(color="white")),
            yaxis=dict(title_font=dict(color="white"), tickfont=dict(color="white")),
            legend=dict(font=dict(color="#FFFFFF")),
            showlegend=True
        )

        fig4.update_traces(
            mode='lines+markers',
            line_shape='spline',
            fill='tozeroy',
            marker=dict(size=6)
        )
        st.plotly_chart(fig4,use_container_width=True)

        cO1,cO2 = st.columns([1,1])
        with st.container():
            with cO1:
                fig5 = go.Figure(
                data=go.Pie(
                    labels=st.session_state.base[st.session_state.base["Label"]=="Alerte"]["Client"].value_counts().index,
                    values=st.session_state.base[st.session_state.base["Label"]=="Alerte"]["Client"].value_counts().values,hole=0.7,marker=dict(colors=px.colors.sequential.Blues)))
            
                fig5.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(family="Segoe UI", size=14, color="white"),
                    legend=dict(
                    font=dict(color="#FFFFFF")
                ))
                st.plotly_chart(fig5, use_container_width=True)
            with cO2:
                fig6 = go.Figure(
                data=go.Pie(
                    labels=st.session_state.base[st.session_state.base["Label"]=="Alerte"]["Activité"].value_counts().index,
                    values=st.session_state.base[st.session_state.base["Label"]=="Alerte"]["Activité"].value_counts().values,hole=0.7,marker=dict(colors=px.colors.sequential.Reds)))
            
                fig6.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(family="Segoe UI", size=14, color="white"),
                    legend=dict(
                    font=dict(color="#FFFFFF")
                ))
                st.plotly_chart(fig6, use_container_width=True)

        cl1,cl2 = st.columns([4,1]) 
        with cl2:     
            clients = st.multiselect("Clients",list(st.session_state.base.Client.unique()),list(st.session_state.base.Client.unique()))
            activites = st.multiselect("Secteurs d'activité",list(st.session_state.base.Activité.unique()),list(st.session_state.base.Activité.unique()))
        with cl1:
            df2=st.session_state.base[["Client","Activité","Label"]]
            df_filtered = df2[df2["Label"]=="Alerte"][
            (df2[df2["Label"]=="Alerte"]["Client"].isin(clients)) |
            (df2[df2["Label"]=="Alerte"]["Activité"].isin(activites))
        ]
            df_groupe = df_filtered.groupby(["Activité", "Client"]).size().reset_index(name="Nb_alertes")
            fig7 = go.Figure()
            for activite in df_groupe["Activité"].unique():
                df_activite = df_groupe[df_groupe["Activité"] == activite]
                
                fig7.add_trace(go.Bar(
                    x=df_activite["Client"],
                    y=df_activite["Nb_alertes"],
                    name=activite,
                    marker_color="#13E8F7",
                    width=0.005
                ))
            
            # Mise en forme
            fig7.update_layout(
                barmode='group',
                xaxis_title="Client",
                yaxis_title="Nb_alertes",
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                xaxis=dict(title_font=dict(color="white"), tickfont=dict(color="white")),
                yaxis=dict(title_font=dict(color="white"), tickfont=dict(color="white")),
                legend=dict(font=dict(color="#FFFFFF")),
                showlegend=True,
                font=dict(color='white')
            )

            st.plotly_chart(fig7, use_container_width=True)

        df4 = st.session_state.base.copy()
        df_alertes = df4[df4["Label"] == "Alerte"]
        df_daily = df_alertes.groupby(df_alertes["Date"].dt.to_period('M').dt.to_timestamp()).size().reset_index(name="Nb_alertes")

        fig8 = px.line(df_daily, x="Date", y="Nb_alertes",
                    markers=True)

        # (Optionnel) style
        fig8.update_traces(line=dict(color='cyan'), fill='tozeroy', mode='lines+markers')
        fig8.update_layout(
            xaxis_title="Date",
            yaxis_title="Nombre d'alertes",
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(title_font=dict(color="white"), tickfont=dict(color="white"),tickformat="%B %Y"),
            yaxis=dict(title_font=dict(color="white"), tickfont=dict(color="white")),
            legend=dict(font=dict(color="#FFFFFF")),
            showlegend=True,
            font=dict(color='white')
        )

        st.plotly_chart(fig8, use_container_width=True)

        deltas = df_alertes["Date"].diff(periods=-1).dropna()

        # Moyenne
        duree_moyenne = deltas.mean()

        # Affichage
        st.write("Durée moyenne entre 2 alertes")
        st.write(duree_moyenne)


        df_alertes["Date"] = pd.to_datetime(df_alertes["Date"])

        resultats = []

        for client, group in df_alertes.groupby("Client"):
            deltas = group["Date"].diff(periods=-1).dropna()
            if len(deltas) > 0:
                moyenne = deltas.mean()
            else:
                moyenne = pd.NaT  # Pas assez de dates pour calculer un intervalle
            resultats.append({"Client": client, "Durée_moyenne": moyenne})

        # Créer le DataFrame final
        df_durees = pd.DataFrame(resultats)
        max_val = df_durees["Durée_moyenne"].max()
        df_durees["%_durée"] = (df_durees["Durée_moyenne"] / max_val * 100).round(1)

        search_client = st.multiselect("Client",list(df_durees.Client.unique()),[])

        # 🔹 Filtrage conditionnel
        if search_client:
            df_filtre = df_durees[df_durees["Client"].isin(search_client)]
        else:
            df_filtre = df_durees.copy()

        # Préparer la config pour barre de progression
        columns_config = {
            "%_durée": st.column_config.ProgressColumn(
                "Durée moyenne (barre)",
                min_value=0,
                max_value=100,
                format=" "
                
            )
        }
        df_filtre.sort_values(by="Durée_moyenne",ascending=True,inplace=True)
        df_filtre["Durée_moyenne"]=df_durees["Durée_moyenne"].apply(lambda x: str(x))
        # Affichage avec st.data_editor
        st.write("Durée moyenne entre alertes par client")
        st.data_editor(
            df_filtre[["Client", "Durée_moyenne", "%_durée"]],
            column_config=columns_config,
            hide_index=True,
            disabled=True
        )
        # Affichage

        #st.dataframe(df_durees)
except AttributeError as l:
     st.error("Connexion expirée.")
     st.code(l)