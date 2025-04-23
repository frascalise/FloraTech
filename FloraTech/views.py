import json
import requests
import random
from django.db import connection
from django.http import JsonResponse
from django.shortcuts import render, redirect
from accounts.models import *
from django.contrib.auth.decorators import login_required
from accounts.views import get_weather_forecast
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
from collections import defaultdict
from datetime import datetime
from django.db.models import Q
from django.http import HttpResponse
from django.contrib.auth.models import User

from weather.meteo import richiesta_meteo
from weather.aiModel import WeatherModel

weatherModel = WeatherModel()


def welcome_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    return render(request, "welcome/welcome.html")

@login_required
def home_view(request):
    # Ottieni i dati meteo (presumibilmente da una funzione esterna)
    weather_data = richiesta_meteo(request)
    user = request.user

    # Recupera i giardini associati all'utente
    user_gardens = Garden.objects.filter(fk_raspberry__fk_owner=user)

    gardens_data = []
    for garden in user_gardens:
        moisture_data = garden.moisture
        
        moisture_labels = [entry['timestamp'] for entry in moisture_data]
        moisture_values = [entry['moisture'] for entry in moisture_data] 
        
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
    
    # Passa i dati alla template
    return render(request, "home/home.html", {"weather": weather_data, "user": user, "gardens": gardens_data})

@login_required
def garden_view(request, garden_id):
    garden = Garden.objects.get(id=garden_id)
    sensors = Sensor.objects.filter(Q(fk_garden=garden) | Q(fk_garden__isnull=True))

    # Ordina moisture per timestamp
    sorted_moisture = sorted(garden.moisture, key=lambda x: x['timestamp'])

    # Crea dizionario {data: [valori]}
    moisture_by_day = defaultdict(list)
    for entry in sorted_moisture:
        date_str = entry["timestamp"]
        date = datetime.fromisoformat(date_str).date()  # solo giorno
        moisture_by_day[date].append(entry["moisture"])

    # Calcola media per ogni giorno
    daily_avg = {day: sum(vals) / len(vals) for day, vals in moisture_by_day.items()}

    # Ordina per data (in caso non siano in ordine)
    sorted_days = sorted(daily_avg.keys())
    moisture_labels = [day.strftime("%Y-%m-%d") for day in sorted_days]
    moisture_values = [round(daily_avg[day], 2) for day in sorted_days]

    for i in range(len(moisture_values)):
        moisture_values[i] = moisture_values[i] * 100 / 1023

    return render(request, "garden/garden.html", {
        "garden": garden,
        "sensors": sensors,
        "moisture_labels": moisture_labels,
        "moisture_values": moisture_values,
    })

@login_required
def edit_garden(request, garden_id):
    garden = Garden.objects.get(id=garden_id)
    available_plants = Plant.objects.all()
    print("Available plants: ", available_plants)
    
    if request.method == "POST":
        # Modifica il nome del giardino
        new_label = request.POST.get("label")
        if new_label:
            garden.label = new_label

        # Modifica la quantità delle piante esistenti
        updated_plants = []

        for plant_data in garden.plants:
            plant_name = plant_data.get('name')
            new_quantity = request.POST.get(f"plant_{plant_name}")

            if new_quantity is not None:
                try:
                    new_quantity = int(new_quantity)
                    if new_quantity > 0:
                        updated_plants.append({'name': plant_name, 'quantity': new_quantity})
                    # Se è 0 o negativa, non la aggiunge (quindi viene rimossa)
                except ValueError:
                    updated_plants.append(plant_data)
            else:
                updated_plants.append(plant_data)

        # Aggiungi nuova pianta, solo se non già presente
        new_plant_id = request.POST.get("new_plant")
        if new_plant_id:
            try:
                new_plant = Plant.objects.get(id=new_plant_id)
                existing_plant_names = {p['name'] for p in updated_plants}
                if new_plant.name not in existing_plant_names:
                    updated_plants.append({'name': new_plant.name, 'quantity': 1})
            except Plant.DoesNotExist:
                pass

        # Salva le modifiche
        garden.plants = updated_plants
        garden.save()

        return redirect("edit_garden", garden_id=garden.id)

    return render(request, "garden/edit.html", {
        "garden": garden,
        "plants": available_plants
    })

