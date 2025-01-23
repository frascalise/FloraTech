from django.db import models
from devices.models import SensorDevice, Hub

class TelematryData(models.Model):
    ##owner_id = models.ForeignKey(appuser) ??
    parent_sensor = models.ForeignKey(SensorDevice, on_delete = models.DO_NOTHING)
    parent_hub = models.ForeignKey(Hub, on_delete=models.DO_NOTHING)

    received_date = models.DateTimeField(auto_now=True)
    ##the process that recives new telematry updates the old records
    is_last_transmitted = models.BooleanField(default=True)
    previously_transmitted = models.IntegerField(null=True)
    next_transmitted = models.IntegerField(null=True)

    ## dati effettivi raccolti
    humidity = models.FloatField()
    """
        other data ...
    """



