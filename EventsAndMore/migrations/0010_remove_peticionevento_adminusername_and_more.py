# Generated by Django 4.0.3 on 2022-05-24 07:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EventsAndMore', '0009_merge_20220524_0747'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='peticionevento',
            name='adminUsername',
        ),
        migrations.RemoveField(
            model_name='peticionevento',
            name='idEvento',
        ),
        migrations.AddField(
            model_name='peticionevento',
            name='concedido',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='peticionevento',
            name='nombre',
            field=models.CharField(default='default', max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='peticionevento',
            name='revisado',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='webuser',
            name='is_organizer',
            field=models.BooleanField(default=False),
        ),
    ]
