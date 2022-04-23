from django.db import models

from django.contrib.auth.models import AbstractUser
# Create your models here.
# class User(models.Model):
#     username = models.CharField(primary_key=True, max_length=30)

#     def __str__(self):
#         return str(self.username)

#TODO: nos ha dicho que podemos poner dentro de webuser al cliente y al visitante, que no es una guarrada si para uno de los roles tenemos atributos sin usar
from django.utils.datetime_safe import date


class WebUser(AbstractUser):
    is_client = models.BooleanField(default=False)
    is_visitor = models.BooleanField(default=False)
    is_gestor = models.BooleanField(default=False)


class Cliente(models.Model): #WebUser
    User = models.OneToOneField(WebUser, on_delete=models.CASCADE, primary_key=True)
    CIF = models.CharField(unique=True, max_length=9)

    def __str__(self):
        return str(self.User)


class Gestor(models.Model):
    User = models.OneToOneField(WebUser, on_delete=models.CASCADE, primary_key=True)

    def __str__(self):
        return str(self.User)


# class Staff(models.Model): #WebUser
#     ROLES = (
#         ("Gestor", "Gestor de stands"),
#         ("Direccion", "Personal de direccion"),
#        ("Serv Adicionales", "Departamento de servicios adicionales"),
#         ("Org Events", "Organizador de eventos")
#      )
#     role = models.CharField(choices=ROLES, max_length=100)
#     Name = models.CharField(max_length=20)
#
#     def __str__(self):
#         return f'{self.role} --- {self.Name}'


class Event(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50, blank=False, null=False)
    descripcion = models.CharField(max_length=200, blank=False, null=False)
    fecha_ini = models.DateField(default=date.today)
    fecha_fin = models.DateField(default=date.today)

    def __str__(self):
        return str(self.nombre)


class Stand(models.Model):
    id = models.AutoField(primary_key=True)
    idEvento = models.ForeignKey(Event, on_delete=models.CASCADE)
    occupied = models.BooleanField(blank=False, null=False)
    description = models.CharField(max_length=200, blank=False, null=False)

    def __str__(self):
        return str(self.description)


class PeticionStand(models.Model):
    id = models.AutoField(primary_key=True)
    idStand = models.ForeignKey(Stand, on_delete=models.CASCADE)
    clientUsername = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    gestorUsername = models.ForeignKey(Gestor, on_delete=models.CASCADE, blank=True, null=True)
    idEvento = models.ForeignKey(Event, default=1, on_delete=models.CASCADE)
    fecha = models.DateField(default=date.today, blank=False, null=False)
    estado = models.BooleanField(default=False)
    revisado = models.BooleanField(default=False)