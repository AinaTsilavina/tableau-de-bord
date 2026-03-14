from django.db.models import FloatField, F
from django.db.models.functions import TruncMonth, Cast
from django.db.models import Avg, Sum, IntegerField
from django.shortcuts import render

from .models import Rh

def info_rh(request):
    try:
         rh = Rh.objects.annotate(mois=TruncMonth('date'), pourcentage = Cast(F('absence'), FloatField()) * 100 / Cast(F('effectif'), FloatField()))
    except IndexError:
        rh = 0

    rh_j = rh.order_by('-date')[:3]

    #rh_m = rh.values('mois').annotate(moyen_absence = Avg('absence'), moyen_effectif =Avg('effectif'), taux_abs= Avg('pourcentage')).order_by('-mois')
    rh_m = rh.values('mois').annotate(taux_abs= Avg('pourcentage')).order_by('mois')
    #print(rh_m)



    context = {
        'rh': rh_j, # On stocke l'information dans le contexte pour l'afficher dans la vue
        'rh_m': rh_m,
    }
    return render(request, 'inforh.html',context)
