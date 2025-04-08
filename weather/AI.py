import pandas as pd
import sklearn as sk
from sklearn.preprocessing import MaxAbsScaler
from sklearn.model_selection import train_test_split
from sklearn import svm
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import GridSearchCV
import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_absolute_error, mean_squared_error, mean_squared_log_error

model = LinearRegression()
def StartingTraining():
    #creazione dataset
    week1_df = pd.read_csv("csv_data\data_union_from14to21_032025.csv",sep=",")
    week2_df = pd.read_csv("csv_data\data_union_from21to27_032025.csv",sep=',')
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
    #preparazione training e test set

    X = np.array(dataset)
    Y = target.values
    X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.15, random_state=42)
    #creazione modelli


    LinReg = LinearRegression()
    parameters = {"fit_intercept": [True, False], 
        "copy_X": [True, False],
        "positive": [True, False],
             }
    grid = GridSearchCV(estimator=LinReg, param_grid = parameters)
    grid.fit(X_train, y_train)

    OptLinReg = LinearRegression(copy_X=True, fit_intercept=False, positive=True)

    OptLinReg.fit(X_train, y_train)



    RFReg = RandomForestRegressor()
    parameters = {"n_estimators": [25, 50, 100, 125],
        "criterion": ['squared_error', 'absolute_error', 'friedman_mse', 'poisson'],
        "max_depth": [2,3,4],
        "max_features": ['sqrt', 'log2'],
        "warm_start": [True,False],
             }
    grid = GridSearchCV(estimator=RFReg, param_grid = parameters)
    grid.fit(X_train, y_train)


    grid.best_params_

    OptRFReg = RandomForestRegressor(criterion='absolute_error',max_depth=3,max_features="log2",n_estimators=50,warm_start=True)

    OptRFReg.fit(X_train, y_train)


    SVMReg = svm.SVR()
    parameters = {
        "degree": [2, 3, 4],
        "gamma": ['scale', 'auto'],
        "coef0": [0,0.1,0.25],
        "tol": [0.001, 0.01,0.1],
        "C": [1, 10, 5],
        "epsilon": [0.1, 0.2, 0.25, 0.08],
             }
    grid = GridSearchCV(estimator=SVMReg, param_grid = parameters)
    grid.fit(X_train, y_train)

    OptSVMReg = svm.SVR(C=10,coef0=0,degree=2,epsilon=0.25,gamma="scale",tol=0.1)

    OptSVMReg.fit(X_train, y_train)

    model=OptLinReg


def Prediction(data):
    model.predict(data)