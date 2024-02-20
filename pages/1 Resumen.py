import streamlit as st 
import pandas as pd 
import numpy as np 
import plotly.express as px
import plotly.graph_objects as go 
from plotly.subplots import make_subplots
# from datetime import datetime
# from datetime import date

import pydeck as pdk

import pages.modules.preparing_tables as tables

st.set_page_config(page_title= "Resumen",
                   page_icon= ":soccer:",
                   layout="wide")
st.title("Resumen de la Historia de La Liga")

st.markdown(
        '''
            ## Cuales son los actores más importantes y cuales son los trazos más importantes que han marcado la historia de La Liga ?
            
            Los siguientes gráficos te daran un resumen general de lo que ha pasado desde 1928.
            En la historia de la liga han habido 71 equipos que han participado. Varios equipos han participado
            continuamente en el torneo desde su inicio. 
            A pesar de haber tantos equipos que han participado consistentement, son muy pocos los que han ganado esta copa.
            Hemos escogido los equipos que han participado 20 veces o más para hacer las siguientes gráficas que muestran
            su úbicación geográfica, la cantidad de veces que han partciciado y el número de trofeos que han obtenido.     
                
'''
    )

#hacer dos graficos
col1, col2 = st.columns(2)

df = tables.sunb_table('data/clasificacion.csv')
#grafico de bara con equipos que han participado mas de 20 veces
with col1:
    st.subheader(
        '''Quién ha ganado La Liga
              
            
'''
    )

with col1:
    sunfig = px.sunburst(data_frame = df,
                  values     = "Participación",
                  path       = ["1Copa_o+", "Equipo"],
                  hover_name = 'Equipo',
                  hover_data = "Copa",
                  #color      = "Participacion"
                #   title = "Quién ha ganado la liga"
                 )
    #sunfig.update_traces(textinfo = "label+percent parent")
    st.plotly_chart(sunfig)
    
    with st.expander("Instrucciones"):
        st.markdown(
            '''
                1- pasar el cursor sobre las gráfica (acción -hover) o hacer click en True/False para aprender más sobre
                los participantes y ganadores de La Liga.
        '''
        )


# código para hacer el mapa con la ubicación de los estadios
    
dm = tables.mapa_talbe('data/estadios.csv', 'data/clasificacion.csv')

with col2:
    st.subheader('''Mapa de la ubicación de los equipos   ''')
    layer = pdk.Layer(
        'ColumnLayer',
        dm,
        get_position=['lng', 'lat'],
        get_elevation="Participación",
        auto_highlight=True,
        # lineWidthUnits='pixels',
        # lineWidthMinPixels =1,
        # getLineWidth=10,
        elevation_scale=5000,
        pickable=True,
        extruded=True,
        get_radius=10000000,
        get_fill_color=["Participación", 180, "Participación * 40", 255],
        coverage=8,
        # offset= [-2,-4],
    )

    view_state = pdk.ViewState(
        longitude=-9.043,
        latitude=37.0194,
        zoom=4,
        min_zoom=2,
        max_zoom=20,
        pitch=40.5,
        bearing=-27.36)
    # Render
    r = pdk.Deck(map_style= 'mapbox://styles/mapbox/dark-v10',
                    layers=layer, 
                    initial_view_state=view_state,
                    tooltip = {
                        "html":
                        "<b>{Estadio}<br />"
                        "de {Equipo},<br />"
                        "<b>ganaron {Copa} vece(s) La Liga, <br />"
                        "<b>de {Participación} participaciones",                    
                        },
                    api_keys= {'mapbox': st.secrets['mapbox']}
                )
    st.pydeck_chart(r)
    
    with st.expander("Instrucciones"):
        st.markdown(
        '''
            1- el tamaño de las columans corresponde a la cantidad de veces que el equipo participó en
            La Liga. Pasar el cursor sobre mapa (acción -hover) para aprender más sobre los equipos.
            Usa la rueda del ratón (acción -scroll), pinchar o click + movimiento del ratón para navegar
            en el mapa o hacer zoom.  
            Ctr + click te permite cambiar el ángulo de observación en 3 dimensiones.
            '''
        )       



dd = tables.cumsum_table("data/clasificacion.csv")
eq = dd['Equipo'].unique().tolist()

st.subheader('Cantidad de ligas ganadas por equipo a lo largo de los años')
container = st.container()
select_all = st.checkbox("seleccione todos", value=False)

if select_all:
    selected_options = container.multiselect("ecoger uno o más equipos:",
        eq,eq)
else:
    selected_options =  container.multiselect("ecoger uno o más equipos:",
        eq, default=['Barcelona','Real Madrid'])

dd = dd[dd['Equipo'].isin(selected_options)]
fig = px.bar(dd, 
            x="Equipo", 
            y='copas',
            color='Equipo', 
            title="Con algunas Copas de más?",
            range_y=[0,40],
            #  range_y=[0,40],
            animation_frame="Temp",
            animation_group="Equipo",
            )
fig.update_layout(width=1000)
fig.layout.updatemenus[0].buttons[0].args[1]['frame']['duration'] = 15
fig.layout.updatemenus[0].buttons[0].args[1]['transition']['duration'] = 5
st.plotly_chart(fig)
