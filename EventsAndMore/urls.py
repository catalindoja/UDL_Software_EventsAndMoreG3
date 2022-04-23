from tkinter import N
from django.urls import path
from .views import *
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('events/', EventsView.as_view(), name='events'),
    path('register/', RegisterView.as_view(), name='register'),
    path('register/signup_client/', SignupClientView.as_view(), name='signup_client'),
    path('incidences/', IncidencesView.as_view(), name='incidences'),
    path('stand_requests/', StandRequestView.as_view(), name='stand_requests'),
    path('stand_distribution/', StandDistributionView, name='stand_distribution'),
]

urlpatterns += staticfiles_urlpatterns()
