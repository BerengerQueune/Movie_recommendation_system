######################################################################################
######################################################################################
###########################     LIBRAIRIES    ########################################
######################################################################################
######################################################################################

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
from sklearn.neighbors import NearestNeighbors
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import imdb
import imdb.helpers


######################################################################################
######################################################################################
###########################     CSS CODE   ###########################################
######################################################################################
######################################################################################

# CSS code to hide footer and header automatically installed on streamlit page
# I keep the main menu so people can switch from dark to light and vice versa
hide_menu= """
<style>
    #MainMenu {visibility:visible;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

</style>
"""

######################################################################################
######################################################################################
###########################     DONNEES    ###########################################
######################################################################################
######################################################################################

#df_recommandation = pd.read_csv('https://raw.githubusercontent.com/BerengerQueune/ABC-Data/main/Berenger/Database_projet/df_recommendation.csv?token=AU6BUZUA5UESEPKRRJQIESLBS53UU')
df = pd.read_csv('https://raw.githubusercontent.com/BerengerQueune/ABC-Data/main/Berenger/Database_projet/df_base.csv?token=AU6BUZWHN456IAMFBUWFFSDBTELCU')
FULL_DF = pd.read_csv('https://raw.githubusercontent.com/BerengerQueune/ABC-Data/main/Aurore/KPI/DF_FULL_GENRES211117.csv?token=AUTGRH2WPDMVJ7DBATL3KWDBTYLIM')


# Loading dataframe, df_input_movies = your favorite movies
# df_output_movies = movie suggested
df_output_movies = pd.read_csv('https://raw.githubusercontent.com/BerengerQueune/ABC-Data/main/Berenger/Database_projet/df_recommandation.csv?token=AU6BUZU75XQAMO3ALFRQGCTBTZFHU')
df_input_movies = pd.read_csv('https://raw.githubusercontent.com/BerengerQueune/ABC-Data/main/Berenger/Database_projet/table_finale_alphabetique_numero_2.csv?token=AU6BUZVXK46AQSMDSIAFPITBT6KLG')


######################################################################################
######################################################################################
###########################     FONCTIONS    #########################################
######################################################################################
######################################################################################


@st.cache
def load_df(url):
    df = pd.read_csv(url)
    df.set_index(df.iloc[:,0], inplace=True)
    df = df.iloc[:, 1:]
    return df



######################################################################################
######################################################################################
###########################     INTERFACE    #########################################
######################################################################################
######################################################################################


#set the page layout to automatically use full horoizontal size + get and icon and name inside the internet browser
st.set_page_config(page_title="ABC'S", page_icon=":heart:", layout='wide')


def main():
    # This is used to activate the CSS code at the top
    st.markdown(hide_menu, unsafe_allow_html=True)
    
    
    # Menu and Sidebar creation
    menu = ["Pr??sentation du Projet", "Analyses et KPI","Syst??me de recommandation", "Axes d'Am??lioration"]
    choice = st.sidebar.selectbox("", menu) 


######################################################################################
######################################################################################
###########################     AURORE     ###########################################
######################################################################################
######################################################################################
    if choice == "Pr??sentation du Projet":
                # CSS code within markdown to center the title
        st.markdown("<h1 style='text-align: center;'>Pr??sentation du Projet</h1>", unsafe_allow_html=True)
                # This create a nice grey line between the title and the multiselect menu
        st.write("---------------------------------------------------------")
        st.subheader('')
        st.subheader("Le Projet")

        st.markdown(
        """
        Le _PROJET ABC'S_ est issu d???un projet d?????cole organis?? par la __Wild Code School__. Il intervient dans le cadre de notre formation de Data Analyst, 2 mois apr??s son d??but.

        L???objectif de ce projet est le suivant :

        Nous sommes une ??quipe de Data Analysts freelance.
        Un cin??ma en perte de vitesse situ?? dans la Creuse nous contacte car il a d??cid?? de passer le cap du digital en cr??ant un site Internet taill?? pour les locaux.
        Notre client nous demande de cr??er un moteur de recommandations de films qui ?? terme, enverra des notifications via internet.

        Aucun client du cin??ma n'ayant ?? ce jour renseign?? ses pr??f??rences, nous sommes donc dans une situation de __cold start__. Cependant, notre client nous a fourni une base de donn??es bas??e sur la plateforme IMDb.

        """
        )
        st.subheader('')
        st.subheader("L'??quipe")

        st.markdown(
        """
        Notre ??quipe est compos??e de 4 ??l??ves issus de la promo Data Green de la __Wild Code School__ :
        - [Aurore LEMA??TRE](https://github.com/alema86)
        - [B??renger QUEUNE](https://github.com/BerengerQueune)
        - [Christophe LEFEBVRE](https://github.com/clefebvre2021)
        - [St??phane ESSOUMAN](https://github.com/Liostephe)

        Tous les quatre formons l'??quipe ABC'S Data.
        """
        )
        col1, col2, col3 = st.columns(3)
        with col2:
            st.image("https://d1qg2exw9ypjcp.cloudfront.net/assets/prod/24134/210x210-9_cropped_1377120495_p182hcd8rofaq1t491u06kih16o13.png")

        st.subheader('')
        st.subheader("Notre cliente")

        col1, col2, col3 = st.columns(3)
        with col1:
            st.image("https://i.ibb.co/0hnKBMX/Framboise2.png")

        st.markdown(
        """
        Notre cliente est Framboise de Papincourt, petite fille du Comte de Montmirail. Elle a 25 ans et dirige un cin??ma en perte de vitesse qui s'appelle "LE KINO".

        Elle fait appel ?? nous car elle est d??sesp??r??e. Son cin??ma ne fait pas de b??n??fice, ses cr??anciers sont ?? sa porte et ses probl??mes financiers sont tels qu'elle a d?? demander un nouveau pr??t dans une banque. Ce qui va ?? l'encontre de ses principes.

        Issue d'une famille noble, elle ne peut pas faire appel ?? ses proches qui sont fortun??s, car elle a reni?? sa famille. En effet, ces derniers ne partagent pas sa vision des choses; exemple : elle est vegan alors que l'activit?? principale de sa famille est la chasse...

        Elle diffusait initialement des films qui la touchaient afin d'essayer de partager sa vision du monde. Ainsi, la films diffus??s ??taient principalement des documentaires traitant de l'??cologie, du f??minisme indiens, en VOSTFR, et de la paix universelle.

        Elle est oblig??e de faire changer de cap son cin??ma et est pr??te ?? diffuser des films qui vont ?? l'encontre de ses convictions si ??a lui permet de ne pas mettre la cl?? sous la porte et ??viter d'??tre la raillerie de sa famille.
        Faire du b??n??fice ?? terme serait un plus, car ??a lui permettrait d'offrir ?? ses futurs enfants Harmony, Safran et Kiwi un environnement dans lequel ils pourront s'??panouir comme elle en r??ve.

        Ainsi, elle nous donne carte blanche dans le rendu de notre travail.
        """  
        )    
        st.subheader('')
        st.subheader("Notre mission")

        st.markdown(
        """
        Nous devons fournir ?? notre client les outils d???analyse de la base de donn??es issue de **IMDB**.
       
        Il nous est demand?? de :
        """
        )
        st.markdown(
        """ 
        - Faire une rapide pr??sentation de la base de donn??es (sur notre espace collaboratif sur Github)
        """
        )
        st.markdown(
        """ 
        - Fournir ?? notre client quelques statistiques sur les films :
        """
        )
        st.markdown(
        """ 
            * Films : types, dur??es...
        """
        )
        st.markdown(
        """ 
            * Acteurs : nombre de films, type de films...
        """
        )
        st.markdown(
        """ 
        - Pr??senter les TOP 10 des films par ann??es et genres
        """
        )
        st.markdown(
        """ 
        - Pr??senter les TOP 5 des acteurs/actrices par ann??es et genres
        """
        )
        st.markdown(
        """ 
        - Retourner une liste de films recommand??s en fonction d'IDs ou de noms de films choisis par un utilisateur
        """
        )
        st.markdown(
        """ 
        - Il faudra entra??ner des outils de Machine Learning : 
        """
        )
        st.markdown(
        """ 
	        * Recommandation de films proches d???un film cible gr??ce ?? un mod??le de **KNN**
        """
        )
        st.markdown(
        """ 
	        * Proposition d???une r??trospective avec un mod??le de **R??gression Logistique**
        """
        )

        st.subheader('')
        st.subheader("Outils")

        st.markdown(
        """
        Le projet est enti??rement fait sous **Python** avec une touche de CSS.

        Nous avons utilis?? les librairies suivantes :    
        - Pandas
        - Sklearn
        - Plotly
        - Streamlit
        - IMDbPY
        """
        )

        st.subheader('')
        st.subheader("Base de donn??es")

        st.markdown(
        """
        Comme ??nonc?? ci-avant, notre client nous a fourni une base de donn??es bas??e sur la plateforme IMDb. 
        Nous pouvons les retrouver [**ici**](https://datasets.imdbws.com/), l'explicatif des datasets [**l??**](https://www.imdb.com/interfaces/).

        Nous laissons ?? disposition notre analyse de ces bases de donn??es sur Github dans [**notre espace collaboratif**](https://github.com/BerengerQueune/ABC-Data).
        """
        )

