import json
from django.db import connection
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from accounts.models import *
from django.contrib.auth.decorators import login_required
from accounts.views import get_weather_forecast
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime


def welcome_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    return render(request, "welcome/welcome.html")

@login_required
def home_view(request):
    # Ottieni i dati meteo (presumibilmente da una funzione esterna)
    weather_data = get_weather_forecast(request)
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
    sensors = Sensor.objects.filter(fk_garden=garden) | Sensor.objects.filter(fk_garden__isnull=True)

    sorted_moisture = sorted(garden.moisture, key=lambda x: x['timestamp'])

    moisture_labels = [
        datetime.fromisoformat(entry['timestamp']).isoformat()
        for entry in sorted_moisture
    ]
    moisture_values = [entry['moisture'] for entry in sorted_moisture]

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
        'fk_raspberry': 1,
        'label': 'Garden Test',
        'moisture': [],
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
            sensorData['garden'] = sensor.fk_garden.id
        else:
            sensorData['id'] = data[i]['id']
            sensorData['role'] = None
            sensorData['garden'] = None
            
        response.append(sensorData)

    return JsonResponse(response)

# Add a new sensor to the database
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

    print("Data: ", data)

    garden = Garden.objects.get(id=data['garden'], fk_raspberry=raspberry_id)
    garden.moisture.append(data)
    garden.moisture.sort(key=lambda x: x['timestamp'])
    garden.save()

    print("Garden: ", garden)

    return JsonResponse({'message': 'Moisture data added successfully!', 'data': data})