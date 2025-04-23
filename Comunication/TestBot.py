import telebot
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from weather.meteo import update
from FloraTech.views import VerifyTelegramUser,NewEntrance,TelegramIdProvider
import random
import json
TOKEN_ID = '7789512707:AAFdHTHgdALOO745NlUPHftmClXrRBUMzjo'
WEBHOOK_URL = 'https://floratech.leonardonels.com/comunication'
#USER_ID=903195749 
from .models import Telegram
# Inizializza il bot Telegram
bot = telebot.TeleBot(TOKEN_ID)
user_state={}

@bot.message_handler(commands=['start'])
def send_welcome(message):
        if Telegram.ControlEntrance(message.chat.id):
             bot.reply_to(message,'Non serve ricominciare, qui siamo a posto')
        else:
            bot.reply_to(message,"Ciao! Benvenuto su Floratech\n Per dare il via al tuo nuovo fututo verde ti chiedo di eseguire il comando /new")
   

@bot.message_handler(commands=['help'])
def send_help(message):
    if Telegram.ControlEntrance(message.chat.id):
         bot.reply_to(message,'come posso aiutarti?')
    else:
         bot.reply_to(message,'esegui prima /start')

def WarningMessage():
        value=Telegram.TelegramUser(0)
        bot.send_message(value,'Sta per splodere tutto')
    

@bot.message_handler(commands=['new'])
def AddNewUser(message):
        if not Telegram.ControlEntrance(message.chat.id):
            bot.send_message(message.chat.id,'Scrivi il tuo nome utente')
            bot.register_next_step_handler(message,VerifyCode)
        else:
            bot.send_message(message.chat.id,'Risulti già iscritto. Non serve reiscriversi')
def VerifyCode(message):
    if message.text[0]!='/':
        number=random.randint(100000,999999)
        user_state[message.chat.id]={'palla':'345678'}

        user_state[message.chat.id]={'username':message.text}
        value=VerifyTelegramUser(message.text,message.chat.id,number)
        
        if value==1:
            bot.send_message(message.chat.id,f'il tuo codice è 123456')
        
            bot.send_message(message.chat.id,'Scrivi il codice che ti è stato inviato')
            bot.register_next_step_handler(message,Decision)
        else:
            bot.send_message(message.chat.id,'Non risulti presente nel sistema')
    else: bot.reply_to(message,'Non scrivere comandi. Ricomincia')

def Decision(message):
    number='123456'
    if message.text == number:
         NewEntrance(user_state[message.chat.id]['username'],message.chat.id)
         Telegram.NewTelegramUser(message.chat.id)
         bot.send_message(message.chat.id,'accesso avvenuto')
    else:
         bot.send_message(message.chat.id,'accesso negato')

@bot.message_handler(commands=['meteo'])
def MeteoProvider(message):
        if Telegram.ControlEntrance(message.chat.id):
            metei,date=update()
            stringa="PREVISIONI METEO PER I PROSSIMI GIORNI\n"
            for i in range(3):
                 stringa+=f"giorno: {date[i]} sarà {metei[i]}\n"
            bot.send_message(message.chat.id,stringa)
        else:
            bot.reply_to(message,'esegui prima il comando /start')

@bot.message_handler(commands=['write'])
def WriteSomething(message):
    if Telegram.ControlEntrance(message.chat.id):
        #value=Telegram.TelegramUser()
        #value=Telegram.TelegramUser()
        bot.send_message(message.chat.id,'Apelle, figlio di apollo fece una palla di pelle di pollo')
    else:
        bot.reply_to(message, "Ti chiedo di eseguire il comando /new")
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

def Alert(request,problema,username):
    
    #value=Telegram.TelegramUser(telegram_id)
    value=TelegramIdProvider(username)
    match problema:
        case 'sensor' : bot.send_message(value,'[WARNING]\nComunicazione con sensore assente')
        case 'hub': bot.send_message(value,'[WARNING]\nProblems from the Hub')
        case 'storm': bot.send_message(value,'[WARNING]\n A storm is arriving in few hours')
    return HttpResponse(status=200)



