import json
from django.db import connection
from django.shortcuts import render, redirect
from accounts.models import *
from django.contrib.auth.decorators import login_required
from accounts.views import get_weather_forecast
from django.views.decorators.csrf import csrf_exempt


def welcome_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    return render(request, "welcome/welcome.html")

@login_required
def home_view(request):
    weather_data = get_weather_forecast(request)
    user = request.user
    
    user_gardens = Garden.objects.filter(fk_raspberry__fk_owner=user)

    gardens_data = []
    for garden in user_gardens:
        moisture_data = garden.moisture
        moisture_labels = [entry['timestamp'] for entry in moisture_data]
        moisture_values = [entry['value'] for entry in moisture_data]
        
        plants_data = garden.plants
        plants_names = [entry['name'] for entry in plants_data]
        plants_quantities = [entry['quantity'] for entry in plants_data]

        gardens_data.append({
            "id": garden.id,
            "label": garden.label,
            "moisture_labels": moisture_labels,
            "moisture_values": moisture_values,
            "plants_names": plants_names,
            "plants_quantities": plants_quantities,
        })
    
    return render(request, "home/home.html", {"weather": weather_data, "user": user, "gardens": gardens_data})

@login_required
def garden_view(request, garden_id):
    garden = Garden.objects.get(id=garden_id)
    sensors = Sensor.objects.filter(fk_garden=garden) | Sensor.objects.filter(fk_garden__isnull=True)

    moisture_labels = [entry['timestamp'] for entry in garden.moisture]
    moisture_values = [entry['value'] for entry in garden.moisture]

    return render(request, "garden/garden.html", {
        "garden": garden,
        "sensors": sensors,
        "moisture_labels": moisture_labels,
        "moisture_values": moisture_values,
    })

@login_required
def activate_sensor(request, sensor_id, garden_id):
    sensor = Sensor.objects.get(id=sensor_id)
    garden = Garden.objects.get(id=garden_id)

    if sensor.status == 'not working':
        sensor.status = 'working'
        sensor.fk_garden = garden
        sensor.is_associated = True
        sensor.save()
    
    if garden.status == 'not working':
        garden.status = 'working'
        garden.save()
        

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

    gardenSensors = Sensor.objects.filter(fk_garden=garden)
    if all(s.status == 'not working' for s in gardenSensors):
        garden.status = 'not working'
        garden.save()
        
    return redirect('garden', garden_id=garden_id)

#** -------------------------------- PRODUCTION API -------------------------------- **#
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
        'moisture': [
            {'timestamp': '2023-04-21 12:00:00', 'value': 50},
            {'timestamp': '2023-04-22 12:00:00', 'value': 60},
            {'timestamp': '2023-04-23 12:00:00', 'value': 65},
            {'timestamp': '2023-04-24 12:00:00', 'value': 40},
            {'timestamp': '2023-04-25 12:00:00', 'value': 64},
            {'timestamp': '2023-04-26 12:00:00', 'value': 70},
            {'timestamp': '2023-04-27 12:00:00', 'value': 50},
            {'timestamp': '2023-04-28 12:00:00', 'value': 40},
            {'timestamp': '2023-04-29 12:00:00', 'value': 85},
        ],
        'plants': [
            {'name': 'Tomato', 'quantity': 5},
            {'name': 'Cucumber', 'quantity': 3},
            {'name': 'Lettuce', 'quantity': 10},
        ],
    }

    raspberry = Raspberry.objects.create(fk_owner=data_raspberry['username'], label=data_raspberry['label'])
    
    garden = Garden.objects.create(fk_raspberry=raspberry, label=data_garden['label'])
    garden.moisture = data_garden['moisture']
    garden.plants = data_garden['plants']
    garden.save()

    data_sensor = [
        {'idSensor': 1, 'is_associated': True, 'status': 'working', 'fk_garden': garden, 'label': 'Humidity Sensor near the plants'},
        {'idSensor': 2, 'is_associated': False, 'status': 'not working', 'fk_garden': None, 'label': 'Humidity Sensor near the water tank'},
        {'idSensor': 3, 'is_associated': True, 'status': 'working', 'fk_garden': garden, 'label': 'Water Pump'},
        {'idSensor': 4, 'is_associated': False, 'status': 'not working', 'fk_garden': None, 'label': 'Temperature Sensor'},
        {'idSensor': 2, 'is_associated': True, 'status': 'working', 'fk_garden': garden, 'label': 'Soil Moisture Sensor'},
    ]

    print("Data Sensor: ", data_sensor)

    for sensor_data in data_sensor:
        Sensor.objects.create(
            idSensor=sensor_data['idSensor'],
            is_associated=sensor_data['is_associated'],
            status=sensor_data['status'],
            fk_garden=sensor_data['fk_garden'],
            label=sensor_data['label']
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
@csrf_exempt
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
@csrf_exempt
def new_sensor(request):
    if request.method == 'POST':
        data = json.loads(request.body)

    print("Data: ", data)

    # Il garden è 0 perchè l'utente deve associarlo manualmente
    sensor = Sensor.objects.create(
        idSensor = data['id'],
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
@csrf_exempt
def add_garden(request, raspberry_id):
    if request.method == 'POST':
        data = json.loads(request.body)
        data = {'id': 1, 'role': 'sensor', 'last_ping': '2025-04-03 11:08:55.570102', 'garden': 0}
    else:
        data = {'id': 1, 'role': 'sensor', 'last_ping': '2025-04-03 11:08:55.570102', 'garden': 0}

    response = {'raspberry_id': raspberry_id, 'sensor_id': 1, 'garden': 2} # Aggiunta del giardino al sensore
    return render(request, 'api/api.html', {'data': response})
