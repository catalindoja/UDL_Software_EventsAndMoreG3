from django.test import TestCase
from django.contrib.auth.models import *
from .models import *
# Create your tests here.

class UseryCreationTestCase(TestCase):
    def setUp(self):
        user = WebUser.objects.create_user(username='testuser')
        user.is_client = True

    def test_client_creation_and_retrieval(self):
        user = WebUser.objects.get(username='testuser')
        self.assertEqual(user.username, 'testuser')


class StandPetitionTestCase(TestCase):
    def setUp(self):
        event = Event.objects.create(nombre='Event1', descripcion='desc ev 1', fecha_ini='2022-10-15', fecha_fin='2022-10-18')
        client = WebUser.objects.create_user(username='testuser')
        client.is_client = True
        client = Cliente.objects.create(User=client, CIF='333333333')
        gestor = WebUser.objects.create_user(username='testuser2')
        gestor.is_gestor = True
        stand = Stand.objects.create(idEvento=event, occupied=False, description='stand 1')
        peticion = PeticionStand.objects.create(idStand=stand, clientUsername=client, idEvento=event,
                                                fecha='2022-10-15', concedido=False, revisado=False)

    def test_creation_stand_petition(self):
        petition = PeticionStand.objects.get(fecha='2022-10-15')
        self.assertEqual(petition.fecha.strftime('%Y-%m-%d'), '2022-10-15')

    def test_organizer_gives_checked(self):
        gestor = WebUser.objects.get(username='testuser2')
        gestor = Gestor.objects.create(User=gestor)
        petition = PeticionStand.objects.get(fecha='2022-10-15')
        petition.gestorUsername = gestor
        petition.checked = True
        self.assertEqual(petition.checked, True)