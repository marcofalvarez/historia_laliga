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
import pages.modules.ml_clusters as ml
st.set_page_config(page_title= "Resumen",
                   page_icon= ":soccer:",
                   layout="wide")

st.markdown("""
        <style>
        @font-face {
            font-family: 'LALIGAText-Regular';
            src: url('https://assets.laliga.com/assets/public/fonts/LALIGAText-Regular.woff2') format('woff2');
        }

        *  {
            font-family: 'LALIGAText-Regular', sans-serif;
        }
        </style>
        """, unsafe_allow_html=True)

st.markdown("""     
            <style>         
                     
            .st-emotion-cache-pkbazv {             
            color: rgb(255, 255, 255); 
                     
            }     
            </style> """, 
            unsafe_allow_html=True,
            )

st.title("Resumen de la Historia de La Liga")
st.divider()
st.markdown(
    '''
    ## Explorando la Historia de La Liga Española

    ¿Quiénes son los actores más importantes y cuáles son los momentos clave que han marcado la historia de La Liga?

    A continuación, te presentamos un resumen general desde 1928 hasta la actualidad:
    '''
)

st.markdown(
    '''
    ## Participación de Equipos

    Desde su inicio en 1928, un total de 71 equipos han participado en La Liga. 
    Algunos equipos han mantenido su presencia constante en el torneo a lo largo de los años.
    Sin embargo, son muy pocos los que han logrado alzarse con el trofeo.
    Hemos seleccionado aquellos equipos que han participado en 20 o más temporadas para presentar la siguiente información:
    - Su ubicación geográfica.
    - La cantidad de veces que han participado en el torneo.
    - El número de trofeos que han obtenido.
    '''
)
st.divider()
css="""
<style>
    [data-testid="stForm"] {
        background: LightBlue;
    }
</style>
"""
st.write(css, unsafe_allow_html=True)
#hacer dos graficos
col1, col2 = st.columns(2)

df = tables.sunb_table('data/clasificacion.csv')
#grafico de bara con equipos que han participado mas de 20 veces
with col1:
    st.subheader(
        '''¿Quién ha ganado La Liga?
              
            
'''
    )

    with st.expander("**Instrucciones:**"):
        st.info(
            '''
        1. Pasa el cursor sobre la gráfica para ver información detallada sobre los participantes y ganadores de La Liga.
        2. Haz clic en los elementos de la gráfica para explorar diferentes niveles de detalle.
        '''
        )

    sunfig = px.sunburst(data_frame = df,
                  values     = "Participación",
                  path       = ["1Copa_o+", "Equipo"],
                  hover_name = 'Equipo',
                  hover_data = "Copa",
                  #color      = "Participacion"
                #   title = "Quién ha ganado la liga"
                 )
    #sunfig.update_traces(textinfo = "label+percent parent")
    st.plotly_chart(sunfig,
                    use_container_width=True,
                    )


# código para hacer el mapa con la ubicación de los estadios
    
dm = tables.mapa_talbe('data/estadios.csv', 'data/clasificacion.csv')

with col2:
    st.subheader('''Mapa de la ubicación de los equipos   ''')
    with st.expander("**Instrucciones:**"):
        st.info(
        '''
            1. El tamaño de las columans corresponde a la cantidad de veces que el equipo participó en
            La Liga. 
            2. Pasar el cursor sobre mapa (acción -hover) para aprender más sobre los equipos.  
            3. Usa la rueda del ratón (acción -scroll), pinchar o click + movimiento del ratón para navegar
            en el mapa o hacer zoom.  
            4. Ctr + click te permite cambiar el ángulo de observación en 3 dimensiones.   
            '''
        )       

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
    st.pydeck_chart(r, 
                    use_container_width=True,
                    )
    
  
st.divider()

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
st.plotly_chart(fig,
                use_container_width=True,
                )

st.divider()
