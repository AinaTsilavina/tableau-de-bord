from django.db import models

from django.utils import timezone

class Temperature_armoire(models.Model):
    id = models.AutoField(primary_key=True, verbose_name="Identifiant")
    batiment = models.CharField(max_length=100, verbose_name="Batiment")
    local = models.CharField(max_length=250, verbose_name="Localisation")                        
    num = models.IntegerField(verbose_name="Numéro")
    cat = models.CharField(max_length=250, verbose_name="Catégorie")
    element = models.CharField(max_length=100, null=True, blank=True, verbose_name="Elément")
    temperature = models.IntegerField(verbose_name="Température")
    date = models.DateField(default=timezone.now, verbose_name="Date")

    def __str__(self):
        #return str(self.num)
        return f"Numéro: {self.num} | Date:{self.date} %"
