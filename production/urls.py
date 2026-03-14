from django.conf import settings
from django.urls import path

from . import views

app_name = "production"

urlpatterns = [
    path('info_production', views.info_production, name="info_production"),
]