from sklearn.base import TransformerMixin
from sklearn.base import BaseEstimator
import pandas as pd
import numpy as np
from funciones import df_optimized



# Scalers para FECHA--> transformación a seno y coseno (CosSinMesHoraMinuto, CosSinDiaSemana)


class CosSinMesHoraMinuto(TransformerMixin,BaseEstimator):

    def __init__(self, input_col):
        
        self.input_col = input_col
        pass

    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):

        months_in_year = 12
        hours_in_day = 23
        minutes_in_hour = 60

        X_return = pd.DataFrame()

        X_return['sin_mes'] = np.sin(2*np.pi*X[self.input_col].dt.month/months_in_year)
        X_return['cos_mes'] = np.cos(2*np.pi*X[self.input_col].dt.month/months_in_year)


        X_return['sin_hora'] = np.sin(2*np.pi*X[self.input_col].dt.hour/hours_in_day)
        X_return['cos_hora'] = np.cos(2*np.pi*X[self.input_col].dt.hour/hours_in_day)

        X_return['sin_minute'] = np.sin(2*np.pi*X[self.input_col].dt.minute/minutes_in_hour)
        X_return['cos_minute'] = np.cos(2*np.pi*X[self.input_col].dt.minute/minutes_in_hour)


        return np.array(X_return)


class CosSinDiaSemana(TransformerMixin,BaseEstimator):

    def __init__(self):
        pass

    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):

        X_return = pd.DataFrame()

        days_in_week = 7


        X_return['sin_dia_semana'] = np.sin(2*np.pi*X.Dia_de_Semana/days_in_week)
        X_return['cos_dia_semana'] = np.cos(2*np.pi*X.Dia_de_Semana/days_in_week)


        return np.array(X_return)


class DegreeTransformer(TransformerMixin,BaseEstimator):

    def __init__(self, input_col):

        self.input_col = input_col
        pass

    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):

        X = pd.DataFrame(X)
        X = X.iloc[:,0]
        
        X_return = pd.DataFrame()

        X_return['sin_grade'] = np.sin(2*np.pi*X/360)
        X_return['cos_grade'] = np.cos(2*np.pi*X/360)

        return np.array(X_return)


class CosSinMesDia(TransformerMixin,BaseEstimator):

    def __init__(self, input_col):
        
        self.input_col = input_col
        pass

    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):

        months_in_year = 12
        day_in_month = 30

        X_return = pd.DataFrame()

        X_return['sin_mes'] = np.sin(2*np.pi*X[self.input_col].dt.month/months_in_year)
        X_return['cos_mes'] = np.cos(2*np.pi*X[self.input_col].dt.month/months_in_year)
        
        X_return['sin_day'] = np.sin(2*np.pi*X[self.input_col].dt.day/day_in_month)
        X_return['cos_day'] = np.cos(2*np.pi*X[self.input_col].dt.day/day_in_month)

        
        return np.array(X_return)
    
 
