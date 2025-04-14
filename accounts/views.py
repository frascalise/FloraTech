#import openmeteo_requests
#import requests_cache
import requests
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
#from retry_requests import retry
from django.http import JsonResponse

import telebot
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Telegram

weather_icons = {      
    "0":{
        "day":{
            "description":"Sunny",
            "image":"http://openweathermap.org/img/wn/01d@2x.png"
        },
        "night":{
            "description":"Clear",
            "image":"http://openweathermap.org/img/wn/01n@2x.png"
        }
    },
    "1":{
        "day":{
            "description":"Mainly Sunny",
            "image":"http://openweathermap.org/img/wn/01d@2x.png"
        },
        "night":{
            "description":"Mainly Clear",
            "image":"http://openweathermap.org/img/wn/01n@2x.png"
        }
    },
    "2":{
        "day":{
            "description":"Partly Cloudy",
            "image":"http://openweathermap.org/img/wn/02d@2x.png"
        },
        "night":{
            "description":"Partly Cloudy",
            "image":"http://openweathermap.org/img/wn/02n@2x.png"
        }
    },
    "3":{
        "day":{
            "description":"Cloudy",
            "image":"http://openweathermap.org/img/wn/03d@2x.png"
        },
        "night":{
            "description":"Cloudy",
            "image":"http://openweathermap.org/img/wn/03n@2x.png"
        }
    },
    "45":{
        "day":{
            "description":"Foggy",
            "image":"http://openweathermap.org/img/wn/50d@2x.png"
        },
        "night":{
            "description":"Foggy",
            "image":"http://openweathermap.org/img/wn/50n@2x.png"
        }
    },
    "48":{
        "day":{
            "description":"Rime Fog",
            "image":"http://openweathermap.org/img/wn/50d@2x.png"
        },
        "night":{
            "description":"Rime Fog",
            "image":"http://openweathermap.org/img/wn/50n@2x.png"
        }
    },
    "51":{
        "day":{
            "description":"Light Drizzle",
            "image":"http://openweathermap.org/img/wn/09d@2x.png"
        },
        "night":{
            "description":"Light Drizzle",
            "image":"http://openweathermap.org/img/wn/09n@2x.png"
        }
    },
    "53":{
        "day":{
            "description":"Drizzle",
            "image":"http://openweathermap.org/img/wn/09d@2x.png"
        },
        "night":{
            "description":"Drizzle",
            "image":"http://openweathermap.org/img/wn/09n@2x.png"
        }
    },
    "55":{
        "day":{
            "description":"Heavy Drizzle",
            "image":"http://openweathermap.org/img/wn/09d@2x.png"
        },
        "night":{
            "description":"Heavy Drizzle",
            "image":"http://openweathermap.org/img/wn/09n@2x.png"
        }
    },
    "56":{
        "day":{
            "description":"Light Freezing Drizzle",
            "image":"http://openweathermap.org/img/wn/09d@2x.png"
        },
        "night":{
            "description":"Light Freezing Drizzle",
            "image":"http://openweathermap.org/img/wn/09n@2x.png"
        }
    },
    "57":{
        "day":{
            "description":"Freezing Drizzle",
            "image":"http://openweathermap.org/img/wn/09d@2x.png"
        },
        "night":{
            "description":"Freezing Drizzle",
            "image":"http://openweathermap.org/img/wn/09n@2x.png"
        }
    },
    "61":{
        "day":{
            "description":"Light Rain",
            "image":"http://openweathermap.org/img/wn/10d@2x.png"
        },
        "night":{
            "description":"Light Rain",
            "image":"http://openweathermap.org/img/wn/10n@2x.png"
        }
    },
    "63":{
        "day":{
            "description":"Rain",
            "image":"http://openweathermap.org/img/wn/10d@2x.png"
        },
        "night":{
            "description":"Rain",
            "image":"http://openweathermap.org/img/wn/10n@2x.png"
        }
    },
    "65":{
        "day":{
            "description":"Heavy Rain",
            "image":"http://openweathermap.org/img/wn/10d@2x.png"
        },
        "night":{
            "description":"Heavy Rain",
            "image":"http://openweathermap.org/img/wn/10n@2x.png"
        }
    },
    "66":{
        "day":{
            "description":"Light Freezing Rain",
            "image":"http://openweathermap.org/img/wn/10d@2x.png"
        },
        "night":{
            "description":"Light Freezing Rain",
            "image":"http://openweathermap.org/img/wn/10n@2x.png"
        }
    },
    "67":{
        "day":{
            "description":"Freezing Rain",
            "image":"http://openweathermap.org/img/wn/10d@2x.png"
        },
        "night":{
            "description":"Freezing Rain",
            "image":"http://openweathermap.org/img/wn/10n@2x.png"
        }
    },
    "71":{
        "day":{
            "description":"Light Snow",
            "image":"http://openweathermap.org/img/wn/13d@2x.png"
        },
        "night":{
            "description":"Light Snow",
            "image":"http://openweathermap.org/img/wn/13n@2x.png"
        }
    },
    "73":{
        "day":{
            "description":"Snow",
            "image":"http://openweathermap.org/img/wn/13d@2x.png"
        },
        "night":{
            "description":"Snow",
            "image":"http://openweathermap.org/img/wn/13n@2x.png"
        }
    },
    "75":{
        "day":{
            "description":"Heavy Snow",
            "image":"http://openweathermap.org/img/wn/13d@2x.png"
        },
        "night":{
            "description":"Heavy Snow",
            "image":"http://openweathermap.org/img/wn/13n@2x.png"
        }
    },
    "77":{
        "day":{
            "description":"Snow Grains",
            "image":"http://openweathermap.org/img/wn/13d@2x.png"
        },
        "night":{
            "description":"Snow Grains",
            "image":"http://openweathermap.org/img/wn/13n@2x.png"
        }
    },
    "80":{
        "day":{
            "description":"Light Showers",
            "image":"http://openweathermap.org/img/wn/09d@2x.png"
        },
        "night":{
            "description":"Light Showers",
            "image":"http://openweathermap.org/img/wn/09n@2x.png"
        }
    },
    "81":{
        "day":{
            "description":"Showers",
            "image":"http://openweathermap.org/img/wn/09d@2x.png"
        },
        "night":{
            "description":"Showers",
            "image":"http://openweathermap.org/img/wn/09n@2x.png"
        }
    },
    "82":{
        "day":{
            "description":"Heavy Showers",
            "image":"http://openweathermap.org/img/wn/09d@2x.png"
        },
        "night":{
            "description":"Heavy Showers",
            "image":"http://openweathermap.org/img/wn/09n@2x.png"
        }
    },
    "85":{
        "day":{
            "description":"Light Snow Showers",
            "image":"http://openweathermap.org/img/wn/13d@2x.png"
        },
        "night":{
            "description":"Light Snow Showers",
            "image":"http://openweathermap.org/img/wn/13n@2x.png"
        }
    },
    "86":{
        "day":{
            "description":"Snow Showers",
            "image":"http://openweathermap.org/img/wn/13d@2x.png"
        },
        "night":{
            "description":"Snow Showers",
            "image":"http://openweathermap.org/img/wn/13n@2x.png"
        }
    },
    "95":{
        "day":{
            "description":"Thunderstorm",
            "image":"http://openweathermap.org/img/wn/11d@2x.png"
        },
        "night":{
            "description":"Thunderstorm",
            "image":"http://openweathermap.org/img/wn/11n@2x.png"
        }
    },
    "96":{
        "day":{
            "description":"Light Thunderstorms With Hail",
            "image":"http://openweathermap.org/img/wn/11d@2x.png"
        },
        "night":{
            "description":"Light Thunderstorms With Hail",
            "image":"http://openweathermap.org/img/wn/11n@2x.png"
        }
    },
    "99":{
        "day":{
            "description":"Thunderstorm With Hail",
            "image":"http://openweathermap.org/img/wn/11d@2x.png"
        },
        "night":{
            "description":"Thunderstorm With Hail",
            "image":"http://openweathermap.org/img/wn/11n@2x.png"
        }
    }
}

