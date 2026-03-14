from django.db import models

from django.utils import timezone

class Formation(models.Model):
    id = models.AutoField(primary_key=True, verbose_name="Identifiant")
    intitule = models.CharField(max_length=200, unique=True, verbose_name="Intitulé")

    def __str__(self):
        return f"{self.intitule}"
    
    
class Type(models.Model):
    id = models.IntegerField(primary_key=True, verbose_name="Identifiant") 
    nom = models.CharField(max_length=50, verbose_name="Nom")

    def __str__(self):
        return self.nom
    
class Participant(models.Model):
    mle = models.IntegerField(primary_key=True, verbose_name="Matricule")
    nom = models.CharField(max_length=150, verbose_name="Nom")
    prenom = models.CharField(max_length=150, null=True, blank=True, verbose_name="Prénom")
    fonction = models.CharField(max_length=150, verbose_name="Fonction")
    depart = models.CharField(max_length=150, verbose_name="Departement")
    type = models.ForeignKey("Type", on_delete=models.SET_NULL, null=True, verbose_name="Type")

    def __str__(self):
        return f"{self.nom} {self.prenom} ({self.mle})"

class Session(models.Model):
    code = models.CharField(primary_key=True, max_length=10, verbose_name="Code")
    formation = models.ForeignKey("Formation", on_delete=models.SET_NULL, null=True, verbose_name="Formation")
    groupe = models.CharField(max_length=100, verbose_name="Groupe")
    d_debut = models.DateField(default=timezone.now, verbose_name="Date debut")
    d_fin = models.DateField(default=timezone.now, verbose_name="Date fin")
    h_debut = models.TimeField(default=timezone.now, verbose_name="Heure debut")
    h_fin = models.TimeField(default=timezone.now, verbose_name="Heure fin")
    salle = models.CharField(max_length=150, verbose_name="Salle")
    remarque = models.CharField(max_length=200, null=True, blank=True, verbose_name="Remarque")
    participant = models.ManyToManyField(Participant, related_name="sessions", verbose_name="Participants")

    def __str__(self):
        return self.code