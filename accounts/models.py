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
    fk_raspberry con cui comunicare
    etichetta (nome custom)
    lista con umidità medie (e relativo timestamp)
    lista con temperature (e relativo timestamp)
    lista con ml di acqua per irrigare tutto (e relativo timestamp)

sensori:
    id  (mandato da leo)
    is_associato? (bool)
    status (bool) --> default è working  (mandato da leo)
    tipo ("sensore" o "attuatore") (mandato da leo)
    fk_orto a cui è associato   (mandato da leo)

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

class Telegram(models.Model):
    id = models.AutoField(primary_key=True)
    fk_owner = models.CharField(max_length=50)
    telegram_id= models.CharField(max_length=10)  
    
class Garden(models.Model):
    id = models.AutoField(primary_key=True)
    fk_raspberry = models.ForeignKey(Raspberry, on_delete=models.CASCADE)
    label = models.CharField(max_length=50)
    moisture = models.JSONField(default=list)
    status = models.CharField(default="not working", max_length=50) # [ working, not working ]
    plants = models.JSONField(default=list)
    location = models.CharField(max_length=50, default="unknown")
    latitude = models.FloatField(default=0.0) 
    longitude = models.FloatField(default=0.0)
    surface_area = models.FloatField(default=0.0) # Surface area of the garden in square meters

class Sensor(models.Model):
    id = models.AutoField(primary_key=True)
    idSensor = models.IntegerField(null=True, blank=True) # ID of the sensor as sent by Leo
    fk_garden = models.ForeignKey(Garden, on_delete=models.CASCADE, null=True, blank=True)
    fk_raspberry = models.ForeignKey(Raspberry, on_delete=models.CASCADE, null=True, blank=True)
    is_associated = models.BooleanField()
    status = models.CharField(default="working", max_length=50) # [ working, not working ]
    type = models.CharField(default="sensor", max_length=50) # [ sensor, actuator ]
    label = models.CharField(max_length=50, default="sensor")  # Custom label for the sensor

class Weather(models.Model):
    timestamp = models.DateTimeField(primary_key=True)
    location = models.CharField(max_length=50)
    temp_min = models.FloatField()
    temp_max = models.FloatField()
    precipitations = models.CharField(max_length=50)
    precipitations_mm = models.FloatField()


class Water(models.Model):
    fk_garden = models.ForeignKey(Garden, on_delete=models.CASCADE, null=True, blank=True)
    timestamp = models.DateTimeField(primary_key=True)
    waterQuantity = models.FloatField()

class Plant(models.Model):
    PLANT_CHOICES = [
        ("ONION", "Onion"),
        ("TOMATO", "Tomato"),
        ("SUGARCANE", "Sugarcane"),
        ("COTTON", "Cotton"),
        ("MUSTARD", "Mustard"),
        ("WHEAT", "Wheat"),
        ("BEAN", "Bean"),
        ("CITRUS", "Citrus"),
        ("MAIZE", "Maize"),
        ("MELON", "Melon"),
        ("RICE", "Rice"),
        ("POTATO", "Potato"),
        ("CABBAGE", "Cabbage"),
        ("SOYBEAN", "Soybean"),
        ("BANANA", "Banana"),
    ]

    name = models.CharField(max_length=20, choices=PLANT_CHOICES)

    def __str__(self):
        return f"{self.name}"
    
