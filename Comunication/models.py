from django.db import models

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
        Telegram.objects.all().delete()
        p_db=Telegram()
        p_db.user_id=str(data)
        p_db.entered=True
        p_db.save()

    def TelegramUser():
        values= Telegram.objects.all()
        print(values)
        return values[0].user_id
        
    
    