######################################################################################
######################################################################################
###########################     BERENGER     #########################################
######################################################################################
######################################################################################

# Result from your choice inside the menu
    elif choice == 'Syst??me de recommandation':

        # CSS code within markdown to center the title
        st.markdown("<h1 style='text-align: center;'>Recommandation de Films</h1>", unsafe_allow_html=True)

        # Variable X used for Machine Learning
        X = df_output_movies[['Action',
            'Adventure', 'Animation', 'Biography', 'Comedy', 'Crime', 'Documentary',
            'Drama', 'Fantasy', 'History', 'Horror', 'Music', 'Musical', 'Mystery',
            'Romance', 'Sci-Fi', 'Sport', 'Thriller', 'Western']]

        # This create a nice grey line between the title and the multiselect menu
        st.write("---------------------------------------------------------")
        



        # Variables to insert df_input inside the multiselect menu
        MOVIES = df_input_movies['primaryTitle'].unique()
        MOVIES_SELECTED = st.multiselect(' ', MOVIES)

        # Mask to filter dataframe
        mask_movies = df_input_movies['primaryTitle'].isin(MOVIES_SELECTED)
        data = df_input_movies[mask_movies]

        # Variables to gather the genre of all movies selected within the multiselect menu
        user_choice6 = data[['Action',
            'Adventure', 'Animation', 'Biography', 'Comedy', 'Crime', 'Documentary',
            'Drama', 'Fantasy', 'History', 'Horror', 'Music', 'Musical', 'Mystery',
            'Romance', 'Sci-Fi', 'Sport', 'Thriller', 'Western']]

        # KNN nearest neighbors to find the 5 nearest neighbors
        distanceKNN = NearestNeighbors(n_neighbors=5).fit(X)
        # I divide the genre of all movies based on the number of movies
        genres_divided_by_number_of_movies = user_choice6/len(data)
        # I make the sum of all genres into a new dataframe in order to find a central point for all the movies selected
        sum_of_genres = genres_divided_by_number_of_movies.sum()
        df_sum_of_genres = pd.DataFrame(sum_of_genres)

        # I transpose rows to columns so the dataframe shape matches the expectation for the recommandation
        df_final_genres = df_sum_of_genres.T

        # KNN method to find the nearest neighbors
        df_final_genres = distanceKNN.kneighbors(df_final_genres)
        # A reshape again... not sure if really required
        df_final_genres = df_final_genres[1].reshape(1,5)[0]
        # Looking for index of movies that matches the most
        liste_finale = df_output_movies.iloc[df_final_genres]

        # Creation of a variable used later to each instance of nearest neighbors (5) within a different columns
        numero_colonne = 0

        # Small space
        st.write(" ")
        st.write(" ")

        # creating instance of IMDb this is a library to easily get the poster of the movie recommanded
        ia = imdb.IMDb()
        # if/else: if there is 0 movie selected, then there is no recommandation
        if len(user_choice6) == 0:
            pass
        else:
            # CSS title followed by space
            st.markdown("<h5 style='text-align: center;'>Ces films devraient plaire ?? vos clients :</h5>", unsafe_allow_html=True)
            st.write(" ")
            st.write(" ")
            # Creation of 5 columns
            cols = st.columns(5)
            for i in range(len(liste_finale)):
                
                # For Each columns
                with cols[numero_colonne]:
                    # Get the name of the movie
                    movie_name = liste_finale.iloc[i]["primaryTitle"]
                    # Get the tconst (used to gather poster image)
                    code = liste_finale.iloc[i]["tconst"]
                    # Remove the "tt" string at start of the tconst
                    code = code.replace("tt", "")
                    # getting information from the movie related to previous tconst
                    series = ia.get_movie(code)
                    try:
                        # If there is a cover for this movie, print the cover + the name of the movie as caption and use automatically full size of the column
                        st.image(imdb.helpers.fullSizeCoverURL(series), use_column_width='auto', caption=movie_name)
                    except:
                        # If there is no cover, use this image picked randomly over internet + the name of the movie as caption and use automatically full size of the column
                        st.image("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRYEBKhlYYZa4Saksn04meXChE44J1PU9BCZA&usqp=CAU", 
                        use_column_width="always", caption=movie_name)
                # Add one to the numero_colonne variable so next nearest neighbors will be inside the following column
                numero_colonne +=1

    
