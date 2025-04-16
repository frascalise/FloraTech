import telebot
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Telegram
import json
import os
import json
TOKEN = '7789512707:AAFdHTHgdALOO745NlUPHftmClXrRBUMzjo'
WEBHOOK_URL = 'https://floratech.leonardonels.com/accounts'
USER_ID=903195749 
