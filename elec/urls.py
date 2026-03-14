from django.conf import settings
from django.urls import path, include
from . import views

app_name = "elec"

urlpatterns = [
    path('info_temperature', views.info_temperature, name="info_temperature"),
]