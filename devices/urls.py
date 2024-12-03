from django.urls import path

from devices.views import myDevicesList, deviceDetails

urlpatterns = [
    path("", myDevicesList, name="house"),
    path("details/<int:id>/", deviceDetails, name="house_details"),
]