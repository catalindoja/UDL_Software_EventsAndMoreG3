import csv
import io

from django.contrib.auth import login  # eto que éh?
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView, ListView
from django.views.generic.edit import CreateView
from datetime import datetime
# import datetime

from .forms import *
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from django.views import View
from xhtml2pdf import pisa


# Create your views here.
class HomePageView(TemplateView):
    template_name = 'home.html'


class EventsView(TemplateView):
    template_name = 'events.html'


class RegisterView(TemplateView):
    template_name = 'register.html'


class SignupClientView(TemplateView):
    template_name = 'signup_client.html'


class AddServicesSeletionView(TemplateView):
    template_name = 'select_add.html'


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


class SignupVisitorView(CreateView):
    model = WebUser
    form_class = VisitorSignupForm
    template_name = 'signup_visitor.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'visitor'
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
            id = len(Event.objects.all()) + 1
            # fecha_ini = date.today()
            # fecha_fin = date.today()
            new_event = Event(id, nombre, descripcion, fecha_fin, fecha_fin)
            print(new_event)
            form.save()
            return redirect('events')
            # return super(CreateNewEvent).form_valid(form)
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
            # if nombre != null:
            # if form.is_valid():
            eventos = Event.objects.filter(nombre__contains=nombre)
            dictionary = {'eventos': eventos, 'form': form}
            return render(request, 'events.html', dictionary)
    else:
        form = FilterEvents()
        eventos = Event.objects.all()
        dictionary = {'eventos': eventos, 'form': form}
        return render(request, 'events.html', dictionary)


def EventViewSpecific(request, idEvent):
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

    # def update_peticon_stand(self, form, pk):


def eventosPeticionStandGestorList(request):
    if request.user.is_gestor:
        eventos = Event.objects.all()
        dictionary = {'eventos': eventos}
        return render(request, 'lista_eventos_peticion_stand.html', dictionary)
    else:
        print("Error el user no es un gestor")
        return redirect('/')


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
                if form.instance.concedido is True:
                    stand = Stand.objects.get(id=form.instance.idStand.id)
                    stand.occupied = True
                    stand.save()
                form.save()
                return redirect('lista_stands_revisados')

        context = {'form': form}
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
                if peticion.concedido is True and peticion.revisado is True:
                    peticion.estado_peticion = 'Aceptada'
                elif peticion.revisado is True and peticion.concedido is False:
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
                if peticion.concedido is True:
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
        formB = FilterIncidences(request.POST)
        formI = SendStandIncidenceForm(request.POST)
        if formI.is_valid():
            name = request.user.username
            current_user = WebUser.objects.get(username=name)
            current_client = Cliente.objects.get(User=current_user)
            formI.instance.Client_Username = current_client
            formI.save()
            formB = FilterIncidences()
            incidences = StandIncidence.objects.all()
            return redirect('/')
            context = {
                'User': request.user.username,
                'formB': formB,  # añadido pa que no se borre al enviar incidencia
                'formI': formI,
                'incidences': incidences,
            }

            return render(request, 'incidences.html', context)

        if formB.is_valid():
            objstand = formB.cleaned_data['Stand_Incidenced']
            objevent = formB.cleaned_data['Current_Event']
            stand_incidence = objstand.incidencies.filter(Current_Event=objevent)
            # event_incidence =  objevent.evento.all()
            # stand_incidence = stand_incidence.filter(Current_Event=event_incidence)
            formI = SendStandIncidenceForm()
            incidences = StandIncidence.objects.all()
            content = {'StandIncidence_List': stand_incidence,
                       'User': request.user.username,
                       'formB': formB,
                       'formI': formI, # añadido pa que no se borre al filtrar incidencias
                       'incidences': incidences,
                       }
            return render(request, 'incidences.html', content)
    else:
        formB = FilterIncidences()
        formI = SendStandIncidenceForm()
        template_name = 'incidences.html'
        StandIncidence_List = StandIncidence.objects.all()
        incidences = StandIncidence.objects.all()
        content = {'StandIncidence_List': StandIncidence_List,
                   'User': request.user.username,
                   'formB': formB,
                   'formI': formI,
                   'incidences': incidences,
                   }
        return render(request, 'incidences.html', content)


