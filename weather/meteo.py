import requests
from .BOT import WarningMessage
import json

def update():
    url=costruzione_richiesta()
    response = requests.get(url)
    json_result = response.json()
    print(json_result['daily']['weather_code'])
    if json_result['daily']['weather_code'][4]==63:WarningMessage()
    return json_result["daily"]["weather_code"],json_result["daily"]["time"]

def richiesta_meteo():
    url=costruzione_richiesta()
    response = requests.get(url)
    json_result = response.json()
    codici=traduzione_codici_meteo(json_result["daily"]["weather_code"])
    pacco=[]
    for i in range(7):
        pacco.append({"codice":codici[i],\
                      "data":json_result["daily"]["time"][i],\
                        "TempMax":json_result["daily"]["temperature_2m_max"][i],\
                        "TempMin":json_result["daily"]["temperature_2m_min"][i]})
    return pacco

def RichiestaPerModello():
    url=costruzione_richiesta()
    response = requests.get(url)
    json_result = response.json()
    return json_result['daily']

def traduzione_codici_meteo(WC):
    prevision=[]
    for i in WC:
        match i:
            case 0:
                prevision.append("http://openweathermap.org/img/wn/01d@2x.png")
            case 1|2|3:
                prevision.append("http://openweathermap.org/img/wn/02d@2x.png")
            case 45|48:
                prevision.append("http://openweathermap.org/img/wn/50d@2x.png")
            case 61|63|65:
                prevision.append("http://openweathermap.org/img/wn/10d@2x.png")    
            case 66|67:
                prevision.append("http://openweathermap.org/img/wn/13d@2x.png") 
            case 71|73|75:
                prevision.append("http://openweathermap.org/img/wn/13d@2x.png") 
            case 77:
                prevision.append("http://openweathermap.org/img/wn/13d@2x.png")
            case 80|81|82:
                prevision.append("http://openweathermap.org/img/wn/10d@2x.png")
            case 85|86:
                prevision.append("http://openweathermap.org/img/wn/10d@2x.png")
            case 95:
                prevision.append("http://openweathermap.org/img/wn/11d@2x.png")
            case 96|99:
                prevision.append("http://openweathermap.org/img/wn/11d@2x.png")
    return prevision

def costruzione_richiesta():
    lat,lon=get_position()
    start="https://api.open-meteo.com/v1/forecast?"
    position="latitude="+str(lat)+"&longitude="+str(lon)
    var_meteo=variabili_meteo()
    zona=TimeZone()
    giorni=Days()
    url=start+position+"&"+var_meteo+"&"+zona+"&"+giorni
    return url

def variabili_meteo():
    stringa="daily=weather_code,temperature_2m_max,temperature_2m_min,daylight_duration,wind_speed_10m_max,wind_gusts_10m_max,wind_direction_10m_dominant,et0_fao_evapotranspiration,rain_sum,precipitation_sum,showers_sum"
    return stringa
def TimeZone():
    return "timezone=Europe"+'%'+"2FBerlin"
def Days():
    return "past_days=3&forecast_days=4"#past_days=3&
def get_position():
    return 44.64,10.99

def spacchettamento(date):
    anni=[]
    mesi=[]
    giorni=[]
    for i in date:
        anni.append(i[0:4])
        mesi.append(i[5:7])
        giorni.append(i[8:10])
        

    return anni,mesi,giorni