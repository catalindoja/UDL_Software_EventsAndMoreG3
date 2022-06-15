from django.urls import path, reverse

from . import views
from .views import *
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('events/', EventsViewlist, name='events'),
    path('events/event/<idEvent>', EventViewSpecific, name='event_specific'),
    path('create_event/', CreateNewEvent, name='new event'),
    path('register/', RegisterView.as_view(), name='register'),
    path('register/signup_client/', SignupClientView.as_view(), name='signup_client'),
    path('events/<int:pk>/stands/create/', StandsView.as_view(), name='stands'),
    path('events/<int:pk>/stands/', StandsListView.as_view(), name='stands_list'),
    path('peticion_stand_cliente/', PeticionStandClienteView.as_view(), name='peticion_stand_cliente'),
    path('lista_eventos_peticion_stand/', views.eventosPeticionStandGestorList,
         name='lista_eventos_peticion_stand'),
    path('lista_peticiones_stand/<str:key>/', views.peticionStandGestorList, name='lista_peticiones_stand'),
    path('peticion_stand_gestor/<str:pk>/', views.updatePeticionStandGestor, name='peticion_stand_gestor'),
    path('lista_peticiones_cliente/', views.listaPeticionesCliente, name='lista_peticiones_cliente'),
    path('lista_stands_revisados/', views.listaStandsAsignadosGestor, name='lista_stands_revisados'),
    path('incidences/', IncidencesView, name='incidences'),
    #path('incidences/send_stand_incidences/', SendStandIncidenceView.as_view(), name='send_stand_incidence'),
    path('incidences/previous_incidences/', PreviousIncidencesView, name='previous_incidences'),
    path('lista_incidencias_gestor/<str:pk>/', views.updateIncidenciaStandGestor, name='lista_incidencias_gestor'),
    path('request/', RequestView, name='request'),

    path('peticion_serv_adicional_cliente/', PeticionServAdicionalClienteView.as_view(),
         name='peticion_serv_adicional_cliente'),
    path('lista_peticiones_serv_adicional_cliente/', views.listaPeticionesServAdicionalCliente,
         name='lista_peticiones_serv_adicional_cliente'),

    path('peticion_serv_adicional_dept/<str:pk>/', views.updatePeticionServAdicionalDepartamento,
         name='peticion_serv_adicional_dept'),
    path('lista_eventos_peticion_serv_adicional/', views.eventosPeticionServAdicionalList,
         name='lista_eventos_peticion_serv_adicional'),
    path('lista_peticiones_serv_adicional/<str:key>/', views.peticionServicioAdicionalDepartamentoList,
         name='lista_peticiones_serv_adicional'),

    path('peticion_evento/', peticionDeEvento, name='Peticion_de_evento'),
    path('peticion_evento/update/<str:pk>/', updatePeticionDeEvento, name='Update_Peticion_deEvento'),
    path('select_request/', SelectRequestView.as_view(), name='select_request'),

    path('peticion_evento/',peticionDeEvento, name='Peticion_de_evento'),
    path('peticion_evento/update/<str:pk>/',updatePeticionDeEvento, name='Update_Peticion_deEvento'),

    path('additional_services/', AdditionalServicesView.as_view(), name='additional_services'),

    path('incidences_for_deptAdditionalServ/', incidences_for_deptAdditionalServView,
         name='incidences_for_deptAdditionalServ'),
    path('incidences_for_deptAdditionalServ/<int:pk>/', Incidences_for_deptAdditionalServ_DetailView,
         name='incidences_details'),
    path('incidences_for_deptAdditionalServ/<int:pk>/edit/', incidences_deptAdditionalServ_details_editView,
         name='incidences_details_edit'),
    path('select_incidences/', selectIncidenceView, name='select_incidences'),
    path('select_add/', AddServicesSeletionView.as_view(), name='selection_add'),
    path('send_incidences_additionalServ_client/', send_incidence_additionalServ_client,
         name='send_incidence_additionalServ_client'),

    # management Department, 3rd iteration

    # bill generation
    path('bills/', billsView, name='bills'),
    path('bills/eventSelected/<int:pk>/', eventSelectedView, name='eventSelected'),
    path('bills/eventSelected/<int:pk>/<int:pk2>/', prepareBillView, name='prepareBill'),
    path('bills/eventSelected/<int:pk>/<int:pk2>/createBill/', createBillView, name='createBill'),

    # monthly balance generation
    path('monthlyBalance/', monthlyBalanceView, name='monthlyBalance'),
    path('monthlyBalance/<int:pk>/', balanceDetailsView, name='balanceDetails'),
    path('monthlyBalance/<int:pk>/<int:pk2>/', ticketDetailsView, name='ticketDetail'),
    path('monthlyBalance/<int:pk>/<int:pkBill>/', billDetailsView, name='billDetails'),

    path('billDetail/<int:pk>/', billDetailsView, name='billDetailsAux'),

    # client stuff, 3rd iteration

    path('listBills/', listBillsView, name='listBills'),
    path('clientBills/', clientBillsView, name='clientBills'),
    path('clientBills/<int:pk>/', payBillView, name='payBill'),

#TODO: arreglar esta basura en algún momento
    path('listBills/search', BillsSearch, name='listBillsSearcher'),
    path('bills/eventSelected/<int:pk>/<int:pk2>/pdf', generatePDFBill, name="generatePdfBill"),
    path('bills/eventSelected/<int:pk>/<int:pk2>/createBill/pdf', generatePDFBill, name="generatePdfBill"),

    path('encuesta_satisfaccion/', EncuestaSatisfaccionView.as_view(),
         name='encuesta_satisfaccion'),
    path('lista_eventos_encuesta_satisfaccion/', eventosEncuestaSatisfaccionDeptDireccion,
         name='lista_eventos_encuesta_satisfaccion'),
    path('lista_encuestas_satisfaccion/<str:key>/', views.encuestaSatisfaccionDeptDireccionList,
         name='lista_encuestas_satisfaccion'),
    path('compra_entrada/', EntradaView.as_view(), name='compra_entrada'),
    path('añadir_servicio_adicional/', AddServicioAdicionalView.as_view(), name='añadir_servicio_adicional'),

]

urlpatterns += staticfiles_urlpatterns()
