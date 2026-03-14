from django.shortcuts import render
from django.db.models import Prefetch, Case, When, Value, CharField
from django.db.models.functions import ExtractYear, ExtractMonth, ExtractWeek
from django.utils.encoding import smart_str
from datetime import date
import calendar
import locale

from .models import Formation, Type, Participant, Session

#Définir la locale en français
# locale.setlocale(locale.LC_TIME, "fr_FR.UTF-8")

def plan_formation(request):
    #Récupérer la dernière session pour définir le mois/année par défaut
    dernier_session = Session.objects.order_by("-d_debut").first()
    if dernier_session:
        mois_defaut = dernier_session.d_debut.month
        annee_defaut = dernier_session.d_debut.year
    else:
        #Calcul du mois en cours
        aujourdhui = date.today()
        mois_defaut = aujourdhui.month
        annee_defaut = aujourdhui.year

    #Récupération des filtres dans la requête
    annee = request.GET.get('annee')
    mois =  request.GET.get('mois')
    semaine = request.GET.get('semaine')
    intitule  = request.GET.get('intitule')

    groupes = Session.objects.all().select_related('formation').prefetch_related('participant')

    #Application des filtres
    if annee:
        groupes = groupes.filter(d_debut__year=annee)
    else:
        groupes = groupes.filter(d_debut__year=annee_defaut, d_debut__month=mois_defaut)
    if mois:
        groupes = groupes.filter(d_debut__month=mois)
    if semaine:
        groupes = groupes.annotate(week=ExtractWeek('d_debut')).filter(week=semaine)

    if intitule:
        groupes = groupes.filter(formation__intitule=intitule)

    #Pour les dropdowns (filtres)
    mois_fr = ["", "Janvier", "Février", "Mars", "Avril", "Mai", "Juin", "Juillet", "Août", "Septembre", "Octobre", "Novembre", "Décembre"]
    #initiation du mois en français
    annees = Session.objects.annotate(y=ExtractYear('d_debut')).values_list('y', flat=True).distinct().order_by('y')
    mois_nums = Session.objects.annotate(m=ExtractMonth('d_debut')).values_list('m', flat=True).distinct().order_by('m')
    #mois_list = [smart_str(calendar.month_name[m].capitalize(), encoding='utf-8', strings_only=False, errors='strict') for m in mois_nums] 

    mois_list = (
        Session.objects
        .annotate(m=ExtractMonth('d_debut'))
        .annotate(
            mois_nom=Case(
                *[When(m=i, then=Value(mois_fr[i])) for i in range(1, 13)],
                output_field=CharField()
            )
        )
        .values_list('m', 'mois_nom')
        .distinct()
        .order_by('m')
    )
   
    #semaines = Session.objects.annotate(s=ExtractWeek('d_debut')).values_list('s', flat=True).distinct().order_by('s')
    semaines = (Session.objects.annotate(y=ExtractYear("d_debut"), w=ExtractWeek('d_debut')).values_list('w', flat=True).distinct().order_by('w'))
    #intitules = Formation.objects.values_list('intitule', flat=True).distinct().order_by('intitule')
    intitules = Formation.objects.values_list('intitule', flat=True).distinct().order_by('intitule')
    #Types filtrés = seulement ceux qui ont au moins 1 participant avec session filtrée 
    types = Type.objects.filter(participant__sessions__in=groupes).distinct().prefetch_related(
        Prefetch(
            'participant_set',
            queryset=Participant.objects.prefetch_related(
                Prefetch(
                    'sessions',
                    queryset=groupes.select_related('formation')
                )
            )
        )
    )

    #Pour éviter des appels DB supplémentaires
    groupes_pks = set(groupes.values_list('pk', flat=True))

    #Construire pour chaque type: session_for_type (list) et, pour chaque session, participants_for_type (list)
    for t in types:
        sessions_map = {}
        #Parcours des participants déjà prefetchés 
        for participant in getattr(t, 'participant_set').all():
            for session in getattr(participant, 'sessions').all():
                if session.pk not in groupes_pks:
                    continue
                if session.pk not in sessions_map:
                    session.participants_for_type = []
                    sessions_map[session.pk] = session
                
                sessions_map[session.pk].participants_for_type.append(participant)

        #Trier les sessions(optionnel) par date/heure/intitulé/groupe pour affichage cohérent
        sorted_sessions = sorted(
            sessions_map.values(),
            key=lambda s: (s.d_debut or date.min, s.h_debut or 0, (s.formation.intitule if s.formation else ''), s.groupe or '')
        )
        t.sessions_for_type = sorted_sessions

    context = {
        "types": types,
        "groupes":groupes,
        "annees": annees,
        "mois_list": mois_list,
        "semaines": semaines,
        "intitules": intitules,
        "filters": {
            "annee": annee if annee is not None else annee_defaut, #int(annee) if annee else annee_defaut,
            "mois": mois if mois is not None else mois_defaut, #int(mois) if mois else mois_defaut,
            "semaine": semaine, #int(semaine) if semaine else None,
            "intitule": intitule,
        }
    }
    
    return render(request, "planformation.html", context)

       