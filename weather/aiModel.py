import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import joblib
import os
from django.conf import settings
import requests

from .meteo import costruzione_richiesta
from accounts.models import Garden, Sensor

class WeatherModel:
    
    precipitation_model = LinearRegression()
    plant_data = None 

    def __init__(self):
        self.model = joblib.load(os.path.join(settings.BASE_DIR, 'weather/static/model_params/model.pkl'))
        self.plant_data = pd.read_csv(os.path.join(settings.BASE_DIR, 'weather/static/PLANT_DATASET.csv')).dropna()
    
    def build_df(self, lat, lon):
        """
        Costruisce e ritorna il dataframe con le previsioni meteo per i prossimi 4 giorni (oggi incluso)
        """

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

    
    def get_daily_water_predictions(self, garden_id, lat=44.6478, lon=10.9254):

        df_api = self.build_df(lat, lon)

        weather_data = np.array(df_api)

        preds = self.model.predict(weather_data)
        predictedPrecipitationsSum = 0

        for pred in preds:
            predictedPrecipitationsSum += pred

        groundWater = self.get_ground_water(garden_id)

        #if realPrecipitationsSum > const and get_ground_water() = 0 -> consudero realPrecipitationsSum=0
        realPrecipitationsSum, TmaxSum, TminSum = self.get_past_weater_data(lat, lon)

        if realPrecipitationsSum > 2 and groundWater == 0:
            ## inventati un controllo migliore per verificare che al giardino arrivi l'acqua
            realPrecipitationsSum = 0
            predictedPrecipitationsSum = 0

        TWeekMaxAvg=(TmaxSum + sum(df_api["temperature_2m_max"]))/7
        TWeekMinAvg=(TminSum + sum(df_api["temperature_2m_min"]))/7


        weeklyWaterNeeds = self.get_water_needs(garden_id, TWeekMaxAvg, TWeekMinAvg)

        waterErogated = self.get_water_erogated(garden_id)
        
        return weeklyWaterNeeds - predictedPrecipitationsSum - realPrecipitationsSum - waterErogated - groundWater
    
    
    def get_past_weater_data(self, lat, lon):
        """
        Ritorna la somma delle precipitazioni effettivamente ricevute gli scorsi 3 giorni
        """
        param = "daily=precipitation_sum,temperature_2m_max,temperature_2m_min"

        url = 'https://api.open-meteo.com/v1/forecast?latitude={}&longitude={}&daily=precipitation_sum,temperature_2m_max,temperature_2m_min&timezone=Europe%2FBerlin&past_days=3&forecast_days=0'.format(lat, lon)
        response = requests.get(url)
        json_result = response.json()

        return [sum(json_result["daily"]["precipitation_sum"]), sum(json_result["daily"]["temperature_2m_max"]), sum(json_result["daily"]["temperature_2m_min"])]
    
    def get_water_erogated(self, garden_id):
        """
        Ritorna l'acqua erogata artificialmente gli scorsi 3 giorni
        """
        garden = Garden.objects.get(id=garden_id)

        water = 0
        #for telem in garden.water:
        #    water += telem['value']
#
        #water = water/len(garden.water)

        return water

    def get_ground_water(self, garden_id):
        """
        Ritorna una stima dell'acqua presente nel terreno a partire dai dati nel sensore
        """
        garden = Garden.objects.get(id=garden_id)
        moisture = 0

        for telem in garden.moisture:
            moisture += telem['value']

        moisture = moisture/len(garden.moisture)

        #IMPORTANT convert the moisture measurement to the right unit!!!

        constantDepth = 10 #(mm)

        groundWater = moisture/100 * constantDepth
        
        return groundWater


    def get_water_needs(self, garden_id, Tmax, Tmin):
        """
        Ritorna una media del fabbisogno idrico settimanale della culture contenute nell'orto identificato dal garden_id
        """

        #CROP TYPES: ['BANANA' 'SOYABEAN' 'CABBAGE' 'POTATO' 'RICE' 'MELON' 'MAIZE' 'CITRUS' 'BEAN' 'WHEAT' 'MUSTARD' 'COTTON' 'SUGARCANE' 'TOMATO' 'ONION']
        
        soilType = 'HUMID' # => from the sensor ['DRY' 'HUMID' 'WET']
        weatherCondition = 'NORMAL' #['NORMAL' 'SUNNY' 'WINDY' 'RAINY']
        region = 'SEMI HUMID' #['DESERT' 'SEMI ARID' 'SEMI HUMID' 'HUMID']
        binnedTemperature = [] # will be binned week average ['10-20' '20-30' '30-40' '40-50']

        WATER_REQUIREMENT_AVG = np.mean(self.plant_data['WATER REQUIREMENT'])

        garden = Garden.objects.get(id=garden_id)

        crops = [entry['type'] for entry in garden.plants]

        for temperature in [Tmax, Tmin]:
            if temperature < 20:
                binnedTemperature.append('10-20')
            elif 20 <= temperature < 30:
                binnedTemperature.append('20-30')
            elif 30 <= temperature < 40:
                binnedTemperature.append('30-40')
            else:
                binnedTemperature.append('40-50')

        if not crops:
            crops = ['BANANA', 'SOYABEAN', 'CABBAGE', 'POTATO', 'RICE', 'MELON', 'MAIZE', 'CITRUS', 'BEAN', 'WHEAT', 'MUSTARD', 'COTTON', 'SUGARCANE', 'TOMATO', 'ONION']

        wreq = np.mean(self.plant_data[
            (self.plant_data['CROP TYPE'].isin(crops)) & 
            (self.plant_data['WEATHER CONDITION'] == weatherCondition) &
            (self.plant_data['REGION'] == region) &
            (self.plant_data['SOIL TYPE'] == soilType) &
            (self.plant_data['TEMPERATURE'].isin(binnedTemperature))
            ]['WATER REQUIREMENT'].values)

        if not wreq:
            wreq = WATER_REQUIREMENT_AVG
        
        return wreq
