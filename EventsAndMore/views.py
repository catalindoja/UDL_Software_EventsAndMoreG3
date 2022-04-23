from re import template
from datetime import date
from django.shortcuts import redirect, render
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.http import require_POST
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

#def CreateNewEvent(request):
    #   form = CreateEvents()
    #   return render(request, "create_events.html", {'form': form})

def CreateNewEvent(request):
    if request.method == "POST":
        form = CreateEvents(request.POST)
        if form.is_valid():
            nombre = form.cleaned_data['nombre']
            descripcion = form.cleaned_data['descripcion']
            fecha_ini = form.cleaned_data['fecha_ini']
            fecha_fin = form.cleaned_data['fecha_fin']
            id = len(Event.objects.all()) +1
            #fecha_ini = date.today()
            #fecha_fin = date.today()
            new_event = Event(id,nombre,descripcion,fecha_fin,fecha_fin)
            print(new_event)
            form.save()
            return redirect('events')
            #return super(CreateNewEvent).form_valid(form)
    else:
        form = CreateEvents()
    return render(request, "create_events.html", {'form': form})

def EventsViewlist(request):
    eventos = Event.objects.all()
    dictionary = {'eventos': eventos}
    return render(request, 'events.html', dictionary)

#class EventsView(CreateView):
    #model = Event
    #eventos = Event.objects.all()
    #dictionary = {'eventos': eventos}
    #template_name = 'create_events.html'
        #return render(request, 'events.html', dictionary)

#class CreateNewEvent(CreateView):
        #model = Event
        #form_class = CreateEvents
        #template_name = 'create_events.html'

        #def form_valid(self, form):
           #form.instance.user = self.request.user
           #print("HHHHHHHHHHHHHHHHHHHH")
           #return super(CreateNewEvent, self).form_valid(form)