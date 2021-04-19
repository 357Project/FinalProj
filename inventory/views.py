from django.shortcuts import render, redirect
from .models import Location, VehicleLocation, Vehicle, VehicleAttribute, CustomVehicleAttribute, CustomVehicleAttributeOptions, StringVehicleAttribute, IntegerVehicleAttribute, CurrencyVehicleAttribute, DateTimeVehicleAttribute, VehicleType
from users.models import Dealership, DealershipUser
from django.contrib.auth.decorators import login_required
from django.http.response import JsonResponse

from datetime import date
from decimal import Decimal

# Create your views here.
@login_required(login_url='login')
def view_inventory(request):
    # get dealership associated to user
    dealership = DealershipUser.objects.filter(user=request.user).first().dealership
    # get custom vehicle attributes
    attributes = CustomVehicleAttribute.objects.filter(dealership=dealership.pk, visible_inventory=True).order_by('order_position').all()
    all_attributes = CustomVehicleAttribute.objects.filter(dealership=dealership.pk).order_by('order_position').all()
    all_locations = Location.objects.filter(dealership=dealership.pk).all()
    # query vehicles for dealership
    vehicle_list = Vehicle.objects.filter(dealership=dealership.pk).all()
    context = {
        'inventoryShow': ' show',
        'viewInventoryActive': ' active',
        'attributes': attributes,
        'vehicleList': vehicle_list,
        'allAttributes': all_attributes,
        'allLocations': all_locations,
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
def modify_vehicle_view(request):
    serial_number = ""
    if request.GET.get('serialNumber'):
        serial_number = request.GET.get('serialNumber')
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
        'modifyVehicleActive': ' active',
        'attributesLeft': attributes_left,
        'attributesRight': attributes_right,
        'date': date.today(),
        'serialNumber': serial_number
    }
    return render(request, 'pages/modify-vehicle.html', context)

@login_required(login_url='login')
def add_vehicle(request):
    serial_number = request.POST.get('serial-number')
    arrived_on = request.POST.get('arrived-on')
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
        if attribute.attribute_type == 'str' or attribute.attribute_type == 'drop':
            # create new vehicle attribute
            new_attribute = VehicleAttribute(vehicle=new_vehicle)
            new_attribute.save()
            # link this attribute to the custom attribute
            new_vehicle_type = VehicleType(custom_attribute=attribute, vehicle_attribute=new_attribute)
            new_vehicle_type.save()
            # add to StringVehicleAttribute
            new_string_attribute = StringVehicleAttribute(vehicle_attribute=new_attribute, string_value=input_field)
            new_string_attribute.save()
        elif attribute.attribute_type == 'int':
            # create new vehicle attribute
            new_attribute = VehicleAttribute(vehicle=new_vehicle)
            new_attribute.save()
            # link this attribute to the custom attribute
            new_vehicle_type = VehicleType(custom_attribute=attribute, vehicle_attribute=new_attribute)
            new_vehicle_type.save()
            # add to IntegerVehicleAttribute
            new_integer_attribute = IntegerVehicleAttribute(vehicle_attribute=new_attribute, integer_value=int(input_field))
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
            new_currency_attribute = CurrencyVehicleAttribute(vehicle_attribute=new_attribute, decimal_value=rounded_decimal)
            new_currency_attribute.save()
        elif attribute.attribute_type == 'date':
            # create new vehicle attribute
            new_attribute = VehicleAttribute(vehicle=new_vehicle)
            new_attribute.save()
            # link this attribute to the custom attribute
            new_vehicle_type = VehicleType(custom_attribute=attribute, vehicle_attribute=new_attribute)
            new_vehicle_type.save()
            # add to DateTimeVehicleAttribute
            new_date_time_attribute = DateTimeVehicleAttribute(vehicle_attribute=new_attribute, date_time_value=input_field)
            new_date_time_attribute.save()
        else:
            print('Something went wrong, attribute has a wrong attribute type.')
        
    return redirect('view-inventory')

@login_required(login_url='login')
def modify_vehicle(request):
    serial_number = request.POST.get('serial-number')
    arrived_on = request.POST.get('arrived-on')
    vehicle_pk = request.POST.get('vehicle-pk')

    # first save the vehicle with default attributes
    # date_added will get automatically created, and last modified is left null for now
    old_vehicle = Vehicle.objects.get(pk=vehicle_pk)
    old_vehicle.serial = serial_number
    old_vehicle.arrived_on = arrived_on
    old_vehicle.save()

    attributes = CustomVehicleAttribute.objects.filter(dealership=old_vehicle.dealership).all()
    for attribute in attributes:
        input_field = request.POST.get(f'custom-attribute-{attribute.pk}')

        try:
            vehicle_attribute = VehicleType.objects.select_related('vehicle_attribute').get(custom_attribute=attribute, vehicle_attribute__vehicle=old_vehicle)
            if vehicle_attribute.custom_attribute.attribute_type == "str" or vehicle_attribute.custom_attribute.attribute_type == "drop":
                attribute_value = StringVehicleAttribute.objects.get(vehicle_attribute=vehicle_attribute.vehicle_attribute)
                attribute_value.string_value = input_field
                attribute_value.save()
        except:
            # vehicle attribute doesn't exist yet, create a new one
             if attribute.attribute_type == 'str' or attribute.attribute_type == 'drop':
                # create new vehicle attribute
                new_attribute = VehicleAttribute(vehicle=old_vehicle)
                new_attribute.save()
                # link this attribute to the custom attribute
                new_vehicle_type = VehicleType(custom_attribute=attribute, vehicle_attribute=new_attribute)
                new_vehicle_type.save()
                # add to StringVehicleAttribute
                new_string_attribute = StringVehicleAttribute(vehicle_attribute=new_attribute, string_value=input_field)
                new_string_attribute.save()
    
    return redirect('modify-vehicle-view')

