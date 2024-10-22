from django.contrib import admin
from .models import Garden, Subgarden, Sensor

# Register your models here.
admin.site.register(Garden)
admin.site.register(Subgarden)
admin.site.register(Sensor)