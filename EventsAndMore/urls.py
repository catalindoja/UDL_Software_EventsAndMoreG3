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

    path('incidences_for_deptAdditionalServ/', incidences_for_deptAdditionalServView,
         name='incidences_for_deptAdditionalServ'),
    path('incidences_for_deptAdditionalServ/<int:pk>/', Incidences_for_deptAdditionalServ_DetailView,
         name='incidences_details'),
    path('incidences_for_deptAdditionalServ/<int:pk>/edit/', incidences_deptAdditionalServ_details_editView,
         name='incidences_details_edit'),
]

urlpatterns += staticfiles_urlpatterns()
