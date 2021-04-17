from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    path('view/', view_inventory, name='view-inventory'),
    path('add/', add_vehicle_view, name='add-vehicle-view'),
    path('add-vehicle/', add_vehicle, name='add-vehicle'),
    path('get-attribute-values/', get_attribute_values, name='get-attribute-values'),
    path('get-vehicle-properties/', get_vehicle_properties, name='get-vehicle-properties'),
    path('get-location-properties/', get_location_properties, name='get-location-properties'),
]