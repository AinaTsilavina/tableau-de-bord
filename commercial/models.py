from decimal import Decimal
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver

# Client
class Client(models.Model):
    id = models.IntegerField(primary_key=True, verbose_name="Identifiant")
    nom = models.CharField(max_length=50, verbose_name="Nom")

    def __str__(self):
        return str(self.id)
    
#Production par jour
class Production(models.Model):
    id = models.AutoField(primary_key=True, verbose_name="Identifiant")
    prod = models.IntegerField(null=True, blank=True, verbose_name="Production")
    moyenne = models.IntegerField(null=True, blank=True, verbose_name="Production moyenne")
    client = models.ForeignKey("Client", on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Client")
    date = models.DateField(verbose_name="Date de production")

    class Meta:
        constraints = [models.UniqueConstraint(fields=['date','client'], name="unique_prod_client")]

    def __str__(self):
        return str(self.id)
    
# Solde
class Solde_cmd(models.Model):
    id = models.AutoField(primary_key=True, verbose_name="Identifiant")
    client = models.ForeignKey("Client", on_delete =models.SET_NULL, null=True, verbose_name="Client")
    s_bateau = models.IntegerField(verbose_name="Solde Bateau")
    s_avion = models.IntegerField(verbose_name="Solde Avion")
    solde = models.IntegerField(verbose_name="Solde")
    cmd_mere = models.IntegerField(verbose_name="Commande mère")
    semaine = models.IntegerField(verbose_name="Semaine")
    annee = models.IntegerField(choices=[(i, i) for i in range(1980, 2101)], verbose_name="Année", default=2025)

    class Meta:
        constraints = [models.UniqueConstraint(fields=['annee','semaine','client'], name="unique_solde_semaine")]

    def __str__(self):
        return str(self.semaine)
    
