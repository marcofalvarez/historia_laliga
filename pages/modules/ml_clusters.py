import random
import numpy as np
import pandas as pd
from datetime import datetime
from datetime import date
import sklearn
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.cluster import KMeans

def group_temporadas(_csv_file):
    df= pd.read_csv(_csv_file)
    df = df[(df['Posicion'].between(1,10)) & (df['Temporada'] < "2023-24")].groupby(['Temporada']).mean(numeric_only=True).reset_index()

    df['Temp'] = df['Temporada'].map(lambda x : x.split("-")[0])
    df = df.loc[:,['Temporada', 'Temp','Posicion','PT', 'PJ', 'PG', 'PE', 'PP', 'GF', 'GC', 'PT_C', 'PJ_C', 'PG_C','PE_C', 'PP_C', 'GF_C', 'GC_C', 'PT_F', 'PJ_F', 'PG_F', 'PE_F', 'PP_F',
    'GF_F', 'GC_F']]
    df['Temp'] = df['Temp'].astype(int)
    return df

def scaling_data(df):
    x_scaler = MinMaxScaler()
    data = x_scaler.fit_transform(df.iloc[:,3:])
    return data

def making_clusters(data, df):

    def run_model(data, n):
        kmeans = KMeans(n_clusters = n, random_state=42)

        model = kmeans.fit(data)
        cluster = kmeans.labels_
        inertia = kmeans.inertia_
        return model, cluster, inertia

    model2, cluster2, inertia2 = run_model(data, 2)
    model3, cluster3, inertia3 = run_model(data, 3)
    model4, cluster4, inertia4 = run_model(data, 4)

    df['cluster2'] = cluster2
    df['cluster3'] = cluster3
    df['cluster4'] = cluster4
    return df

def inertias(data):
    
    inercias = list() 

    for k in range(1, 11): 
        kmeans = KMeans(n_clusters = k, random_state=42)
        kmeans.fit(data)     
        inercias.append(kmeans.inertia_) 

    return inercias