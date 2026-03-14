from django.contrib import admin

from .models import Temperature_armoire

class Temperature_armoireAdmin(admin.ModelAdmin):
    list_display = ['id','batiment','local','num','cat','element','temperature','date']
    search_fields = ['num','date']
    list_filter = ['date']
admin.site.register(Temperature_armoire,Temperature_armoireAdmin)
