from django.db import models
from .meteo import richiesta_meteo,spacchettamento,update

class Previsione(models.Model):
    dm=models.IntegerField(default=0)
    anno = models.IntegerField(default=2023)
    mese = models.IntegerField(default=12)
    giorno = models.IntegerField(default=4)
    meteo=models.CharField(max_length=50)

    def __str__(self):
        return "ID: " + str(self.pk) + ": Mese="+ str(self.mese) + ", Giorno= " + str(self.giorno)


    class Meta:
        verbose_name_plural = 'Previsione'
   

    def refresh():
        Previsione.objects.all().delete()
        #Previsioni=richiesta_meteo()
        metei,date=update()
        anni,mesi,giorni=spacchettamento(date)
        c=0
        #print(metei)
        for i in giorni:
            p_db=Previsione()
            p_db.pk=(c-3)
            p_db.anno=anni[c]
            p_db.mese=mesi[c]
            p_db.giorno=i
            p_db.meteo=metei[c]
            p_db.save()
            c=c+1
        prevision=Previsione.objects.all()
            
        return 0
    
# Create your models here.
