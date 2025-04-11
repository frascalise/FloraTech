from django.contrib import admin
from .models import Garden, Sensor, Raspberry, Water
admin.site.register(Raspberry)
admin.site.register(Garden)
admin.site.register(Water)

# Register your models here.
