
import streamlit as st 
import pandas as pd 
import numpy as np 
import plotly.express as px
import plotly.graph_objects as go 
from plotly.subplots import make_subplots
import pages.modules.preparing_tables as tables
# from st_aggrid import AgGrid, GridUpdateMode, DataReturnMode, JsCode, GridOptionsBuilder, ColumnsAutoSizeMode
# from st_aggrid.grid_options_builder import GridOptionsBuilder
st.set_page_config(page_title= "Temporadas",
                   page_icon= ":soccer:",
                   layout="wide")

st.title("Resultados al final de temporada")
st.divider()

#Use the menu on the right to customize the table that you want to display. 
#Once the you are happy with your selection select Vale!. 
st.markdown(
        '''
            ## Esta es una ventana en el tiempo para cada temporada!
            Esta página te permite apresiar los detalles más importantes por temporada  

        '''
)

with st.expander("Instrucciones"):
                st.markdown(
        '''           
                1- Escoger la temporada que te interese,  
                2- Escoger cuales posiciones quieres ver
                   (posición corresponde 1 al equipo ganador)  
                3- Ecoger el tipo de estádisticas  
                4- Hacer click en Vale!  
                5- Pasar el cursor sobre la gráfica (acción -hover)
                   para obtener el detalle de las estádisticas
                   dentro de las gráficas  
                
                '''
                )
#funcion para cargar la tabla excel

df = tables.generic_table2("data/clasificacion.csv")
# st.dataframe(data=df)



form1 = st.sidebar.form(key='opciones_tabla')
temps = df['Temporada'].unique().tolist()
pos = df['Posicion'].unique().tolist()
stat = []
selec_temp = form1.selectbox('escoger una temporada', temps, )
selec_pos = form1.slider(label='escoger una o más posiciones en la tabla', min_value= min(pos), max_value= max(pos),value=(1,3))
selec_stat = form1.radio('escojer el tipo de estadística',('total', 'en casa', 'de visitante'))

css="""
<style>
    [data-testid="stForm"] {
        background: LightBlue;
    }
</style>
"""
st.write(css, unsafe_allow_html=True)

if selec_stat == 'total':
    stat = ['Equipo','Posicion','PT', 'PJ', 'PG', 'PE', 'PP', 'GF','GC']
    with st.expander("Leyenda"):
          leyenda = (
            '''
            'PT':'Puntos Totales',  
            'PJ':'Partidos Jugados',  
            'PG':'Partidos Ganados',  
            'PE':'Partidos Empatados',  
            'PP':'Partidos Perdidos',  
            'GF':'Goles a Favor',  
            'GC':'Goles en Contra',  
            '''
        )
elif selec_stat == 'en casa':
    stat = ['Equipo','Posicion','PT_C', 'PJ_C', 'PG_C', 'PE_C', 'PP_C', 'GF_C', 'GC_C']
    with st.expander("Leyenda"):
          leyenda = (
            '''
            'PT_C':'Puntos Totales (en casa)',  
            'PJ_C':'Partidos Jugados (en casa)',  
            'PG_C':'Partidos Ganados (en casa)',  
            'PE_C':'Partidos Empatados (en casa)',  
            'PP_C':'Partidos Perdidos (en casa)',  
            'GF_C':'Goles a Favor (en casa)',  
            'GC_C':'Goles en Contra (en casa)',    
            '''
        )
elif selec_stat == 'de visitante':
    stat = ['Equipo','Posicion','PT_F', 'PJ_F', 'PG_F', 'PE_F', 'PP_F', 'GF_F', 'GC_F']
    with st.expander("Leyenda"):
          leyenda = (
            '''
            'PT_F':'Puntos Totales (fuera de casa)',  
            'PJ_F':'Partidos Jugados (fuera de casa)',  
            'PG_F':'Partidos Ganados (fuera de casa)',  
            'PE_F':'Partidos Empatados (fuera de casa)',  
            'PP_F':'Partidos Perdidos (fuera de casa)',  
            'GF_F':'Goles a Favor (fuera de casa)',  
            'GC_F':'Goles en Contra (fuera de casa)'      
            '''
        )
make_table = form1.form_submit_button('vale!')

if make_table:
    
    st.header("Temporada: ")
    st.subheader(selec_temp) 
    #st.write(selec_pos[0], selec_pos[1])
    
    st.dataframe(data=df[(df['Temporada'] == selec_temp) & (df['Posicion'].between(left=selec_pos[0], right=selec_pos[1], inclusive='both'))][stat], hide_index=True)
           #columns_auto_size_mode=ColumnsAutoSizeMode.FIT_CONTENTS)
    
    st.markdown(leyenda)
    st.divider()
    
    df_stat = df[(df['Temporada'] == selec_temp) & (df['Posicion'].between(left=selec_pos[0], right=selec_pos[1], inclusive='both'))][stat].reset_index()
    partidos = df_stat.columns[5:8]
    puntos = df_stat.columns[3]
    
    fig = px.bar(df_stat, 
                 x="Equipo", 
                 y=partidos, 
                 title="Points and games played")
    fig.add_scatter(x=df_stat['Equipo'], 
                y=df_stat[puntos], 
                name = 'Points')
    st.plotly_chart(fig)
    st.divider()

    
    equipo = df_stat.columns[1]
    goles_f = df_stat.columns[8]
    goles_c = df_stat.columns[9]
    
    gfig = go.Figure()
    gfig.add_trace(go.Scatter(x = df_stat[equipo], 
                           y = -(df_stat[goles_c]), 
                           fill='tonexty', 
                           name='goles en contra')) # fill down to next y
    gfig.add_trace(go.Scatter(x = df_stat[equipo], 
                           y = df_stat[goles_f], 
                           fill='tozeroy', 
                           name='goles a favor')) # fill down to xaxis

    #gfig.update_traces(stackgroup=1)
    #   Set x-axis title
    gfig.update_xaxes(title_text="Diferencia de Goles")

    st.plotly_chart(gfig,
                    use_container_width=True,
                    )
    st.divider()


