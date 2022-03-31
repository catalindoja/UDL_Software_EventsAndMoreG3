from django.shortcuts import render
from django.shortcuts import render
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView, UpdateView
from .models import *


# Create your views here.
class HomePageView(TemplateView):
    template_name = 'home.html'


class EventsView(TemplateView):
    template_name = 'events.html'
