from django.shortcuts import render
from .models import Vehicle, VehicleAttribute, CustomVehicleAttribute, CustomVehicleAttributeOptions
from users.models import Dealership, DealershipUser
from django.contrib.auth.decorators import login_required

from datetime import date

# Create your views here.
@login_required(login_url='login')
def view_inventory(request):
    # get dealership associated to user
    dealership = DealershipUser.objects.filter(user=request.user).first().dealership
    # get custom vehicle attributes
    attributes = CustomVehicleAttribute.objects.filter(dealership=dealership.pk, visible_inventory=True).order_by('order_position').all()
    context = {
        'inventoryShow': ' show',
        'viewInventoryActive': ' active',
        'attributes': attributes
    }
    return render(request, 'pages/inventory.html', context)

@login_required(login_url='login')
def add_vehicle_view(request):
    attributes_left = []
    attributes_right = []
    # get dealership associated to user
    dealership = DealershipUser.objects.filter(user=request.user).first().dealership
    # get custom vehicle attributes
    attributes = CustomVehicleAttribute.objects.filter(dealership=dealership.pk).order_by('-order_position').all()
    middle = int(len(attributes) / 2)
    attributes_right = attributes[:middle]
    attributes_left = attributes[middle:]
    context = {
        'inventoryShow': ' show',
        'addVehicleActive': ' active',
        'attributesLeft': attributes_left,
        'attributesRight': attributes_right,
        'date': date.today(),
    }
    return render(request, 'pages/add-vehicle.html', context)
