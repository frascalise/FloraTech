from django.db import models
from appuser.models import Appuser

class Hub(models.Model):
    # hub_id = models.IntegerField(unique=True)
    owner = models.ForeignKey(Appuser, on_delete=models.CASCADE)  # Relation with Appuser
    hub_type = models.CharField(max_length=100, default="Raspberry PI")
    installation_date = models.DateField(auto_now=True)
    hub_status = models.CharField(max_length=100, default="working")
    name = models.CharField(max_length=100, default="My House")
    location = models.CharField(max_length=100)
    picture = models.ImageField(upload_to='hub_pics/', default='photo/hub_pics/default.jpg')

    def getHubType(self):
        return self.hub_type
    
    def getInstallationDate(self):
        return self.installation_date
    
    def getHubStatus(self):
        return self.hub_status

    def getName(self):
        return self.name
    
    def getLocation(self):
        return self.location
    
    def getPicture(self):
        return self.picture
    

class SensorDevice(models.Model):
    
    parent_hub = models.ForeignKey(Hub, on_delete=models.CASCADE)

    #composite_id = parent_hub + '#' + id

    sensor_type = models.CharField(max_length=100, default="Arduino")
    installation_date = models.DateField(auto_now=True)
    last_update_date = models.DateField(auto_now=True)
    last_transmitted_telematry = models.JSONField(default='{}')
    
    plant_ref = models.CharField(max_length=100, default="Generic culture") #this should be a select field
