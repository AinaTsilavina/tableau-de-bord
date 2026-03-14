from django.shortcuts import render
from django.db.models import Max

from .models import Transit

def info_transit(request):
    derniere_dates = Transit.objects.aggregate(Max('date'))['date__max']
    valeur = Transit.objects.filter(date= derniere_dates).order_by("type","categ","info")

    context = {
        'valeur': valeur,
        'dat' : derniere_dates,
    }

    return render(request, "infotransit.html", context)