def RequestView(request):
    if request.user.is_client:
        peticiones = PeticionStand.objects.all()
        arr_peticiones = []
        for peticion in peticiones:
            if peticion.clientUsername == Cliente.objects.get(User=request.user):
                if peticion.concedido is True and peticion.revisado is True:
                    peticion.estado_peticion = 'Aceptada'
                elif peticion.revisado is True and peticion.concedido is False:
                    peticion.estado_peticion = 'Denegada'
                else:
                    peticion.estado_peticion = 'Pendiente de revision'
                arr_peticiones.append(peticion)
        dictionary = {'peticiones': arr_peticiones}
        return render(request, 'request.html', dictionary)
    else:
        print("Error el user no es un cliente")
        return redirect('/')

# ESTO ES MÄS INUTIL QUE VOSOTROS ESCRIBIENDO EN CASTELLANO
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
                return redirect('previous_incidences')

        context = {'form': form}
        return render(request, 'lista_incidencias_gestor.html', context)
    else:
        print("Error el user no es un gestor")
        return redirect('/')


def peticionDeEvento(request):
    if request.user.is_organizer:
        if request.method == "POST":
            form = PeticionEventoform(request.POST)
            if form.is_valid():
                motivo = form.cleaned_data['motivo']
                organizador = Organizer.objects.get(User=request.user)
                form.instance.organizerUsername = organizador
                form.save()
                return redirect('Peticion_de_evento')
        else:
            form = PeticionEventoform()
            PeticionesDeEvento = PeticionEvento.objects.all()
            PeticionesDeEvento = PeticionesDeEvento.filter(organizerUsername=Organizer.objects.get(User=request.user))
            context = {'PeticionesDeEvento': PeticionesDeEvento,
                       'form': form
                       }
            return render(request, "peticion_evento.html", context)
    if request.user.is_superuser:
        if request.method == "POST":
            return redirect('/')
        else:
            form = PeticionEventoAdmin()
            PeticionEvento_List = PeticionEvento.objects.all()
            content = {'PeticionEvento_List': PeticionEvento_List,
                       'form': form
                       }
            return render(request, "adminPeticionesEvento.html", content)
    else:
        return redirect('/')

class SelectRequestView(TemplateView):
    template_name = 'select_request.html'



class PeticionServAdicionalClienteView(CreateView):
    model = PeticionServAdicional
    form_class = PeticionServAdicionalClienteForm
    template_name = 'peticion_servicio_adicional_cliente.html'
    def form_valid(self, form):
        if self.request.user.is_client:
            client = Cliente.objects.get(User=self.request.user)
            form.instance.clientUsername = client
            form.save()
            return redirect('/')
        else:
            print("Error, user is not a client")
            return redirect('/')


class PeticionServAdicionalDepartamentoView(CreateView):
    model = PeticionServAdicional
    form_class = PeticionServAdicionalDepartamentoForm
    template_name = 'peticion_servicio_adicional_departamento.html'

    def form_valid(self, form):
        if self.request.user.is_gestor:
            gestor = Gestor.objects.get(User=self.request.user)
            form.instance.gestorUsername = gestor
            form.save()
            return redirect('lista_stands_revisados')
        else:
            print("Error, user is not a gestor")
            return redirect('/')


def updatePeticionServAdicionalDepartamento(request, pk):
    if request.user.is_deptAdditionalServ:
        peticion = PeticionServAdicional.objects.get(id=pk)
        form = PeticionServAdicionalDepartamentoForm(instance=peticion)

        if request.method == 'POST':
            form = PeticionServAdicionalDepartamentoForm(request.POST, instance=peticion)
            additionaldepts = DeptAdditionalServ.objects.all()
            my_dept = None
            for d in additionaldepts:
                if d.User.username == request.user.username:
                    my_dept = d
            form.instance.deptAdditionalServUsername = my_dept
            # print(my_dept)
            if form.is_valid():
                form.save()
                return redirect('/lista_eventos_peticion_serv_adicional/')

        context = {'form': form}
        # return render(request, 'peticion_stand_gestor.html', context)
        # context = {'form':form}
        return render(request, 'peticion_servicio_adicional_departamento.html', context)
    else:
        print("Error el user no es un departamento de servicios adicionales")
        return redirect('/')


