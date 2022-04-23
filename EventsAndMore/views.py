
from datetime import date
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

class IncidencesView(TemplateView):
    template_name = 'incidences.html'

class StandRequestView(TemplateView):
    template_name = 'stand_requests.html'

def StandDistributionView(request):
    Event_list = Event.objects.all()
    Stand_list = Stand.objects.all()
    Distribution_List = Distribution.objects.all()
    
    today = date.today()
    Active_events_list = []
    for event in Event_list:
        if event.Date_End >= today:
            Active_events_list.append(event)

    for active_event in Active_events_list:
        print(active_event.Name)
    

    context = { 'Event_list' : Active_events_list,
                'Stand_list' : Stand_list,
                'Distribution_List' : Distribution_List,
                }
    return render(request, 'stand_distribution.html', context)

