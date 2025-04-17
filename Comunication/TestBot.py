import telebot
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import os
import json
TOKEN_ID = '7789512707:AAFdHTHgdALOO745NlUPHftmClXrRBUMzjo'
WEBHOOK_URL = 'https://floratech.leonardonels.com/comunication'
USER_ID=903195749 
from .models import Telegram
# Inizializza il bot Telegram
bot = telebot.TeleBot(TOKEN_ID)

# Handler per il comando /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Ciao! Sono un bot webhook Django di prova.")
    print(message.chat.id)

# Handler per il comando /help
@bot.message_handler(commands=['help'])
def send_help(message):
    bot.reply_to(message, "Questo è un bot di prova basato su webhook con Django.")
    value = Telegram.TelegramUser()
    print(value)

def WarningMessage():
    bot.send_message(USER_ID,'Sta per splodere tutto')
    print('qualcosa')

@bot.message_handler(commands=['new'])
def AddNewUser(message):
    #bot.send_message(USER_ID,'Aggiunto nuovo utente')
    Telegram.NewTelegramUser(message.chat.id)
    bot.send_message(USER_ID,'Aggiunto nuovo utente')

@bot.message_handler(commands=['write'])
def WriteSomething(message):
    
    bot.send_message(USER_ID,'Apelle, figlio di apollo fece una palla di pelle di pollo')

@csrf_exempt 
def webhook_view(request):
    if request.method == 'POST':
        try:
            json_string = request.body.decode('utf-8')
            update = telebot.types.Update.de_json(json_string)
            bot.process_new_updates([update])
            return HttpResponse(status=200)
        except Exception as e:
            print(f"Errore durante la ricezione del webhook: {e}")
            return HttpResponse(status=500)
    else:
        return HttpResponse('OK', status=200)

# Funzione per impostare il webhook (da eseguire una sola volta o tramite un comando Django custom)
def set_webhook(request):
    bot.set_webhook(url=f"{WEBHOOK_URL}/{TOKEN_ID}/")
    print(f"Webhook impostato su: {WEBHOOK_URL}/{TOKEN_ID}")
    return HttpResponse(status=200)

# Funzione per eliminare il webhook (utile per passare al polling o per debug)
def delete_webhook():
    bot.delete_webhook()
    print("Webhook eliminato.")