def listaPeticionesServAdicionalCliente(request):
    if request.user.is_client:
        peticiones = PeticionServAdicional.objects.all()
        arr_peticiones = []
        for peticion in peticiones:
            if peticion.clientUsername == Cliente.objects.get(User=request.user):
                if peticion.concedido is True and peticion.revisado is True:
                    peticion.estado_peticion = 'Aceptada'
                elif peticion.revisado is True and peticion.concedido is False:
                    peticion.estado_peticion = 'Denegada'
                else:
                    peticion.estado_peticion = 'Pendiente de revision'
                arr_peticiones.append(peticion)
        dictionary = {'peticiones': arr_peticiones}
        return render(request, 'lista_peticiones_serv_adicional_cliente.html', dictionary)
    else:
        print("Error el user no es un cliente")
        return redirect('/')


def eventosPeticionServAdicionalList(request):
    if request.user.is_deptAdditionalServ:
        eventos = Event.objects.all()
        dictionary = {'eventos': eventos}
        return render(request, 'lista_eventos_peticion_serv_adicional.html', dictionary)
    else:
        print("Error el user no es un departamento de servicios adicionales")
        return redirect('/')


def peticionServicioAdicionalDepartamentoList(request, key):
    if request.user.is_deptAdditionalServ:
        peticiones = PeticionServAdicional.objects.all()
        arr_peticiones = []
        for peticion in peticiones:
            if peticion.revisado is False and peticion.idEvento == Event.objects.get(id=key):
                arr_peticiones.append(peticion)
        dictionary = {'peticiones': arr_peticiones}
        return render(request, 'lista_peticiones_dept_servicios_adicionales.html', dictionary)
    else:
        print("Error el user no es un gestor")
        return redirect('/')


def updatePeticionDeEvento(request, pk):
    if request.user.is_superuser:
        peticionEvento = PeticionEvento.objects.get(id=pk)
        form = PeticionEventoAdmin(instance=peticionEvento)

        if request.method == 'POST':
            form = PeticionEventoAdmin(request.POST, instance=peticionEvento)
            if form.is_valid():
                if form.instance.concedido is True:
                    peticionEvento = PeticionEvento.objects.get(id=form.instance.id)
                    peticionEvento.concedido = True
                    peticionEvento.revisado = True
                    peticionEvento.save()
                else:
                    peticionEvento = PeticionEvento.objects.get(id=form.instance.id)
                    peticionEvento.concedido = False
                    peticionEvento.revisado = True
                    peticionEvento.save()
                return redirect('Peticion_de_evento')
        context = {'peticionEvento': peticionEvento,
                   'form': form
                   }
        return render(request, 'peticion_eventoUpdate.html', context)
    else:
        return redirect('/')


class AdditionalServicesView(View):
    def get(self, request):
        template_name = 'additional_services.html'
        return render(request, template_name)

    def post(self, request):
        user = request.user  # get the current login user details
        paramFile = io.TextIOWrapper(request.FILES['additionalServiceFile'].file)
        portfolio1 = csv.DictReader(paramFile, delimiter=';')
        objs = []
        for row in portfolio1:
            print(row)
            objs.append(
                AdditionalService(
                    nombre=row['nombre'],
                    # No se porque pero lee nombre con 'ï»¿' primero, asi que he tenido que apañarlo y poner ï»¿nombre XD
                    descripcion=row['descripcion'],
                    habilitado=bool(row['habilitado']),
                    precio=int(row['precio']),
                    empresa_colaboradora=row['empresa_colaboradora']

                )

            )
        try:
            return redirect('/')
            # buggassssso
            msg = AdditionalService.objects.bulk_create(objs)
            returnmsg = {"status_code": 200}
            print('imported successfully')
        except Exception as e:
            print('Error While Importing Data: ', e)
            returnmsg = {"status_code": 500}

        return JsonResponse(returnmsg)


'''
def incidences_for_deptAdditionalServView(request):
    incidences_list = IncidenciasServAdicional.objects.all()
    category_list = ["Missing", "Bugged", "Wrong", "Broken", "Help"]
    context = {
        'incidences_list': incidences_list,
        'User': request.user.username,
    }

    return render(request, 'incidences_for_deptAdditionalServ.html', context)
'''