@login_required
def settings_view(request, garden_id):
    garden = Garden.objects.get(id=garden_id)

    if request.method == "POST":
        location = request.POST.get("location")
        surface_area = request.POST.get("surface_area")

        if location:
            garden.location = location
            garden.location = location

            url = f"https://nominatim.openstreetmap.org/search"
            params = {
                "q": location,
                "format": "json",
                "limit": 1
            }

            try:
                response = requests.get(url, params=params, headers={'User-Agent': 'FloraTechApp/1.0'})
                data = response.json()

                if data:
                    garden.latitude = float(data[0]["lat"])
                    garden.longitude = float(data[0]["lon"])
            except Exception as e:
                print(f"Errore durante il recupero coordinate: {e}")
        if surface_area:
            try:
                garden.surface_area = float(surface_area)
            except ValueError:
                return redirect("settings", garden_id=garden.id)

        garden.save()
        return redirect("garden", garden_id=garden.id)

    return render(request, "garden/settings.html", {"garden": garden})

@login_required
def delete_garden(request, garden_id):
    garden = Garden.objects.get(id=garden_id)
    garden.delete()
    
    return redirect('home')

@login_required
def new_garden(request):
    garden = Garden.objects.create(fk_raspberry=Raspberry.objects.get(fk_owner=request.user))
    garden.label = "Garden " + str(garden.id)
    garden.moisture = []
    garden.plants = []
    garden.save()

    return redirect('home')

