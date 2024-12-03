from django.shortcuts import render
from .models import Hub, SensorDevice

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

