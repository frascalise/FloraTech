from django.shortcuts import render
import requests
from .models import Previsione
from django.http import HttpResponse
from django.views.generic.detail import DetailView 
from django.views.generic.list import ListView
from .meteo import richiesta_meteo
from .aiModel import WeatherModel
from .AI import Prediction,StartingTraining

weatherModel = WeatherModel()


def nextPrecipitationSum(request):
    predSum = weatherModel.get_daily_water_predictions(garden_id=2)

    if predSum <= 0:
        return HttpResponse("NO NEED TO WATER TODAY")
    
    else:
        return HttpResponse(predSum)

class PrevisionDetail(DetailView):
    model = Previsione
    template_name = 'meteo.html'
    
    def forecast():
        return 0

def home(request):
    return HttpResponse("hola" + str(request.user))

def refresh(request):
    Previsione.refresh()
    return HttpResponse("fatto")
def fornire(request):
    print(Previsione.stampa())
    return HttpResponse("Domani sarà bello")
def chiamata(request):
    risultato=Prediction()
    context={'valori':risultato}
    return render(request,"acqua.html",context)