@login_required
def edit_sensor(request, sensor_id, garden_id):
    sensor = Sensor.objects.get(id=sensor_id)
    garden = Garden.objects.get(id=garden_id)

    if request.method == "POST":
        label = request.POST.get("label")
        
        if label:
            sensor.label = label
        else:
            sensor.label = sensor.type
        sensor.save()

        return redirect("garden", garden_id=garden.id)

    return render(request, "garden/edit_sensor.html", {"garden": garden})
    

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
        'username': 'admin',    # password: floratech1
        'label': 'RASPBERRY TEST',
    }

    data_garden = {
        'fk_raspberry': 1,
        'label': 'Garden Test',
        'moisture': [{'timestamp': '2025-04-12 16:14:22.414395', 'moisture': 794, 'sensor_from': 10, 'garden': 1}, {'timestamp': '2025-04-13 16:14:31.346044', 'moisture': 794, 'sensor_from': 10, 'garden': 1}, {'timestamp': '2025-04-14 16:14:40.280807', 'moisture': 794, 'sensor_from': 10, 'garden': 1}, {'timestamp': '2025-04-11 16:14:49.217141', 'moisture': 795, 'sensor_from': 10, 'garden': 1}, {'timestamp': '2025-04-11 16:14:58.150797', 'moisture': 794, 'sensor_from': 10, 'garden': 1}, {'timestamp': '2025-04-11 16:15:07.085934', 'moisture': 795, 'sensor_from': 10, 'garden': 1}, {'timestamp': '2025-04-14 16:15:16.020279', 'moisture': 794, 'sensor_from': 10, 'garden': 1}, {'timestamp': '2025-04-11 16:15:24.954200', 'moisture': 794, 'sensor_from': 10, 'garden': 1}, {'timestamp': '2025-04-11 16:15:33.888822', 'moisture': 794, 'sensor_from': 10, 'garden': 1}, {'timestamp': '2025-04-11 16:15:42.835102', 'moisture': 794, 'sensor_from': 10, 'garden': 1}, {'timestamp': '2025-04-11 16:16:00.693254', 'moisture': 794, 'sensor_from': 10, 'garden': 1}, {'timestamp': '2025-04-11 16:16:09.630516', 'moisture': 794, 'sensor_from': 10, 'garden': 1}, {'timestamp': '2025-04-11 16:16:18.565234', 'moisture': 794, 'sensor_from': 10, 'garden': 1}, {'timestamp': '2025-04-11 16:16:27.499489', 'moisture': 794, 'sensor_from': 10, 'garden': 1}, {'timestamp': '2025-04-11 16:19:17.257998', 'moisture': 794, 'sensor_from': 10, 'garden': 1}, {'timestamp': '2025-04-11 16:19:26.192496', 'moisture': 794, 'sensor_from': 10, 'garden': 1}, {'timestamp': '2025-04-11 16:19:35.127375', 'moisture': 794, 'sensor_from': 10, 'garden': 1}, {'timestamp': '2025-04-11 16:19:44.061125', 'moisture': 795, 'sensor_from': 10, 'garden': 1}, {'timestamp': '2025-04-11 16:19:52.997814', 'moisture': 794, 'sensor_from': 10, 'garden': 1}, {'timestamp': '2025-04-11 16:20:01.928535', 'moisture': 794, 'sensor_from': 10, 'garden': 1}, {'timestamp': '2025-04-11 16:20:10.864961', 'moisture': 794, 'sensor_from': 10, 'garden': 1}, {'timestamp': '2025-04-11 16:20:19.798581', 'moisture': 795, 'sensor_from': 10, 'garden': 1}, {'timestamp': '2025-04-11 16:20:28.731473', 'moisture': 794, 'sensor_from': 10, 'garden': 1}, {'timestamp': '2025-04-11 16:20:37.669183', 'moisture': 794, 'sensor_from': 10, 'garden': 1}, {'timestamp': '2025-04-11 16:20:46.601846', 'moisture': 794, 'sensor_from': 10, 'garden': 1}, {'timestamp': '2025-04-11 16:20:55.535298', 'moisture': 794, 'sensor_from': 10, 'garden': 1}, {'timestamp': '2025-04-11 16:21:04.472946', 'moisture': 794, 'sensor_from': 10, 'garden': 1}, {'timestamp': '2025-04-11 16:21:22.337892', 'moisture': 794, 'sensor_from': 10, 'garden': 1}, {'timestamp': '2025-04-11 16:21:31.273187', 'moisture': 794, 'sensor_from': 10, 'garden': 1}, {'timestamp': '2025-04-11 16:21:40.209395', 'moisture': 794, 'sensor_from': 10, 'garden': 1}, {'timestamp': '2025-04-11 16:21:49.141601', 'moisture': 795, 'sensor_from': 10, 'garden': 1}, {'timestamp': '2025-04-11 16:21:58.152333', 'moisture': 794, 'sensor_from': 10, 'garden': 1}, {'timestamp': '2025-04-11 16:22:07.030330', 'moisture': 794, 'sensor_from': 10, 'garden': 1}, {'timestamp': '2025-04-11 16:22:16.068179', 'moisture': 794, 'sensor_from': 10, 'garden': 1}, {'timestamp': '2025-04-11 16:22:24.881183', 'moisture': 795, 'sensor_from': 10, 'garden': 1}, {'timestamp': '2025-04-11 16:22:33.859732', 'moisture': 794, 'sensor_from': 10, 'garden': 1}, {'timestamp': '2025-04-11 16:22:42.947330', 'moisture': 794, 'sensor_from': 10, 'garden': 1}, {'timestamp': '2025-04-11 16:22:51.682106', 'moisture': 794, 'sensor_from': 10, 'garden': 1}, {'timestamp': '2025-04-11 16:23:00.617203', 'moisture': 794, 'sensor_from': 10, 'garden': 1}, {'timestamp': '2025-04-11 16:23:09.554060', 'moisture': 795, 'sensor_from': 10, 'garden': 1}, {'timestamp': '2025-04-11 16:23:18.488184', 'moisture': 794, 'sensor_from': 10, 'garden': 1}, {'timestamp': '2025-04-11 16:23:27.421804', 'moisture': 794, 'sensor_from': 10, 'garden': 1}, {'timestamp': '2025-04-11 16:23:36.404134', 'moisture': 794, 'sensor_from': 10, 'garden': 1}, {'timestamp': '2025-04-11 16:23:45.487621', 'moisture': 795, 'sensor_from': 10, 'garden': 1}, {'timestamp': '2025-04-11 16:23:54.224856', 'moisture': 794, 'sensor_from': 10, 'garden': 1}, {'timestamp': '2025-04-11 16:24:03.244742', 'moisture': 794, 'sensor_from': 10, 'garden': 1}, {'timestamp': '2025-04-11 16:24:12.093125', 'moisture': 794, 'sensor_from': 10, 'garden': 1}, {'timestamp': '2025-04-11 16:24:21.027397', 'moisture': 794, 'sensor_from': 10, 'garden': 1}, {'timestamp': '2025-04-11 16:24:29.964162', 'moisture': 794, 'sensor_from': 10, 'garden': 1}, {'timestamp': '2025-04-11 16:24:38.897189', 'moisture': 795, 'sensor_from': 10, 'garden': 1}, {'timestamp': '2025-04-11 16:24:47.831332', 'moisture': 794, 'sensor_from': 10, 'garden': 1}, {'timestamp': '2025-04-11 16:24:56.766156', 'moisture': 794, 'sensor_from': 10, 'garden': 1}, {'timestamp': '2025-04-11 16:25:05.702954', 'moisture': 794, 'sensor_from': 10, 'garden': 1}, {'timestamp': '2025-04-11 16:25:14.639908', 'moisture': 794, 'sensor_from': 10, 'garden': 1}],
        'plants': [
            {'name': 'TOMATO', 'quantity': 5},
            {'name': 'BANANA', 'quantity': 3},
        ],
    }

    raspberry = Raspberry.objects.create(fk_owner=data_raspberry['username'], label=data_raspberry['label'])
    
    garden = Garden.objects.create(fk_raspberry=raspberry, label=data_garden['label'])
    garden.moisture = data_garden['moisture']
    garden.plants = data_garden['plants']
    garden.save()

    # Create the sensors
    # id	idSensor	fk_garden_id	fk_raspberry_id	is_associated	status	type	label
    # 1	10	None	1	False	not working	sensor	Sensor
    # 2	11	None	1	False	not working	sensor	Sensor
    # 3	15	1	1	True	working	actuator	Actuator
    sensor1 = Sensor.objects.create(idSensor=10, fk_garden=garden, fk_raspberry=raspberry, is_associated=False, status='not working', type='sensor', label='Sensor')
    sensor2 = Sensor.objects.create(idSensor=11, fk_garden=garden, fk_raspberry=raspberry, is_associated=False, status='not working', type='sensor', label='Sensor')
    sensor3 = Sensor.objects.create(idSensor=15, fk_garden=garden, fk_raspberry=raspberry, is_associated=True, status='working', type='actuator', label='Actuator')
    sensor1.save()
    sensor2.save()
    sensor3.save()

    PLANT_CHOICES = [
        ("ONION", "Onion"),
        ("TOMATO", "Tomato"),
        ("SUGARCANE", "Sugarcane"),
        ("COTTON", "Cotton"),
        ("MUSTARD", "Mustard"),
        ("WHEAT", "Wheat"),
        ("BEAN", "Bean"),
        ("CITRUS", "Citrus"),
        ("MAIZE", "Maize"),
        ("MELON", "Melon"),
        ("RICE", "Rice"),
        ("POTATO", "Potato"),
        ("CABBAGE", "Cabbage"),
        ("SOYBEAN", "Soybean"),
        ("BANANA", "Banana"),
    ]
    
    for i in PLANT_CHOICES:
        plant = Plant.objects.create(name=i[0])
        plant.save()

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
    sensor = Sensor.objects.get(idSensor=sensor_id, fk_raspberry_id=raspberry_id)
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
    sensor = Sensor.objects.get(idSensor=sensor_id, fk_raspberry_id=raspberry_id)
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
def check_sensor(request, raspberry_id):
    if request.method == 'POST':
        data = json.loads(request.body)

    # [{'id': 1, 'role': 'sensor', 'last_ping': '2025-04-03 11:08:55.570102', 'garden': 0}]
    response = []
    for i in range(len(data)):
        sensorData = {}
        sensor = Sensor.objects.get(idSensor=data[i]['id'], fk_raspberry_id=raspberry_id)
        if sensor:
            sensorData['id'] = sensor.idSensor
            sensorData['role'] = sensor.type
            if sensor.fk_garden:
                sensorData['garden'] = sensor.fk_garden.id
            else:
                sensorData['garden'] = None
        else:
            sensorData['id'] = data[i]['id']
            sensorData['role'] = None
            sensorData['garden'] = None
            
        response.append(sensorData)
        print("Response: ", response)

    return JsonResponse(response, safe=False)

