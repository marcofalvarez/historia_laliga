import streamlit as st 
import pandas as pd 
import numpy as np 
import plotly.express as px
import plotly.graph_objects as go 
from plotly.subplots import make_subplots
from datetime import datetime
from datetime import date




#funcion para cargar la tabla excel
@st.cache_data
def data_upload(archivo):
    df = pd.read_csv(archivo)
    return df

@st.cache_data
def generic_tables(archivo):
    df = data_upload(archivo)
    #cambiando el formato de la columna Temporada

    df['Temp'] = df['Temporada'].map(lambda x : x.split("-")[0])
    df['Temp'] = df['Temp'].astype(str)

    df = df.loc[:,['Temporada', 'Temp','Posicion','Equipo','PT', 'PJ', 'PG', 'PE', 'PP', 'GF', 'GC', 'PT_C', 'PJ_C', 'PG_C',
    'PE_C', 'PP_C', 'GF_C', 'GC_C', 'PT_F', 'PJ_F', 'PG_F', 'PE_F', 'PP_F',
    'GF_F', 'GC_F']]
    return df

@st.cache_data
def sunb_table(_csv_file):
    df = data_upload(_csv_file)
    #conteo de las veces que cada equipo ha participado en la liga    
    df_part = df.groupby('Equipo').size().reset_index()
    df_part.rename(columns = {'Equipo':'Equipo', 0 :'Participación'}, inplace = True)
    #conteo de las veces que cada equipo ha ganado en la liga 
    df_p1 = df[(df['Posicion'] == 1)].groupby('Equipo').count().reset_index()
    df_p1.rename(columns = {'Temporada':'Copa'}, inplace = True)
    df_p1.drop(['Posicion', 'PT', 'PJ', 'PG', 'PE', 'PP', 'GF',
               'GC', 'PT_C', 'PJ_C', 'PG_C', 'PE_C', 'PP_C', 'GF_C', 'GC_C', 'PT_F',
               'PJ_F', 'PG_F', 'PE_F', 'PP_F', 'GF_F', 'GC_F'], axis = 1, inplace = True)
    
    #unir los dos últimos dataframes para obtener una tabla con participacion y numero de copas ganadas
    df_p2=pd.merge(df_part,df_p1, left_on='Equipo', right_on='Equipo', how='left')
    df_p2.rename(columns = {0:'Participacion'}, inplace = True)
    df_p2.fillna(0, inplace=True)
    df_p2['1Copa_o+'] = df_p2['Copa'].map(lambda x : bool(x))
    return df_p2[(df_p2["Participación"] >= 20)]

@st.cache_data
def part_table(_csv_file):
    df = data_upload(_csv_file)
    df = df[df['Posicion'] == 1].reset_index()
    #hacer una columna con el año de la temporada
    df['Temp'] = df['Temporada'].map(lambda x : x.split("-")[0])
    df['Temp'] = df['Temp'].map(lambda x : datetime.strptime(x, '%Y'))
    df['Temp'] = df['Temp'].astype(str)

    #ordenar las columnas
    df = df.loc[:,['Temporada', 'Temp','Posicion','Equipo','PT', 'PJ', 'PG', 'PE', 'PP', 'GF', 'GC', 'PT_C', 'PJ_C', 'PG_C',
        'PE_C', 'PP_C', 'GF_C', 'GC_C', 'PT_F', 'PJ_F', 'PG_F', 'PE_F', 'PP_F',
        'GF_F', 'GC_F']]
    return df

@st.cache_data
def mapa_talbe(_csv_estadios, _csv_file):
    
    ds = data_upload(_csv_estadios)
    df = sunb_table(_csv_file)
    ds['Equipo'] = ds['Equipo'].map(lambda x : "Athletic Club de Bilbao" if x == "Atlético de Bilbao" else x)
    df_p3=pd.merge(df,ds, left_on='Equipo', right_on='Equipo', how='left')
    df_p3['Latitud'] = df_p3['Latitud'].astype(float)
    df_p3['Longitud'] = df_p3['Longitud'].astype(float)
    df_p3 = df_p3.rename(columns= {'Latitud' : 'lat', 'Longitud': 'lng'})
    return df_p3

