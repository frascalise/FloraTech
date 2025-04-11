import json
from django.db import connection
from django.shortcuts import render, redirect
from accounts.models import *
from django.contrib.auth.decorators import login_required
from accounts.views import get_weather_forecast
from weather.meteo import richiesta_meteo

def welcome_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    return render(request, "welcome/welcome.html")

@login_required
def home_view(request):
    weather_data = get_weather_forecast(request)
    user = request.user
    user_gardens = Garden.objects.filter(fk_raspberry__fk_owner=user.username)

    gardens_data = [
        {
            "id": garden.id,
            "label": garden.label,
            "humidity": [entry['value'] for entry in garden.humidity],  
            "temperature": [entry['value'] for entry in garden.temperature]
        }
        for garden in user_gardens
    ]
    
    return render(request, "home/home.html", {"weather": weather_data, "user": user, "gardens": gardens_data})

@login_required
def garden_view(request, garden_id):
    garden = Garden.objects.get(id=garden_id)
    sensors = Sensor.objects.filter(fk_garden=garden) | Sensor.objects.filter(fk_garden__isnull=True)
    return render(request, "garden/garden.html", {"garden": garden, "sensors": sensors})

@login_required
def activate_sensor(request, sensor_id, garden_id):
    sensor = Sensor.objects.get(id=sensor_id)
    garden = Garden.objects.get(id=garden_id)

    if sensor.status == 'not working':
        sensor.status = 'working'
        sensor.fk_garden = garden
        sensor.is_associated = True
        sensor.save()

    return redirect('garden', garden_id=garden_id)

@login_required
def deactivate_sensor(request, sensor_id, garden_id):
    sensor = Sensor.objects.get(id=sensor_id)
    garden = Garden.objects.get(id=garden_id)

    if sensor.status == 'working':
        sensor.status = 'not working'
        sensor.fk_garden = None
        sensor.is_associated = False
        sensor.save()
        
    return redirect('garden', garden_id=garden_id)

#** -------------------------------- TEST API -------------------------------- **#
# For testing purposes only
# Add all the elements to the database
def setup(request):
    # Dati per il Raspberry e il Garden
    data_raspberry = {
        'username': 'frascalise',
        'label': 'RASPBERRY TEST',
    }

    data_garden = {
        'fk_raspberry': 1,  # Assicurati che questa FK punti a un Raspberry esistente
        'label': 'Garden Test',
        'humidity': [
            {'timestamp': '2023-04-03 11:08:55.570102', 'value': 50},
            {'timestamp': '2023-04-03 11:10:36.912720', 'value': 55},
            {'timestamp': '2023-04-03 11:56:05.367690', 'value': 60},
        ],
        'temperature': [
            {'timestamp': '2023-04-03 11:08:55.570102', 'value': 20},
            {'timestamp': '2023-04-03 11:10:36.912720', 'value': 25},
            {'timestamp': '2023-04-03 11:56:05.367690', 'value': 30},
        ],
        'water': [
            {'timestamp': '2023-04-03 11:08:55.570102', 'value': 100},
            {'timestamp': '2023-04-03 11:10:36.912720', 'value': 150},
            {'timestamp': '2023-04-03 11:56:05.367690', 'value': 200},
        ],
    }

    raspberry = Raspberry.objects.create(fk_owner=data_raspberry['username'], label=data_raspberry['label'])
    
    garden = Garden.objects.create(fk_raspberry=raspberry, label=data_garden['label'])
    garden.humidity = data_garden['humidity']
    garden.temperature = data_garden['temperature']
    garden.water = data_garden['water']
    garden.save()

    data_sensor = [
        {'is_associated': True, 'status': 'working', 'fk_garden': garden},
        {'is_associated': True, 'status': 'not working', 'fk_garden': garden},
        {'is_associated': True, 'status': 'working', 'fk_garden': garden},
    ]

    print("Data Sensor: ", data_sensor)

    for sensor_data in data_sensor:
        Sensor.objects.create(
            is_associated=sensor_data['is_associated'],
            status=sensor_data['status'],
            fk_garden=sensor_data['fk_garden']
        )
    
    data = {
        'raspberry_id': raspberry.id,
        'garden_id': garden.id,
        'message': 'Raspberry and garden successfully added!',
    }

    return render(request, 'api/api.html', {'data': data})

