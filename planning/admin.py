from django.contrib import admin

from .models import Famille

class FamilleAdmin(admin.ModelAdmin):
    list_display = ['id','chaine','references','moyenne']
    search_fields = ['id','chaine']
    list_filter = ['chaine']
admin.site.register(Famille,FamilleAdmin)