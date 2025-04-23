from django.contrib import admin
from django.urls import path, include
from . import TestBot

app_name='Comunication'

urlpatterns = [
    path(f'{TestBot.TOKEN_ID}/',TestBot.webhook_view,name='indirizzamento'),
    path('set/',TestBot.set_webhook,name='settare')
    
]
