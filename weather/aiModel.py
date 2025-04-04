import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import joblib
import os
from django.conf import settings
import requests

from .meteo import costruzione_richiesta

class WeatherModel:
    
    precipitation_model = LinearRegression()
    plant_data = None 

    def __init__(self):
        self.model = joblib.load(os.path.join(settings.BASE_DIR, 'weather/static/model_params/model.pkl'))
        self.plant_data = pd.read_csv(os.path.join(settings.BASE_DIR, 'weather/static/PLANT_DATASET.csv')).dropna()
    
    def build_df(self, lat, lon):

        #query apy for next 3 days forecast (today included)
        param = "&daily=rain_sum,weather_code,temperature_2m_max,wind_speed_10m_max,precipitation_sum,daylight_duration,temperature_2m_min,wind_gusts_10m_max,et0_fao_evapotranspiration,showers_sum,wind_direction_10m_dominant"

        url = 'https://api.open-meteo.com/v1/forecast?latitude={}&longitude={}&daily=rain_sum,weather_code,temperature_2m_max,wind_speed_10m_max,precipitation_sum,daylight_duration,temperature_2m_min,wind_gusts_10m_max,et0_fao_evapotranspiration,showers_sum,wind_direction_10m_dominant&timezone=Europe%2FBerlin&forecast_days=4'.format(lat, lon)
        response = requests.get(url)
        json_result = response.json()

        df_api = pd.DataFrame()

        df_api['rain_sum']=json_result["daily"]["rain_sum"]
        df_api['weather_code']=json_result["daily"]["weather_code"]
        df_api['temperature_2m_max']=json_result["daily"]["temperature_2m_max"]
        df_api['wind_speed_10m_max']=json_result["daily"]["wind_speed_10m_max"]
        df_api['precipitation_sum']=json_result["daily"]["precipitation_sum"]
        df_api['daylight_duration']=json_result["daily"]["daylight_duration"]
        df_api['temperature_2m_min']=json_result["daily"]["temperature_2m_min"]
        df_api['wind_gusts_10m_max']=json_result["daily"]["wind_gusts_10m_max"]
        df_api['et0_fao_evapotranspiration']=json_result["daily"]["et0_fao_evapotranspiration"]
        df_api['showers_sum']=json_result["daily"]["showers_sum"]
        df_api['wind_direction_10m_dominant']=json_result["daily"]["wind_direction_10m_dominant"]
        df_api['PRED_DIST']=[0,1,2,3]

        return df_api

    
    def get_accurate_predictions(self, cropType="CABBAGE", lat=44.6478, lon=10.9254):

        df_api = self.build_df(lat, lon)

        weather_data = np.array(df_api)

        preds = self.model.predict(weather_data)
        predSum = 0

        for pred in preds:
            predSum += pred

        self.get_water_needs(cropType, lat, lon)

        return predSum #return the sum of precipitation for the next 4 days (today included)


    def get_water_needs(self, cropType="CABBAGE", lat=44.6478, lon=10.9254):

        #CROP TYPES: ['BANANA' 'SOYABEAN' 'CABBAGE' 'POTATO' 'RICE' 'MELON' 'MAIZE' 'CITRUS' 'BEAN' 'WHEAT' 'MUSTARD' 'COTTON' 'SUGARCANE' 'TOMATO' 'ONION']

        soilType = None # => from the sensor ['DRY' 'HUMID' 'WET']
        weatherCondition = None #['NORMAL' 'SUNNY' 'WINDY' 'RAINY']
        region = 'SEMI HUMID' #['DESERT' 'SEMI ARID' 'SEMI HUMID' 'HUMID']
        temperature = None # will be binned week average ['10-20' '20-30' '30-40' '40-50']

        WATER_REQUIREMENT_AVG = np.mean(self.plant_data['WATER REQUIREMENT'])

        #print(self.plant_data[(self.plant_data['CROP TYPE'] == 'POTATO') & (self.plant_data['WEATHER CONDITION'] == 'NORMAL')])
