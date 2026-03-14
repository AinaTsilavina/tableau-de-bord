from django.conf import settings
from django.urls import path

from . import views

app_name = "rh"
#from .views import ViewsToBeImported

urlpatterns = [
    path('info_rh', views.info_rh, name='info_rh')
]