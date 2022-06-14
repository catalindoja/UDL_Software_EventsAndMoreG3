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
    path('incidences/send_stand_incidences/', SendStandIncidenceView.as_view(), name='send_stand_incidence'),
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
    path('send_incidences_additionalServ_client/', send_incidence_additionalServ_client,
         name='send_incidence_additionalServ_client'),
    path('compra_entrada/', EntradaView.as_view(), name='compra_entrada'),
]

urlpatterns += staticfiles_urlpatterns()
