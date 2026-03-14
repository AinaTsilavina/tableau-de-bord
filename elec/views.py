from django.shortcuts import render
from django.db.models import Max
from datetime import date, timedelta
from collections import defaultdict
from itertools import groupby
from operator import itemgetter

from .models import Temperature_armoire

def info_temperature(request):
    # Filtres
    filtre_site = request.GET.get("site")
    filtre_periode = request.GET.get("periode", "tous")
    filtre_statut = request.GET.get("statut")

    # Récupération de la dernière date
    derniere_date = Temperature_armoire.objects.aggregate(Max('date'))['date__max']

    if derniere_date:
        annee = derniere_date.year
        date_debut_defaut = date(annee, 1, 1)
        date_fin_defaut = date(annee, 12, 31)

        if filtre_periode == "semaine":
            date_debut = derniere_date - timedelta(days=6)
            date_fin = derniere_date
        elif filtre_periode == "mois":
            date_debut = derniere_date.replace(day=1)
            date_fin = derniere_date
        else:
            date_debut = date_debut_defaut
            date_fin = date_fin_defaut

        temperatures = Temperature_armoire.objects.filter(date__range=(date_debut, date_fin))

        if filtre_site:
            temperatures = temperatures.filter(batiment=filtre_site)

        dates = sorted(temperatures.values_list('date', flat=True).distinct(), reverse=True)

        tableau = {}
        for temp in temperatures:
            key = (temp.batiment, temp.num, temp.local, temp.cat, temp.element)
            if key not in tableau:
                tableau[key] = {
                    'batiment': temp.batiment,
                    'armoire': temp.num,
                    'emplacement': temp.local,
                    'designation': temp.cat,
                    'composant': temp.element,
                    'temperatures': {},
                    'statut': '✅ OK'
                }
            tableau[key]['temperatures'][temp.date] = temp.temperature

        for ligne in tableau.values():
            temp_derniere_date = ligne['temperatures'].get(derniere_date)
            if temp_derniere_date and temp_derniere_date > 79:
                ligne['statut'] = '🚨 Critique'
            else:
                ligne['statut'] = '✅ OK'

        if filtre_statut:
            tableau = {
                k: v for k, v in tableau.items()
                if (filtre_statut == "critique" and v['statut'] == '🚨 Critique') or
                   (filtre_statut == "ok" and v['statut'] == '✅ OK')
            }

    else:
        dates, tableau = [], {}

    sites_disponibles = Temperature_armoire.objects.values_list('batiment', flat=True).distinct()

    # Regrouper en site_list
    grouped_by_site = defaultdict(list)
    for ligne in tableau.values():
        grouped_by_site[ligne['batiment']].append(ligne)

    site_list = []
    for site, lignes_site in grouped_by_site.items():
        # Trier pour groupby
        lignes_site.sort(key=lambda x: (x['armoire'], x['emplacement'], x['designation']))
        
        lignes_regroupees = []

        # Regroupement final pour calcul de rowspan
        for armoire_key, lignes_armoire in groupby(lignes_site, key=itemgetter('armoire')):
            lignes_armoire = list(lignes_armoire)

            for emplacement_key, lignes_emplacement in groupby(lignes_armoire, key=itemgetter('emplacement')):
                lignes_emplacement = list(lignes_emplacement)

                for designation_key, lignes_designation in groupby(lignes_emplacement, key=itemgetter('designation')):
                    lignes_designation = list(lignes_designation)
                    rowspan = len(lignes_designation)
                    # Marque la première ligne avec un rowspan
                    for idx, ligne in enumerate(lignes_designation):
                        ligne['show_site'] = False
                        ligne['show_armoire'] = False
                        ligne['show_emplacement'] = False
                        ligne['show_designation'] = False
                        ligne['designation_rowspan'] = 1

                        if idx == 0:
                            ligne['show_designation'] = True
                            ligne['designation_rowspan'] = rowspan
                    lignes_regroupees.extend(lignes_designation)

        # Appliquer le rowspan pour site et armoire
        for idx, ligne in enumerate(lignes_regroupees):
            if idx == 0 or ligne['armoire'] != lignes_regroupees[idx-1]['armoire']:
                ligne['show_armoire'] = True
                ligne['armoire_rowspan'] = sum(1 for l in lignes_regroupees if l['armoire'] == ligne['armoire'])
            if idx == 0:
                ligne['show_site'] = True
                ligne['site_rowspan'] = len(lignes_regroupees)

        site_list.append({
            'site': site,
            'list': lignes_regroupees,
        })        


    context = {
        'dates': dates,
        'site_list': site_list,
        'sites': sites_disponibles,
        'range_30': range(1, 31),
    }

    return render(request, 'infotemperature.html', context)
