from django.db import models
from users.models import Dealership

# Create your models here.
class Vehicle(models.Model):
    dealership = models.ForeignKey(Dealership, on_delete=models.PROTECT)
    serial = models.CharField(max_length=25, unique=True)
    arrived_on = models.DateField(null=True)
    date_added = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(null=True)

class CustomVehicleAttribute(models.Model):
    desc = models.CharField(max_length=100)
    dealership = models.ForeignKey(Dealership, on_delete=models.PROTECT)
    visible_inventory = models.BooleanField(default=False)
    order_position = models.IntegerField(default=0)
    attribute_type = models.CharField(max_length=10)

class VehicleAttribute(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)

class VehicleType(models.Model):
    custom_attribute = models.ForeignKey(CustomVehicleAttribute, on_delete=models.CASCADE)
    vehicle_attribute = models.OneToOneField(VehicleAttribute, on_delete=models.CASCADE)

class StringVehicleAttribute(models.Model):
    vehicle = models.ForeignKey(VehicleAttribute, on_delete=models.CASCADE)
    string_value = models.CharField(max_length=200)

class IntegerVehicleAttribute(models.Model):
    vehicle = models.ForeignKey(VehicleAttribute, on_delete=models.CASCADE)
    integer_value = models.IntegerField(default=0)

class CurrencyVehicleAttribute(models.Model):
    vehicle = models.ForeignKey(VehicleAttribute, on_delete=models.CASCADE)
    decimal_value = models.DecimalField(default=0, decimal_places=2, max_digits=12)

class DateTimeVehicleAttribute(models.Model):
    vehicle = models.ForeignKey(VehicleAttribute, on_delete=models.CASCADE)
    date_time_value = models.DateTimeField(null=True)

class CustomVehicleAttributeOptions(models.Model):
    attribute = models.ForeignKey(CustomVehicleAttribute, on_delete=models.CASCADE)
    option = models.CharField(max_length=100)