def incidences_for_deptAdditionalServView(request):
    incidences_list = IncidenciasServAdicional.objects.all()
    category_list = ["Missing", "Bugged", "Wrong", "Broken", "Help", "Other"]

    context = {
        'incidences_list': incidences_list,
        'User': request.user.username,
        'category_list': category_list,
    }

    return render(request, "incidences_for_deptAdditionalServ.html", context)


def Incidences_for_deptAdditionalServ_DetailView(request, pk):
    incidence = IncidenciasServAdicional.objects.get(id=pk)

    context = {
        'incidence': incidence
    }

    return render(request, 'incidences_for_deptAdditionalServ_details.html', context)


def incidences_deptAdditionalServ_details_editView(request, pk):
    if request.user.is_deptAdditionalServ:
        incidence = IncidenciasServAdicional.objects.get(id=pk)
        form = IncidenciaServicioDeptForm(instance=incidence)

        if request.method == 'POST':
            form = IncidenciaServicioDeptForm(request.POST, instance=incidence)
            depts = DeptAdditionalServ.objects.all()

            my_dept = None
            for d in depts:
                if d.User.username == request.user.username:
                    my_dept = d

            form.instance.deptAdditionalServUsername = my_dept
            if form.is_valid():
                form.save()
                return redirect('incidences_for_deptAdditionalServ')

        context = {'form': form}
        return render(request, 'incidences_deptAdditionalServ_details_edit.html', context)
    else:
        print("Error el user no es miembro del departamento de servicios adocionales ")
        return redirect('/')


def selectIncidenceView(request):
    return render(request, 'select_incidences.html', {})


def send_incidence_additionalServ_client(request):
    if request.method == 'POST':

        form = SendIncidencesAdditionalServClientForm(request.POST)
        name = request.user.username
        current_user = WebUser.objects.get(username=name)
        current_client = Cliente.objects.get(User=current_user)
        form.instance.clientUsername = current_client
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = SendIncidencesAdditionalServClientForm()

    incidences = IncidenciasServAdicional.objects.all()

    context = {
        'form': form,
        'incidences': incidences,
        'User': request.user.username,
    }

    return render(request, 'incidences_additionalServ.html', context)


def billsView(request):
    event_list = Event.objects.all()

    #    print(f'eventos: {event_list}')

    context = {
        'event_list': event_list,
    }

    return render(request, 'bills.html', context)


def eventSelectedView(request, pk):
    client_list = []
    emptyEvent = False

    assitance_list = PeticionStand.objects.all()

    for assistant in assitance_list:

        if assistant.idEvento.pk == pk and assistant.clientUsername not in client_list:
            client_list.append(assistant.clientUsername)

    if len(client_list) == 0:
        emptyEvent = True

    context = {
        'client_list': client_list,
        'idEvent': pk,
        'empty': emptyEvent,
    }

    return render(request, 'event_selected.html', context)


def generatePDFBill(request, pk, pk2):
    event = Event.objects.get(pk=pk)
    client = Cliente.objects.get(pk=pk2)

    total_price = 0
    services_requested = []
    additional_services_list = PeticionServAdicional.objects.all()

    for additional_service in additional_services_list:
        if additional_service.clientUsername == client \
                and additional_service.idEvento == event:
            services_requested.append(additional_service)
            total_price += additional_service.idAdditionalService.precio
            total_price += additional_service.cargoExtra

    stands_requested = []
    stands_list = PeticionStand.objects.all()
    for stand in stands_list:
        if stand.clientUsername == client and stand.idEvento == event:
            stands_requested.append(stand)
            total_price += stand.idStand.price

    request.session['price'] = total_price

    context = {
        'event': event,
        'client': client,
        'services_requested': services_requested,
        'stands_requested': stands_requested,
        'total_price': total_price,
    }
    pdf = render_to_pdf('pdfBills.html', context)
    return HttpResponse(pdf, content_type='application/pdf')


def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None


