from django.db import models

from django.utils import timezone

# Create your models here.
class Rh(models.Model):
    id = models.AutoField(primary_key=True, verbose_name="Identifiant")
    absence = models.IntegerField(default=0, verbose_name="Absence")
    effectif = models.IntegerField(default=0, verbose_name="Effectif")
    date = models.DateField(default=timezone.now, unique=True, verbose_name="Date")

    def __str__(self):
        return str(self.date)