def get_weather_forecast(request):
    latitude = 44.698993
    longitude = 10.629686
    
    url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&daily=weather_code,temperature_2m_min,temperature_2m_max&timezone=Europe/Rome"

    try:
        response = requests.get(url)
        data = response.json()
        
        # Estrarre temperature minime e massime
        forecast = []
        dates = data["daily"]["time"]
        temp_min = data["daily"]["temperature_2m_min"]
        temp_max = data["daily"]["temperature_2m_max"]
        weather_codes = data["daily"]["weather_code"]

        for i in range(len(dates)):
            forecast.append({
                "date": dates[i],
                "temp_min": temp_min[i],
                "temp_max": temp_max[i],
                "weather_code": weather_icons.get(str(weather_codes), {"day": {"image": ""}})
            })

        return forecast
    
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


def register_view(request):
    err_pres=[]
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            print("vaffa")
            return redirect("home")
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    err_pres.append(error)
            
    else:
        form = UserCreationForm()
    return render(request, "accounts/register/register.html", {"form": form,'err_pres':len(err_pres),'err':err_pres})

def login_view(request):
    err_pres=[]
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("home")
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    err_pres.append(error)
    else:
        form = AuthenticationForm()
    return render(request, "accounts/login/login.html", {"form": form,'err_pres':len(err_pres),'err':err_pres})

def logout_view(request):
    logout(request)
    return redirect("welcome")


'''telegram'''
TOKEN = '7789512707:AAFdHTHgdALOO745NlUPHftmClXrRBUMzjo'
WEBHOOK_URL = 'https://floratech.leonardonels.com/accounts'
USER_ID=903195749 

# Inizializza il bot Telegram
bot = telebot.TeleBot(TOKEN)

# Handler per il comando /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Ciao! Sono un bot webhook Django di prova.")
    print(message.chat.id)

# Handler per il comando /help
@bot.message_handler(commands=['help'])
def send_help(message):
    bot.reply_to(message, "Questo è un bot di prova basato su webhook con Django.")


def WarningMessage():
    bot.send_message(USER_ID,'Sta per splodere tutto')
    print('qualcosa')
@bot.message_handler(commands=['new'])
def AddNewUser(message):
    #user.AddNewUser(message.chat.id)
    bot.send_message(USER_ID,'Aggiunto nuovo utente')

# View Django per gestire gli aggiornamenti del webhook
@csrf_exempt #da mettere ASSOLUTAMENTE in caso di collegamenti con il file url
def webhook_view(request):
    if request.method == 'POST':
        try:
            json_string = request.body.decode('utf-8')
            update = telebot.types.Update.de_json(json_string)
            bot.process_new_updates([update])
            return HttpResponse(status=200)
        except Exception as e:
            print(f"Errore durante la ricezione del webhook: {e}")
            return HttpResponse(status=500)
    else:
        return HttpResponse('OK', status=200)

# Funzione per impostare il webhook (da eseguire una sola volta o tramite un comando Django custom)
def set_webhook(request):
    bot.set_webhook(url=f"{WEBHOOK_URL}/{TOKEN}/")
    print(f"Webhook impostato su: {WEBHOOK_URL}/{TOKEN}")
    return HttpResponse(status=200)

# Funzione per eliminare il webhook (utile per passare al polling o per debug)
def delete_webhook():
    bot.delete_webhook()
    print("Webhook eliminato.")
