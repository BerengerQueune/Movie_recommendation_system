import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import pydeck as pdk
import datetime as dt
import plotly.express as px
import ipywidgets as widgets
from plotly.subplots import make_subplots
import plotly.graph_objects as go

st.beta_set_page_config( layout='wide')

st.title("Projet : recommandation de films")  # add a title
clicked = st.button("Coucou")
st.write("Ce projet effectué au sein de l'école Wild Code School a pour but de nous faire créer un moteur de recommandation de films.")

st.write("Un cinéma en perte de vitesse situé dans la Creuse vous contacte. Il a décidé de passer le cap du digital en créant un site Internet taillé pour les locaux.")

st.write("Pour commencer, nous devons explorer la base de données afin de répondre aux questions suivantes :")
st.write("- Quels sont les pays qui produisent le plus de films ?")
st.write("- Quels sont les acteurs les plus présents ? À quelle période ?")
st.write("- La durée moyenne des films s’allonge ou se raccourcit avec les années ?")
st.write("- Les acteurs de série sont-ils les mêmes qu’au cinéma ?")
st.write("- Les acteurs ont en moyenne quel âge ?")
st.write("- Quels sont les films les mieux notés ? Partagent-ils des caractéristiques communes ?")





acteur_par_periode = pd.read_csv("https://raw.githubusercontent.com/BerengerQueune/ABC-Data/main/Berenger/Streamlit/acteur_par_periode.csv?token=AU6BUZWYJ6GYLJLQVDQCLZTBSZ2NK")
link = 'https://raw.githubusercontent.com/BerengerQueune/ABC-Data/main/Berenger/Streamlit/top10.csv?token=AU6BUZSEQED65VJVLNSX4FLBS2IYO'
top10 = pd.read_csv(link)
presence_acteur = pd.read_csv('https://raw.githubusercontent.com/BerengerQueune/ABC-Data/main/Berenger/Streamlit/presence_acteurs.csv?token=AU6BUZRUOZP7577TQEBP5ODBS2IXQ')
link2 = 'https://raw.githubusercontent.com/BerengerQueune/ABC-Data/main/Berenger/Streamlit/film3.csv?token=AU6BUZQSZO7FES64E636CRLBS2IWM'
film = pd.read_csv(link2)
link3 = 'https://raw.githubusercontent.com/BerengerQueune/ABC-Data/main/Berenger/Streamlit/concat_liste50.csv?token=AU6BUZSY6OPPE25EYFUWFELBS2IS4'
link4 = 'https://raw.githubusercontent.com/BerengerQueune/ABC-Data/main/Berenger/Streamlit/concat_listeTopFilm.csv?token=AU6BUZUX7HJJXUSIP47YANLBS2IVA'
link5 = 'https://raw.githubusercontent.com/BerengerQueune/ABC-Data/main/Berenger/Streamlit/concat_listeTopTV.csv?token=AU6BUZWRESNKYQ36Y652SJLBS2IVW'
concat_liste_50 = pd.read_csv(link3)
concat_listeTopFilm = pd.read_csv(link4)
concat_listeTopTV = pd.read_csv(link5)

fig = px.bar(presence_acteur, x="primaryName", y ='index', color = 'index',
    title = 'Quels sont les acteurs les plus présents ?',
    labels = {'primaryName': 'Nombre de films', 'index': 'Acteurs'},
    width=800, height=600)

fig.update_layout(showlegend=False, title_x=0.5, yaxis={'visible': True})

st.plotly_chart(fig)

fig = px.bar(acteur_par_periode, x = 'count', y="rank", text ='primaryName', color = 'primaryName',
    title = 'Quels sont les acteurs les plus présents par périodes ?',
    labels = {'startYear': 'Période', 'primaryName': 'Acteurs'},
    orientation='h',
    animation_frame="startYear",
    range_x=[0,150],
    range_y=[0,6],
    width=800, height=500)
 
fig.update_traces(textfont_size=12, textposition='outside')
fig.update_layout()
fig.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = 1000

fig.update_layout(showlegend=False, title_x=0.5)

st.plotly_chart(fig)

test5 = px.bar(top10, x='Pays', y='Nb de films', color="Nb de films", color_continuous_scale=px.colors.sequential.Viridis, title = 'Pays produisants le plus de film depuis 1960', width=700, height=500)

st.plotly_chart(test5)


fig = make_subplots(rows=2, cols=2)

fig.add_trace(go.Line(x = film["startYear"], y=film["runtimeMinutes"]),
              row=1, col=1)

fig.add_trace(go.Line(x = film["startYear"], y=film["runtimeMinutes"]),
              row=1, col=2)

fig.add_trace(go.Line(x = film["startYear"], y=film["runtimeMinutes"]),
              row=2, col=1)

fig.add_trace(go.Line(x = film["startYear"], y=film["runtimeMinutes"]),
              row=2, col=2)

fig.update_layout(autosize=False, template='plotly_dark', width = 1500, height = 700, showlegend=False)

fig.update_xaxes(title_text="", row=1, col=1)
fig.update_yaxes(title_text="Minutes", row=1, col=1)


fig.update_xaxes(title_text="", row=1, col=2)
fig.update_yaxes(title_text="Minutes", row=1, col=2, range=[80, 100])


fig.update_xaxes(title_text="", row=1, col=1)
fig.update_yaxes(title_text="Minutes", row=2, col=1, range=[50, 100])


fig.update_xaxes(title_text="", row=1, col=2)
fig.update_yaxes(title_text="Minutes", row=2, col=2, range=[0, 100])

fig.update_layout(height=1000, width=1400, title_text="Evolution de la durée des films depuis 1960", title_x=0.5)



st.plotly_chart(fig)


fig = px.bar(data_frame = concat_liste_50, x= "primaryName", y="nb", color = 'type', color_discrete_sequence=["darkred", "green"],labels=dict(primaryName="Nom de l'acteur", nb="Nombre de films"))
fig.update_layout(title_text="Top 20 des acteurs ayant tournés autant au cinéma qu'à la TV", width=1000, height=600)

st.plotly_chart(fig)



fig = px.bar(data_frame = concat_listeTopFilm, x= "primaryName", y="nb", color = 'type', color_discrete_sequence=["blue", "lime"], labels=dict(primaryName="Nom de l'acteur", nb="Nombre de films", color = 'type'))
fig.update_layout(title_text="Top 20 des acteurs ayant tournés le plus du film au cinéma", title_x=0.5, width=1000, height=600)

st.plotly_chart(fig)


fig = px.bar(data_frame = concat_listeTopTV, x= "primaryName", y="nb", color = 'type', color_discrete_sequence=["orange", "olive"], labels=dict(primaryName="Nom de l'acteur", nb="Nombre de films"))
fig.update_layout(title_text="Top 20 des acteurs ayant tournés le plus du film à la télévision", title_x=0.5, width=1000, height=600)

st.plotly_chart(fig)