def prepareBillView(request, pk, pk2):
    event = Event.objects.get(pk=pk)
    client = Cliente.objects.get(pk=pk2)

    total_price = 0
    services_requested = []
    additional_services_list = PeticionServAdicional.objects.all()

    for additional_service in additional_services_list:
        if additional_service.clientUsername == client \
                and additional_service.idEvento == event:
            services_requested.append(additional_service)
            total_price += additional_service.idAdditionalService.precio
            total_price += additional_service.cargoExtra

    stands_requested = []
    stands_list = PeticionStand.objects.all()
    for stand in stands_list:
        if stand.clientUsername == client and stand.idEvento == event:
            stands_requested.append(stand)
            total_price += stand.idStand.price

    request.session['price'] = total_price

    context = {
        'event': event,
        'client': client,
        'services_requested': services_requested,
        'stands_requested': stands_requested,
        'total_price': total_price,
    }
    return render(request, 'prepare_bill.html', context)


def createBillView(request, pk, pk2):
    '''
    ¿Por qué no hacemos la creación de la factura en prepare_bill?
    Porque quizá el manager quiera ver cómo va a ser la factura, pero todavía no quiere generarla,
    porque no ha terminado el evento, o porque faltan cosas por añadirse a la lista de cosas a pagar.
    Also, no lo hago con un CreateView porque se ponen los campos de forma automática,
    y considero que para eso no hace falta poner un form donde no se tenga que tocar nada.
    '''

    created = False
    new_bill = None
    existing_bill = None

    event = Event.objects.get(pk=pk)
    client = Cliente.objects.get(pk=pk2)
    manager = DeptManagement.objects.get(User=request.user)
    price = request.session['price']

    try:
        existing_bill = Bill.objects.get(clientUsername=client, idEvent=event)
        created = True
    except Bill.DoesNotExist:
        new_bill = Bill.objects.create(clientUsername=client, managerUsername=manager, idEvent=event, total_price=price)

    context = {
        'client': client,
        'event': event,
        'bill': new_bill,
        'created': created,
        'existing_bill': existing_bill,
    }

    return render(request, 'create_bill.html', context)


def BillsSearch(request):
    if request.method == "POST":
        formB = BillFilter(request.POST)
        if formB.is_valid():
            # objclient = formB.cleaned_data['clientUsername']
            objevent = formB.cleaned_data['idEvent']
            # objManager = formB.cleaned_data['managerUsername']
            # payed = formB.cleaned_data['payed']
            # date = formB.cleaned_data['date']

            # BillSearch = Bill.objects.all()
            # BillSearch = BillSearch.filter(clientUsername=objclient)
            # stand_incidence = objstand.incidencies.filter(Current_Event=objevent)
            # event_incidence =  objevent.evento.all()
            # stand_incidence = stand_incidence.filter(Current_Event=event_incidence)

            unpayed_bills = [bill for bill in Bill.objects.all()
                             if (bill.payed is False and bill.idEvent == objevent)]

            context = {'unpayed_bills': unpayed_bills,
                       'User': request.user.username,
                       'formB': formB
                       }
            return render(request, 'BillsSearch.html', context)
    else:
        formB = BillFilter()
        template_name = 'incidences.html'
        context = {
            'User': request.user.username,
            'formB': formB,
        }
        return render(request, 'BillsSearch.html', context)


def listBillsView(request):
    unpayed_bills = [bill for bill in Bill.objects.all() if
                     bill.payed is False]

    clients_list = Cliente.objects.all()
    bills_list = Bill.objects.all()

    context = {
        'unpayed_bills': unpayed_bills,
        'bills_list': bills_list,
        'clients_list': clients_list,
    }
    return render(request, 'list_bills.html', context)


