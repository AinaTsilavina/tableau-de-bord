from django.shortcuts import render
from django.db.models import Avg, Count, Max, F
from django.db.models.functions import TruncWeek, TruncMonth
from .models import Production, Chaine
import calendar, locale
from collections import defaultdict

#Définir la locale en français
# locale.setlocale(locale.LC_TIME, 'fr_FR.UTF-8')


Op = {'jour': F('date'), 'semaine': TruncWeek('date'), 'mois': TruncMonth('date')}

# Methodes python

# Traitement des données du model 'Chaine' pour qu'il affiche les resultats par 'jour', 'semaine', 'mois'
# paramètre: 'choix', type: string, default_value: 'jour'
# valeur de retour: dictionnaire, content: queryset prod_chaine, queryset prod_depart, list periode
def traitement_chaine(choix= 'jour', nb_valeur=5):
    prod = Chaine.objects.values('num_chaine__chef_depart', 'num_chaine_id', periode = Op[choix]).annotate(eff = Avg('efficience'))
    list_periode = list(reversed(prod.values_list('periode', flat=True).order_by('-periode').distinct()[:nb_valeur]))
    prod_chaine = prod.filter(periode__in=list_periode)
    prod_depart = prod_chaine.values('num_chaine__chef_depart', 'periode').annotate(eff = Avg('efficience')).order_by('num_chaine__chef_depart')
    #Liste de tuples contenant la période brute + formatée
    periodes_formatees = []
    for periode in list_periode:
        if choix == 'semaine':
            periode_str =  f"Semaine {periode.isocalendar()[1]}"
        elif choix == 'mois':
            periode_str = calendar.month_name[periode.month].capitalize()
        else:
            periode_jour = periode.strftime("%d %B %Y")
            periode_str = periode_jour[0:3] + periode_jour[3:].capitalize()
        
        periodes_formatees.append({
            'brut': periode,
            'formate': periode_str
        })

    #Dictionnaire chart chaine
    eff_dict = defaultdict(dict)
    for item in prod_depart:
        chef = item['num_chaine__chef_depart']
        periode = item['periode']
        eff = item['eff']
        eff_dict[chef][periode] = eff

    return {
        'chaine': prod_chaine, 
        'departement': prod_depart,
        'periode': periodes_formatees,
        'eff_dict': eff_dict
    }


# Traitement des données du model 'Produciton' pour qu'il affiche les resultats par 'jour', 'semaine', 'mois'
# paramètre:'choix', type: string, default_value: 'jour'
# valeur de retour: objet, type: queryset , content: 'efficience', 'efficience moyenne', 'retouche', 'second_choix'
def traitement_prod(choix= 'jour'):
    prod = Production.objects.values(periode = Op[choix]).annotate(eff = Avg('efficience'), moyen = Avg('effimoyen'), retouche = Avg('retouche'), second_choix = Avg('second_choix'))
    return prod

# Methodes de views
def info_production(request):
    #Autre methode pour le production genéral (avec appel de fonction)
    prod_jour = traitement_prod().order_by('-periode')[:5]
    prod_semaine1 = traitement_prod(choix='semaine').order_by('-periode__year', '-periode')[:5]
    prod_semaine = list(reversed(prod_semaine1))
    prod_mois = traitement_prod(choix='mois').order_by('-periode__year', 'periode')

    #Production chaine
    chaine_jour = traitement_chaine()
    chaine_hebdo = traitement_chaine('semaine')
    chaine_mois = traitement_chaine('mois')

    context = {
        'prod_jour': prod_jour,
        'prod_semaine': prod_semaine,
        'prod_mois': prod_mois,
        'prod_chaine': {'Journalier':chaine_jour, 'Hebdomadaire': chaine_hebdo, 'Mensuel': chaine_mois}
    }
    return render(request, 'infoproduction.html',context)
