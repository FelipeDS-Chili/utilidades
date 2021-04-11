import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import requests
from bs4 import BeautifulSoup
import re
import os
import time

def reconstruct_data(df, columna_filtro, columna_a_reconstruir, n):

    '''
    Esta función es para reconstruir los NaN values con regressiones lineales entre segmentos sin datos.
    De tal forma que los graficos de lineas se vean continuos y no con vacios
    La funcion completa los graficos lineales por para cada categoria (ej: pais)
    Columna_filtro es la columna por la cual se filtrara la data para tratarla parcialmente
    columna_a_reconstruir es la columna la cual se insertará data para ser utilizada en graficos
    n: es el numero de columna que es la columna a reconstruir
    '''

    for country in list(df[columna_filtro].unique()):

        data_pais = df[df[columna_filtro] == country].copy()

        if data_pais[data_pais[columna_filtro] == country][columna_a_reconstruir].isnull().sum() == len(data_pais[data_pais[columna_filtro] == country][columna_a_reconstruir]):
            continue


        if pd.isnull( data_pais.iloc[0,n] ):

            data_pais.iloc[0,n] = 0

        if pd.isnull( data_pais.iloc[len(data_pais)-1,n] ):

            data_pais.iloc[len(data_pais)-1,n] = data_pais[data_pais[columna_filtro] == country][columna_a_reconstruir].dropna().tail(1).iloc[0]

        empty = []

        for idx, value in enumerate(data_pais[columna_a_reconstruir]):

            if pd.isnull(value):
                empty.append(idx)

        if len(empty) > 0:



            last_digit = empty[0] #digito para iterar nan values index list
            diff_empty = []

            for idx in empty:
                diff = idx - last_digit
                diff_empty.append(diff)
                last_digit = idx

            del diff_empty[0]

            if len(diff_empty) > 0:

                before_value_idx = empty[0]-1
                before_value = data_pais[columna_a_reconstruir].iloc[before_value_idx]
                empty.insert(len(empty), 9) # numero ficticio para que se lean todos los valores después




                for idx, diff_num in enumerate(diff_empty):


                    if diff_num != 1:

                        ended_value_idx = empty[idx] + 1
                        ended_value = data_pais[columna_a_reconstruir].iloc[ended_value_idx]
                        coef = np.polyfit([before_value_idx, ended_value_idx], [before_value, ended_value], 1)

                        #calcular regression para nan values index
                        #insertarlos en el df
                        values_to_fill = np.array([i for i in range(before_value_idx+1,ended_value_idx)])*coef[0] + coef[1]

                        for idx_2, i in enumerate(range(before_value_idx+1, ended_value_idx)):

                            data_pais.iloc[i,n] = values_to_fill[idx_2]
                            df[df[columna_filtro]==country] = data_pais

                        if (idx + 1) < len(empty):

                            before_value_idx = empty[idx + 1] - 1
                            before_value = data_pais[columna_a_reconstruir].iloc[before_value_idx]

                        if (idx + 1) == len(diff_empty):

                            ended_value_idx = empty[idx+1] + 1
                            ended_value = data_pais[columna_a_reconstruir].iloc[ended_value_idx]
                            coef = np.polyfit([before_value_idx, ended_value_idx], [before_value, ended_value], 1)

                            #calcular regression para nan values index
                            #insertarlos en el df
                            values_to_fill = np.array([i for i in range(before_value_idx+1,ended_value_idx)])*coef[0] + coef[1]

                            for idx_2, i in enumerate(range(before_value_idx+1, ended_value_idx)):

                                data_pais.iloc[i,n] = values_to_fill[idx_2]
                                df[df[columna_filtro]==country] = data_pais

                    else:

                        if (idx + 1) == len(diff_empty):

                            ended_value_idx = empty[idx+1] + 1
                            ended_value = data_pais[columna_a_reconstruir].iloc[ended_value_idx]
                            coef = np.polyfit([before_value_idx, ended_value_idx], [before_value, ended_value], 1)

                            #calcular regression para nan values index
                            #insertarlos en el df
                            values_to_fill = np.array([i for i in range(before_value_idx+1,ended_value_idx)])*coef[0] + coef[1]

                            for idx_2, i in enumerate(range(before_value_idx+1, ended_value_idx)):

                                data_pais.iloc[i,n] = values_to_fill[idx_2]
                                df[df[columna_filtro]==country] = data_pais

            elif (len(diff_empty) ==0 and len(empty) == 1):

                        before_value_idx = empty[0] - 1

                        before_value = data_pais[columna_a_reconstruir].iloc[before_value_idx]


                        ended_value_idx = empty[0] + 1

                        ended_value = data_pais[columna_a_reconstruir].iloc[ended_value_idx]


                        coef = np.polyfit([before_value_idx, ended_value_idx], [before_value, ended_value], 1)


                        values_to_fill = np.array([i for i in range(before_value_idx+1,ended_value_idx)])*coef[0] + coef[1]

                        for idx_2, i in enumerate(range(before_value_idx+1, ended_value_idx)):

                            data_pais.iloc[i,n] = values_to_fill[idx_2]
                            df[df[columna_filtro]==country] = data_pais



    return df


def get_population(country):

    '''
    Retorna la poblacion del pais en el 2019/2020
    '''

    if country:

        country = country.replace(' ','-')
        country = country.lower()

        url = f'https://www.worldometers.info/world-population/{country}-population/'

        response = requests.get(url)

        if response.status_code == 200:

            html = response.text

            soup = BeautifulSoup(html, 'html.parser')

            if re.search(r"\d{5,}", soup.find(class_ = "col-md-8 country-pop-description").find_all('li')[0].text.replace(',','')):

                population = int(re.search(r"\d{5,}", soup.find(class_ = "col-md-8 country-pop-description").find_all('li')[0].text.replace(',','')).group(0))

                return population

            return None

        return None

    return None

def haversine_vectorized(df,
                         start_lat="pickup_latitude",
                         start_lon="pickup_longitude",
                         end_lat="dropoff_latitude",
                         end_lon="dropoff_longitude"):
    """
        Calculate the great circle distance between two points
        on the earth (specified in decimal degrees).
        Vectorized version of the haversine distance for pandas df
        Computes distance in kms
    """

    lat_1_rad, lon_1_rad = np.radians(df[start_lat].astype(float)), np.radians(df[start_lon].astype(float))
    lat_2_rad, lon_2_rad = np.radians(df[end_lat].astype(float)), np.radians(df[end_lon].astype(float))
    dlon = lon_2_rad - lon_1_rad
    dlat = lat_2_rad - lat_1_rad

    a = np.sin(dlat / 2.0) ** 2 + np.cos(lat_1_rad) * np.cos(lat_2_rad) * np.sin(dlon / 2.0) ** 2
    c = 2 * np.arcsin(np.sqrt(a))
    return 6371 * c


def minkowski_distance(df, p,
                       start_lat="pickup_latitude",
                       start_lon="pickup_longitude",
                       end_lat="dropoff_latitude",
                       end_lon="dropoff_longitude"):
    x1 = df[start_lon]
    x2 = df[end_lon]
    y1 = df[start_lat]
    y2 = df[end_lat]
    return ((abs(x2 - x1) ** p) + (abs(y2 - y1)) ** p) ** (1 / p)



################
#  DECORATORS  #
################

def simple_time_tracker(method):
    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()
        if 'log_time' in kw:
            name = kw.get('log_name', method.__name__.upper())
            kw['log_time'][name] = int((te - ts))
        else:
            print(method.__name__, round(te - ts, 2))
        return result

