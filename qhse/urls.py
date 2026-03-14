from django.conf import settings
from django.urls import path

from . import views

app_name = "qhse"

urlpatterns = [
    path('info_qhse', views.info_qhse, name="info_qhse"),
]