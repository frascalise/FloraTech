import json
import random
from django.shortcuts import render, redirect
from accounts.models import *
from django.contrib.auth.decorators import login_required
from accounts.views import get_weather_forecast
from django.http import JsonResponse

def welcome_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    return render(request, "welcome/welcome.html")

@login_required
def home_view(request):
    weather_data = get_weather_forecast(request)
    return render(request, "home/home.html", {"weather": weather_data})

@login_required
def garden_view(request):
    return render(request, "garden/garden.html")

#** -------------------------------- API -------------------------------- **#

# For testing purposes only
# Add a raspberry to the database
def api_test(request):
    data = {
        'username': 'frascalise',
        'raspberry_id': random.randint(1, 100),
        'label': 'RASPBERRY TEST',
    }

    # Adding raspberry to database
    raspberry = Raspberry.objects.create(id=data['raspberry_id'], fk_owner=data['username'], label=data['label'])
    raspberry.save()
    
    return render(request, 'api/api.html', {'data': data})

# For testing purposes only
# Show all the data
def show_all(request):
    raspberry = Raspberry.objects.all()
    garden = Garden.objects.all()
    sensor = Sensor.objects.all()
    weather = Weather.objects.all()

    data = {
        'raspberry': Raspberry,
        'garden': Garden,
        'sensor': Sensor,
        'weather': Weather,
    }
    return render(request, 'api/api.html', {'data': data})
    

# The sensor is working!
# Sensor status is 'working'
def sensor_working(request, raspberry_id, sensor_id):
    data = {
        'raspberry_id': raspberry_id,
        'sensor_id': sensor_id,
        'status': 'working',
    }

    return render(request, 'api/api.html', {'data': data})

# The sensor is not working!
# Sensor status is in warning_message
def sensor_warning(request, raspberry_id, sensor_id, warning_message):
    data = {
        'raspberry_id': raspberry_id,
        'sensor_id': sensor_id,
        'warning_message': warning_message,
    }

    return render(request, 'api/api.html', {'data': data})

# Check if sensor is in the right garden and everything is ok
# Faccio delle query e in teoria devo restituire quello che c'è nella lista di json che mi è stato mandato
# (se tutto coincide allora ok)
def check_sensor(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        data = [
                    {'id': 1, 'role': 'sensor', 'last_ping': '2025-04-03 11:08:55.570102', 'garden': 0},
                    {'id': 2, 'role': 'sensor', 'last_ping': '2025-04-03 11:10:36.912720', 'garden': 0},
                    {'id': 3, 'role': 'sensor', 'last_ping': '2025-04-03 11:56:05.367690', 'garden': 0},
                    {'id': 4, 'role': 'sensor', 'last_ping': '2025-04-03 12:00:49.042357', 'garden': 0},
                ]
    else:
        data = [
                    {'id': 1, 'role': 'sensor', 'last_ping': '2025-04-03 11:08:55.570102', 'garden': 0},
                    {'id': 2, 'role': 'sensor', 'last_ping': '2025-04-03 11:10:36.912720', 'garden': 0},
                    {'id': 3, 'role': 'sensor', 'last_ping': '2025-04-03 11:56:05.367690', 'garden': 0},
                    {'id': 4, 'role': 'sensor', 'last_ping': '2025-04-03 12:00:49.042357', 'garden': 0},
                ]
    
    return render(request, 'api/api.html', {'data': data})

# Add a new sensor to the database
def new_sensor(request, raspberry_id):
    if request.method == 'POST':
        data = json.loads(request.body)
        data = {'id': 1, 'role': 'sensor', 'last_ping': '2025-04-03 11:08:55.570102', 'garden': 0}
    else:
        data = {'id': 1, 'role': 'sensor', 'last_ping': '2025-04-03 11:08:55.570102', 'garden': 0}

    # Aggiunta del sensore al giardino

    return render(request, 'api/api.html', {'data': data})

# Add garden to a sensor
def add_garden(request, raspberry_id):
    if request.method == 'POST':
        data = json.loads(request.body)
        data = {'id': 1, 'role': 'sensor', 'last_ping': '2025-04-03 11:08:55.570102', 'garden': 0}
    else:
        data = {'id': 1, 'role': 'sensor', 'last_ping': '2025-04-03 11:08:55.570102', 'garden': 0}

    response = {'raspberry_id': raspberry_id, 'sensor_id': 1, 'garden': 2} # Aggiunta del giardino al sensore
    return render(request, 'api/api.html', {'data': response})
