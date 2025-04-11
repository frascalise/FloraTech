import telebot

API_TOKEN = ''

bot = telebot.TeleBot(API_TOKEN)


# Handle '/start' and '/help'
@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    bot.reply_to(message, """\
Ciao a tutti bastardi!!\
""")


# Handle all other messages with content_type 'text' (content_types defaults to ['text'])
@bot.message_handler(func=lambda message: True)
def echo_message(message):
    if(message.text=='Ciao'):
        bot.reply_to(message, 'Sparati')
    elif(message.text=='come sei gentile'):
        bot.reply_to(message,'grazie culattacchione')


bot.infinity_polling()




