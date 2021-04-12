from django.contrib import admin
from .models import Vehicle, VehicleAttribute, CustomVehicleAttribute, CustomVehicleAttributeOptions, StringVehicleAttribute, IntegerVehicleAttribute,  CurrencyVehicleAttribute, DateTimeVehicleAttribute, VehicleType

# Register your models here.
admin.site.register(Vehicle)
admin.site.register(VehicleAttribute)
admin.site.register(CustomVehicleAttribute)
admin.site.register(CustomVehicleAttributeOptions)
admin.site.register(StringVehicleAttribute)
admin.site.register(IntegerVehicleAttribute)
admin.site.register(CurrencyVehicleAttribute)
admin.site.register(DateTimeVehicleAttribute)
admin.site.register(VehicleType)