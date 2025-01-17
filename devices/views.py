from django.shortcuts import render
from .models import Hub, SensorDevice
from telematry.models import TelematryData
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import plotly.express as px
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
    if s_telem:
        fig = px.line(
            x=[t.received_date for t in s_telem],
            y=[t.humidity for t in s_telem],
            title="Andamento umidità",
            labels={'x':'data ricezione', 'y':'valore umidità'}
        )

        fig.update_xaxes(tickformat="%Y %m\n%d %H %S")

        fig.update_layout(title={
            'font_size':22,
            'xanchor':'center',
            'x': 0.5}
        )

        chart = fig.to_html()

        context = {
            "details": True,
            "sensor": sensor,
            "graph": chart
        }

    else:
        context = {
            "details": True,
            "sensor": sensor,
            "graph": '<p>No data for this sensor</p>'
        }

    return render(request, 'devices/sensor/sensorPage.html', context)

@csrf_exempt
def setSensorTelematry(request, parent_hub, id):

    if request.method == "POST":
        sensor = SensorDevice.objects.get(id=id, parent_hub=parent_hub)
        data = json.loads(request.body)

        newhumidity = data["humidity"]
        newhumidity = float(newhumidity)

        def __get_or_none(model, *args, **kwargs):
            try:
                return model.objects.get(*args, **kwargs)
            except model.DoesNotExist:
                return None

        #prevTemetry = TelematryData.objects.get(parent_sensor=id, parent_hub=parent_hub, is_last_transmitted=True)
        prevTemetry = __get_or_none(TelematryData, parent_sensor=id, parent_hub=parent_hub, is_last_transmitted=True)
        if prevTemetry:
            previd = prevTemetry.pk
            prevTemetry.is_last_transmitted = False
            prevTemetry.save()
        else:
            previd = None

        newTelemetry = TelematryData()

        newTelemetry.parent_sensor = SensorDevice.objects.get(pk=id)
        newTelemetry.parent_hub = Hub.objects.get(pk=parent_hub)
        newTelemetry.received_date = datetime.datetime.now()
        newTelemetry.is_last_transmitted = True
        newTelemetry.previously_transmitted = previd
        newTelemetry.next_transmitted = None
        newTelemetry.humidity = newhumidity

        newTelemetry.save()

        sensor.last_transmitted_telematry = data
        sensor.last_update_date = datetime.datetime.now()
        sensor.save()
        return HttpResponse("Data updated")
    


