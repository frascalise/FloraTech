from django.shortcuts import render
import requests
from .models import Previsione
from django.http import HttpResponse
from django.views.generic.detail import DetailView 
from django.views.generic.list import ListView
from .meteo import richiesta_meteo
from .aiModel import WeatherModel

weatherModel = WeatherModel()


def nextPrecipitationSum(request):
    predSum = weatherModel.get_accurate_predictions(garden_id=1, sensor_id=1)

    return HttpResponse(predSum)



class PrevisionDetail(DetailView):
    model = Previsione
    template_name = 'meteo.html'
    
    def forecast():
        return 0
    
def LookForecast(request):
    previsioni = Previsione.objects.all()  # recupera tutte le righe della tabella
    context = {
        "previsioni": previsioni
    }
    return render(request, "meteo.html", context)  

def home(request):
    return HttpResponse("hola" + str(request.user))

def refresh(request):
    Previsione.refresh()
    return HttpResponse("fatto")
def fornire(request):
    Previsione.stampa()
    return HttpResponse("Domani sarà bello")