@st.cache_data   
def cumsum_table(_csv_file):
    dd= data_upload(_csv_file)
    dd['Temp'] = dd['Temporada'].map(lambda x : x.split("-")[0])
    dd['Temp'] = dd['Temp'].astype(int)
    dd = dd[(dd['Posicion'].between(1,5)) & (dd['Temp'] < 2023)].reset_index()
    dd['Temp'] = dd['Temp'].astype(str)

    ddp1 = dd[dd["Posicion"] == 1].reset_index()

    equipo1 = ddp1.Equipo.unique().tolist()
    equipo1 = [[equipo1[i] for i in range(9)]*92]

    temp1 = ddp1.Temp.unique().tolist()
    temp1 = [[temp1[i]]*9 for i in range(len(temp1))]
    temp1 = [i for r in temp1 for i in r]

    dfn = pd.DataFrame(list(zip(equipo1[0], temp1)), columns = ["Equipo", "Temp"])

    df3 = pd.merge(dfn, ddp1, left_on = ["Equipo", 'Temp'], right_on = ["Equipo", 'Temp'], how = "left" )
    df3 = df3.fillna(0)

    df4 = df3.drop(['level_0', 'index', 'Temporada','PT',
           'PJ', 'PG', 'PE', 'PP', 'GF', 'GC', 'PT_C', 'PJ_C', 'PG_C', 'PE_C',
           'PP_C', 'GF_C', 'GC_C', 'PT_F', 'PJ_F', 'PG_F', 'PE_F', 'PP_F', 'GF_F',
           'GC_F'], axis=1)

    df4.sort_values(['Equipo', "Temp"], inplace=True)
    df4 = df4.reset_index(drop=True)

    Bilbao_l = [df4['Posicion'][i] for i in range(0, 92)]
    Bilbao_l = [sum(Bilbao_l[0:i[0]+1]) for i in enumerate(Bilbao_l)]

    Atlético_Madrid_l = [df4['Posicion'][i] for i in range(92, 184)]
    Atlético_Madrid_l = [sum(Atlético_Madrid_l[0:i[0]+1]) for i in enumerate(Atlético_Madrid_l)]

    Barcelona_l = [df4['Posicion'][i] for i in range(184, 276)]
    Barcelona_l = [sum(Barcelona_l[0:i[0]+1]) for i in enumerate(Barcelona_l)]

    Betis_l = [df4['Posicion'][i] for i in range(276, 368)]
    Betis_l = [sum(Betis_l[0:i[0]+1]) for i in enumerate(Betis_l)]

    Deportivo_Coruna_l = [df4['Posicion'][i] for i in range(368, 460)]
    Deportivo_Coruna_l = [sum(Deportivo_Coruna_l[0:i[0]+1]) for i in enumerate(Deportivo_Coruna_l)]

    Real_Madrid_l = [df4['Posicion'][i] for i in range(460, 552)]
    Real_Madrid_l = [sum(Real_Madrid_l[0:i[0]+1]) for i in enumerate(Real_Madrid_l)]

    Real_Sociedad_l = [df4['Posicion'][i] for i in range(552, 644)]
    Real_Sociedad_l = [sum(Real_Sociedad_l[0:i[0]+1]) for i in enumerate(Real_Sociedad_l)]

    Sevilla_l = [df4['Posicion'][i] for i in range(644, 736)]
    Sevilla_l = [sum(Sevilla_l[0:i[0]+1]) for i in enumerate(Sevilla_l)]

    Valencia_l = [df4['Posicion'][i] for i in range(736, 828)]
    Valencia_l = [sum(Valencia_l[0:i[0]+1]) for i in enumerate(Valencia_l)]

    cumsum_total = Bilbao_l + Atlético_Madrid_l + Barcelona_l + Betis_l + Deportivo_Coruna_l + Real_Madrid_l + Real_Sociedad_l + Sevilla_l + Valencia_l

    df4['copas'] = cumsum_total
    return df4