from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    path('', dashboard_view, name='dashboard'),
    path('settings/', settings_view, name='settings'),
    path('settings/add-vehicle-attribute/', add_vehicle_attribute, name="add-vehicle-attribute"),
    path('settings/delete-vehicle-attribute/', delete_vehicle_attribute, name="delete-vehicle-attribute"),
    path('settings/save-vehicle-attribute/', save_vehicle_attribute, name="save-vehicle-attribute"),
    path('settings/add-location/', add_location, name='add-location')
]