def monthlyBalanceView(request):
    final_days = [
        # TODO: deberia poder ser de cualquier año. hacer algo tipo if month and day is tal, then is final day
        datetime(2022, 1, 31),
        datetime(2022, 2, 28),
        # datetime(2022, 2, 29),
        datetime(2022, 3, 31),
        datetime(2022, 4, 30),
        datetime(2022, 5, 31),
        datetime(2022, 6, 30),
        datetime(2022, 7, 31),
        datetime(2022, 8, 31),
        datetime(2022, 9, 30),
        datetime(2022, 10, 31),
        datetime(2022, 11, 30),
        datetime(2022, 12, 31),
    ]
    bill_incomes = []
    ticket_incomes = []
    expenses = []
    new_balance = None
    created = False  # para controlar que solo creemos un balance al mes

    today = datetime.today()
    today = datetime(today.year, today.month, 30)  # TODO: borrar

    empty = False  # Oops! no balances yet.
    balance_list = Balance.objects.all()
    if balance_list is []:
        empty = True

    # miramos si tenemos un balance con la fecha de hoy. Lo hago así por poder usar el mismo tipo de fecha.
    # si hiciera un objects.get(), tendria que buscar con formato datetime.date, y yo tengo datetime.datetime
    for existing_balance in balance_list:
        temp_date = datetime(existing_balance.date.year, existing_balance.date.month, existing_balance.date.day)
        temp_date = today  # TODO: borrar
        if temp_date == today:
            created = True

    if today in final_days and not created:  # si estamos a final de mes:

        first_day = datetime(today.year, today.month, 1)
        # consideramos que los incomes son las entradas vendidas + facturas pagadas
        bills = Bill.objects.all()
        for bill in bills:

            temp_date = datetime(bill.date.year, bill.date.month, bill.date.day)
            # para poder comparar fechas del mismo tipo.
            # bill.date es en formato datetime.date, y el resto son datetime.datetime

            if bill.payed and first_day < temp_date < today:
                # ojo, deberian considerarse diferentes las fechas de emision de factura y la fecha de pago?
                bill_incomes.append(bill)  # agregamos a la lista de ganancias

        tickets = Entrada.objects.all()
        for ticket in tickets:
            temp_date = datetime(ticket.Date.year, ticket.Date.month, ticket.Date.day)
            if first_day < temp_date < today:
                ticket_incomes.append(ticket)
        '''
        tickets = Ticket.objects.all()
        for ticket in tickets:
            temp_date = datetime(ticket.date.year, ticket.date.month, ticket.date.day)
            if ticket.sold and first_day < temp_date < today:
                ticket_incomes.append(ticket)
        '''

        # aqui los gastos dependen mucho.
        # Vamos a suponer que los gastos es lo que vale el servicio,

        services_petition_list = PeticionServAdicional.objects.all()
        for service_petition in services_petition_list:
            temp_date = datetime(service_petition.fecha.year, service_petition.fecha.month, service_petition.fecha.day)
            if first_day < temp_date < today:
                expenses.append(service_petition.idAdditionalService)

        # finalmente, creamos el balance

        new_balance = Balance.objects.create()

        total_incomes = 0.0
        total_expenses = 0.0
        for bill_income in bill_incomes:
            total_incomes += bill_income.total_price
            BalanceIncome.objects.create(idBalance=new_balance, idBill=bill_income, is_bill=True)

        for ticket in ticket_incomes:
            total_incomes += ticket.PRICE_TICKET * ticket.Quantity
            ticket.Price = ticket.PRICE_TICKET * ticket.Quantity
            ticket.save()
            BalanceIncome.objects.create(idBalance=new_balance, idTicket=ticket, is_ticket=True)

        # for ticket in ticket_incomes:
        #     total_incomes += ticket.price
        #     BalanceIncome.objects.create(idBalance=new_balance, idTicket=ticket, is_ticket=True)
        for expense in expenses:
            total_expenses += expense.precio
            BalanceExpense.objects.create(idBalance=new_balance, idService=expense)

        new_balance.incomes = total_incomes
        new_balance.expenses = total_expenses
        new_balance.result = total_incomes - total_expenses
        new_balance.save()

    context = {
        'balance_list': balance_list,
        'empty': empty,
    }

    return render(request, 'monthlyBalance.html', context)


def balanceDetailsView(request, pk):
    balance = Balance.objects.get(id=pk)

    incomes = BalanceIncome.objects.filter(idBalance=balance)
    expenses = BalanceExpense.objects.filter(idBalance=balance)

    context = {
        'balance': balance,
        'incomes': incomes,
        'expenses': expenses,
    }

    return render(request, 'balanceDetails.html', context)


def ticketDetailsView(request, pk, pk2):
    ticket = Entrada.objects.get(id=pk2)

    context = {
        'ticket': ticket,
    }

    return render(request, 'ticketDetails.html', context)


