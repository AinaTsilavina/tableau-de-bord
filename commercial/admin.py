from django.contrib import admin
from django import forms
from .models import Solde_cmd, Client, Production

class ClientAdmin(admin.ModelAdmin):
    list_display = ['id', 'nom']
    search_fields = ['id', 'nom']
    list_filter = ['id']
admin.site.register(Client, ClientAdmin)

class ProdAdmin(admin.ModelAdmin):
    list_display = ['id', 'prod', 'moyenne', 'client', 'date']
    search_fields = ['id', 'client', 'date']
    list_filter = ['client', 'date']
admin.site.register(Production, ProdAdmin)

class ProdAdminForm(forms.ModelForm):
    class Meta:
        model = Production
        fields = '__all__'

class SoldeCmdAdminForm(forms.ModelForm):
    class Meta:
        model = Solde_cmd
        fields = '__all__'
        widgets = {
            'annee': forms.Select(choices=[(i, i) for i in range(2100, 1979, -1)]),
        }

class Solde_cmdAdmin(admin.ModelAdmin):
    form = SoldeCmdAdminForm
    list_display = ['id', 'client', 's_bateau', 's_avion', 'solde', 'cmd_mere', 'semaine', 'annee']
    search_fields = ['id', 'client', 'semaine', 'annee']
    list_filter = ['client', 'semaine', 'annee']
admin.site.register(Solde_cmd, Solde_cmdAdmin)
