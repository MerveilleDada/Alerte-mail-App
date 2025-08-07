import streamlit as st
st.set_page_config(page_title="Alerte-mail-App",layout='wide',page_icon="📊",initial_sidebar_state="collapsed")
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
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
try:
    if st.session_state.compte_d==1:
        st.session_state.base = st.session_state.base_passee
except AttributeError:
    pass
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
        df_alertes = st.session_state.base[st.session_state.base["Label"] == "Alerte"]
        if len(df_alertes)==0:
            st.info("Aucune alerte détectée.")
        elif len(df_alertes)==1:
            st.info("Une seule alerte détectée. Voire 'Visualisation'.")
        else:
            st.header("Dashboard Alerte")
            c1,c2,c3 = st.columns([1,1,1])

            with c1:
                fig = go.Figure(
                    data=go.Pie(
                        labels=st.session_state.base["Label"].value_counts().index,
                        values=st.session_state.base["Label"].value_counts().values,hole=0.7,marker=dict(colors=px.colors.sequential.Reds_r),opacity=0.8))
            
                fig.update_layout(
                    title = dict(text="Répartition des mails extraits",xanchor='center',x=0.5),
                    margin=dict(l=25),
                    plot_bgcolor="rgba(0,0,0,0)",
                    paper_bgcolor="rgba(0,0,0,0.1)",
                    font=dict(family="Segoe UI", size=14, color="#FFFFFF"),
                    legend=dict(font=dict(color="#FFFFFF",style='italic'),bgcolor="rgba(0,0,0,0)")
                )

                st.plotly_chart(fig, use_container_width=True)
                    

            with c2:
                heure_counts = df_alertes.Heure_journee.value_counts().sort_index()
                df_heure = heure_counts.reset_index()
                df_heure.columns = ['Heure', 'Nb']

                tickvals = list(range(df_heure["Heure"].min(), df_heure["Heure"].max() + 1))
                ticktext = [f"{x} h" for x in tickvals]

                fig2=px.bar(df_heure,x='Heure',y='Nb',color_discrete_sequence=["red"],opacity=0.45)
                fig2.update_yaxes(title_text="Nombre d'alertes")
                fig2.update_xaxes(title_text='Heure')
                fig2.update_layout(
                    margin=dict(l=10,r=20),
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0.1)',
                    font=dict(family="Segoe UI", size=14, color="white"),
                    bargap=0.1,
                    xaxis=dict(title_font=dict(color="white"), tickfont=dict(color="white"),showgrid=True,gridcolor="rgba(255, 255, 255, 0)",tickformat=".0f",dtick=1,tickmode="array",tickvals=tickvals,ticktext=ticktext),
                    yaxis=dict(title_font=dict(color="white"), tickfont=dict(color="white"),showgrid=True,gridcolor="rgba(255, 255, 255, 0.2)",tickformat=".0f",tickmode="linear",dtick=1),
                    legend=dict(
                    font=dict(color="#FFFFFF")
                ))
                st.plotly_chart(fig2,use_container_width=True)
            with c3:
                jour_counts = df_alertes.Jour_semaine.value_counts().sort_values(ascending=True)

                df_jour = jour_counts.reset_index()
                df_jour.columns = ['Jour', 'Nb']

                fig3 = px.bar(
                    df_jour,
                    x='Nb',
                    y='Jour',
                    orientation='h',
                    color_discrete_sequence=["red"],opacity=0.45
            )

                fig3.update_layout(
                    margin=dict(l=10,r=30),
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0.1)',
                    font=dict(family="Segoe UI", size=14, color="white"),
                    bargap=0.15,
                    xaxis=dict(title="Nombre d'alertes",title_font=dict(color="white"), tickfont=dict(color="white"),showgrid=True,gridcolor="rgba(255, 255, 255, 0)",tickformat=".0f",tickmode="linear",dtick=1),
                    yaxis=dict(title='Jour',title_font=dict(color="white"), tickfont=dict(color="white"),showgrid=True,gridcolor="rgba(255, 255, 255, 0.2)"),
                )

                fig3.update_traces(
                    marker=dict(line=dict(width=1, color='rgba(255,255,255,0.2)')),
                    hoverlabel=dict(bgcolor="black", font_size=13, font_family="Segoe UI")
                )
                
                st.plotly_chart(fig3, use_container_width=True)

            
            df_grouped = df_alertes.groupby(["Jour_semaine", "Heure_journee"]).size().reset_index(name="Nombre d'alertes")


            ordre_jours = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]
            df_grouped["Jour_semaine"] = pd.Categorical(df_grouped["Jour_semaine"], categories=ordre_jours, ordered=True)

            tickvals = list(range(df_grouped["Heure_journee"].min(), df_grouped["Heure_journee"].max() + 1))
            ticktext = [f"{x} h" for x in tickvals]

            fig4 = px.area(
            df_grouped,
            x='Heure_journee',
            y="Nombre d'alertes",
            color='Jour_semaine',
            line_group='Jour_semaine',
            markers=True,
            color_discrete_sequence=["#5374C9", "#0ABAB5", "#7FCDCA", "#BBD5E8", "#54DDFF", "#00FFF7", "#B8FFFD"].reverse()

            )

            fig4.update_layout(
                title = dict(text="Alertes par heure et par jour"),
                margin=dict(r=20),
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(family="Segoe UI", size=14,color="#FFFFFF"),
                xaxis=dict(title="Heure",title_font=dict(color="white"), tickfont=dict(color="white"),showgrid=True,gridcolor="rgba(255, 255, 255, 0)",tickformat=".0f",tickmode="array",tickvals=tickvals,ticktext=ticktext,dtick=1),
                yaxis=dict(title_font=dict(color="white"), tickfont=dict(color="white"),showgrid=True,gridcolor="rgba(255, 255, 255, 0.2)",tickformat=".0f",tickmode="linear",dtick=1),
                legend=dict(font=dict(color="#FFFFFF",style='italic'),x=1.05,xanchor="left",bgcolor='rgba(0,0,0,0)'),
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
                        labels=df_alertes["Client"].value_counts().index,
                        values=df_alertes["Client"].value_counts().values,hole=0.7,marker=dict(colors=px.colors.sequential.Blues)))
                
                    fig5.update_layout(
                        title=dict(text="Alertes par client",xanchor='center',x=0.45),
                        plot_bgcolor="rgba(0,0,0,0)",
                        paper_bgcolor="rgba(0,0,0,0.1)",
                        font=dict(family="Segoe UI", size=14, color="#FFFFFF"),
                        legend=dict(font=dict(color="#FFFFFF",style='italic'),bgcolor="rgba(0,0,0,0)"))
                    st.plotly_chart(fig5, use_container_width=True)
                with cO2:
                    fig6 = go.Figure(
                    data=go.Pie(
                        labels=df_alertes["Activité"].value_counts().index,
                        values=df_alertes["Activité"].value_counts().values,hole=0.7,marker=dict(colors=px.colors.sequential.Reds)))
                
                    fig6.update_layout(
                        title=dict(text="Alertes par secteur d'activité",xanchor='center',x=0.45),
                        plot_bgcolor="rgba(0,0,0,0)",
                        paper_bgcolor="rgba(0,0,0,0.1)",
                        font=dict(family="Segoe UI", size=14, color="#FFFFFF"),
                        legend=dict(font=dict(color="#FFFFFF",style='italic'),bgcolor="rgba(0,0,0,0)"))
                    st.plotly_chart(fig6, use_container_width=True)

            cl1,cl2 = st.columns([4,1]) 
            with cl2:     
                st.write(" ")
                st.write(" ")
                st.write(" ")
                st.write(" ")
                st.write(" ")
                st.write(" ")
                clients = st.multiselect("Clients",list(df_alertes.Client.unique()),list(df_alertes.Client.unique()))
                activites = st.multiselect("Secteurs d'activité",list(df_alertes.Activité.unique()),list(df_alertes.Activité.unique()))
            with cl1:
                df2=df_alertes[["Client","Activité","Label"]]
                df_filtered = df2[(df2["Client"].isin(clients))|(df2["Activité"].isin(activites))]

                df_groupe = df_filtered.groupby(["Activité", "Client"]).size().reset_index(name="Nombre d'alertes")
                fig7 = go.Figure()
                for activite in df_groupe["Activité"].unique():
                    df_activite = df_groupe[df_groupe["Activité"] == activite]
                    
                    fig7.add_trace(go.Bar(
                        x=df_activite["Client"],
                        y=df_activite["Nombre d'alertes"],
                        name=activite,
                        marker_color="#13E8F7",
                        width=0.005
                    ))
                
                # Mise en forme
                fig7.update_layout(
                    title = dict(text="Alertes par client suivant le secteur d'activité"),
                    barmode='group',
                    xaxis_title="Client",
                    yaxis_title="Nombre d'alertes",
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    xaxis=dict(title_font=dict(color="white"), tickfont=dict(color="white"),showgrid=True,gridcolor="rgba(255, 255, 255, 0.25)"),
                    yaxis=dict(title_font=dict(color="white"), tickfont=dict(color="white"),showgrid=True,gridcolor="rgba(255, 255, 255, 0.25)",tickformat=".0f",tickmode="linear",dtick=1),
                    legend=dict(font=dict(color="#FFFFFF",style='italic'),bgcolor='rgba(0,0,0,0)'),
                    showlegend=True,
                    font=dict(color='white')
                )

                st.plotly_chart(fig7, use_container_width=True)

            df_daily = df_alertes.groupby(df_alertes["Date"].dt.to_period('M').dt.to_timestamp()).size().reset_index(name="Nombre d'alertes")

            fig8 = px.line(df_daily, x="Date", y="Nombre d'alertes",
                        markers=True)

            fig8.update_traces(line=dict(color='#B8FFFD'), fill='tozeroy', mode='lines+markers')
            fig8.update_layout(
                title = "Evolution temporelle",
                xaxis_title="Date",
                yaxis_title="Nombre d'alertes",
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                xaxis=dict(title_font=dict(color="white"), tickfont=dict(color="white"),tickformat="%B %Y",showgrid=True,
                        gridcolor="rgba(255, 255, 255, 0.25)",tickmode="linear",dtick=1),
                yaxis=dict(title_font=dict(color="white"), tickfont=dict(color="white"),showgrid=True,
                        gridcolor="rgba(255, 255, 255, 0.25)",tickformat=".0f",tickmode="linear",dtick=1),
                legend=dict(font=dict(color="#FFFFFF")),
                showlegend=True,
                font=dict(color='white')
            )

            st.plotly_chart(fig8, use_container_width=True)
            
            deltas = df_alertes["Date"].diff(periods=-1).dropna()

            duree_moyenne = deltas.mean()

            st.write("Durée moyenne entre 2 alertes")
            st.write(duree_moyenne)


            df_alertes["Date"] = pd.to_datetime(df_alertes["Date"])

            resultats = []

            for client, group in df_alertes.groupby("Client"):
                deltas = group["Date"].diff(periods=-1).dropna()
                if len(deltas) > 0:
                    moyenne = deltas.mean()
                else:
                    moyenne = pd.NaT 
                resultats.append({"Client": client, "Durée_moyenne": moyenne})

            df_durees = pd.DataFrame(resultats)
            max_val = df_durees["Durée_moyenne"].max()
            df_durees["%_durée"] = (df_durees["Durée_moyenne"] / max_val * 100).round(1)

            search_client = st.multiselect("Client",list(df_durees.Client.unique()),[],placeholder="...")

            # 🔹 Filtrage conditionnel
            if search_client:
                df_filtre = df_durees[df_durees["Client"].isin(search_client)]
            else:
                df_filtre = df_durees.copy()

            # Préparation de la config pour barre de progression
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
        
except AttributeError as l:
    st.warning("Connexion expirée. Reconnectez-vous")

except socket.gaierror as f:
    st.error("Hors ligne")

try:
    if st.session_state.compte_d==1:
        st.session_state.base = pd.DataFrame()
except AttributeError:
    pass