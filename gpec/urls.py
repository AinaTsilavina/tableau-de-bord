from django.conf import settings
from django.urls import path

from . import views

app_name = "gpec"

urlpatterns = [
    path('plan_formation', views.plan_formation, name="plan_formation"),
]