######################################################################################
######################################################################################
###########################     AURORE     ###########################################
######################################################################################
######################################################################################   



    elif choice == "Analyses et KPI":

        
        

        link2 = 'https://raw.githubusercontent.com/BerengerQueune/ABC-Data/main/Berenger/Streamlit/film3.csv?token=AUTGRH7SSI52W67SWYW35Z3BT7VCQ'
        film = pd.read_csv(link2)


        


        #######################################
        ########  Introduction     ############
        #######################################

                        # CSS code within markdown to center the title
        st.markdown("<h1 style='text-align: center;'>Analyses et KPI</h1>", unsafe_allow_html=True)
                # This create a nice grey line between the title and the multiselect menu
        st.write("---------------------------------------------------------")
        st.write("")
        st.subheader("Analyses de la base de donn??es et KPI") # add a subtitle

        st.write("Comme ??nonc?? dans notre partie **'Pr??sentation du Projet'**, il nous est demand?? de :")
        st.markdown(
        """
        - Faire une rapide pr??sentation de la base de donn??es (que vous pouvez retrouver [ici](https://github.com/BerengerQueune/ABC-Data/blob/main/Aurore/Analyses_BDD_Etape%201.ipynb))
        - Faire une analyse compl??te de la base de donn??es, en r??pondant aux questions suivantes :
            * Quels sont les pays qui distribuent le plus de films ?
            * Quels sont les acteurs les plus pr??sents ? ?? quelle p??riode ?
            * La dur??e moyenne des films s???allonge ou se raccourcit avec les ann??es ?
            * Les acteurs de s??rie sont-ils les m??mes qu???au cin??ma ? 
            * Les acteurs ont en moyenne quel ??ge ? 
            * Quels sont les films les mieux not??s ? Partagent-ils des caract??ristiques communes ?
        """
        )
        st.write(' ')
        st.write(' ')
        st.write(' ')
        st.write(' ')
        #######################################
        ########    GRAPHIQUES     ############
        #######################################

        #######################################
        ########  Q01 -Christophe  ############
        #######################################
        st.subheader("Quels sont les pays qui distribuent le plus de films ?") # add a subtitle


        top10 = pd.read_csv('https://raw.githubusercontent.com/BerengerQueune/ABC-Data/main/Berenger/Streamlit/top10.csv?token=AUTGRH3VKF2D42DBVDKVIADBT7VO6')

        col1, col2 = st.columns([1, 2])
        with col1:
            st.write(' ')
            st.markdown(
                """
                Le dataset a ??t?? ??labor?? ?? partir de deux fichiers : title.basics et title.akas.

                Lors de notre analyse de la base de donn??es, nous avons pu observer une grande vari??t?? de types d'oeuvres r??pertori??es par IMDb. 

                Ainsi, ?? partir de title.basics, il a ??t?? choisi de ne retenir que les films ('movie') et t??l??films ('tvMovie) r??alis??s apr??s 1960, limitant notre p??rim??tre d???analyse aux films les plus r??cents. Les courts-m??trages (???short???) ont ??galement ??t?? retir??s.
                Les lignes n'ayant pas de donn??es pour les items suivants ont ??t?? supprim??es de notre DataFrame: ann??e de r??alisation ('startYear'), de dur??e ('runtimeMinutes') ou de genres ('genres').

                De la m??me fa??on, les films qui n???ont pas de r??gion dans le fichiers title.akas ont ??t?? supprim??s.

                Une jointure a ??t?? r??alis??e entre les deux DataFrame afin d???ajouter la r??gion aux colonnes de la base de donn??es title.basics.

                Afin de r??aliser le graphique, un [dataframe attitr??](https://raw.githubusercontent.com/BerengerQueune/ABC-Data/main/Berenger/Streamlit/top10.csv?token=AU6BUZSEQED65VJVLNSX4FLBS2IYO) reprenant  le top 10 des pays ayant distribu?? le plus de films et t??l??films a ??t?? produit.

                [Lien Notebook](https://github.com/BerengerQueune/ABC-Data/blob/main/Christophe/Projet%202%20-%20Quels%20sont%20les%20pays%20qui%20produisent%20le%20plus%20de%20films.ipynb)

                """
                )

        with col2:
            top10Graph = px.bar(top10, x='Pays', y='Nb de films', color="Nb de films")
            top10Graph.update_layout(title_text="Palmar??s des pays selon la distribution des oeuvres cin??matographiques", title_x=0.5, width=1000, height=600, template='plotly_dark')
            st.plotly_chart(top10Graph)

        st.write("")
        st.image("https://i.ibb.co/NV1RFNH/C-mod.png") 
        st.markdown("""
                Ce graphique montre clairement une pr??dominance des USA dans le nombre de films distribu??s, puisque leur nombre d??passe la somme de ceux r??alis??s dans les deux pays suivants ?? savoir la Grande-Bretagne et la France.               
                A noter que l???on retrouve en troisi??me position des films dont l???origine est inconnue XWW. Cette r??gion signifie 'World Wide' et correspond aux oeuvres que l'on peut retrouver sur internet (web, Youtube...).
                On note ??galement que trois des 5 continents sont repr??sent??s dans le top10.
                La France confirme cependant sa position de cin??phile en ??tant dans le top 3 si nous excluons la r??gion 'XWW'.
                """
                )
        st.write(' ')
        st.write(' ')
        st.write(' ')
        #####################################
        ########  Q02 -B??renger  ############
        #####################################
        st.subheader("Quels sont les acteurs les plus pr??sents ?") # add a subtitle
 
        presence_acteur = pd.read_csv('https://raw.githubusercontent.com/BerengerQueune/ABC-Data/main/Berenger/Database_projet/presence_acteurs.csv?token=AU6BUZU76KCNKK6X5NKIZ6DBTZPVI')

        col1, col2 = st.columns([2, 1])
        with col2:
            st.write(' ')
            st.markdown(
                """
                Le dataset a ??t?? ??labor?? ?? partir de 3 fichiers : name.basics.tsv, title.principals.tsv et title.basics.tsv.

                Nous avons nettoy?? la base de donn??es de la fa??on suivante :
                - dans le df relatif ?? 'title.principals.tsv', nous avons gard?? les colonnes 'tconst', 'titleType', 'startYear', 'runtimeMinutes' et 'genres'
                    - dans la colonne 'category' nous avons gard?? les 'actor' et 'actress'
                    - dans la colonne 'character', nous avons supprim?? les ```\R```, les 'Narrator', 'Various' et 'Additional Voices'
                - dans le df relatif ?? 'title.basics.tsv', nous avons gard?? les colonnes 'tconst', 'nconst', 'category' et 'characters'

                Afin de r??aliser le graphique, un [dataframe attitr??]('https://raw.githubusercontent.com/BerengerQueune/ABC-Data/main/Berenger/Database_projet/presence_acteurs.csv?token=AU6BUZU76KCNKK6X5NKIZ6DBTZPVI') reprenant les 20 acteurs les plus pr??sents quelle que soit l'??poque a ??t?? produit.

                [Lien Notebook](https://raw.githubusercontent.com/BerengerQueune/ABC-Data/main/Berenger/Quels_sont_les_acteurs_les_plus_pr%C3%A9sents.ipynb?token=AUTGRHYRYCTRXKOZDDLVIELBTZL3I)

                """
                )

        with col1:
            fig = px.bar(presence_acteur, x="primaryName", y ='index', color = 'index',
            title = 'Quels sont les acteurs les plus pr??sents ?',
            labels = {'primaryName': 'Nombre de films', 'index': 'Acteurs'},
            width=800, height=600)

            fig.update_layout(showlegend=False, title_x=0.5, yaxis={'visible': True}, template='plotly_dark')

            st.plotly_chart(fig)

        st.write("")
        st.image("https://i.ibb.co/bHkZJb7/B-mod.png") 
        st.markdown("""
                Nous avons trouv?? int??ressant, dans le cadre de nos ??tudes, de r??pondre ?? cette question car cela a ??t?? l'occasion de s'exercer ?? explorer et nettoyer une base de donn??es. Cependant, nous trouvons que la r??ponse en elle-m??me n'apporte que peu d'??l??ments, voire aucun, qui puissent aider notre cliente ?? prendre des d??cisions.
                """
                )


        st.write(' ')
        st.write(' ')
        st.write(' ')
        #####################################
        ########  Q03 -B??renger  ############
        #####################################
        st.subheader("Quels sont les acteurs les plus pr??sents, ?? quelle p??riode ?") # add a subtitle

        acteur_par_periode = pd.read_csv("https://raw.githubusercontent.com/BerengerQueune/ABC-Data/main/Berenger/Streamlit/acteur_par_periode.csv?token=AUTGRH4M4FBOFMK6DAW3X33BT6Z2S")
        col1, col2 = st.columns([1, 2])
        with col1:
            st.write(' ')
            st.write('')
            st.write(' ')
            st.write(' ')
            st.markdown(
                """
            
                Pour ce graphique, nous avons pu utiliser une partie du travail effectu?? dans la question pr??c??dente.

                Afin de r??aliser le graphique, un [dataframe attitr??]('https://raw.githubusercontent.com/BerengerQueune/ABC-Data/main/Berenger/Streamlit/acteur_par_periode.csv?token=AU6BUZWYJ6GYLJLQVDQCLZTBSZ2NK') reprenant les 5 acteurs les plus pr??sents pour chaque d??cennies depuis 1910.

                [Lien Notebook](https://raw.githubusercontent.com/BerengerQueune/ABC-Data/main/Berenger/Quels_sont_les_acteurs_les_plus_pr%C3%A9sents.ipynb?token=AUTGRHYRYCTRXKOZDDLVIELBTZL3I)

                """
                )

        with col2:
            
            fig = px.bar(acteur_par_periode, x = 'count', y="rank", text ='primaryName', color = 'primaryName',
            title = 'Quels sont les acteurs les plus pr??sents par p??riodes ?',
            labels = {'startYear': 'P??riode', 'primaryName': 'Acteurs'},
            orientation='h',
            animation_frame="startYear",
            range_x=[0,150],
            range_y=[0,6],
            width=800, height=500)
        
            fig.update_traces(textfont_size=12, textposition='outside')
            fig.update_layout(template='plotly_dark')
            fig.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = 1000

            fig.update_layout(showlegend=False, title_x=0.5)

            st.plotly_chart(fig)

        st.write("")
        st.image("https://i.ibb.co/bHkZJb7/B-mod.png") 
        st.markdown("""
                Dans le cadre de nos ??tudes, il est int??ressant de r??pondre ?? cette question car cela a ??t?? l'occasion de s'exercer ?? l'exploration et au nettoyage d'une base de donn??es. 
                
                Cependant, la r??ponse en elle-m??me n'apporte elle aussi que peu d'??l??ments, voire aucun, qui puissent aider notre cliente ?? prendre des d??cisions. 

                """
                )
        st.write(' ')
        st.write(' ')
        st.write(' ')
        #######################################
        ########  Q04 -Christophe  ############
        #######################################
        st.subheader("La dur??e moyenne des films s???allonge ou se raccourcit avec les ann??es ?") # add a subtitle
 
        presence_acteur = pd.read_csv('https://raw.githubusercontent.com/BerengerQueune/ABC-Data/main/Berenger/Database_projet/presence_acteurs.csv?token=AU6BUZU76KCNKK6X5NKIZ6DBTZPVI')

        st.markdown(
                """
                Le dataset a ??t?? ??labor?? ?? partir d???un seul fichier : title.basics.tsv.

                Le fichier title.basics a ??t?? trait?? comme pour la question relative aux pays les plus distributeurs (Q01), ?? l???exception du type qui a ??t?? limit?? aux films ('movie'); les 'tvMovie' ont donc ??t?? supprim??s.
                Nous avons calcul?? la dur??e moyenne des films par ann??e et conserv?? que les ann??es ??chues.

                Afin de r??aliser le graphique, un [dataframe attitr??](https://raw.githubusercontent.com/BerengerQueune/ABC-Data/main/Berenger/Database_projet/presence_acteurs.csv?token=AU6BUZU76KCNKK6X5NKIZ6DBTZPVI) reprennant toutes les informations requises a ??t?? produit.

                [Lien Notebook](https://raw.githubusercontent.com/BerengerQueune/ABC-Data/main/Christophe/Projet%202%20-%20La%20dur%C3%A9e%20moyenne%20des%20films%20s%E2%80%99allonge%20ou%20se%20raccourcit%20avec%20les%20ann%C3%A9es.ipynb?token=AUTGRH3TRSZ7CDJ62ME6XU3BT44DO)

                """
            )

        fig = make_subplots(rows=2, cols=2)

        fig.add_trace(go.Line(x = film["startYear"], y=film["runtimeMinutes"]),row=1, col=1)
        fig.update_xaxes(title_text="", row=1, col=1)
        fig.update_yaxes(title_text="", row=1, col=1)

        fig.add_trace(go.Line(x = film["startYear"], y=film["runtimeMinutes"]), row=1, col=2)
        fig.update_xaxes(title_text="", row=1, col=2)
        fig.update_yaxes(title_text="", row=1, col=2, range=[80, 100])

        fig.add_trace(go.Line(x = film["startYear"], y=film["runtimeMinutes"]),row=2, col=1)
        fig.update_xaxes(title_text="", row=1, col=1)
        fig.update_yaxes(title_text="", row=2, col=1, range=[50, 100])

        fig.add_trace(go.Line(x = film["startYear"], y=film["runtimeMinutes"]),row=2, col=2)
        fig.update_xaxes(title_text="", row=1, col=2)
        fig.update_yaxes(title_text="", row=2, col=2, range=[0, 100])

        fig.update_layout(height=1000, width=1400, title_text="Evolution de la dur??e des films en minutes depuis 1960", title_x=0.5, showlegend=False, template='plotly_dark', autosize=False)

        st.plotly_chart(fig)

        st.write("")
        st.image("https://i.ibb.co/NV1RFNH/C-mod.png") 
        st.markdown("""
                La lecture du premier graphique (en haut ?? gauche), donne l???impression d???une grande variabilit?? de la dur??e des films entre 1960 et 2020.
                Il s???agit en fait d???un biais de lecture li?? ?? l?????chelle utilis??e. Comme la dur??e varie r??ellement peu (entre 87 et 95 mn), l?????chelle du graphique a ??t?? automatiquement adapt??e et fait ressortir une variation importante.
                
                Les trois graphiques suivants montrent donc les donn??es avec une ??chelle de plus en plus large.

                Si l???on regarde le dernier graphique (avec une ??chelle de 0 ?? 100), la dur??e des films d???une ann??e sur l???autre para??t ?? peu pr??s stable.
                """
                )
        st.write(' ')
        st.write(' ')
        st.write(' ')
        #######################################
        ########  Q05 -Christophe  ############
        #######################################
        st.subheader("Les acteurs de s??rie sont-ils les m??mes qu???au cin??ma ?") # add a subtitle
 
        concat_liste_50 = pd.read_csv('https://raw.githubusercontent.com/BerengerQueune/ABC-Data/main/Berenger/Streamlit/concat_liste50.csv?token=AUTGRH3NFGVAAGE7BWNHXW3BT7VXW')
        concat_listeTopFilm = pd.read_csv('https://raw.githubusercontent.com/BerengerQueune/ABC-Data/main/Berenger/Streamlit/concat_listeTopFilm.csv?token=AUTGRHZX2ORHPD4O4BU5KL3BT7V2I')
        concat_listeTopTV = pd.read_csv('https://raw.githubusercontent.com/BerengerQueune/ABC-Data/main/Berenger/Streamlit/concat_listeTopTV.csv?token=AUTGRH6HV3KXHBV5F5IJWHTBT7V3S')

        st.markdown(
                """
                Le dataset a ??t?? ??labor?? ?? partir de trois fichiers : title.basics et title.principals et name.basics.

                Le fichier title.basics a ??t?? trait?? comme pour la question n??1.
                
                A partir de title.basics, il a ??t?? choisi de ne retenir que les films et t??l??films r??alis??s ?? partir de 1960, afin de limiter le p??rim??tre d???analyse aux films les plus r??cents. Les courts m??trages (???short???) ont ??galement ??t?? retir??s.
                Un certain nombre de ces films n???ont pas d???ann??e de r??alisation, de dur??e ou de genres. Ils ont donc ??t?? supprim??s de la base.

                Le fichier title.principals a ??t?? filtr?? pour ne conserver que les items actrices et acteurs. Le fichier name.basics ?? permis de faire le lien avec leur nom.

                Afin de r??aliser le graphique, 3 dataframes attitr??s reprenant toutes les informations dont nous avions besoin ont ??t?? produits :
                - [Top 20 des acteurs ayant tourn?? autant de films que de t??l??films](concat_liste_50)
                - [Top 20 des acteurs ayant tourn?? le plus de films](concat_listeTopFilm)
                - [Top 20 des acteurs ayant tourn?? le plus de t??l??films](concat_listeTopTV)

                [Lien Notebook](https://github.com/BerengerQueune/ABC-Data/blob/main/Christophe/Projet%202%20-%20Quels%20sont%20les%20pays%20qui%20produisent%20le%20plus%20de%20films.ipynb)

                Les ??l??ments en notre possession nous ont permis de cr??er 3 graphiques :
                """
            )

        col1, col2 = st.columns([1, 2])
        with col1:
            st.write(' ')
            st.write(' ')
            st.write(' ')
            st.write(' ')
            st.write(' ')
            st.write(' ')
            st.write(' ')
            st.write(' ')
            st.write(' ')
            st.write(' ')
            st.write(' ')
            st.write(' ')
            st.markdown(
                """
                        **Top 20 des acteurs ayant tourn?? autant de films que de t??l??films**

                         Il s???agit des acteurs des acteurs qui ont tourn?? le plus tout en faisant autant de t??l??film que de film.
                        La quantit?? de films par acteurs semble assez faible par rapport aux deux cat??gories suivantes.
                """
                )

        with col2:
            fig = px.bar(data_frame = concat_liste_50, x= "primaryName", y="nb", color = 'type', color_discrete_sequence=["darkred", "green"],labels=dict(primaryName="Nom de l'acteur", nb="Nombre de films"))
            fig.update_layout(title_text="Top 20 des acteurs ayant tourn??s autant au cin??ma qu'?? la TV", width=1000, height=600, template='plotly_dark')

            st.plotly_chart(fig)

        st.write("")
        st.write("")

        col1, col2 = st.columns([1, 2])
        with col1:
            st.write(' ')
            st.write(' ')
            st.write(' ')
            st.write(' ')
            st.write(' ')
            st.write(' ')
            st.write(' ')
            st.write(' ')
            st.write(' ')
            st.write(' ')
            st.write(' ')
            st.write(' ')
            st.markdown(
                """
                        **Top 20 des acteurs ayant tourn?? le plus de films**

                        Le graphique montre clairement que les acteurs ayant le plus tourn??s au cin??ma ont fait tr??s peu de t??l??films.
                        Il faut effectivement zoomer sur le graphique pour s???apercevoir que 4 d???entre aux ont tourn??s dans un ou deux t??l??films seulement.
                """
                )

        with col2:
            fig = px.bar(data_frame = concat_listeTopFilm, x= "primaryName", y="nb", color = 'type', color_discrete_sequence=["blue", "lime"], labels=dict(primaryName="Nom de l'acteur", nb="Nombre de films", color = 'type'))
            fig.update_layout(title_text="Top 20 des acteurs ayant tourn??s le plus de films au cin??ma", title_x=0.5, width=1000, height=600, template='plotly_dark')

            st.plotly_chart(fig)

        st.write("")
        st.write("")

        col1, col2 = st.columns([1, 2])
        with col1:
            st.write(' ')
            st.write(' ')
            st.write(' ')
            st.write(' ')
            st.write(' ')
            st.write(' ')
            st.write(' ')
            st.write(' ')
            st.write(' ')
            st.write(' ')
            st.write(' ')
            st.write(' ')
            st.markdown(
                """
                        **Top 20 des acteurs ayant tourn?? le plus de t??l??films**

                        On s???aper??oit qu????? l???inverse des acteurs de cin??ma, les acteurs ayant tourn??s le plus de t??l??films ont ??galement tourn??s des films au cin??ma.
                        Cependant, au global ont remarque qu'ils ont tourn??s dans moins de films mais ont tous fait au moins des apparitions au cin??ma.
                """
            )

        with col2:
            fig = px.bar(data_frame = concat_listeTopTV, x= "primaryName", y="nb", color = 'type', color_discrete_sequence=["orange", "olive"], labels=dict(primaryName="Nom de l'acteur", nb="Nombre de films"))
            fig.update_layout(title_text="Top 20 des acteurs ayant tourn??s le plus de t??l??films", title_x=0.5, width=1000, height=600, template='plotly_dark')

            st.plotly_chart(fig)
        
        st.write('')
        st.write(' ')
        st.write(' ')

        #######################################
        ##########  Q06 -Aurore  ##############
        #######################################
        st.subheader("Les acteurs ont en moyenne quel ??ge ?") # add a subtitle
        Age_DF_clean = pd.read_csv('https://raw.githubusercontent.com/BerengerQueune/ABC-Data/main/Aurore/KPI/Age_acteurs20211118.csv?token=AUTGRH6AOVYKCSBEBIWDCLTBT5VZI')
        st.markdown(
                """
                Le dataset a ??t?? ??labor?? ?? partir de 3 fichiers : name.basics.tsv, title.principals.tsv et title.basics.tsv.

                Apr??s s??lection des colonnes ?? utiliser, nous avons nettoy?? la base de donn??es comme ?? notre habitude.

                Nous avons appliqu?? les filtres suivants, tant pour notre analyse que pour des besoins techniques (limite de taille du csv)
                - s??lection de tous les acteurs et actrices
                - s??lection des films et t??l??films dont la dur??e est sup??rieure ?? 60 minutes et dont la date de production est post??rieure ?? 1960
                
                Apr??s la jointure des 3 dataset, nous avons :
                - ajout?? une colonne "??ge" qui correspond ?? la diff??rence entre les valeurs des colonnes 'birthYear' et 'startYear'
                - du fait d'une base pas 'propre', nous avons discrimin?? les outliers et gard?? pour la colonne '??ge' toutes les valeurs situ??es entre 0 et 110

                Afin de r??aliser le graphique, un [dataframe attitr??]('https://raw.githubusercontent.com/BerengerQueune/ABC-Data/main/Aurore/KPI/Age_acteurs20211118.csv?token=AUTGRH6AOVYKCSBEBIWDCLTBT5VZI') reprenant les donn??es dont nous avions besoin pour la pr??sentation des graphiques a ??t?? produit.

                [Lien Notebook]('https://github.com/BerengerQueune/ABC-Data/blob/main/Aurore/KPI/Moyenne%20%C3%A2ge%20Acteurs.ipynb')

                """
                )
        st.image("https://i.ibb.co/4SxFQYy/A-mod.png")
        
        
        ######GRAPH01#########
        col1, col2 = st.columns([2, 1])
        with col2:
            st.write(' ')
            st.write(' ')
            st.write(' ')
            st.write(' ')
            st.write(' ')
            st.write(' ')
            st.write(' ')
            st.markdown(
                """
                D'apr??s ce boxplot, la moyenne d'??ge, tout sexe confondu, est de 40 ans.
                
                Le graphique fait nettement appara??tre une amplitude tr??s large puisque l'??ge des acteurs s?????tend de 0 ?? 110 ans.
                
                Cependant, les ??ges sup??rieurs ?? 80 ans sont consid??r??s comme des outliers. Les acteurs au-del?? de cet ??ge sont donc malgr?? tout peu nombreux.
                
                Il est ?? noter ??galement que l'??ge des acteurs se concentre sur une plage limit??e puisque 50% d???entre eux sont entre 29 ans et 49 ans avec une moyenne ?? 40 ans.
                """
                )

        with col1:

            fig = go.Figure()
            fig.add_trace(go.Box(y=Age_DF_clean["Age"], name = 'Population', marker_color='lightgreen', boxmean=True # represent mean
            ))
            fig.update_yaxes(title= 'Age')

            fig.update_layout(title_text="Age des acteurs et actrices : Zoom", title_x=0.5, width=1000, height=600, template='plotly_dark')



            st.plotly_chart(fig)
        st.write("")    
        st.write("")






        ######GRAPH02#########
        col1, col2 = st.columns([2, 1])
        with col2:
            st.write(' ')
            st.write(' ')
            st.write(' ')
            st.write(' ')
            st.write(' ')
            st.write(' ')
            st.write(' ') 
            st.write(' ')
            st.write(' ')
            st.write(' ')            
            st.markdown(
                """
                Voici les moyennes d'??ge par genre, pour les personnes ayant tourn?? dans des films et des t??l??films :
                - Acteurs :     43 ans
                - Actrices :    36 ans

                Voici l'??ge central pour ces m??mes populations :
                - Acteurs :     41 ans
                - Actrices :    32 ans

                Lorsque l???on s??pare les hommes et les femmes dans l???analyse, on s???aper??oit que ces derni??res terminent g??n??ralement leur carri??res plus jeunes que leur homologues masculins. Elles commencent ??galement plus jeunes.
                
                L?????cart entre les ages m??dians illustre bien cette diff??rence puisque l'??ge m??dian des actrices est de 32 ans contre 41 ans pour les hommes.
                
                Nous constatons qu???il y a beaucoup d???outliers dans les deux cas mais pour les hommes ils sont au-del?? de 80 ans alors que pour les femmes cela d??bute ?? 68 ans ce qui confirme le point pr??c??dent.

                """
                )

        with col1:

            fig = go.Figure()
            fig = px.box(Age_DF_clean,y="Age", color="category")
            fig.update_yaxes(title= 'Age')
            fig.update_xaxes(title= 'Population')

            fig.update_layout(title_text="Age des acteurs et actrices : par genre", title_x=0.5, width=1000, height=600, template='plotly_dark')
            
            st.plotly_chart(fig)

        st.write("")    
        st.write("")





        ######GRAPH03#########
        col1, col2 = st.columns([2, 1])
        with col2:
            st.write(' ')
            st.write(' ')
            st.write(' ')
            st.write(' ')
            st.write(' ')
            st.write(' ')
            st.write(' ') 
            st.markdown(
                """
                Voici les moyennes d'??ge par sexe et par cat??gorie de film :
                - Films :
                    - Acteurs :     42 ans
                    - Actrices :    35 ans
                - T??l??films :
                    - Acteurs :     45 ans
                    - Actrices :    40 ans
                            
 
                Voici l'??ge central des populations sexe et par cat??gorie de film :
                - Films :
                    - Acteurs :     41 ans
                    - Actrices :    31 ans
                - T??l??films :
                    - Acteurs :     44 ans
                    - Actrices :    37 ans

                Les observations sur le graphique par genre sont bien ??videmment toujours vraies pour celui-ci. On note que le ph??nom??ne est le m??me que ce soit au cin??ma ou ?? la t??l??. Cependant ?? la t??l??, les actrices et acteurs sont globalement plus ??g??s.
                
                Cela semble plus marqu?? pour les femmes puisque l'??ge m??dian passe de 31 ans au cin??ma ?? 37 ans ?? la t??l?? soit 6 ans de plus, alors que chez les hommes l?????cart est seulement de 3 ans (44 ans contre 41 ans).

                """
                )

        with col1:
            fig = go.Figure()
            fig = px.box(Age_DF_clean, x="titleType", y="Age", color="category")
            fig.update_yaxes(title= 'Age')

            fig.update_layout(title_text="Age des acteurs et actrices : par type de film et genre", title_x=0.5, width=1000, height=600, template='plotly_dark')
            

            st.plotly_chart(fig)
        st.write("")
        st.write('')
        st.write(' ')
        st.write(' ')
        #######################################
        ##########  Q07 -Aurore  ##############
        #######################################
        st.subheader("Quels sont les films les mieux not??s ?") # add a subtitle


        qualify_movies = pd.read_csv('https://raw.githubusercontent.com/BerengerQueune/ABC-Data/main/Aurore/KPI/DF_FULL_GENRES211117.csv?token=AUTGRH2J25FKEQLFK7VPH5TBT7DVE')
        st.write(' ')
        st.markdown(
                """
                Le dataset a ??t?? ??labor?? ?? partir de 5 fichiers : name_basics.tsv, title_basics.tsv, title_principasl.tsv, title_ratings.csv et title_akas.csv .

                Apr??s s??lection des colonnes ?? utiliser, nous avons nettoy?? la base de donn??es comme ?? notre habitude. 

                Nous avons principalement utilis?? les m??mes filtres que pour la question suivante afin de garder une coh??rence dans notre analyse, et toujours aussi pour des raisons techniques (Dataset h??berg??s sur Github).

                Dans ce dataset, nous avons aussi ajout?? une colonne 'moyenne_pond??r??e', qui pond??re les valeurs de la colonne 'averageRating' selon celles de la colonne 'numVotes', selon la formule de pond??ration de la note fournie par IMDb :
                """
                )
        st.latex(r'''
                    Weighted\; Rating (WR) = (\frac{v}{v + m} . R) + (\frac{m}{v + m} . C)
                    ''')
        st.markdown(
                """
                O?? :
                - v est le nombre de votes (= numVotes)
                - m est le nombre minimum de votes requis pour ??tre list??
                - R est la moyenne des notes ditribu??es par les votants (= averageRating) 
                - C est le vote moyen sur l'ensemble du dataset

                Nous avons ??tabli une fonction qui est la suivante pour cela :
                """
                )
        code = '''def movie_ponderation(x,m=m,C=C):
                            v=x['numVotes']
                            R=x['averageRating']
                            # calculation based on IMDB formula
    
                            return (v/(v+m)*R) + (m/(m+v)*C)'''
        st.code(code, language='python')
        st.markdown(
                """            

                Afin de r??aliser le graphique, un [dataframe attitr??](https://raw.githubusercontent.com/BerengerQueune/ABC-Data/main/Aurore/KPI/DF_FULL_GENRES211117.csv?token=AUTGRH2J25FKEQLFK7VPH5TBT7DVE) reprenant toutes les informations dont nous avions besoin pour cette analyse a ??t?? produit.

                [Lien Notebook](https://github.com/BerengerQueune/ABC-Data/blob/main/Christophe/Projet%202%20-%20Quels%20sont%20les%20pays%20qui%20produisent%20le%20plus%20de%20films.ipynb)

                """
                )
        st.image("https://i.ibb.co/4SxFQYy/A-mod.png")

        ##################
        st.title('Quels sont les films les mieux not??s ?')
        qualify_movies_DF_FULL2 = qualify_movies.sort_values('moyenne_ponderee', ascending=False)
        qualify_movies_DF_FULL2['text_graph'] = 'Note : ' + qualify_movies_DF_FULL2['moyenne_ponderee'].round(2).astype(str) + ', nombre de votes : '+ qualify_movies_DF_FULL2['numVotes'].astype(str)

        fig = px.bar(qualify_movies_DF_FULL2, x='moyenne_ponderee', y='primaryTitle',title = 'Top 10 des films distribu??s en France depuis 1960', text = 'text_graph', orientation='h', range_x=[0,11],labels = {'moyenne_ponderee': 'Note', 'primaryTitle': 'Films'})
        fig.update_yaxes(range=(9.5, -.5))
        fig.update_layout(title_text="Top 10 des films distribu??s en France depuis 1960", title_x=0.5, width=1000, height=600, template='plotly_dark')

        st.plotly_chart(fig)

        ################
        st.title('Top 10 des films distribu??s en France depuis 1960 par d??cennies')

        groupedDf = qualify_movies.groupby(['Periode', 'primaryTitle'] ).size()
        df_final  = pd.DataFrame({'inter' : groupedDf.groupby(level='Periode').nlargest(5).reset_index(level=0, drop=True)})
        df_final.reset_index(inplace=True)
        df_final2 = df_final.tail(70)
        df_final2['rank'] = df_final2.groupby('Periode')['inter'].rank(method = 'first')

        fig = px.bar(df_final2, x = 'inter',y ='rank', text = 'primaryTitle',color = 'primaryTitle',
        title = 'Top 10 des films distribu??s en France depuis 1960 par d??cennies',
        labels = {'Periode': 'P??riode', 'primaryTitle': 'Films'},
        orientation='h',
        animation_frame="Periode",
        range_x=[0,11],
        range_y=[0,6],
        width=1000, height=800)
 
        fig.update_traces(textfont_size=12, textposition='outside')
        fig.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = 1000

        fig.update_layout(showlegend=False, title_x=0.5, width=1000, height=600, template='plotly_dark')
            
        st.plotly_chart(fig)

        st.write("")

        st.title('Quels sont les films les mieux not??s - Caract??ristiques communes ?')
        FULL_DF = pd.read_csv('https://raw.githubusercontent.com/BerengerQueune/ABC-Data/main/Aurore/KPI/DF_FULL_GENRES211117.csv?token=AUTGRH6TVDSC4VN4IF6LDHLBT7FC6')


        fig = px.scatter_3d(FULL_DF,x="genre1",y ='genre2', z= 'genre3', color = 'moyenne_ponderee' )
        fig.update_layout(title_text="Caract??ristiques communes des films les mieux not??s", title_x=0.5, width=1000, height=600, template='plotly_dark')
            
        st.plotly_chart(fig)

        st.markdown("""
                Nous remarquons qu'avec la quantit?? de donn??es en notre possession, il est tr??s difficile d'interpr??ter ce scatterplot pour d??terminer quelle association de genres permettrait aux films de maximiser leurs chances d'??tre bien not??.
                Zoomons donc sur les films dont la moyenne pond??r??e est sup??rieure ?? 8/10 :
                """
                )

        #####################################
        st.title('Quels sont les films les mieux not??s (+ de 8/10) - Caract??ristiques communes ?')
        qualify_movies2 = qualify_movies.copy()
        qualify_movies2 = qualify_movies2[qualify_movies2['moyenne_ponderee'] >= 8 ]
        qualify_movies2 = qualify_movies2[qualify_movies2['moyenne_ponderee'] <= 9 ]

        fig = px.scatter_3d(qualify_movies2,x="genre1",y ='genre2', z= 'genre3', color = 'moyenne_ponderee'  )
        fig.update_layout(title_text="Caract??ristiques communes des films les mieux not??s", title_x=0.5, width=1000, height=600, template='plotly_dark')
            
        st.plotly_chart(fig)

        st.markdown("""
                La moyenne pond??r??e la plus ??lev??e ??tant 8.96, nous avons aussi pris en borne haute 9/10 afin de mettre plus en avant les valeurs ?? interpr??ter dans ce scatterplot.
                Nous pouvons remarquer que l'association de genres qui d??tient cette note est "Action/Crime/Drama".
                """
                )


        ####################################
        col1, col2 = st.columns([1, 1])
        with col1:
            st.title('Note moyenne par genre de films')
            moyenne_genre = pd.pivot_table(FULL_DF,values="averageRating",columns="genre1",aggfunc=np.mean)
            moyenne_genre_unstacked = moyenne_genre.unstack().unstack()
            moyenne_genre_unstacked =moyenne_genre_unstacked.sort_values('averageRating')

            Genres = moyenne_genre_unstacked.index
            moyenne = moyenne_genre_unstacked['averageRating']

            fig = px.bar(moyenne_genre_unstacked, x=Genres, y =moyenne, labels = {'averageRating': 'Note moyenne', 'genre1': 'Genres de 1er rang'},color = moyenne_genre_unstacked.index,title = 'Note moyenne par genre de films ',width=600, height=450)
            fig.update_layout(showlegend=False, title_x=0.5, yaxis={'visible': True}, template='plotly_dark')
            fig.update_xaxes(tickangle=-45)
            st.plotly_chart(fig)

        with col2:
            st.title('Nombre moyen de votes par genre')
            nb_moyen_votes = pd.pivot_table(FULL_DF,values="numVotes",columns="genre1",aggfunc=np.mean)
            nb_moyen_votes_unstacked = nb_moyen_votes.unstack().unstack()
            nb_moyen_votes_unstacked = nb_moyen_votes_unstacked.sort_values('numVotes').round()

            genres = nb_moyen_votes_unstacked.index
            nb_votes = nb_moyen_votes_unstacked['numVotes']

            fig = px.bar(nb_moyen_votes_unstacked, x=genres, y =nb_votes, labels = {'numVotes': 'Nombre moyen de votes', 'genre1': 'Genres de 1er rang'}, color = nb_moyen_votes_unstacked.index,title = "Nombre moyen de votes par genre",width=600, height=450)
            fig.update_layout(showlegend=False, title_x=0.5, yaxis={'visible': True}, template='plotly_dark')
            fig.update_xaxes(tickangle=-45)
            
            st.plotly_chart(fig)

        st.markdown("""
                Il para??t opportun d???analyser simultan??ment les deux graphiques.

                En effet, nous constatons que Western est ?? la fois le genre ou la note moyenne est la plus ??lev??e mais ??galement celui o?? le nombre moyen de votes est le plus important. Cela permet d???affirmer qu???il s???agit vraisemblablement du genre pr??f??r?? sur la p??riode ??tudi??e. Le genre ???Famille???, bien qu???un peu moins bien not??, est ??galement dans ce cas. 
                
                A l???inverse, le thriller qui arrive en 17??me et derni??re position sur la note moyenne est en 16??me position sur le nombre moyen de votes Les amateurs de Thriller sont-ils moins enclins ?? voter ? Est ce qu???ils votent essentiellement quand le film ne leur plait pas ou est ce que les thrillers sont simplement moins bons que les westerns ? Nous n???avons pas ici suffisamment d?????l??ments pour le d??terminer.
                
                Le troisi??me cas est celui des documentaires. Leur note moyenne est tr??s bonne puisqu???ils sont en deuxi??me position. Par contre, ils sont en derni??re position en ce qui concerne le nombre de votes. En ce qui concerne ce genre, on peut estimer que cel?? provient du nombre de personnes qui vont voir ces films. Celui doit en effet ??tre moins important que pour les autres. Nous n???avons cependant pas d?????l??ment ici pour nous le confirmer.

                """
                )
        st.write(' ')
        st.write(' ')
        st.write(' ')

        #######################################
        ########  KPI -Christophe  ############
        #######################################
        st.title('Pour aller plus loin... Quelques KPI !')
        st.write(' ')
        st.image("https://i.ibb.co/NV1RFNH/C-mod.png")
        st.markdown("""
        [Lien Notebook](https://github.com/BerengerQueune/ABC-Data/blob/main/Christophe/Scripts%20VF/KPI%20r%C3%A9alisateurs%20-%202021_11_17.ipynb)
        """
                )
        st.write(' ')
        st.markdown("""
        [DataFrame](https://raw.githubusercontent.com/BerengerQueune/ABC-Data/main/Christophe/df_final_director.csv?token=AVCI5TY6PATH3QY4C25CC5TBT5IIA)
                """
                )        

        df_final = pd.read_csv('https://raw.githubusercontent.com/BerengerQueune/ABC-Data/main/Christophe/df_final_director.csv?token=AVCI5TY6PATH3QY4C25CC5TBT5IIA')

        #R??alisation du graphique
        fig = px.bar(df_final, x = 'count', y="rang", text ='director', color = 'director',
        title = 'Les r??alisateurs qui ont fait le plus de film par d??cennie',
        labels = {'count':'Nombre de films','periode': 'D??cennie', 'director': 'R??alisateur'},
        orientation='h',
        animation_frame="periode",
        range_x=[0,9],
        #range_y=[0,4],
        width=700, height=450)
 
        fig.update_traces(textfont_size=12, textposition='outside')
        fig.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = 1000

        fig.update_layout(showlegend=False, title_x=0.5, width=1000, height=600, template='plotly_dark')
            
        st.plotly_chart(fig)

        ###############################
        #Cr??ation d'un dataframe avec les 3 r??alisateurs ayant r??alis?? le plus de film depuis 1960
        df_director_nbFilm = pd.DataFrame(df_final.value_counts('director'))
        df_director_nbFilm.reset_index(inplace = True)
        df_director_nbFilm.columns = ['director', 'nbFilm']

        #Calcul du rang
        df_director_nbFilm['Rang'] = df_director_nbFilm.index + 1
        df_director_nbFilm = df_director_nbFilm.head(3)

        st.write(' ')
        st.write(' ')
        ###############################
        st.markdown("""
        [DataFrame](https://raw.githubusercontent.com/BerengerQueune/ABC-Data/main/Christophe/df_director_nbFilm.csv?token=AVCI5T7CVK5U4UHCL66ABS3BT5INA)
                """
                )
        st.write(' ')
        df_director_nbFilm = pd.read_csv('https://raw.githubusercontent.com/BerengerQueune/ABC-Data/main/Christophe/df_director_nbFilm.csv?token=AVCI5T7CVK5U4UHCL66ABS3BT5INA')

        #R??alisation du graphique
        fig = px.bar(df_director_nbFilm, x = 'nbFilm', y="Rang", text ='director', color = 'director',
            title = 'Les r??alisateurs qui ont fait le plus de film depuis 1960', 
            labels = {'nbFilm': 'Nombre de films', 'director': 'R??alisateur'},orientation='h', range_x=[0,30], range_y=[0,4],width=700, height=450)

        fig.update_layout(showlegend=False, title_x=0.5, width=1000, height=600, template='plotly_dark')
            
        st.plotly_chart(fig)
        st.write(' ')
        st.write(' ')       
        
        st.markdown("""
        [Lien Notebook](https://github.com/BerengerQueune/ABC-Data/blob/main/Christophe/Scripts%20VF/Score%20acteurs%20-%202021_11_18.ipynb)
        """
                )
        st.write(' ')
        st.markdown("""
        [DataFrame](https://raw.githubusercontent.com/BerengerQueune/ABC-Data/main/Christophe/df_rating.csv?token=AVCI5T6KBWAVG7CL46KTL3DBT6GOU)
                """
                )
        st.write(' ')
        df_rating = pd.read_csv('https://raw.githubusercontent.com/BerengerQueune/ABC-Data/main/Christophe/df_rating.csv?token=AVCI5T6KBWAVG7CL46KTL3DBT6GOU')

        fig = px.bar(df_rating.head(30), x = 'Acteur', y = 'averageRating', color='averageRating', 
             title = 'Les acteurs ayant les meilleurs notes', 
             labels={'Acteur':'Acteurs', 'averageRating':'Note moyenne'}, range_y=[8,9.5], width=900, height=600)

        fig.update_layout(showlegend=False, title_x=0.5, width=1000, height=600, template='plotly_dark')
            
        st.plotly_chart(fig)

        st.write(' ')
        st.write(' ')
        st.write(' ')







