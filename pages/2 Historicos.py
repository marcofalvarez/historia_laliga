import streamlit as st 
import pandas as pd 
import numpy as np 
import plotly.express as px
import plotly.graph_objects as go 
from plotly.subplots import make_subplots
# from datetime import datetime
# from datetime import date
import pages.modules.preparing_tables as tables

#titulo y configuración de la pagina
st.set_page_config(page_title= "Históricos",
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
st.title("Estadísticas a lo largo de los años")
st.divider()
#opciones al lado de la pagina para 2 tipos de visualizaciones
form2 = st.sidebar.form(key='opciones_historicos')

tipo_datos = form2.radio('Escoger los datos a desplegar', 
                         ['de ganadores de La Liga', 'por equipo'],
                         captions=["Resumen general para el equipo ganador para cada temporada", "Comparación entre equipos"])
hist_graphs = form2.form_submit_button('¡Vale!')


css="""
<style>
    [data-testid="stForm"] {
        background: LightBlue;
    }
</style>
"""
st.write(css, unsafe_allow_html=True)


def mostrar_instrucciones():
    st.info(
        '''
        **Instrucciones:**

        1. Escoge una o más estadísticas que te interesen.
        2. Haz clic en "¡Vale!".
        3. Pasa el cursor sobre la gráfica para obtener más información sobre el equipo ganador de cada temporada de La Liga.
        4. Puedes cambiar la resolución temporal mediante el menú en la parte superior de la gráfica o directamente utilizando el control deslizante ubicado debajo de la misma. Desliza el cursor del mouse cuando aparezcan las flechas dobles.
        '''
    )


#si selecciona las estadísticas históricas para el equipo ganador de la copa
if tipo_datos == 'de ganadores de La Liga':
    st.markdown(
        '''
            ## ¿Qué esfuerzo se requiere para ganar La Liga?
            Este gráfico pretende contestar a esta pregunta así cómo
            darnos pistas sobre la evolución a través del tiempo.
                '''
    )
    mostrar_instrucciones()


    #funcion para cargar la tabla excel

 
    df = tables.part_table('data/clasificacion.csv')

    #hacer el cuadro con los equipos escogidos
    formg = st.form(key='opciones_grafico')
    opciones_i = df.columns[4:]
    opciones_f = formg.multiselect('Estadísticas de los ganadores de La Liga', opciones_i, placeholder='Elija una opción')
    make_eleccion = formg.form_submit_button('¡Vale!')

    #indicar los gráficos por hacer en funcion de equipos escogidos por el usuario
    if make_eleccion:
    #     st.write(opciones_f)
    # Create figures

        prfig = make_subplots()
        for i, col in enumerate(opciones_f,0):
            prfig.add_trace(go.Scatter(x = df['Temp'], y = df[opciones_f[i]], mode ='lines', name = col, hovertext=df['Equipo']))
            prfig.update_layout(title_text= "Historial del equipo ganador de La Liga por año")

            prfig.update_layout(
                xaxis=dict(
                    rangeselector=dict(
                        buttons=list([
                            dict(count=10,
                                label="1 década",
                                step="year",
                                stepmode="backward"),
                            dict(count=25,
                                label="25 años",
                                step="year",
                                stepmode="backward"),
                            dict(count=50,
                                label="50 años",
                                step="year",
                                stepmode="backward"),
                            # dict(count=1,
                            #     label="1y",
                            #     step="year",
                            #     stepmode="backward"),
                            dict(step="all")
                        ])
                    ),
                    rangeslider=dict(
                        visible=True
                    ),
                    type="date"
                )
            )
        prfig.update_xaxes(title_text="Temporada")
        st.plotly_chart(prfig,
                        use_container_width=True,
                        )

#si la opciones es para hacer comparaciones entre equipos
else:
    st.markdown(
        '''
            ## ¿Cómo se comparan los equipos entre sí?
            Este gráfico pretende contestar a esta pregunta así como
            darnos pistas sobre la evolución a través del tiempo.
            '''
    )

    mostrar_instrucciones()
    
    df = tables.generic_table1('data/clasificacion.csv')

    #hacer la tabla con los equipos esogidos por el usuario
    formeq = st.form(key='opciones_equipos')
    
    lista_eq = list(df['Equipo'].unique())
    opciones_eq = formeq.multiselect('Escoge un equipo', lista_eq)
    
    lista_es = df.columns[4:]
    opciones_est = formeq.multiselect('Escoge una estadística ', lista_es)
    
    make_eq = formeq.form_submit_button('¡Vale!')
    cols_f = ['Temp','Posicion','Equipo']
    cols_f.extend(opciones_est)
    df = df[(df["Equipo"].isin(lista_eq))][cols_f]

    if make_eq:
        dfe2 = df[(df["Equipo"].isin(opciones_eq))][cols_f]
        for i, col in enumerate(opciones_est,0):
            figeq = px.line(data_frame = dfe2,
                            x = 'Temp',
                            y = dfe2[opciones_est[i]],
                            color = 'Equipo',
                            hover_name = 'Posicion'
                        )
            figeq.update_layout(title_text= f" {opciones_est[i]} por año de {opciones_eq}")

            figeq.update_layout(
                xaxis=dict(
                    rangeselector=dict(
                        buttons=list([
                            dict(count=10,
                                label="1 década",
                                step="year",
                                stepmode="backward"),
                            dict(count=25,
                                label="25 años",
                                step="year",
                                stepmode="backward"),
                            dict(count=50,
                                label="50 años",
                                step="year",
                                stepmode="backward"),
                            # dict(count=1,
                            #     label="1y",
                            #     step="year",
                            #     stepmode="backward"),
                            dict(step="all")
                        ])
                    ),
                    rangeslider=dict(
                        visible=True
                    ),
                    type="date"
                )
            )
            figeq.update_xaxes(title_text="Temporada")

            st.plotly_chart(figeq, 
                            use_container_width=True,
                            )
            st.divider()