# DONE: Add a new sensor to the database
@csrf_exempt
def new_sensor(request, raspberry_id):
    if request.method == 'POST':
        data = json.loads(request.body)

    print("Data: ", data)

    # Il garden è None perchè l'utente deve associarlo manualmente
    sensor = Sensor.objects.create(
        idSensor = data['id'],
        is_associated = False,
        type = data['role'],
        status = 'not working',
        fk_garden = None,
        fk_raspberry = Raspberry.objects.get(id=raspberry_id)
    )

    if sensor.type == 'actuator':
        sensor.label = 'Actuator'
    elif sensor.type == 'sensor':
        sensor.label = 'Sensor'

    sensor.save()

    response = {
        'sensor_id': sensor.id,
        'type': sensor.type,
        'status': sensor.status,
        'fk_garden': sensor.fk_garden,
        'message': 'Sensor successfully added!',
    }

    return render(request, 'api/api.html', {'data': response})

# DONE: Add garden to a sensor
@csrf_exempt
def add_garden(request, raspberry_id):
    if request.method == 'POST':
        data = json.loads(request.body)

    sensor = Sensor.objects.get(idSensor=data['id'], fk_raspberry__id=raspberry_id)
    sensorGardenId = sensor.fk_garden.id if sensor.fk_garden else None

    response = {'raspberry_id': raspberry_id, 'sensor_id': sensor.idSensor, 'garden': sensorGardenId}

    return JsonResponse(response)

