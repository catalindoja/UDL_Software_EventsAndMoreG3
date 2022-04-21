from django.urls import path
from .views import *
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('events/', EventsView.as_view(), name='events'),
    path('create_event/',crear_nuevo_evento),
    path('register/', RegisterView.as_view(), name='register'),
    path('register/signup_client/', SignupClientView.as_view(), name='signup_client'),
]

urlpatterns += staticfiles_urlpatterns()
