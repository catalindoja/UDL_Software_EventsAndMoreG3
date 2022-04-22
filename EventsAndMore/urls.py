from django.urls import path
from .views import *
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('events/', EventsView.as_view(), name='events'),
    path('register/', RegisterView.as_view(), name='register'),
    path('register/signup_client/', SignupClientView.as_view(), name='signup_client'),
    path('peticion_stand_cliente/', PeticionStandClienteView.as_view(), name='peticion_stand_cliente'),
]

urlpatterns += staticfiles_urlpatterns()
