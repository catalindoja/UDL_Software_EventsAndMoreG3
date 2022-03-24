from django.db import models


# Create your models here.
class User(models.Model):
    username = models.CharField(primary_key=True, max_length=30)

    def __str__(self):
        return str(self.username)


class Cliente(User):
    CIF = models.CharField(primary_key=True, max_length=9)

    def __str__(self):
        return str(self.CIF)


class Admin(User):
    ROLES = (
        ("Gestor", "Gestor de stands"),
        ("Direccion", "Personal de direccion"),
        ("Serv Adicionales", "Departamento de servicios adicionales")
    )
    role = models.CharField(choices=ROLES, max_length=100)

    def __str__(self):
        return str(self.role)
