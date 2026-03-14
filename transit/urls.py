from django.conf import settings
from django.urls import path

from . import views

app_name = "transit"

urlpatterns = [
    path('info_transit', views.info_transit, name="info_transit"),
]