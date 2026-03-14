from django.contrib import admin

from .models import Controle

class ControleAdmin(admin.ModelAdmin):
    list_display = ['id','retouche','second_choix','date']
    search_fields=['date']
    list_filter = ['date']
admin.site.register(Controle,ControleAdmin)