from django.db import models
from .meteo import richiesta_meteo,spacchettamento,update

class Previsione(models.Model):
    dm=models.IntegerField(default=0)
    AMG=models.CharField(max_length=50,default='2023-04-04')
    codici=models.IntegerField(default=0)
    temp_max=models.FloatField(default=15.5)
    temp_min=models.FloatField(default=0.1)

    def __str__(self):
        return "ID: " + str(self.pk)


    class Meta:
        verbose_name_plural = 'Previsione'
   
    def stampa():
        stampe=Previsione.objects.all()
        dati_meteo=[]
        for i in stampe:
            dati_meteo.append(i)
        return dati_meteo
    def refresh():
        Previsione.objects.all().delete()
        #Previsioni=richiesta_meteo()
        metei,date=update()
        #anni,mesi,giorni=spacchettamento(date)
        c=0
        #print(metei)
        for i in metei:
            p_db=Previsione()
            p_db.pk=(c-3)
            p_db.AMG=date[c]
            p_db.codici=i
            p_db.save()
            c=c+1
        prevision=Previsione.objects.all()
            
        return 0
    
# Create your models here.
