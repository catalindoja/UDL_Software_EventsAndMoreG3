# Generated by Django 4.0.3 on 2022-05-26 08:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EventsAndMore', '0011_merge_20220526_0833'),
    ]

    operations = [
        migrations.AddField(
            model_name='incidenciasservadicional',
            name='category',
            field=models.CharField(choices=[('Missing', 'Mi servicio adicional no ha llegado'), ('Bugged', 'Mi servicio adicional no funciona correctamente'), ('Wrong', 'Mi servicio adicional no es el que pedí'), ('Broken', 'Mi servicio adicional se ha roto'), ('Help', 'Necesito ayuda para usar el servicio adicional'), ('Other', 'Miscelánea')], default='default', max_length=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='incidenciasservadicional',
            name='checked',
            field=models.BooleanField(default=False),
        ),
    ]
