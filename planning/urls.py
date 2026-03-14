from django.conf import settings
from django.urls import path
from . import views

app_name = "planning"

urlpatterns = [
    path('info_planning', views.info_planning, name="info_planning"),
]