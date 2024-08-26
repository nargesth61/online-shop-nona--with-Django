from django.shortcuts import render
from django.views.generic import TemplateView
from .models import *
from django.contrib import messages
from django.views.generic import CreateView
from django.shortcuts import redirect
# Create your views here.

class IndexView(TemplateView):
    template_name = "website/index.html" 