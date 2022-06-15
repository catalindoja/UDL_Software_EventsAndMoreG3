from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(WebUser)
admin.site.register(Cliente)
admin.site.register(Gestor)
admin.site.register(Stand)
admin.site.register(Event)
admin.site.register(PeticionStand)
admin.site.register(StandIncidence)
# sprint2
admin.site.register(Organizer)
admin.site.register(DeptAdditionalServ)
admin.site.register(AdditionalService)
admin.site.register(PeticionServAdicional)
admin.site.register(IncidenciasServAdicional)
admin.site.register(PeticionEvento)
admin.site.register(ListaNegra)
# sprint3
admin.site.register(Bill)
admin.site.register(DeptManagement)
admin.site.register(Balance)
admin.site.register(Visitor)
admin.site.register(EncuestaSatisfaccion)

admin.site.register(Entrada)
