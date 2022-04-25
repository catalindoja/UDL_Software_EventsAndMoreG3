from re import template
from django.shortcuts import redirect, render, get_object_or_404
from django.shortcuts import render
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView
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


class StandsView(CreateView):
    model = Stand
    fields = ['description']
    template_name = "createStand.html"

    def get_context_data(self, **kwargs):
        kwargs['event_name'] = get_object_or_404(Event, pk=self.kwargs['pk']).nombre
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        form.instance.idEvento = get_object_or_404(Event, pk=self.kwargs['pk'])
        form.instance.occupied = False
        return super(StandsView, self).form_valid(form)


class StandsListView(ListView):
    model = Stand
    paginate_by = 50
    template_name = "standsList.html"

    def get_queryset(self):
        return Stand.objects.filter(idEvento__stand__id=self.kwargs['pk'])