# DONE: Add moisture to the garden 
@csrf_exempt
def add_moisture(request, raspberry_id):
    data = {}
    if request.method == 'POST':
        data = json.loads(request.body)

    garden = Garden.objects.get(id=data['garden'], fk_raspberry=raspberry_id)
    garden.moisture.append(data)
    garden.moisture.sort(key=lambda x: x['timestamp'])
    garden.save()

    return JsonResponse({'message': 'Moisture data added successfully!', 'data': data})

@csrf_exempt
def get_daily_water_needs(request, raspberry_id, garden_id):
    garden = Garden.objects.get(id=garden_id, fk_raspberry=raspberry_id)
    lat, lon = garden.latitude, garden.longitude

    waterQ = weatherModel.get_daily_water_predictions(garden_id, lat, lon)
    if waterQ > 0.5: #threshold
        newIrrigationEntry = Water(garden_id, datetime.now(), waterQ)
        newIrrigationEntry.save()
    else:
        waterQ = 0

    return JsonResponse({'message': 'Returning the daily water volume needed', 'data': waterQ})

@csrf_exempt
def get_temperature(request):
    if request.method == 'POST':
       data = json.loads(request.body)

    print("Data: ", data)

    garden = Garden.objects.get(id=data['garden_id'])
    lat, lon = garden.latitude, garden.longitude
    
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
    weather_json = requests.get(url)
    json_result = weather_json.json()

    temperature = json_result["current_weather"]["temperature"]

    response = {"temperature": temperature}
    return JsonResponse(response)

@csrf_exempt
def get_water(request):
    if request.method == 'POST':
        data = json.loads(request.body)

    garden = Garden.objects.get(id=data['garden_id'])
    lat, lon = garden.latitude, garden.longitude

    waterQ = weatherModel.get_daily_water_predictions(data['garden_id'], lat, lon)
    if waterQ > 0.5: #threshold
        newIrrigationEntry = Water(garden.id, datetime.now(), waterQ)
        newIrrigationEntry.save()
    else:
        waterQ = 0

    waterQ = waterQ*garden.surface_area
    print("\n\n\n\nWaterQ: ", waterQ, "\n\n\n\n\n")

    return JsonResponse({'message': 'Returning the daily water volume needed', 'data': waterQ})

def VerifyTelegramUser(owner,tele_id,number):
    p_db=User.objects.all()
    presente=False
    for i in p_db:
        if i.username==owner:
            presente=True
    if presente:
        return 1
    return 0
        
def NewEntrance(owner,tele_id):
    #Telegram.objects.all().delete()
    value=Telegram.objects.create(fk_owner=owner,telegram_id=tele_id)
    value.save()
def TelegramIdProvider(username):
    return Telegram.objects.get(fk_owner=username).telegram_id
