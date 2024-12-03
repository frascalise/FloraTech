from django.urls import path

from devices.views import myDevicesList, deviceDetails, setSensorTelematry, sensorDetails

urlpatterns = [
    path("", myDevicesList, name="house"),
    path("details/<int:id>/", deviceDetails, name="house_details"),
    path("details/<int:parent_hub>/sensor/<int:id>/", sensorDetails, name="sensor_details"),
    path("telematry/<int:parent_hub>/sensor/<int:id>/", setSensorTelematry),
]