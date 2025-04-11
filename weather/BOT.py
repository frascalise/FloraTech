from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from telegram import Bot,Update
from telegram import CommandHandler, MessageHandler, Filters, Dispatcher
import json
@csrf_exempt
def webhook(request):
    # Token del tuo bot Telegram
    TOKEN = '7789512707:AAFdHTHgdALOO745NlUPHftmClXrRBUMzjo'
    bot = Bot(token=TOKEN)
    dispatcher = Dispatcher(bot, update_queue=None, workers=0)

<<<<<<< HEAD
    # Recupera i dati JSON dalla richiesta POST
    data = json.loads(request.body.decode('UTF-8'))
=======
API_TOKEN = ''
>>>>>>> 6fcbf2b674209a2051b08a4c013ba7915347c257

    # Crea l'oggetto Update
    update = Update.de_json(data, bot)

    # Inizializza il dispatcher e registra i gestori
    dispatcher.process_update(update)

    return JsonResponse({"status": "ok"})

def start(update, context):
    update.message.reply_text('Ciao! Sono un bot Telegram integrato con Django!')

def echo(update, context):
    update.message.reply_text(update.message.text)

# Aggiungi i gestori nel dispatcher
Dispatcher.add_handler(CommandHandler("start", start))
Dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

#from telegram import Bot

def set_webhook(request):
    bot = Bot(token='7789512707:AAFdHTHgdALOO745NlUPHftmClXrRBUMzjo')
    webhook_url = 'http://127.0.0.1:8000/weather/webhook/'  # URL del webhook

    # Imposta il webhook
    bot.set_webhook(url=webhook_url)
    return JsonResponse({"status": "webhook set"})
