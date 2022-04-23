from datetime import date
from django.db import models

from django.contrib.auth.models import AbstractUser
# Create your models here.
# class User(models.Model):
#     username = models.CharField(primary_key=True, max_length=30)

#     def __str__(self):
#         return str(self.username)

#TODO: nos ha dicho que podemos poner dentro de webuser al cliente y al visitante, que no es una guarrada si para uno de los roles tenemos atributos sin usar
class WebUser(AbstractUser):
    is_client = models.BooleanField(default=False)
    is_visitor = models.BooleanField(default=False)


class Cliente(models.Model): #WebUser
    User = models.OneToOneField(WebUser, on_delete=models.CASCADE, primary_key=True)
    CIF = models.CharField(unique=True, max_length=9)

    def __str__(self):
        return f'{self.User}'


class Staff(models.Model): #WebUser
    ROLES = (
        ("Gestor", "Gestor de stands"),
        ("Direccion", "Personal de direccion"),
        ("Serv Adicionales", "Departamento de servicios adicionales"),
        ("Org Events", "Organizador de eventos")
    )
    User = models.OneToOneField(WebUser, on_delete=models.CASCADE, primary_key=True)
    role = models.CharField(choices=ROLES, max_length=100)
    Name = models.CharField(max_length=20)

    def __str__(self):
        return f'{self.role} --- {self.Name}'

class Gestor(models.Model):
    User = models.OneToOneField(WebUser, on_delete=models.CASCADE, primary_key=True)
    Name = models.CharField(max_length=20)

class Event(models.Model):
    Id = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=50)
    Description = models.CharField(max_length=200)
    Date_Init = models.DateField(default=date.today)
    Date_End = models.DateField(default=date.today)

    def __str__(self):
        return f'{self.Name}'

class Stand(models.Model):
    #TODO: guardar tambien el nombre del cliente que se ha robado el stand, cuando lo haga
    Id = models.AutoField(primary_key=True)
    # Current_Event = models.ForeignKey(Event, on_delete=models.CASCADE)
    # Occupied = models.BooleanField()
    Description = models.CharField(max_length=200)

    def __str__(self):
        return f'{self.Id}'

class Distribution(models.Model):
    Id_Stand = models.ForeignKey(Stand, on_delete=models.CASCADE)
    Id_Event = models.ForeignKey(Event, on_delete=models.CASCADE)
    Occupied = models.BooleanField()

    def __str__(self):
        return f'Stand {self.Id_Stand} in Event {self.Id_Event}'

class StandRequest(models.Model):
    Id = models.AutoField(primary_key=True)
    Stand_Requested = models.ForeignKey(Stand, on_delete=models.CASCADE)
    Client_Username = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    Gestor_Username = models.ForeignKey(Gestor, on_delete=models.CASCADE, blank=True, null=True)
    Current_Event = models.ForeignKey(Event, on_delete=models.CASCADE)
    Date = models.DateField(default=date.today)
    Status = models.BooleanField(editable=False, default=False)
    Checked = models.BooleanField(editable=False, default=False)

    def __str__(self):
        return f'Request {self.Id}, Stand {self.Stand_Requested}'

class StandIncidence(models.Model):
    Id = models.AutoField(primary_key=True)
    Stand_Incidenced = models.ForeignKey(Stand, on_delete=models.CASCADE)
    Client_Username = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    Gestor_Username = models.ForeignKey(Gestor, on_delete=models.CASCADE, blank=True, null=True)
    Current_Event = models.ForeignKey(Event, on_delete=models.CASCADE)
    Description = models.TextField(max_length=200)
    Date = models.DateField(default=date.today)
    Status = models.BooleanField(editable=False, default=False)
    Checked = models.BooleanField(editable=False, default=False)

    def __str__(self):
        return f'Incidence {self.Id}, Stand {self.Stand_Incidenced}'

