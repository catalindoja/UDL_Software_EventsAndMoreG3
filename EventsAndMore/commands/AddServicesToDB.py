# import pandas as pd
# import csv
# from django.core.management.base import BaseCommand
#
# from EventsAndMore.models import AdditionalService
#
# tmp_data_products = pd.readcsv('static/data/services.csv', sep=',', encoding="utf-8").fillna(" ")
#
#
# class Command(BaseCommand):
#     def handle(self, **options):
#         services = [
#             AdditionalService(
#                 nombre=row['nombre'],
#                 descripcion=row['descripcion'],
#                 habilitado=row['habilitado'],
#                 precio=row['precio'],
#                 empresa_colaboradora=row['empresa_colaboradora']
#             )
#             for row in tmp_data_products.iterrows()
#         ]
#
#         AdditionalService.objects.bulk_create(services)