import streamlit as st 
import pandas as pd 
import numpy as np 
import plotly.express as px
import plotly.graph_objects as go 
from plotly.subplots import make_subplots
from datetime import datetime
from datetime import date
import os

st.set_page_config(page_title= "Equipos",
                   page_icon= ":soccer:",
                   layout="wide")
st.title("Estadísticas de equipos")

#funcion para cargar la tabla 
@st.cache_data
def data_upload():
    df = pd.read_csv("data/porcentajes.csv")
    return df
df = data_upload()

#seleccion de datos historicos
form1 = st.sidebar.form(key='opciones_tabla')
team = df['Equipo'].unique()
stat = []
selec_team = form1.selectbox('ESCOGE UN EQUIPO', team) #, format_func=lambda x: f"{x}")
selec_stat = form1.radio('ESCOJA EL TIPO DE ESTADÍSTICA',('TOTAL', 'LOCAL', 'VISITANTE'))
if selec_stat == 'TOTAL':
    stat = ['Equipo','Partidos_jugados','Partidos_ganados', 'Partidos_perdidos', 'Partidos_empatados', 'Goles_a_favor', 'Goles_en_contra', 'Porcentaje_victorias', 'Porcentaje_derrotas', 'Porcentaje_empates', 'Media_goles_a_favor', 'Media_goles_en_contra']
elif selec_stat == 'LOCAL':
    stat = ['Equipo','Total_partidos_jugados_casa', 'Partidos_ganados_casa', 'Partidos_perdidos_casa', 'Partidos_empatados_casa', 'Porcentaje_victorias_casa', 'Porcentaje_derrotas_casa', 'Porcentaje_empates_casa']
elif selec_stat == 'VISITANTE':
    stat = ['Equipo','Total_partidos_jugados_fuera', 'Partidos_ganados_fuera', 'Partidos_perdidos_fuera', 'Partidos_empatados_fuera', 'Porcentaje_victorias_fuera', 'Porcentaje_derrotas_fuera', 'Porcentaje_empates_fuera']
make_table = form1.form_submit_button('VALE!')

