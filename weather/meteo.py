import requests
import json

def richiesta_meteo():
    url=costruzione_richiesta()
    response = requests.get(url)
    json_result = response.json()
    answer = ""
    print(json_result)
    return traduzione_codici_meteo(json_result["daily"]["weather_code"]),json_result["daily"]["time"]

   

def traduzione_codici_meteo(WC):
    prevision=[]
    for i in WC:
        print(i)
        match i:
            case 0:
                prevision.append("clear sky")
            case 1|2|3:
                prevision.append("presence of clouds")
            case 45|48:
                prevision.append("Fog")
            case 61|63|65:
                prevision.append("Rain")    
            case 66|67:
                prevision.append("Freezing Rain") 
            case 71|73|75:
                prevision.append("Neve") 
            case 77:
                prevision.append("Nevischio")
            case 80|81|82:
                prevision.append("Rovesci di pioggia")
            case 85|86:
                prevision.append("Nevicata")
            case 95:
                prevision.append("Temporale")
            case 96|99:
                prevision.append("Temporale con grandine")
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
    stringa="daily=weather_code,temperature_2m_max,temperature_2m_min,precipitation_sum,precipitation_probability_max"
    return stringa
def TimeZone():
    return "timezone=Europe"+'%'+"2FBerlin"
def Days():
    return "past_days=3&forecast_days=4"
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