from django.utils import timezone
from django.db import models

class Transit(models.Model):
    id = models.AutoField(primary_key=True, verbose_name="Identifiant")
    type = models.CharField(max_length=250, verbose_name="Type")
    info = models.CharField(max_length=250, verbose_name="Information")
    categ = models.CharField(max_length=100, verbose_name="Catégorie")
    valeur = models.FloatField(verbose_name="Valeur")
    devise = models.CharField(max_length=25, verbose_name="Devise")
    delai = models.IntegerField(null=True, verbose_name="Delai")
    date = models.DateField(default=timezone.now,verbose_name="Date d'ajout")

    def __str__(self):
        return str(self.id)
