# Generated by Django 3.2 on 2021-04-12 16:16

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0007_alter_vehicletype_vehicle_attribute'),
    ]

    operations = [
        migrations.AddField(
            model_name='vehicle',
            name='arrived_on',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
