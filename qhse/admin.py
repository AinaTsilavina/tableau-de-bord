from django.contrib import admin

from .models import Certification, Legende, Audit, Non_conformite

class CertificationAdmin(admin.ModelAdmin):
    list_display = ['id','detail']
    search_fields = ['id']
    list_filter = ['id']
admin.site.register(Certification,CertificationAdmin)

class LegendeAdmin(admin.ModelAdmin):
    list_display = ['id','description','couleur','cd_couleur']
    search_fields = ['id','couleur']
    list_filter = ['id']
admin.site.register(Legende,LegendeAdmin)

class AuditAdmin(admin.ModelAdmin):
    list_display = ['id','type','certificat','date','service','resultat']
    search_fields = ['id','type','certificat','date','resultat']
    list_filter = ['id','type','certificat','date','resultat']
admin.site.register(Audit,AuditAdmin)

class Non_conformiteAdmin(admin.ModelAdmin):
    list_display = ['id','type','nombre','audit']
    search_fields = ['id','type','audit']
    list_filter = ['id','type','audit']
admin.site.register(Non_conformite,Non_conformiteAdmin)