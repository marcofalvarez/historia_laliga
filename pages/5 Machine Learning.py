import streamlit as st 
import streamlit as st 
import pandas as pd 
import numpy as np 
import plotly.express as px
import plotly.graph_objects as go 
from plotly.subplots import make_subplots
# from datetime import datetime
# from datetime import date
import plotly.figure_factory as ff

import pages.modules.preparing_tables as tables
import pages.modules.ml_clusters as ml

from sklearn.cluster import AgglomerativeClustering

from scipy.spatial import distance_matrix 

from scipy.cluster.hierarchy import ClusterWarning
from warnings import simplefilter
simplefilter("ignore", ClusterWarning)

from scipy.cluster import hierarchy

st.set_page_config(page_title= "Machine Learning",
                #    layout='centered',
                   page_icon= ":soccer:",
                   layout="wide"
                )

st.markdown("""     
            <style>         
                     
            .st-emotion-cache-pkbazv {             
            color: rgb(255, 255, 255); 
                     
            }     
            </style> """, 
            unsafe_allow_html=True,
            )

# st.sidebar.header('Menú')
st.title('Verificación de hipótesis')
st.divider()
st.markdown(
    '''
        En nuestra busqueda bibliográfica hemos aprendido varias cosas:   

        1. Hasta la temporada *1995/1996* la puntuación se realizaba de forma que el partido ganado era 2 puntos,
        después hasta la actualidad vale 3 puntos.   
        2. Hasta la temporada *1934/1935* hay 10 equipos, hasta la *1940/1941* hay 12 equipos, hasta la *1949/1950*
        son 16 los equipos, a partir de *1971/1972* son 18 los equipos que juegan y desde la temporada *1987/1988*
        son 20 los equipos que la forman, anotando que en la temporada *1995/1996* y *1996/1997* son 22.  
        3. De la temporada de *1936/1937* a *1938/1939* no hay datos debido a que la Guerra Civil en España no 
        permitió que se dispiturá la competición.   

        Estos hechos los hemos verificado mediante la exploración de datos. Hemos visto la fluctuación de puntos
        así como el número de equipos cambiar a lo largo de los años.  
        La diferencia en los gráficos temporales muestran una importante variabilidad y nos llegamos a preguntar 
        cual o cuales son los umbrales en el tiempo dónde el fútbol ha cambiado significativamente. 
        Al mismo tiempo nos preguntamos cómo se comparan los equipos entre si, cúales han obtenido un rendimiento 
        sobresaliente y han dominado en períodos de tiempo considerable.

        Para responder a estas preguntas usamos algorítmos de Machine Learning. Los métodos que más se adaptan a 
        este tipo de preguntas son los modelos no supervisados. Para aprender sobre cambios en el tiempo usamos 
        Kmeans, hemos observado una posible tendencia en los últimos 40 años, cambios en las leyes de puntos y el 
        número de quipos podría influeciar esto. Por otro lado, para estudiar la diferencia entre los equipos 
        usamos un método de aglomeración jérarquico para identificar los equipos más exitosos y más dominantes.   
    '''
)
st.divider()
st.subheader('Modelo Kmeans')
st.divider()
st.markdown(
    '''Para estudiar los cambios temporales tomamos los primeros 10 equipos de cada temporada y calculamos la media
     para todos los datos. 
    Buscamos primero el número óptimo de grupos en nuestro modelo Kmeans para dividir nuestros datos en el tiempo.
     Esto lo hacemos usando el "método del codo". Este método consiste en estudiar mediante un gráfico la variación 
     explicada en función de diferente número de grupos(K). A la variación explicada le llamamos inercia. 
     El siguiente gráfico muestra las inercias para diferente número de clusters (K).
        '''
)
st.divider()
df =ml.group_temporadas("data/clasificacion.csv")
data = ml.scaling_data(df=df)
inercias = ml.inertias(data)

ifig = px.line(x=range(1, len(inercias)+1), y=inercias, hover_name=inercias, markers=True)
ifig.update_layout(title='Inercia en relación a K',
                   xaxis_title='Ks',
                   yaxis_title='Inercia')
st.plotly_chart(ifig, use_container_width=True)
with st.expander("explicación"):
        st.markdown(
        '''Se denomina a este tipo de gráfico "elbow method" o método del codo. Se utiliza para determinar 
        el cambio en variación en fución del número de agrupaciones. En este caso el 'codo' esta entre 2 y 4.
            
            '''
        )       


df = ml.making_clusters(data, df)

css="""
<style>
    [data-testid="stForm"] {
        background: LightBlue;
    }
</style>
"""

