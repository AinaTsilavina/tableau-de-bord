from django.shortcuts import render
from django.db.models import Q

from .models import Famille

def info_planning(request):
    #valeurs = Famille.objects.filter(moyenne__lt=0).order_by("-chaine","id") Valeur négatif
    valeurs = Famille.objects.filter(Q(moyenne__lt = -300) | Q(moyenne__gt = 300)).order_by("-chaine","id") # lt inferieur à, gt supérieur à

    context = {
        'valeur': valeurs,
    }

    return render(request, 'infoplanning.html', context)
