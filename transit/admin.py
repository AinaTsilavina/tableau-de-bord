from django.contrib import admin

from .models import Transit

class TransitAdmin(admin.ModelAdmin):
    list_display = ['id','type','info','categ','valeur','devise','delai','date']
    search_fields = ['id','type']
    list_filter = ['id','type','info','categ','devise','date']
admin.site.register(Transit,TransitAdmin)