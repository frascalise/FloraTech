from django.shortcuts import render
from .models import Hub, SensorDevice
from telematry.models import TelematryData
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import json
import datetime

# Vista per vedera la lista dei miei dispositivi - OK
def myDevicesList(request):
    hublist = Hub.objects.all()
    context = {
        "details": False,
        "hubs": hublist,
    }

    return render(request, 'devices/hub/hubPage.html', context)

def deviceDetails(request, id):

    hub = Hub.objects.get(id=id)

    sensorDevices = SensorDevice.objects.filter(parent_hub__id=id)

    context = {
        "details": True,
        "hub": hub,
        "sensors": sensorDevices,
    }
    return render(request, 'devices/hub/hubPage.html', context)


def sensorDetails(request, parent_hub, id):

    sensor = SensorDevice.objects.get(id=id, parent_hub=parent_hub)

    s_telem = TelematryData.objects.filter(parent_sensor=id, parent_hub=parent_hub)

    context = {
        "details": True,
        "sensor": sensor,
        "telematry": s_telem
    }
    return render(request, 'devices/sensor/sensorPage.html', context)

@csrf_exempt
def setSensorTelematry(request, parent_hub, id):

    if request.method == "POST":
        sensor = SensorDevice.objects.get(id=id, parent_hub=parent_hub)
        data = json.loads(request.body)
        sensor.last_transmitted_telematry = data
        sensor.last_update_date = datetime.datetime.now()
        sensor.save()
        return HttpResponse("Data updated")
    


