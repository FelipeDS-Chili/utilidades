from sklearn.base import TransformerMixin
from sklearn.base import BaseEstimator
from sklearn.pipeline import Pipeline
import pandas as pd
import numpy as np
from funciones import df_optimized



# Scalers para FECHA--> transformación a seno y coseno (CosSinMesHoraMinuto, CosSinDiaSemana)

class CosSinMesHoraMinuto(TransformerMixin,BaseEstimator):

    def __init__(self):
        
        '''
        Only requirement: have the column in the format: YY-MM-DD HH-MM-SS with datetime format
        Returns: sin and cos columns
        '''
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
    def __init__(self):

        '''
        Transformer to pass the week day to a cyclical variable. 
        Format = False --> The column contains the name of the days inside {Lunes, Martes, Miercoles..}
        Format = True --> The column already contains the number of the day inside {1,2,3,4..}
        columna_dia_semana --> column containing the days of week
        '''

        pass

    def fit(self, X, columna_dia_semana ,format = False, y=None):
        return self

    def transform(self, X, columna_dia_semana,format = False, y=None):

        X_return = pd.DataFrame()

        days_in_week = 7
        
        if format:
            X_return['sin_dia_semana'] = np.sin(2*np.pi*X.columna_dia_semana/days_in_week)
            X_return['cos_dia_semana'] = np.cos(2*np.pi*X.columna_dia_semana/days_in_week)
            return np.array(X_return)
        
        else:
            dias_num = {'Lunes':1, 'Martes': 2, 'Miercoles': 3 , 'Jueves': 4, 'Viernes': 5, 'Sabado': 6, 'Domingo': 7}
            X_return[columna_dia_semana] = X.DIANOM.map(dias_num)

            X_return['sin_dia_semana'] = np.sin(2*np.pi*X_return.columna_dia_semana/days_in_week)
            X_return['cos_dia_semana'] = np.cos(2*np.pi*X_return.columna_dia_semana/days_in_week)
            return np.array(X_return.drop(columns = [columna_dia_semana]))
        


class OptimizeDf(BaseEstimator, TransformerMixin):
    def __init__(self):
        '''
        Downcast the data continously in the pipeline.
        Recommended to use after a ColumnTransformer
        '''
        pass
    def transform(self, X, y=None):
        X_ = pd.DataFrame(X)
        return np.array(df_optimized(X_))
    def fit(self, X, y=None):
        return self