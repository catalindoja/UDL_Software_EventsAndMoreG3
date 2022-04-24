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


class PeticionStandClienteView(CreateView):
    model = PeticionStand
    form_class = PeticionStandClienteForm
    template_name = 'peticion_stand_cliente.html'

    def form_valid(self, form):
        if self.request.user.is_client:
            client = Cliente.objects.get(User=self.request.user)
            form.instance.clientUsername = client
            form.save()
            return redirect('lista_peticiones_cliente')
        else:
            print("Error, user is not a client")
            return redirect('/')


class PeticionStandGestorView(CreateView):
    model = PeticionStand
    form_class = PeticionStandGestorForm
    template_name = 'peticion_stand_gestor.html'

    def form_valid(self, form):
        if self.request.user.is_gestor:
            gestor = Gestor.objects.get(User=self.request.user)
            form.instance.gestorUsername = gestor
            form.save()
            return redirect('lista_stands_revisados')
        else:
            print("Error, user is not a gestor")
            return redirect('/')

    #def update_peticon_stand(self, form, pk):


def eventosPeticionStandGestorList(request):
    if request.user.is_gestor:
        eventos = Event.objects.all()
        dictionary = {'eventos': eventos}
        return render(request, 'lista_eventos_peticion_stand.html', dictionary)
    else:
        print("Error el user no es un gestor")
        return redirect('/')
    return 0


def peticionStandGestorList(request, key):
    if request.user.is_gestor:
        peticiones = PeticionStand.objects.all()
        arr_peticiones = []
        for peticion in peticiones:
            if peticion.revisado is False and peticion.idEvento == Event.objects.get(id=key):
                arr_peticiones.append(peticion)
        dictionary = {'peticiones': arr_peticiones}
        return render(request, 'lista_peticiones_stand.html', dictionary)
    else:
        print("Error el user no es un gestor")
        return redirect('/')


def updatePeticionStandGestor(request, pk):
    if request.user.is_gestor:
        peticion = PeticionStand.objects.get(id=pk)
        form = PeticionStandGestorForm(instance=peticion)

        if request.method == 'POST':
            form = PeticionStandGestorForm(request.POST, instance=peticion)
            gestor = Gestor.objects.get(User=request.user)
            form.instance.gestorUsername = gestor
            if form.is_valid():
                form.save()
                return redirect('lista_stands_revisados')

        context = {'form':form}
        return render(request, 'peticion_stand_gestor.html', context)
    else:
        print("Error el user no es un gestor")
        return redirect('/')


def listaPeticionesCliente(request):
    if request.user.is_client:
        peticiones = PeticionStand.objects.all()
        arr_peticiones = []
        for peticion in peticiones:
            if peticion.revisado is True and peticion.clientUsername == Cliente.objects.get(User=request.user):
                if peticion.estado is True:
                    peticion.estado_peticion = 'Aceptada'
                else:
                    peticion.estado_peticion = 'Denegada'
                arr_peticiones.append(peticion)
        dictionary = {'peticiones': arr_peticiones}
        return render(request, 'lista_peticiones_cliente.html', dictionary)
    else:
        print("Error el user no es un cliente")
        return redirect('/')


def listaStandsAsignadosGestor(request):
    if request.user.is_gestor:
        peticiones = PeticionStand.objects.all()
        arr_peticiones = []
        for peticion in peticiones:
            if peticion.revisado is True and peticion.gestorUsername == Gestor.objects.get(User=request.user):
                if peticion.estado is True:
                    peticion.estado_peticion = 'Aceptada'
                else:
                    peticion.estado_peticion = 'Denegada'
                arr_peticiones.append(peticion)
        dictionary = {'peticiones': arr_peticiones}
        return render(request, 'lista_stands_revisados.html', dictionary)
    else:
        print("Error el user no es un cliente")
        return redirect('/')
