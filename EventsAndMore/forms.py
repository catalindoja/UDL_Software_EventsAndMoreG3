from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from django import forms
from .models import *

class ClientSignupForm(UserCreationForm):
    CIF = forms.CharField(max_length=8, widget=forms.TextInput, required=True)

    class Meta(UserCreationForm.Meta):
        model = WebUser

    @transaction.atomic
    def save(self):
        web_user = super().save(commit=False)
        web_user.is_client = True
        web_user.save()
        client = Cliente.objects.create(User = web_user)
        print(self.data.get('CIF'))
        print(client.CIF)
        client.CIF = self.data.get('CIF')
        client.save()
        print(client.CIF)
        # client.CIF.add(*self.cleaned_data.get('CIF'))
        return web_user# web_user

class CreateEvents(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['nombre', 'descripcion', 'fecha_ini','fecha_fin']
        widgets = {
            #'fecha_ini': DateInput(),
            #'fecha_fin': DateInput(),
        }
        exclude = ['gestorUsername']

    #nombre = forms.CharField(label='Nombre del evento: ', required=True)
    #descripcion = forms.CharField(label='Descripción del evento: ', required=True)
    #data_ini = forms.CharField(label='Data de inició: ', required=True)
    #data_fin = forms.DateField(label='Data de finalización: ', required=True)
    #data_test = forms.DateField(label='TEST: ', required=True)

