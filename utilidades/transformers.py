from sklearn.base import TransformerMixin
from sklearn.base import BaseEstimator
from sklearn.pipeline import Pipeline
import pandas as pd
import numpy as np



# Scalers para FECHA--> transformación a seno y coseno (CosSinMesHoraMinuto, CosSinDiaSemana)

class CosSinMesHoraMinuto(TransformerMixin,BaseEstimator):

    '''
    Transformer para usar con ColumnTransformer. Utiliza como entrada un df con una columna fecha datetime.
    Retorna columnas de seno y coseno de MES, HORA y MINUTOS
    '''

    def __init__(self):
        pass

    def fit(self, X, columna_fecha, y=None):
        return self

    def transform(self, X, columna_fecha, y=None):

        months_in_year = 12
        hours_in_day = 23
        minutes_in_hour = 60

        X_return = pd.DataFrame()

        X_return['sin_mes'] = np.sin(2*np.pi*X[columna_fecha].dt.month/months_in_year)
        X_return['cos_mes'] = np.cos(2*np.pi*X[columna_fecha].dt.month/months_in_year)


        X_return['sin_hora'] = np.sin(2*np.pi*X[columna_fecha].dt.hour/hours_in_day)
        X_return['cos_hora'] = np.cos(2*np.pi*X[columna_fecha].dt.hour/hours_in_day)

        X_return['sin_minute'] = np.sin(2*np.pi*X[columna_fecha].dt.minute/minutes_in_hour)
        X_return['cos_minute'] = np.cos(2*np.pi*X[columna_fecha].dt.minute/minutes_in_hour)


        return np.array(X_return)


class CosSinDiaSemana(TransformerMixin,BaseEstimator):

    '''
    Toma como input una columna que tenga como valores dias de la semana (Lunes, Martes..), y los transforma entrada
    numero de día (1,2...7)
    '''


    def __init__(self):
        pass

    def fit(self, X, columna_dia_semana ,y=None):
        return self

    def transform(self, X, columna_dia_semana, y=None):

        X_return = pd.DataFrame()

        days_in_week = 7

        dias_num = {'Lunes':1, 'Martes': 2, 'Miercoles': 3 , 'Jueves': 4, 'Viernes': 5, 'Sabado': 6, 'Domingo': 7}
        X_return[columna_dia_semana] = X.DIANOM.map(dias_num)


        X_return['sin_dia_semana'] = np.sin(2*np.pi*X_return.dia_numero_sem/days_in_week)
        X_return['cos_dia_semana'] = np.cos(2*np.pi*X_return.dia_numero_sem/days_in_week)


        return np.array(X_return.drop(columns = ['dia_numero_sem']))
