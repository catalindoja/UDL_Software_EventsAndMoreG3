from django.contrib import admin
from . models import *
# Register your models here.
admin.site.register(WebUser)
admin.site.register(Cliente)
admin.site.register(Gestor)
admin.site.register(Stand)
admin.site.register(Event)
admin.site.register(PeticionStand)
