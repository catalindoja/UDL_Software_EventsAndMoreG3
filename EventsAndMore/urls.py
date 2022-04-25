
from django.urls import path, reverse
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
    path('stand_requests/send_stand_request/', SendStandRequestView.as_view(), name='send_stand_request'),
    path('stand_requests/previous_requests/', PreviousRequestsView, name='previous_requests'),
    path('incidences/send_stand_incidences/', SendStandIncidenceView.as_view(), name='send_stand_incidence'),
    path('incidences/previous_incidences/', PreviousIncidencesView, name='previous_incidences'),
]

urlpatterns += staticfiles_urlpatterns()
