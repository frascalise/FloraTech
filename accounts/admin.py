from django.contrib import admin
from .models import Garden, Sensor, Raspberry
admin.site.register(Raspberry)
admin.site.register(Garden)
admin.site.register(Sensor)

# Register your models here.
