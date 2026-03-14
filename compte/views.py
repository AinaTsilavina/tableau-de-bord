from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.urls import reverse
import json

# Create your views here.
from .models import User

def LoginUser(request):
    return render(request, 'compte/authentification.html')