@login_required(login_url='login')
def get_attribute_values(request):
    vehicle_pk = request.GET.get('vehicle_pk')

    values = {}
    attributes = VehicleAttribute.objects.filter(vehicle=vehicle_pk).all()
    for attribute in attributes:
        vehicle_type = VehicleType.objects.select_related().get(vehicle_attribute=attribute)
        if vehicle_type.custom_attribute.attribute_type == "str" or vehicle_type.custom_attribute.attribute_type == "drop":
            values[vehicle_type.custom_attribute.pk] = StringVehicleAttribute.objects.get(vehicle_attribute=attribute).string_value
        elif vehicle_type.custom_attribute.attribute_type == "int":
            values[vehicle_type.custom_attribute.pk] = IntegerVehicleAttribute.objects.get(vehicle_attribute=attribute).integer_value
        elif vehicle_type.custom_attribute.attribute_type == "cur":
            values[vehicle_type.custom_attribute.pk] = CurrencyVehicleAttribute.objects.get(vehicle_attribute=attribute).decimal_value
        elif vehicle_type.custom_attribute.attribute_type == "date":
            values[vehicle_type.custom_attribute.pk] = DateTimeVehicleAttribute.objects.get(vehicle_attribute=attribute).date_time_value
    
    return JsonResponse(values)

@login_required(login_url='login')
def get_vehicle_properties(request):
    vehicle_pk = request.GET.get('vehicle_pk')

    vehicle = Vehicle.objects.get(pk=vehicle_pk)
    date_added = str(vehicle.date_added).split("T")[0].split(" ")[0]
    location = 0
    latitude = "45.5017"
    longitude = "-73.5673"
    try:
        location_object = VehicleLocation.objects.get(vehicle=vehicle.pk)
        location = location_object.location.pk
        latitude = location_object.location.latitude
        longitude = location_object.location.longitude
    except:
        location = 0
    values = {
        'serial': vehicle.serial,
        'date_added': date_added,
        'arrived_on': vehicle.arrived_on,
        'location_pk': location,
        'lat': latitude,
        'long': longitude
    }
    return JsonResponse(values)

@login_required(login_url='login')
def get_location_properties(request):
    location_pk = request.GET.get('location_pk')
    vehicle_pk = request.GET.get('vehicle_pk')

    location = Location.objects.get(pk=location_pk)
    vehicle = Vehicle.objects.get(pk=vehicle_pk)
    try:
        vehicle_location = VehicleLocation.objects.get(vehicle=vehicle)
        vehicle_location.location = location
        vehicle_location.save()
    except:
        vehicle_location = VehicleLocation(location=location, vehicle=vehicle)
        vehicle_location.save()
    latitude = location.latitude
    longitude = location.longitude
    values = {
        'lat': latitude,
        'long': longitude
    }
    return JsonResponse(values)

@login_required(login_url='login')
def search_vehicle_properties(request):
    vehicle_serial = request.GET.get('vehicle_serial')
    vehicle = None
    try:
        vehicle = Vehicle.objects.get(serial=vehicle_serial)
    except:
        return JsonResponse({'result': 'Serial number does not exist.'})
    
    attributes = VehicleAttribute.objects.filter(vehicle=vehicle).all()
    values = {
        'serial': vehicle.serial,
        'arrived_on': vehicle.arrived_on,
        'custom_attributes': {},
        'vehicle_pk': vehicle.pk
    }
    for attribute in attributes:
        vehicle_type = VehicleType.objects.get(vehicle_attribute=attribute)
        if vehicle_type.custom_attribute.attribute_type == "str" or vehicle_type.custom_attribute.attribute_type == "drop":
            values['custom_attributes'][vehicle_type.custom_attribute.pk] = StringVehicleAttribute.objects.get(vehicle_attribute=attribute).string_value
        elif vehicle_type.custom_attribute.attribute_type == "int":
            values['custom_attributes'][vehicle_type.custom_attribute.pk] = IntegerVehicleAttribute.objects.get(vehicle_attribute=attribute).integer_value
        elif vehicle_type.custom_attribute.attribute_type == "cur":
            values['custom_attributes'][vehicle_type.custom_attribute.pk] = CurrencyVehicleAttribute.objects.get(vehicle_attribute=attribute).decimal_value
        elif vehicle_type.custom_attribute.attribute_type == "date":
            values['custom_attributes'][vehicle_type.custom_attribute.pk] = DateTimeVehicleAttribute.objects.get(vehicle_attribute=attribute).date_time_value
    return JsonResponse(values)

@login_required(login_url='login')
def delete_vehicle(request):
    vehicles = request.GET.getlist('vehicle_list[]')
    for vehicle_pk in vehicles:
        vehicle = Vehicle.objects.get(pk=vehicle_pk)
        vehicle.delete()
    return JsonResponse({'results': 'success'})