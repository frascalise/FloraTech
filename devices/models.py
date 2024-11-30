from django.db import models

class Hub(models.Model):
    # hub_id = models.IntegerField(unique=True)
    hub_type = models.CharField(max_length=100, default="Raspberry PI")
    installation_date = models.DateField(auto_now=True)
    hub_status = models.CharField(max_length=100, default="working") # working, anomaly, down
    name = models.CharField(max_length=100, default="My House")
    location = models.CharField(max_length=100)
    picture = models.ImageField(upload_to='hub_pics/', default='hub_pics/default.jpg')

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
    