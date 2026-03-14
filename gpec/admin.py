from django.contrib import admin

from .models import Formation, Session, Participant, Type

@admin.register(Formation)
class FormationAdmin(admin.ModelAdmin):
    list_display = ['id','intitule']
    search_fields = ['id','intitule']
    list_filter = ['id','intitule']

@admin.register(Type)
class TypeAdmin(admin.ModelAdmin):
    list_display = ['id','nom']
    search_fields = ['id','nom']
    list_filter = ['id','nom']

@admin.register(Participant)
class ParticipantAdmin(admin.ModelAdmin):
    list_display = ['mle','nom','prenom','fonction','depart','type']
    search_fields = ['mle','fonction','type__nom']
    list_filter = ['mle','fonction','depart','type']

@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ['code','formation','groupe','d_debut','d_fin','h_debut','h_fin','salle','remarque']
    search_fields = ['code','groupe','d_debut','h_debut','salle','remarque','participant']
    list_filter = ['code','formation','groupe','d_debut','d_fin','h_debut','h_fin','salle','remarque','participant']
    filter_horizontal = ['participant']