def billDetailsView(request, pk):
    bill = Bill.objects.get(id=pk)

    context = {
        'bill': bill,
    }

    return render(request, 'billDetails.html', context)


def clientBillsView(request):
    empty_bills = False
    empty_unpaid_bills = False

    client_bills = [bill for bill in Bill.objects.all() if
                    bill.clientUsername.User.username == request.user.username]

    unpaid_client_bills = [bill for bill in Bill.objects.all() if
                           bill.clientUsername.User.username == request.user.username and
                           not bill.payed]

    if not unpaid_client_bills:
        empty_unpaid_bills = True
    if not client_bills:
        empty_bills = True

    context = {
        'client_bills': client_bills,
        'unpaid_client_bills': unpaid_client_bills,
        'empty_unpaid_bills': empty_unpaid_bills,
        'empty_bills': empty_bills,
    }

    return render(request, 'clientBills.html', context)


def payBillView(request, pk):
    bill = Bill.objects.get(id=pk)

    if request.method == 'POST':
        form = PayBillForm(request.POST)
        if form.is_valid():
            payment = form.instance.Payment_details
            name = request.user.username
            current_user = WebUser.objects.get(username=name)
            current_client = Cliente.objects.get(User=current_user)
            current_client.Payment_details = payment
            current_client.save()

            bill.payed = True
            bill.save()
            return redirect('/')
    else:
        form = PayBillForm()

    context = {
        'form': form,
        'bill': bill,
    }

    return render(request, 'payBill.html', context)


class EncuestaSatisfaccionView(CreateView):
    model = EncuestaSatisfaccion
    form_class = EncuestaSatisfaccionForm
    template_name = 'encuesta_satisfaccion.html'

    def form_valid(self, form):
        if self.request.user.is_visitor:
            visitor = Visitor.objects.get(User=self.request.user)
            form.instance.visitanteUsername = visitor
            form.save()
            return redirect('/')
        else:
            print("Error, user is not a visitor")
            return redirect('/')


def eventosEncuestaSatisfaccionDeptDireccion(request):
    if request.user.is_deptManagement:
        eventos = Event.objects.all()
        dictionary = {'eventos': eventos}
        return render(request, 'lista_eventos_encuesta_satisfaccion.html', dictionary)
    else:
        print("Error el user no es un departamento de direccion")
        return redirect('/')


# 15/25 * 100


def encuestaSatisfaccionDeptDireccionList(request, key):
    if request.user.is_deptManagement:
        peticiones = EncuestaSatisfaccion.objects.all()
        arr_peticiones = []
        score = 0
        for peticion in peticiones:
            if peticion.idEvento == Event.objects.get(id=key):
                score = (peticion.puntuacion_organizacion_evento
                         + peticion.puntuacion_personal_evento
                         + peticion.puntuacion_informacion_previa_evento
                         + peticion.puntuacion_duracion_evento
                         + peticion.puntuacion_satisfaccion_evento
                         + peticion.puntuacion_interactividad_evento
                         + peticion.puntuacion_organizacion_empresas
                         + peticion.puntuacion_distribucion_stands
                         + peticion.puntuacion_calificacion_evento
                         + peticion.puntuacion_recomendacion_evento)
                score = score / 50 * 100
                # print(score)
                peticion.score = str(score) + "%"
                arr_peticiones.append(peticion)
        dictionary = {'peticiones': arr_peticiones}
        return render(request, 'lista_encuestas_satisfaccion.html', dictionary)
    else:
        print("Error el user no es un gestor")
        return redirect('/')


class EntradaView(CreateView):
    model = Entrada
    fields = ['idEvent', 'Quantity']
    template_name = "compra_entrada.html"

    def form_valid(self, form):
        form.instance.visitor = get_object_or_404(Visitor, User=self.request.user)
        form.instance.Price = form.instance.Quantity * Entrada.PRICE_TICKET
        form.instance.Date = datetime.now()
        form.save()
        return redirect('home')


class AddServicioAdicionalView(CreateView):
    model = AdditionalService
    fields = ['nombre', 'descripcion', 'habilitado', 'precio', 'empresa_colaboradora']
    template_name = "add_additional_service.html"

    def form_valid(self, form):
        form.save()
        return redirect('home')
