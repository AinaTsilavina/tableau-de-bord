from sqlite3 import Date
from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.urls import reverse
import json
from django.shortcuts import get_object_or_404
from django.utils.timezone import localtime
from django.db.models import Max, Avg, Count
from django.utils.timezone import now
from django.db.models import Case, When, Value, CharField
from collections import defaultdict
from django.db.models.functions import ExtractMonth, ExtractWeek, ExtractYear
import calendar
from decimal import Decimal


from production.models import Production, Info_chaine, Chaine
from rh.models import Rh
from elec.models import Temperature_armoire
from commercial.models import Client, Solde_cmd, Production as Prod
from gpec.models import Session

def info_accueil(request):
    #RH
    try:
        rh1 = Rh.objects.order_by('-date')[:5]
        rh = sorted(rh1, key=lambda x : x.date)
    except IndexError:
        rh = 0

    #Calcule pourcentage
    for info in rh:
        info.pourcentage = (info.absence * 100) / info.effectif

    #Production
    try:
        prod1 = Production.objects.order_by('-date')[:3] #Sélectionne les 2 dernieres date
        prod = sorted(prod1, key=lambda x : x.date) #Trier par ordre ascendant
    except IndexError:
        prod = 0

    #Production Chaine
    derniere_date = Chaine.objects.aggregate(Max('date'))['date__max']
    resultats = Chaine.objects.filter(date=derniere_date).values(
        'num_chaine__chef_depart'
    ).annotate(
        moyenne_efficience=Avg('efficience'),
        moyenne_retouche=Avg('retouche'),
        nombre_chaines = Count('num_chaine', distinct=True)
    ).values('num_chaine__chef_depart', 'nombre_chaines', 'moyenne_efficience', 'moyenne_retouche')
   
    #ELEC
    #Récupérer les valeurs de la dernière date
    dernier_date = Temperature_armoire.objects.aggregate(Max('date'))['date__max']
    elec = Temperature_armoire.objects.filter(date=dernier_date).order_by("batiment","num","local","cat")
    #armoires = Temperature_armoire.objects.filter(date=dernier_date).values("batiment","num").distinct().count()
    armoir = Temperature_armoire.objects.filter(date=dernier_date, temperature__gt = 79 ).values("batiment","num","local").distinct().count()
    bat = Temperature_armoire.objects.filter(date=dernier_date).values("batiment").distinct()

    #Récupérer le nombre total d'armoire @toute epsilon
    nb_armoires = Temperature_armoire.objects.values("batiment","num").distinct().count()
    #Taux d'armoire à haut température
    taux_armoir = ( armoir * 100) / nb_armoires

    #CIAL(solde commande)
    valeur_solde = Solde_cmd.objects.order_by('client__id','-annee', '-semaine')
    #Calcule de nombre de jour de production
    for val_solde in valeur_solde: 
        semaine_prec = val_solde.semaine - 1 
        annee_actu = val_solde.annee

        #Cas particulier: si on est en semaine 1 → on recule à la semaine 52 de l'année précédente
        if semaine_prec == 0:
            semaine_prec = 52
            annee_actu -= 1
            
        prod_cli = list(Prod.objects.filter(client=val_solde.client).order_by('-date'))

        prod_prec = None
        for p in prod_cli:
           year, week, _ = p.date.isocalendar()
           if year == annee_actu and week == semaine_prec:
               prod_prec = p
               break

        if prod_prec and prod_prec.moyenne and prod_prec.moyenne > 0:
            val_solde.nb_jours = round(Decimal(val_solde.solde) / Decimal(prod_prec.moyenne), 2)
        else:
            val_solde.nb_jours = None
    
    #GPEC
    today = now().date()
    sessions = (
        Session.objects.filter(d_debut__gte=today)
        .annotate(
            y=ExtractYear("d_debut"),
            m=ExtractMonth("d_debut"),
            w=ExtractWeek("d_debut"),
        )
        .order_by("d_debut")
    )

    grouped_sessions = defaultdict(list)

    for s in sessions:
        key = (s.formation.intitule, s.d_debut, s.y, s.m, s.w)
        grouped_sessions[key].append({
            "code": s.code,
            "groupe": s.groupe,
        })

    sessions_grouped = []
    for (intitule, date, y, m, w), items in grouped_sessions.items():
        sessions_grouped.append({
            "intitule": intitule,
            "date": date,
            "annee": y,
            "mois": m,
            "semaine": w,
            "details": items,   # liste des codes/groupes
        })

    context = {
        'rh': rh, # On stocke l'information dans le contexte pour l'afficher dans la vue
        'prod': prod,  # On stocke l'information dans le contexte pour l'afficher dans la vue
        'date_ch': derniere_date,
        'prod_ch': resultats,
        'elec': elec,
        'armoir': armoir,
        'date_elec': dernier_date,
        'batiments': bat,
        'valeur_solde': valeur_solde,
        'nb_armoires': nb_armoires,
        'taux_armoir': taux_armoir,
        "sessions_grouped": sessions_grouped,
    }
    return render(request, 'accueil.html',context)


def temperature_par_batiment(request):
    batiment = request.GET.get('batiment')
    dernier_date = Temperature_armoire.objects.aggregate(Max('date'))['date__max']

    nbsupparbat = Temperature_armoire.objects.filter(
        date=dernier_date,
        batiment=batiment,
        temperature__gt=79
    ).values("batiment","num","local").distinct().count()

    #Calculer le nombre des armoires par batiment
    nb_armoirbat = Temperature_armoire.objects.filter(batiment=batiment).values("batiment","num").distinct().count()
    #Taux d'armoire haut température par batiment
    taux_armoirbat = (nbsupparbat * 100) / nb_armoirbat

    return JsonResponse({
        'nbsupparbat': nbsupparbat,
        'restant': nb_armoirbat - nbsupparbat,
        'nb_armoirbat': nb_armoirbat,
        'taux_armoirbat': taux_armoirbat,
    })