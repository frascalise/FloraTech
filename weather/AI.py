import pandas as pd
import numpy as np
import sklearn as sk
import joblib
from .meteo import RichiestaPerModello
from sklearn.preprocessing import MaxAbsScaler
from sklearn.model_selection import train_test_split
from sklearn import svm
from sklearn.linear_model import SGDRegressor
from sklearn.model_selection import GridSearchCV
import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_absolute_error, mean_squared_error, mean_squared_log_error

def StartingTraining():
    #creazione dataset
    week1_df = pd.read_csv("weather/csv_data\data_union_from14to21_032025.csv",sep=",")
    week2_df = pd.read_csv("weather/csv_data\data_union_from21to27_032025.csv",sep=',')
    dataset = pd.concat([week1_df, week2_df], axis=0)

    columns = dataset.columns

    target_attribute = 'precipitation_sum_effettivo'

    target = dataset[[target_attribute]]

    columns = columns.drop([ target_attribute, 'time', 'showers_sum_effettivo', 
                        'wind_direction_10m_dominant_effettivo', 
                        'wind_gusts_10m_max_effettivo', 
                        'daylight_duration_effettivo',
                        'et0_fao_evapotranspiration_effettivo',
                        'location_id',
                        'temperature_2m_max_effettivo', 'temperature_2m_min_effettivo',
                        'wind_speed_10m_max_effettivo', 'rain_sum_effettivo', 'time.1', 'location_id_effettivo', 'weather_code_effettivo'])


    dataset = dataset[columns]
    dataset['PREV_DIST'] = [i % 7 for i in range(len(dataset))]

    mas = MaxAbsScaler()
    new_dataset_transf = mas.fit_transform(dataset)
    new_dataset_transf = pd.DataFrame(new_dataset_transf, columns=dataset.columns)

    dataset = new_dataset_transf
    dataset = dataset[['weather_code',"temperature_2m_max","temperature_2m_min","daylight_duration","wind_speed_10m_max","wind_gusts_10m_max","wind_direction_10m_dominant","et0_fao_evapotranspiration","rain_sum","precipitation_sum","showers_sum",'PREV_DIST']]
    #preparazione training e test set

    X = dataset
    Y = target
    X_train,X_test,Y_train,Y_test=train_test_split(X,Y,test_size=0.25,random_state=42)

    model= SGDRegressor()
    parameter={
        'alpha': [0.0001, 0.001, 0.01, 0.1],  # Parametro di regolarizzazione
        'max_iter': [1000, 2000, 5000],  # Numero massimo di iterazioni
        'tol': [1e-4, 1e-3],  # Tolleranza per la convergenza
        'learning_rate': ['constant', 'optimal', 'invscaling', 'adaptive']
    }
    grid=GridSearchCV(estimator=model,param_grid=parameter)
    grid.fit(X_train,Y_train)

    model=grid.best_estimator_
    model.fit(X_train,Y_train)
    print(model.predict(X_test))
    joblib.dump(model,'model_parameters.pkl')


def Prediction():
    model=joblib.load('model_parameters.pkl')
    previsioni=RichiestaPerModello()
    previsioni['PREV_DIST']=[i%7 for i in range(7)]
    previsioni=RielaborazionePrevisione(previsioni)
   
    risultato=model.predict(previsioni)
    model.partial_fit(previsioni,risultato)
    joblib.dump(model,'model_parameters.pkl')
    return risultato.round(2)
    
def RielaborazionePrevisione(data):
    result=pd.DataFrame(data)
    result=result.drop('time',axis=1)
    max=MaxAbsScaler()
    result=max.fit_transform(result)
    return result