from django.shortcuts import render

from django.db.models import OuterRef, Subquery, Count, Sum, Case, When, F, Value, Q
from django.db.models.functions import ExtractYear
from django.http import JsonResponse, HttpResponse, FileResponse
from django.db.models import IntegerField
from datetime import date
import json
from collections import defaultdict

import os
import platform
import subprocess

from .models import Audit, Certification, Legende, Non_conformite

#VUE APRES MODIFICATION
def info_qhse(request):
    certificats =  Certification.objects.all()
    legend = Legende.objects.all()

    #Récupérer toutes les années
    audits = Audit.objects.annotate(year=ExtractYear('date')).values('type', 'certificat__id', 'year').order_by('type', 'certificat__id', '-year')
   
    #Regrouper ces années par (type, certificat)
    grouper_years = defaultdict(list)

    for audit in audits:
        key = (audit['type'], audit['certificat__id'])
        year = audit['year']
        if year not in grouper_years[key] and len(grouper_years[key]) < 2:
            grouper_years[key].append(year)


    #Obtenir toutes les années pertinentes pour filtrage
    filtre_valid_years = Q()
    for (type_audit, id_certif), years in grouper_years.items():
        filtre_valid_years |= (
            Q(audit__certificat_id=id_certif) & 
            Q(audit__type=type_audit) &
            Q(audit__date__year__in=years)
        )


    #Filtrer et grouper les non_conformités correspondants
    val = (Non_conformite.objects.filter(filtre_valid_years)
    .annotate(annee=ExtractYear('audit__date'))
    .values('audit__type', 'audit__certificat__id', 'annee', 'type')
    .annotate(total=Sum('nombre'))
    .order_by('audit__type', 'audit__certificat__id', 'annee', 'type'))

    #Initialisation : (type, certificat, année) -> {'Mineure':total, 'Majeure': total}
    doughnut_data = defaultdict(lambda: {'MINEURE': 0, 'MAJEURE': 0})

    for item in val:
        key = (item['audit__type'], item['audit__certificat__id'], item['annee'])
        nc_type = item['type']
        total = item['total']

        if nc_type in ['MINEURE', 'MAJEURE']:
            doughnut_data[key][nc_type] += total
    
    #Préparation pour le template
    final_data = []
    for (type_audit, certificat, year), types in doughnut_data.items():
        label = f"{type_audit} - {certificat} - {year}"
        mineure = types.get('MINEURE', 0)
        majeure = types.get('MAJEURE', 0)

        if mineure == 0 and majeure == 0:
            final_data.append({
                'label': label,
                'labels': ['Sans Non_conformité'],
                'data': [1],
                'colors': ['#07D01D']
            })
        elif mineure == 0 and majeure != 0:
            final_data.append({
                'label': label,
                'labels': ['MAJEURE'],
                'data': [majeure],
                'colors': ['#FF6567']
            })

        elif majeure == 0 and mineure != 0:
            final_data.append({
                'label': label,
                'labels': ['MINEURE'],
                'data': [mineure],
                'colors': ['#FEEE08'] 
            })
        else:
            final_data.append({
                'label': label,
                'labels': ['MINEURE', 'MAJEURE'],
                'data': [mineure, majeure],
                'colors': ['#FEEE08','#FF6567']
            })

    print("System :" + platform.system())

    context = {
        'doughnut_json': json.dumps(final_data),
        'certificats': certificats,
        'legend': legend,
        'val': val,
    }
    return render(request, "infoqhse.html", context)


