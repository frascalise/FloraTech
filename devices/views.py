from django.shortcuts import render
from .models import Hub

# Vista per vedera la lista dei miei dispositivi - OK
def myDevicesList(request):
    
    h1 = Hub(location='Modena')
    h1.save()
    h2 = Hub(location='Firenze', hub_status="down")
    h2.save()

    hublist = [
        h1,
        h2
    ]
    context = {
        "details": False,
        "hubs": hublist,
    }

    return render(request, 'devices/hub/hubPage.html', context)

def deviceDetails(request, id):

    device = Hub.objects.get(id=id)

    context = {
        "details": True,
        "hub": device,
    }
    return render(request, 'devices/hub/hubPage.html', context)

