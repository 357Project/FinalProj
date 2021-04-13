from django.shortcuts import render, redirect
from .models import Vehicle, VehicleAttribute, CustomVehicleAttribute, CustomVehicleAttributeOptions, StringVehicleAttribute, IntegerVehicleAttribute, CurrencyVehicleAttribute, DateTimeVehicleAttribute, VehicleType
from users.models import Dealership, DealershipUser
from django.contrib.auth.decorators import login_required

from datetime import date
from decimal import Decimal

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

@login_required(login_url='login')
def add_vehicle(request):
    serial_number = request.POST.get('serial-number')
    arrived_on = request.POST.get('arrived-on')
    print(f"========DEBUG: {arrived_on}==========")
    # get dealership associated to user
    dealership = DealershipUser.objects.filter(user=request.user).first().dealership
    # get custom vehicle attributes
    attributes = CustomVehicleAttribute.objects.filter(dealership=dealership.pk).all()

    # first create the vehicle with default attributes
    # date_added will get automatically created, and last modified is left null for now
    new_vehicle = Vehicle(dealership=dealership, serial=serial_number, arrived_on=arrived_on)
    new_vehicle.save()

    # (OPTIONAL: loop through the fields in the frontend to make sure the data is present before posting the request)

    # for every custom vehicle attribute, get the input from the GET request
    for attribute in attributes:
        input_field = request.POST.get(f'custom-attribute-{attribute.pk}')
        # depending on the attribute type, make some modifications and add them to the right table
        if attribute.attribute_type == 'str':
            # create new vehicle attribute
            new_attribute = VehicleAttribute(vehicle=new_vehicle)
            new_attribute.save()
            # link this attribute to the custom attribute
            new_vehicle_type = VehicleType(custom_attribute=attribute, vehicle_attribute=new_attribute)
            new_vehicle_type.save()
            # add to StringVehicleAttribute
            new_string_attribute = StringVehicleAttribute(vehicle=new_attribute, string_value=input_field)
            new_string_attribute.save()
        elif attribute.attribute_type == 'int':
            # create new vehicle attribute
            new_attribute = VehicleAttribute(vehicle=new_vehicle)
            new_attribute.save()
            # link this attribute to the custom attribute
            new_vehicle_type = VehicleType(custom_attribute=attribute, vehicle_attribute=new_attribute)
            new_vehicle_type.save()
            # add to IntegerVehicleAttribute
            new_integer_attribute = IntegerVehicleAttribute(vehicle=new_attribute, integer_value=int(input_field))
            new_integer_attribute.save()
        elif attribute.attribute_type == 'cur':
            # create new vehicle attribute
            new_attribute = VehicleAttribute(vehicle=new_vehicle)
            new_attribute.save()
            # link this attribute to the custom attribute
            new_vehicle_type = VehicleType(custom_attribute=attribute, vehicle_attribute=new_attribute)
            new_vehicle_type.save()
            # add to CurrencyVehicleAttribute
            # format input into decimal rounded to 2 decimal places
            decimal_value = Decimal(float(input_field))
            rounded_decimal = round(decimal_value, 2)
            new_currency_attribute = CurrencyVehicleAttribute(vehicle=new_attribute, decimal_value=rounded_decimal)
            new_currency_attribute.save()
        elif attribute.attribute_type == 'date':
            # create new vehicle attribute
            new_attribute = VehicleAttribute(vehicle=new_vehicle)
            new_attribute.save()
            # link this attribute to the custom attribute
            new_vehicle_type = VehicleType(custom_attribute=attribute, vehicle_attribute=new_attribute)
            new_vehicle_type.save()
            # add to DateTimeVehicleAttribute
            new_date_time_attribute = DateTimeVehicleAttribute(vehicle=new_attribute, date_time_value=input_field)
            new_date_time_attribute.save()
        else:
            print('Something went wrong, attribute has a wrong attribute type.')
        
    return redirect('view-inventory')