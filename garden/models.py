import os
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser

class Garden(models.Model):
    name = models.CharField(max_length=100)
    latitute = models.FloatField()
    longitude = models.FloatField()

    def getName(self):
        return self.name
    
    def getCoordinates(self):
        return (self.latitute, self.longitude)
    
    def getPlantsNumber(self):
        return self.subgarden_set.count()

class Subgarden(models.Model):
    name = models.CharField(max_length=100)
    plants = models.CharField(max_length=100)
    garden = models.ForeignKey(Garden, on_delete=models.CASCADE)

    def getName(self):
        return self.name
    
    def getPlants(self):
        return self.plants
    
    def getGarden(self):
        return self.garden
    

class Sensor(models.Model):
    subgarden = models.ForeignKey(Subgarden, on_delete=models.CASCADE)