# For testing purposes only
# Show all the data
def show_all(request):
    raspberry = Raspberry.objects.all().values()
    garden = Garden.objects.all().values()
    sensor = Sensor.objects.all().values()
    weather = Weather.objects.all().values()

    data = {
        'raspberry': list(raspberry),
        'garden': list(garden),
        'sensor': list(sensor),
        'weather': list(weather),
    }

    return render(request, 'api/show_all.html', {'data': data})
    
# For testing purposes only
# Delete all the data
def delete_all(request):
    Raspberry.objects.all().delete()
    Garden.objects.all().delete()
    Sensor.objects.all().delete()
    Weather.objects.all().delete()

    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM sqlite_sequence WHERE name='accounts_raspberry'")
        cursor.execute("DELETE FROM sqlite_sequence WHERE name='accounts_garden'")
        cursor.execute("DELETE FROM sqlite_sequence WHERE name='accounts_sensor'")
        cursor.execute("DELETE FROM sqlite_sequence WHERE name='accounts_weather'")

    data = { 'message': 'All data deleted successfully!' }

    return render(request, 'api/api.html', {'data': data})


#** -------------------------------- API -------------------------------- **#
# DONE: The sensor is working! 
# Sensor status is 'working'
def sensor_working(request, raspberry_id, sensor_id):
    sensor = Sensor.objects.get(id=sensor_id, fk_garden__fk_raspberry__id=raspberry_id)
    sensor.status = 'working'
    sensor.save()
    
    data = {
        'raspberry_id': raspberry_id,
        'sensor_id': sensor_id,
        'status': sensor.status,
    }

    return render(request, 'api/api.html', {'data': data})

# DONE: The sensor is not working!
# Sensor status is in warning_message
def sensor_warning(request, raspberry_id, sensor_id, warning_message):
    sensor = Sensor.objects.get(id=sensor_id, fk_garden__fk_raspberry__id=raspberry_id)
    sensor.status = warning_message
    sensor.save()

    data = {
        'raspberry_id': raspberry_id,
        'sensor_id': sensor_id,
        'status': sensor.status,
    }

    return render(request, 'api/api.html', {'data': data})

# Check if sensor is in the right garden and everything is ok
# Faccio delle query e in teoria devo restituire quello che c'è nella lista di json che mi è stato mandato
# (se tutto coincide allora ok --> il controllo lo fa il raspberry)
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
def new_sensor(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        data = {'id': 1, 'role': 'sensor', 'last_ping': '2025-04-03 11:08:55.570102', 'garden': 0}
    else:
        data = {'id': 1, 'role': 'sensor', 'last_ping': '2025-04-03 11:08:55.570102', 'garden': 0}

    # Il garden è 0 perchè l'utente deve associarlo manualmente
    sensor = Sensor.objects.create(
        # id = data['id'],
        is_associated = False,
        type = data['role'],
        status = 'not working',
        fk_garden = None,
    )
    sensor.save()

    response = {
        'sensor_id': sensor.id,
        'type': sensor.type,
        'status': sensor.status,
        'fk_garden': sensor.fk_garden,
        'message': 'Sensor successfully added!',
    }

    return render(request, 'api/api.html', {'data': response})

# Add garden to a sensor
def add_garden(request, raspberry_id):
    if request.method == 'POST':
        data = json.loads(request.body)
        data = {'id': 1, 'role': 'sensor', 'last_ping': '2025-04-03 11:08:55.570102', 'garden': 0}
    else:
        data = {'id': 1, 'role': 'sensor', 'last_ping': '2025-04-03 11:08:55.570102', 'garden': 0}

    response = {'raspberry_id': raspberry_id, 'sensor_id': 1, 'garden': 2} # Aggiunta del giardino al sensore
    return render(request, 'api/api.html', {'data': response})
