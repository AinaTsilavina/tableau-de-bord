from django.db import models

from django.utils import timezone

class Controle(models.Model):
    id = models.AutoField(primary_key=True, verbose_name="Identifiant")
    retouche = models.IntegerField(default=0, verbose_name="Retouche")
    second_choix = models.IntegerField(default=0, verbose_name="Second choix")
    date = models.DateField(default=timezone.now, unique=True, verbose_name="Date")

    def __str__(self):
        return str(self.date)