# valor_k = st.slider('Escoger un valor de K', 2, 4)
with st.form('K choice'):
    valor_k = st.radio(
    "Escoger un valor de K",
    ["2", "3", "4"],
    # captions = ["", "", ""],
    )
    presionar = st.form_submit_button("Vale!")
    if presionar:
        if valor_k == "2":

            # Create figure with secondary y-axis
            fig = make_subplots(specs=[[{"secondary_y": True}]])

            # Add traces
            fig.add_trace(
                go.Scatter(x=df['Temp'], 
                    y=df['PT'], name="PT"),
                secondary_y=False,
            )
            fig.add_trace(
                go.Scatter(x=df['Temp'], 
                    y=df['PJ'], name="PJ"),
                secondary_y=False,
            )

            fig.add_trace(
                go.Scatter(x=df['Temp'], 
                    y=df['PG'], name="PG"),
                secondary_y=False,
            )

            fig.add_trace(
                go.Scatter(x=df['Temp'], 
                    y=df['PP'], name="PT"),
                secondary_y=False,
            )
            fig.add_trace(
                go.Scatter(x=df['Temp'], 
                        y=df['cluster2'], name = 'clusters'),
                secondary_y=True,
            )

            # Add figure title
            fig.update_layout(
                title_text="clustering"
            )

            # Set x-axis title
            fig.update_xaxes(title_text="temp")

            # Set y-axes titles
            fig.update_yaxes(title_text="<b>Resultados</b> estadisticas", secondary_y=False)
            fig.update_yaxes(title_text="<b>Cluster</b> agrupaciones", secondary_y=True)
            st.plotly_chart(fig, use_container_width=True)

        if valor_k == "3":

            # Create figure with secondary y-axis
            fig = make_subplots(specs=[[{"secondary_y": True}]])

            # Add traces
            fig.add_trace(
                go.Scatter(x=df['Temp'], 
                    y=df['PT'], name="PT"),
                secondary_y=False,
            )
            fig.add_trace(
                go.Scatter(x=df['Temp'], 
                    y=df['PJ'], name="PJ"),
                secondary_y=False,
            )

            fig.add_trace(
                go.Scatter(x=df['Temp'], 
                    y=df['PG'], name="PG"),
                secondary_y=False,
            )

            fig.add_trace(
                go.Scatter(x=df['Temp'], 
                    y=df['PP'], name="PT"),
                secondary_y=False,
            )
            fig.add_trace(
                go.Scatter(x=df['Temp'], 
                        y=df['cluster3'], name = 'clusters'),
                secondary_y=True,
            )

            # Add figure title
            fig.update_layout(
                title_text="clustering"
            )

            # Set x-axis title
            fig.update_xaxes(title_text="temp")

            # Set y-axes titles
            fig.update_yaxes(title_text="<b>Resultados</b> estadisticas", secondary_y=False)
            fig.update_yaxes(title_text="<b>Cluster</b> agrupaciones", secondary_y=True)
            st.plotly_chart(fig, use_container_width=True)

        if valor_k == "4":

            # Create figure with secondary y-axis
            fig = make_subplots(specs=[[{"secondary_y": True}]])

            # Add traces
            fig.add_trace(
                go.Scatter(x=df['Temp'], 
                    y=df['PT'], name="PT"),
                secondary_y=False,
            )
            fig.add_trace(
                go.Scatter(x=df['Temp'], 
                    y=df['PJ'], name="PJ"),
                secondary_y=False,
            )

            fig.add_trace(
                go.Scatter(x=df['Temp'], 
                    y=df['PG'], name="PG"),
                secondary_y=False,
            )

            fig.add_trace(
                go.Scatter(x=df['Temp'], 
                    y=df['PP'], name="PT"),
                secondary_y=False,
            )
            fig.add_trace(
                go.Scatter(x=df['Temp'], 
                        y=df['cluster4'], name = 'clusters'),
                secondary_y=True,
            )

            # Add figure title
            fig.update_layout(
                title_text="clustering"
            )

            # Set x-axis title
            fig.update_xaxes(title_text="temp")

            # Set y-axes titles
            fig.update_yaxes(title_text="<b>Resultados</b> estadisticas", secondary_y=False)
            fig.update_yaxes(title_text="<b>Cluster</b> agrupaciones", secondary_y=True)
            st.plotly_chart(fig, use_container_width=True)

with st.expander("explicación"):
        st.markdown(
        '''Podemos ver que las agrupaciones temporales siguen algunas de nuestras observaciones 
        y estudios bibliográficos sobre los cambios en el número de equipos en la liga así como 
        cambios en el número de puntos. La próxima pregunta a resolver será para aprender más 
        sobre diferencias entre el tipo de juego a través del tiempo. Para este tipo de estudios 
         es necesario recopilar más datos por partido y por jugador.  
            '''
        )
st.divider()
df = ml.df_equipos('data/clasificacion.csv')
equipos = df.Equipo.tolist()

X = ml.scalertransform(df)

dist_matrix = distance_matrix(X,X)

fig = ff.create_dendrogram(dist_matrix, 
                           color_threshold=8, 
                           orientation='bottom', 
                           labels=equipos)
fig.update_layout(width=1200, height=500)
st.plotly_chart(fig, use_container_width=True)

st.divider()

agglom = AgglomerativeClustering(n_clusters = 4, linkage = "complete")
agglom.fit(X)

df['agglom'] = agglom.labels_
df['agglom']= df["agglom"].astype('string')
dc = df.sort_values(by=['agglom'])
scfig = px.scatter(dc, x = dc.PG, y = dc.PP,  
                   size=dc.PT, 
                   color = dc.agglom, 
                   hover_data=['Equipo'],
                   color_discrete_map={
                        "0": '#1f77b4',
                        "1": '#d62728',
                        "2": '#17becf',
                        "3": '#2ca02c',
                   }
                   )
scfig.update_layout(
    title="Summary",
    xaxis_title="Partidos Ganados",
    yaxis_title="Partidos Perdidos",
    legend_title="Agrupaciones",
    )
st.plotly_chart(scfig, use_container_width=True)

st.divider()
