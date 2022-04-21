from re import template
from django.shortcuts import redirect, render
from django.shortcuts import render
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView, UpdateView
from .models import *
from .forms import *
from django.contrib.auth import login #eto que éh?

# Create your views here.
class HomePageView(TemplateView):
    template_name = 'home.html'

class EventsView(TemplateView):
    template_name = 'events.html'

class RegisterView(TemplateView):
    template_name = 'register.html'

class SignupClientView(TemplateView):
    template_name = 'signup_client.html'

class SignupClientView(CreateView):
    model = WebUser
    form_class = ClientSignupForm
    template_name = 'signup_client.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'client'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        web_user = form.save()
        login(self.request, web_user)
        return redirect('home')