from django.db import models

'''
1 utente ha 1 raspberry gia presente nel db
tutti gli orti del cliente comunicano con il raspberry del cliente

raspberry:
    id
    fk_proprietario (username dell'utente)
    etichetta (nome custom)

orto: 
    id
    raspberry con cui comunicare
    etichetta (nome custom)
    lista con umidità medie (e relativo timestamp)
    lista con temperature (e relativo timestamp)
    lista con ml di acqua per irrigare tutto (e relativo timestamp)

sensori:
    id
    is_associato? (bool)
    orto a cui è associato

meteo:
    timestamp
    location
    temperatura (min)
    temperatura (max)
    precipitazioni (neve, pioggia, ecc...)
    precipitazioni (mm)

'''

class Raspberry(models.Model):
    id = models.AutoField(primary_key=True)
    fk_owner = models.CharField(max_length=50)
    label = models.CharField(max_length=50)

class Garden(models.Model):
    id = models.AutoField(primary_key=True)
    fk_raspberry = models.ForeignKey(Raspberry, on_delete=models.CASCADE)
    label = models.CharField(max_length=50)
    humidity = models.JSONField()
    temperature = models.JSONField()
    water = models.JSONField()

class Sensor(models.Model):
    id = models.AutoField(primary_key=True)
    is_associated = models.BooleanField()
    fk_garden = models.ForeignKey(Garden, on_delete=models.CASCADE)

class Weather(models.Model):    # HAVE TO MIGRATE
    timestamp = models.DateTimeField(primary_key=True)
    location = models.CharField(max_length=50)
    temp_min = models.FloatField()
    temp_max = models.FloatField()
    precipitations = models.CharField(max_length=50)
    precipitations_mm = models.FloatField()
