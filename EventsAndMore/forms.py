from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.db import transaction
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
        client = Cliente.objects.create(User=web_user)
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


class FilterEvents(forms.ModelForm):
    class Meta:
        model = Event
        fields = fields = ['nombre', 'fecha_ini','fecha_fin']
        widgets = {
            # 'fecha_ini': DateInput(),
            # 'fecha_fin': DateInput(),
        }
        exclude = ['gestorUsername','descripcion']


class PeticionStandClienteForm(forms.ModelForm):
    class Meta:
        model = PeticionStand
        exclude = ['clientUsername', 'gestorUsername', 'estado', 'revisado']


class PeticionStandGestorForm(forms.ModelForm):
    class Meta:
        model = PeticionStand
        exclude = ['gestorUsername']


class SendStandIncidenceForm(forms.ModelForm):
    class Meta:
        model = StandIncidence
        exclude = ['Gestor_Username', 'Date', 'Status', 'Checked', 'Client_Username']


class IncidenciaStandGestorForm(forms.ModelForm):
    class Meta:
        model = StandIncidence
        exclude = ['Gestor_Username']

class Incidencias2Form(forms.Form):
    class Meta:
        model = StandIncidence
        exclude = ['Gestor_Username', 'Date', 'Status', 'Checked', 'Client_Username']