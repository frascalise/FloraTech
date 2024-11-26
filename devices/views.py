from django.shortcuts import render

# Vista per vedera la lista dei miei dispositivi - OK
def myDevicesList(request):
    return render(request, 'devices/hub/hubPage.html')

