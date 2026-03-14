from django.core.validators import RegexValidator
from django.db import models

class Certification(models.Model):
    id = models.CharField(primary_key=True, max_length=25, verbose_name="IDENTIFIANT")
    detail = models.TextField(null=True, verbose_name="DETAIL")

    def __str__(self):
        return str(self.id)
    
class Legende(models.Model):
    id = models.IntegerField(primary_key=True, verbose_name="IDENTIFIANT")
    description = models.CharField(max_length=250, verbose_name="DESCRIPTION")
    couleur = models.CharField(max_length=250, verbose_name="COULEUR")
    hex_validator = RegexValidator(
        regex=r'^#?([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$',
        message="Le code couleur doit être en format hexadécimal (ex: #FFFFFF ou FFFFFF)"
    )
    cd_couleur = models.CharField(max_length=7, validators=[hex_validator], verbose_name="CODE COULEUR")

    def __str__(self):
        return str(self.id)


class Audit(models.Model):
    id = models.AutoField(primary_key=True, verbose_name="IDENTIFIANT")
    type = models.CharField(max_length=250, verbose_name="TYPE")
    certificat = models.ForeignKey("Certification", on_delete=models.SET_NULL, null=True, verbose_name="CERTIFICATIONS")
    date = models.DateField(verbose_name="DATE DERNIER AUDIT")
    service = models.CharField(max_length=250, null=True, verbose_name="SERVICE")
    resultat = models.ForeignKey("Legende", on_delete=models.SET_NULL, null=True, verbose_name="RESULTAT")

    def formatted_date(self):
        return self.date.strftime("%B %Y") 

    def __str__(self):
        return str(self.id)
    

class Non_conformite(models.Model):
    id = models.AutoField(primary_key=True, verbose_name="IDENTIFIANT")
    type = models.CharField(max_length=50, verbose_name="TYPE")
    nombre = models.IntegerField(verbose_name="NOMBRE", default=0)
    audit = models.ForeignKey("Audit", on_delete=models.SET_NULL, null=True, verbose_name="AUDIT")

    def __str__(self):
        return str(self.id)