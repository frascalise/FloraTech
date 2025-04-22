from django.db import models

# Create your models here.
class Telegram(models.Model):
    user_id=models.CharField(max_length=10)
    entered=models.BooleanField(default=False)


    def NewEntrance():
        values= Telegram.objects.all()
        values[0].entered=True
    def ControlEntrance():
        return Telegram.objects.all()[0].entered
            
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
        
    
    