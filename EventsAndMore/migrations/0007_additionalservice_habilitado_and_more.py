# Generated by Django 4.0.3 on 2022-05-10 10:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('EventsAndMore', '0006_additionalservice_deptadditionalserv_organizer_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='additionalservice',
            name='habilitado',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='standincidence',
            name='Stand_Incidenced',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='incidencies', to='EventsAndMore.stand'),
        ),
    ]
