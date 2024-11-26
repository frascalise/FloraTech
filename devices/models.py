from django.db import models

# Create your models here.

class Hub():
    hub_id_auto = models.AutoField(primary_key=True) #PK

    hub_id = models.IntegerField(unique=True)
    hub_type = models.CharField(max_length=100, default="Raspberry PI")
    number_of_registered_devices = models.ImageField()

    date_of_installation = models.DateField()
    date_of_disinstallation = models.DateField(null=True)

    # working, anomaly (yellow status?), down
    #state = models.CharField()






    
    
