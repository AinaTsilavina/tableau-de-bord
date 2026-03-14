from django.contrib import admin
from django.contrib import admin

from .models import Production, Info_chaine, Chaine

#Efficience globale
class ProductionAdmin(admin.ModelAdmin):
    list_display = ['id', 'efficience', 'effimoyen','retouche','second_choix','date']
    search_fields=['date']
    list_filter = ['date']
admin.site.register(Production,ProductionAdmin)

#Chaine
class Info_chaineAdmin(admin.ModelAdmin):
    list_display = ['num', 'chef_ch', 'chef_prod', 'chef_depart']
    search_fields = ['num']
    list_filter = ['num']
admin.site.register(Info_chaine, Info_chaineAdmin)

#Efficience par chaine
class ChaineAdmin(admin.ModelAdmin):
    list_display = ['id', 'num_chaine', 'efficience', 'retouche', 'date']
    search_fields = ['date']
    list_filter = ['num_chaine', 'date']
admin.site.register(Chaine, ChaineAdmin)
