from django.db import models

from django.utils import timezone

#Efficience global
class Production(models.Model):
    id = models.AutoField(primary_key=True, verbose_name="Identifiant")
    efficience = models.FloatField(default=0.0, verbose_name="Efficience")
    effimoyen = models.FloatField(default=0.0, verbose_name="Efficience moyenne")
    retouche = models.FloatField(default=0.0, verbose_name="Retouche")
    second_choix = models.FloatField(default=0.0, verbose_name="Second choix")
    date = models.DateField(default=timezone.now,unique=True, verbose_name="Date")
    
    def __str__(self):
        #return str(self.id)
        return f"ID: {self.id} | Date:{self.date} %"
    
#chaine 
class Info_chaine(models.Model):
    num = models.CharField(primary_key=True, max_length=15, verbose_name="Numéro de chaine")
    chef_ch = models.CharField(max_length=100, null=True, verbose_name="Chef de chaine")
    chef_prod = models.CharField(max_length=100, null=True, verbose_name="Chef de production")
    chef_depart = models.CharField(max_length=100, null=True, verbose_name="Chef de departement")

    def __str__(self):
        return str(self.num)
    
#Efficience par chaine     
class Chaine(models.Model):
    id = models.AutoField(primary_key=True, verbose_name="Identifiant")
    num_chaine = models.ForeignKey("Info_chaine", on_delete=models.SET_NULL, null=True, verbose_name="Numéro de chaine")
    efficience = models.FloatField(default=0.0, verbose_name="Efficience")
    retouche = models.FloatField(default=0.0, verbose_name="Retouche")
    date = models.DateField(default=timezone.now, verbose_name="Date")

    def __str__(self):
        return str(self.id)