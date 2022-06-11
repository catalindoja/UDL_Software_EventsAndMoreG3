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
        return web_user  # web_user


class CreateEvents(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['nombre', 'descripcion', 'fecha_ini', 'fecha_fin']
        widgets = {
            # 'fecha_ini': DateInput(),
            # 'fecha_fin': DateInput(),
        }
        exclude = ['gestorUsername']


class FilterEvents(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['nombre', 'fecha_ini', 'fecha_fin']
        widgets = {
            # 'fecha_ini': DateInput(),
            # 'fecha_fin': DateInput(),
        }
        exclude = ['gestorUsername', 'descripcion']


class FilterIncidences(forms.ModelForm):
    class Meta:
        model = StandIncidence
        fields = ['Stand_Incidenced', 'Current_Event']
        widgets = {
        }
        exclude = ['Id', 'Client_Username', 'Gestor_Username', 'Description', 'Date', 'Status', 'Checked']


class PeticionStandClienteForm(forms.ModelForm):
    class Meta:
        model = PeticionStand
        exclude = ['clientUsername', 'gestorUsername', 'concedido', 'revisado']
        # modificar el queryset para dejarlo los datos que te deja


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


class PeticionServAdicionalClienteForm(forms.ModelForm):
    class Meta:
        model = PeticionServAdicional
        exclude = ['clientUsername', 'deptAdditionalServUsername', 'concedido', 'revisado']


class PeticionServAdicionalDepartamentoForm(forms.ModelForm):
    class Meta:
        model = PeticionServAdicional
        exclude = ['deptAdditionalServUsername']


class PeticionEventoform(forms.ModelForm):
    class Meta:
        model = PeticionEvento
        exclude = ['organizerUsername','adminUsername','concedido','revisado']


class PeticionEventoAdmin(forms.ModelForm):
    class Meta:
        model = PeticionEvento
        exclude = ['organizerUsername','adminUsername','nombre','motivo','revisado']


class IncidenciaServicioDeptForm(forms.ModelForm):
    class Meta:
        model = IncidenciasServAdicional
        exclude = ['deptAdditionalServUsername']


class SendIncidencesAdditionalServClientForm(forms.ModelForm):
    class Meta:
        model = IncidenciasServAdicional
        exclude = ['deptAdditionalServUsername', 'fecha', 'solucionado', 'checked', 'clientUsername']


class EncuestaSatisfaccionForm(forms.ModelForm):
    class Meta:
        model = EncuestaSatisfaccion
        exclude = ['visitanteUsername']