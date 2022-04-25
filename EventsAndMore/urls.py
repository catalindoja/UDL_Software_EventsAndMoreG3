from django.urls import path
from .views import *
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('events/', EventsViewlist, name='events'),
    path('events/event/<idEvent>', EventViewSpecific, name='event_specific'),
    path('create_event/',CreateNewEvent, name='new event'),
    path('register/', RegisterView.as_view(), name='register'),
    path('register/signup_client/', SignupClientView.as_view(), name='signup_client'),
    path('events/<int:pk>/stands/create/', StandsView.as_view(), name='stands'),
    path('events/<int:pk>/stands/', StandsListView.as_view(), name='stands_list'),
]

urlpatterns += staticfiles_urlpatterns()
