# Generated by Django 3.2 on 2021-04-19 13:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0016_alter_vehicletype_vehicle_attribute'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vehicletype',
            name='custom_attribute',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='custom_attribute', to='inventory.customvehicleattribute'),
        ),
    ]