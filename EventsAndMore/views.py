from re import template
from django.shortcuts import redirect, render, get_object_or_404
from datetime import date
from django.shortcuts import redirect, render
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
        form.save()
        return redirect('home')


class StandsListView(ListView):
    model = Stand
    paginate_by = 50
    template_name = "standsList.html"

    def get_queryset(self):
        return Stand.objects.filter(idEvento__stand__id=self.kwargs['pk'])


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
    if request.method == "POST":
        form = FilterEvents(request.POST)
        if form.is_valid():
            nombre = form.cleaned_data['nombre']
            fecha_ini = form.cleaned_data['fecha_ini']
            fecha_fin = form.cleaned_data['fecha_fin']
            #if nombre != null:
            #if form.is_valid():
            eventos = Event.objects.filter(nombre__contains=nombre)
            dictionary = {'eventos': eventos, 'form': form}
            return render(request, 'events.html', dictionary)
    else:
        form = FilterEvents()
        eventos = Event.objects.all()
        dictionary = {'eventos': eventos, 'form': form }
        return render(request, 'events.html',  dictionary)


def EventViewSpecific(request,idEvent):
    evento = Event.objects.get(pk=int(idEvent))
    dictionary = {'evento': evento}
    return render(request, 'eventSpecific.html', dictionary)


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
            gestores = Gestor.objects.all()
            my_gestor = None
            for g in gestores:
                if g.User.username == request.user.username:
                    my_gestor = g
            form.instance.gestorUsername = my_gestor
            if form.is_valid():
                if form.instance.estado is True:
                    stand = Stand.objects.get(id=form.instance.idStand.id)
                    stand.occupied = True
                    stand.save()
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
            if peticion.clientUsername == Cliente.objects.get(User=request.user):
                if peticion.estado is True and peticion.revisado is True:
                    peticion.estado_peticion = 'Aceptada'
                elif peticion.revisado is True and peticion.estado is False:
                    peticion.estado_peticion = 'Denegada'
                else:
                    peticion.estado_peticion = 'Pendiente de revision'
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
            print(peticion)
            gestores = Gestor.objects.all()
            my_gestor = None
            for g in gestores:
                if g.User.username == request.user.username:
                    my_gestor = g
            if peticion.revisado is True and peticion.gestorUsername == my_gestor:
                print("entra")
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


def IncidencesView(request):
    if request.method == "POST":
        form = FilterIncidences(request.POST)
        if form.is_valid():
            nombre = form.cleaned_data['Stand_Incidenced']
            incidences_all = StandIncidence.objects.all()
            incidences_filter = incidences_all.filter(Stand_Incidenced__icontains=nombre)
            content = {'StandIncidence_List': incidences_filter,
                       'User': request.user.username,
                       'form': form
                       }
            return render(request, 'incidences.html', content)
    else:
        form = FilterIncidences()
        template_name = 'incidences.html'
        StandIncidence_List = StandIncidence.objects.all()
        content = {'StandIncidence_List': StandIncidence_List,
                   'User': request.user.username,
                   'form': form
        }
        return render(request, 'incidences.html', content)


def RequestView(request):
    if request.user.is_client:
        peticiones = PeticionStand.objects.all()
        arr_peticiones = []
        for peticion in peticiones:
            if peticion.clientUsername == Cliente.objects.get(User=request.user):
                if peticion.estado is True and peticion.revisado is True:
                    peticion.estado_peticion = 'Aceptada'
                elif peticion.revisado is True and peticion.estado is False:
                    peticion.estado_peticion = 'Denegada'
                else:
                    peticion.estado_peticion = 'Pendiente de revision'
                arr_peticiones.append(peticion)
        dictionary = {'peticiones': arr_peticiones}
        return render(request, 'request.html', dictionary)
    else:
        print("Error el user no es un cliente")
        return redirect('/')


class SendStandIncidenceView(CreateView):
    model = StandIncidence
    form_class = SendStandIncidenceForm
    template_name = 'send_stand_incidence.html'

    def form_valid(self, form):
        my_user = Cliente.objects.all()
        for users in my_user:
            if users.User.username == self.request.user.username:
                my_client = users

        form.instance.Client_Username = my_client
        form.save()
        return redirect('incidences')


def PreviousIncidencesView(request):
    StandIncidence_List = StandIncidence.objects.all()
    content = {'StandIncidence_List': StandIncidence_List,
               'User': request.user.username,
               }
    return render(request, 'previous_incidences.html', content)


def updateIncidenciaStandGestor(request, pk):
    if request.user.is_gestor:
        incidencia = StandIncidence.objects.get(Id=pk)
        form = IncidenciaStandGestorForm(instance=incidencia)

        if request.method == 'POST':
            form = IncidenciaStandGestorForm(request.POST, instance=incidencia)
            gestores = Gestor.objects.all()
            my_gestor = None
            for g in gestores:
                if g.User.username == request.user.username:
                    my_gestor = g

            form.instance.Gestor_Username = my_gestor
            if form.is_valid():
                form.save()
                return redirect('incidences')

        context = {'form':form}
        return render(request, 'lista_incidencias_gestor.html', context)
    else:
        print("Error el user no es un gestor")
        return redirect('/')