from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from accounts.views import get_weather_forecast
from weather.meteo import richiesta_meteo

def welcome_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    return render(request, "welcome/welcome.html")

@login_required
def home_view(request):
    weather_data = richiesta_meteo()
    return render(request, "home/home.html", {"weather": weather_data})

@login_required
def garden_view(request):
    return render(request, "garden/garden.html")
