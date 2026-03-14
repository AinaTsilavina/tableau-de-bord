from django.db import models

# Create your models here.

class Famille(models.Model):
    id = models.IntegerField(primary_key=True, verbose_name="FAMILLE")
    chaine = models.CharField(max_length=255, verbose_name="CHAINE FAMILLE")
    references = models.TextField(null=True, default="", verbose_name="REFERENCES")
    moyenne = models.IntegerField(verbose_name="MOYENNE")

    #Méthode d'ajout préfixe FAMILLE sur id
    @property
    def famille_name(self):
        return f"FAMILLE {self.id}"
      #  return f"{self.chaine} {self.id}"

    @property
    def list_ref(self):
        refs = self.references.split()
        return ["; ".join(refs[i:i+3]) for i in range(0, len(refs), 3)]
    
    def __str__(self):
        return str(self.id)