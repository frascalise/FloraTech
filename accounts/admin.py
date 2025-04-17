from django.contrib import admin
from .models import Garden, Sensor, Raspberry, Water
from .models import Telegram

admin.site.register(Raspberry)
admin.site.register(Garden)
admin.site.register(Water)
admin.site.register(Telegram)
