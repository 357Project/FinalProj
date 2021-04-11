from django.contrib import admin
from .models import Vehicle, VehicleAttribute, CustomVehicleAttribute, CustomVehicleAttributeOptions

# Register your models here.
admin.site.register(Vehicle)
admin.site.register(VehicleAttribute)
admin.site.register(CustomVehicleAttribute)
admin.site.register(CustomVehicleAttributeOptions)