if make_table:
    
    st.header("EQUIPO: ")
    st.subheader(selec_team) 
    st.dataframe(data=df.loc[df['Equipo'] == selec_team, stat])

    # Cargar los datos de los escudos
    escudos_path = "data/ESCUDOS"
    escudo_filename = f"{selec_team}.png"
    escudo_path = os.path.join(escudos_path, escudo_filename)

    # Mostrar el escudo si existe
    if os.path.exists(escudo_path):
        st.image(escudo_path, caption=selec_team, width=100)

    # Crear el primer gráfico de donut para victorias, derrotas y empates
    if selec_stat == 'TOTAL':
        victorias = df.loc[df['Equipo'] == selec_team, 'Partidos_ganados'].values[0]
        derrotas = df.loc[df['Equipo'] == selec_team, 'Partidos_perdidos'].values[0]
        empates = df.loc[df['Equipo'] == selec_team, 'Partidos_empatados'].values[0]
    elif selec_stat == 'LOCAL':
        victorias = df.loc[df['Equipo'] == selec_team, 'Partidos_ganados_casa'].values[0]
        derrotas = df.loc[df['Equipo'] == selec_team, 'Partidos_perdidos_casa'].values[0]
        empates = df.loc[df['Equipo'] == selec_team, 'Partidos_empatados_casa'].values[0]
    elif selec_stat == 'VISITANTE':
        victorias = df.loc[df['Equipo'] == selec_team, 'Partidos_ganados_fuera'].values[0]
        derrotas = df.loc[df['Equipo'] == selec_team, 'Partidos_perdidos_fuera'].values[0]
        empates = df.loc[df['Equipo'] == selec_team, 'Partidos_empatados_fuera'].values[0]

    fig_donut_victorias = go.Figure(data=[go.Pie(labels=['Victorias', 'Derrotas', 'Empates'],
                                         values=[victorias, derrotas, empates])])
    fig_donut_victorias.update_traces(hoverinfo='label+value', textinfo='percent', textfont_size=20,
                               marker=dict(colors=['#2ecc71', '#e74c3c', '#f39c12'], line=dict(color='#FFFFFF', width=2)))
    fig_donut_victorias.update_layout(title_text="Victorias, derrotas y empates",
                               title_font_size=24)
    

    # Crear el segundo gráfico de donut para goles a favor y en contra
    goles_a_favor = df.loc[df['Equipo'] == selec_team, 'Goles_a_favor'].values[0]
    goles_en_contra = df.loc[df['Equipo'] == selec_team, 'Goles_en_contra'].values[0]

    fig_donut_goles = go.Figure(data=[go.Pie(labels=['Goles a favor', 'Goles en contra'],
                                            values=[goles_a_favor, goles_en_contra])])
    fig_donut_goles.update_traces(hoverinfo='label+value', textinfo='percent', textfont_size=20,
                                   marker=dict(colors=['#3498db', '#e74c3c'], line=dict(color='#FFFFFF', width=2)))
    fig_donut_goles.update_layout(title_text="Total de goles a favor y en contra",
                                   title_font_size=24)


    # Dividir el espacio horizontalmente para colocar los gráficos uno al lado del otro
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(fig_donut_victorias, use_container_width=True)
    with col2:
        st.plotly_chart(fig_donut_goles, use_container_width=True)

    # Crear las tarjetas para mostrar la media de goles a favor y en contra
    media_goles_a_favor = df.loc[df['Equipo'] == selec_team, 'Media_goles_a_favor'].values[0]
    media_goles_en_contra = df.loc[df['Equipo'] == selec_team, 'Media_goles_en_contra'].values[0]

    # Crear las tarjetas para mostrar la media de goles a favor y en contra
    st.subheader("Media de goles por partido")
    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="Goles a favor", value=round(media_goles_a_favor, 2), delta=None)
    with col2:
        st.metric(label="Goles en contra", value=round(media_goles_en_contra, 2), delta=None)


    # Filtrar el DataFrame para el equipo seleccionado
    equipo_seleccionado = df[df['Equipo'] == selec_team]

    # Calcular las diferencias absolutas entre la media del equipo seleccionado y la media de cada equipo
    df['Dif_goles_a_favor'] = abs(df['Media_goles_a_favor'] - equipo_seleccionado['Media_goles_a_favor'].iloc[0])
    df['Dif_goles_en_contra'] = abs(df['Media_goles_en_contra'] - equipo_seleccionado['Media_goles_en_contra'].iloc[0])

    # Ordenar el DataFrame por las diferencias calculadas y seleccionar los tres equipos más similares
    equipos_similares = df.sort_values(by=['Dif_goles_a_favor', 'Dif_goles_en_contra']).iloc[1:10]  # Excluimos el equipo seleccionado

    # Combinar el equipo seleccionado y los equipos similares
    equipos = pd.concat([equipo_seleccionado, equipos_similares])
    
    # Crear el gráfico de dispersión
    fig_scatter = px.scatter(equipos, x='Media_goles_a_favor', y='Media_goles_en_contra', text='Equipo',
        title=f'Media de goles a favor y goles en contra para {selec_team} y comparación con equipos similares',
        labels={'Media_goles_a_favor': 'Media de goles a favor', 'Media_goles_en_contra': 'Media de goles en contra'},
        hover_name='Equipo', color_discrete_sequence=['blue'])

    # Establecer los límites de los ejes x e y
    fig_scatter.update_xaxes(range=[0, 5], dtick=0.1)
    fig_scatter.update_yaxes(range=[0, 5], dtick=0.2)

    # Agregar línea de referencia
    fig_scatter.add_shape(type="line", x0=0, y0=0, x1=5, y1=5, line=dict(color="red", width=2))

    # Añadir anotación
    fig_scatter.add_annotation(x=50, y=50, text="Línea de equilibrio", showarrow=False, font=dict(color="red"))

    fig_scatter.update_traces(marker=dict(size=equipos['Goles_a_favor'], color='#ffcbcb', opacity=0.8),
                             textfont=dict(color="#132743"),  # Cambiar el color del texto
                             textposition='top center')  # Colocar el texto encima del marcador
    
    # Centrar el gráfico en los equipos mostrados
    x_center = equipos['Media_goles_a_favor'].mean()
    y_center = equipos['Media_goles_en_contra'].mean()
    fig_scatter.update_layout(xaxis=dict(range=[x_center-2, x_center+2]), yaxis=dict(range=[y_center-2, y_center+2]))

    # Mostrar el gráfico ajustado al ancho de la página
    st.plotly_chart(fig_scatter)

    # Cargar los datos de los estadios
    estadios_df = pd.read_csv("data/equipos_con_urls.csv")
    
    # Cargar los datos de los estadios
    estadio_seleccionado = estadios_df[estadios_df['Equipo'] == selec_team]

    if not estadio_seleccionado.empty:
        # Renombrar las columnas de latitud y longitud
        estadio_seleccionado = estadio_seleccionado.rename(columns={'Latitud': 'lat', 'Longitud': 'lon'})

        # Mostrar la ubicación del estadio y la imagen del estadio en columnas separadas
        col1, col2 = st.columns(2)

        # Columna 1: Mostrar el mapa
        with col1:
            st.subheader("UBICACION ESTADIO:")
            st.map(estadio_seleccionado)

        # Columna 2: Mostrar la imagen del estadio
        with col2:
            st.subheader("ESTADIO:")
            estadio_image_path = os.path.join("data", "Estadios", f"{selec_team}.png")
            if os.path.exists(estadio_image_path):
                st.image(estadio_image_path, caption=selec_team,  width=800)
            else:
                st.warning("Imagen del estadio no encontrada.")

    else:
        st.warning("No se encontró información del estadio para el equipo seleccionado.")




    # Cargar los datos de los estadios
    clasificacion = pd.read_csv("data/clasificacion.csv")

    # Agregar la parte fija a las URLs relativas
    estadios_df['URL'] = 'https://es.wikipedia.org/' + estadios_df['URL']

    # Obtener la URL del equipo seleccionado
    url_equipo_seleccionado = estadios_df[estadios_df['Equipo'] == selec_team]['URL'].values[0]

    # Mostrar el enlace encima de los gráficos de donut
    st.markdown(f"[Más información sobre {selec_team} en Wikipedia]({url_equipo_seleccionado})")


    # Filtrar los datos para el equipo seleccionado desde la temporada 1987-88
    clasif_equipo_desde_1987 = clasificacion[(clasificacion['Equipo'] == selec_team) & (clasificacion['Temporada'] >= '1987-88')]

    # Calcular la cantidad de temporadas jugadas desde 1987-88
    temporadas_jugadas_desde_1987 = clasif_equipo_desde_1987['Temporada'].nunique()

    # Calcular la suma total de puntos desde 1987-88 para el equipo seleccionado
    suma_puntos_desde_1987 = clasif_equipo_desde_1987['PT'].sum()

    # Calcular la media de puntos desde 1987-88 para el equipo seleccionado
    media_puntos_desde_1987 = suma_puntos_desde_1987 / temporadas_jugadas_desde_1987

    # Calcular la media de puntos por temporadas jugadas para el equipo seleccionado
    temporadas_jugadas = clasificacion[clasificacion['Equipo'] == selec_team]['Temporada'].nunique()
    media_puntos_historica = clasificacion[clasificacion['Equipo'] == selec_team]['PT'].sum() / temporadas_jugadas

    # Calcular el número de veces que ha ganado la liga
    veces_ganadas = clasificacion[(clasificacion['Equipo'] == selec_team) & (clasificacion['Posicion'] == 1)].shape[0]

    # Encontrar el récord de puesto de clasificación y el número de puntos conseguidos
    #mejor_clasificacion = clasificacion[clasificacion['Equipo'] == selec_team]['Posicion'].min()
    #año_mejor_clasificacion = clasificacion[(clasificacion['Equipo'] == selec_team) & (clasificacion['Posicion'] == mejor_clasificacion)]#['Temporada'].iloc[0]
    #puntos_año_mejor_clasificacion = clasificacion[(clasificacion['Equipo'] == selec_team) & (clasificacion['Posicion'] == mejor_clasificacion)]#['PT'].iloc[0

    # Encontrar todos los récords de clasificación para el equipo seleccionado
    records_clasificacion = clasificacion[clasificacion['Equipo'] == selec_team].groupby(['Posicion', 'Temporada']).agg({'PT': 'max'}).reset_index()

    # Encontrar la mejor clasificación (la posición más baja) y el número de puntos conseguidos
    mejor_clasificacion = records_clasificacion['Posicion'].min()
    records_mejor_clasificacion = records_clasificacion[records_clasificacion['Posicion'] == mejor_clasificacion]

    # Mostrar las tarjetas
    st.subheader("Estadísticas del equipo seleccionado:")
    st.write("---")  # Agregar una línea horizontal para separar las estadísticas

    # Media de puntos por temporada (Histórica)
    media_puntos_historica_str = f"Media de puntos por temporada (Histórica): {media_puntos_historica:.2f} puntos"
    st.write(media_puntos_historica_str)

    # Media de puntos por temporada (Desde 1987)
    media_puntos_desde_1987_str = f"Media de puntos por temporada (Desde 1987): {media_puntos_desde_1987:.2f} puntos. (Este apartado lo hacemos para ver la media de puntos desde que hay 20 equipos)"
    st.write(media_puntos_desde_1987_str)

    # Número de veces jugadas
    veces_jugadas_str = f"Número de temporadas jugadas: {temporadas_jugadas}"
    st.write(veces_jugadas_str)

    # Número de veces ganadas
    veces_ganadas_str = f"Número de ligas ganadas: {veces_ganadas}"
    st.write(veces_ganadas_str)

    # Récord de clasificación
    if len(records_mejor_clasificacion) > 1:
        st.write("Récord de clasificación:")
        st.table(records_mejor_clasificacion[['Posicion', 'Temporada', 'PT']])
    else:
        año_mejor_clasificacion = records_mejor_clasificacion.iloc[0]['Temporada']
        puntos_año_mejor_clasificacion = records_mejor_clasificacion.iloc[0]['PT']
        st.write(f"Mejor puesto en la clasificación {mejor_clasificacion}º en la temporada{año_mejor_clasificacion} con un total de {puntos_año_mejor_clasificacion} pts")


    


























