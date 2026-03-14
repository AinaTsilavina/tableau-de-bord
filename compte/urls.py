from django.conf import settings
from django.urls import path
from .import views

app_name = "compte"

urlpatterns = [
    path('login', views.LoginUser, name="login"),
]