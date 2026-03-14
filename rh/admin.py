from django.contrib import admin

# Register your models here.
from .models import Rh

class RhAdmin(admin.ModelAdmin):
    list_display = ['id', 'absence', 'effectif', 'date']
    search_fields=['date']
    list_filter = ['date']
admin.site.register(Rh,RhAdmin)