######################################################################################
######################################################################################
###########################     RELEASES     #########################################
######################################################################################
######################################################################################


    if choice == "Axes d'Am??lioration":
        # CSS code within markdown to center the title
        st.markdown("<h1 style='text-align: center;'>Axes d'Am??lioration</h1>", unsafe_allow_html=True)

        # This create a nice grey line between the title and the multiselect menu
        st.write("---------------------------------------------------------")


        st.markdown("""
                Pour redresser la barre de son cin??ma, notre cliente souhaite diffuser uniquement des films r??cents grand public.

                Elle souhaite ??galement ??tre inform??e des films ?? venir qui ont le plus de chances d'avoir du succ??s. Dans ce cadre et dans un premier temps, les m??thodes de Machine Learning n??cessaires pour un r??sultat optimal nous ont sembl?? difficiles ?? mettre en place puisque nous ne pouvions plus compter sur des r??sultats comme la note moyenne ou bien le nombre de vote.

                Pour une premi??re version, nous avons uniquement utilis?? les genres des films pour notre algorithme et les tests que nous avons effectu??s nous ont sembl?? globalement fiables. L'une des raisons de cette fiabilit?? est que le DataFrame utilis?? pour les recommandations se base uniquement sur les films ?? diffuser dans la r??gion FR sur les ann??es 2021 et 2022 ce qui donne un total d'environ 350 films.

                Pour l'instant, notre algorithme fonctionne ainsi :

                - Il regroupe tous les votes qu'il re??oit dans un DataFrame. Cela peut permettre ?? des centaines de spectateurs potentiels de voter pour leurs films pr??f??r??s.
                - Ensuite, l'algorithme fait la somme de chaque genre. Par exemple, 10 films du genre Action donne donc une note de 10 en Action.
                - Puis, l'algorithme divise cette somme par le nombre de films s??lectionn??s afin de cr??er un nouveau film virtuel qui se retrouve au centre de tous les films choisis.
                - Ce syst??me fonctionne tr??s bien avec un seul film. Il fonctionne mal avec deux films tr??s diff??rents mais plus il re??oit de films plus le r??sultat final se lisse et a des chances de plaire au plus grand nombre.

                En l'??tat actuel, pour une premi??re version, nous sommes satisfaits des recommandations propos??es mais nous consid??rons qu'il s'agit davantage d'une aide ?? la d??cision et que notre cliente doit encore utiliser ses connaissances m??tiers afin de faire les bons choix. Notre algorithme est suffisamment bon pour l'y aider.

                A l'avenir, en terme d'axe d'am??lioration sur l'algorithme, nous souhaiterions que celui-ci prenne en compte de nouveaux crit??res comme les acteurs puis le r??alisateur.

                Il est ??galement possible de tenter de faire une pr??diction de note en prenant en compte de nombreux autres facteurs qui ne sont pas disponibles dans la base de donn??es d'IMDB. On sait par exemple que les films Marvel ont tendance ?? faire un carton au cin??ma. La mise en place d'un tel syst??me n??cessiterait davantage de temps et de recherches.

                En ce qui concerne l'interface utilisateur, nous avons not?? des ralentissements sur Streamlit ainsi que des soucis d'acc??s occasionnels. Dans notre cas sp??cifique il semble ??galement que l'affichage des posters soit assez lent. L'algorithme a parfois du mal ?? se mettre ?? jour lorsque nous ajoutons plusieurs films rapidement et il faut parfois attendre qu'il charge tous les posters avant de pouvoir lui faire correctement prendre en compte l'ajout d'un autre film. Il faudrait tester d'autres m??thodes d'affichages des posters afin de voir si cela a un impact positif. Le code ne semble pas optimis?? ?? l'heure actuel.

                Nous sommes satisfait du r??sultat global de notre application. Les r??sultats semblent fiables mais l'application n??cessite encore du travail en terme d'interface utilisateur et de fiabilit?? de l'algorithme. Nous devrons en parler davantage avec Framboise afin de voir ce qu'elle souhaite.
                """
                )
        st.write(' ')
        st.write(' ')
        st.write(' ')
















    
        





main()



