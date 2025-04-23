from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Telegram(models.Model):
    user_id=models.CharField(max_length=10)
    entered=models.BooleanField(default=False)

    def ControlEntrance(data):
        try:
            value=Telegram.objects.get(user_id=str(data)).entered
        except Telegram.DoesNotExist:
            value=False
        return value
            
    def NewTelegramUser(data):
        #Telegram.objects.all().delete()
        presente=False
        p_db=Telegram.objects.all()
        for i in p_db:
            if i.user_id==str(data):
                presente=True
        if not presente:
            p_db2=Telegram()
            p_db2.user_id=str(data)
            p_db2.entered=True
            p_db2.save()
            return "aggiunto"
        else: return "già presente"

    def TelegramUser(index):
        values= Telegram.objects.all()
        #print(values)
        return values[index].user_id
        
    
    