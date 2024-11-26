from django.http import HttpResponseNotFound
from django.shortcuts import render, redirect
from django.contrib import messages
from appuser.models import Appuser

# Vista per la home page - OK
def home(request):
    return render(request, 'home/home.html')

# Vista per vedera la lista dei miei dispositivi - OK
def myDevicesList(request):
    return render(request, 'devices/mydevices.html')

# Vista per la pagina di errore 404 - OK
def error_404(request):
    return HttpResponseNotFound(render(request, 'error/error.html', {'message': 'Error: 404 - Page not found'}))