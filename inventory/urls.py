from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    path('view/', view_inventory, name='view-inventory'),
    path('add/', add_vehicle_view, name='add-vehicle'),
]