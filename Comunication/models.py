from django.db import models

# Create your models here.
class Telegram(models.Model):
    user_id=models.CharField(max_length=10)

    def NewTelegramUser(data):
        print(str(data))

    def TelegramUser():
        print('consegna utente')
    
    