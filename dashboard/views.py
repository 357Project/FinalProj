from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

from inventory.models import Vehicle, VehicleAttribute, CustomVehicleAttribute, CustomVehicleAttributeOptions, Location
from users.models import Dealership, DealershipUser
from .forms import LocationForm

# Create your views here.
@login_required(login_url='login')
def dashboard_view(request):
    context = {
        'homeShow': ' show',
        'dashboardActive': ' active'
    }
    return render(request, 'pages/dashboard.html', context)

@login_required(login_url='login')
def settings_view(request):
    context = {}
    # get the number of custom attributes already created for the dealership associated to this user.
    # first, get dealership associated to account
    dealershipUser = DealershipUser.objects.filter(user=request.user).first()
    if dealershipUser is not None:
        customAttributes = CustomVehicleAttribute.objects.filter(dealership=dealershipUser.dealership.pk).order_by('order_position').all()
        locations = Location.objects.filter(dealership=dealershipUser.dealership).all()
        context = {
            'customAttributes': customAttributes,
            'dealership_pk': dealershipUser.dealership.pk,
            'locations': locations
        }
    return render(request, 'pages/settings.html', context)

@login_required(login_url='login')
def add_vehicle_attribute(request):
    description = request.GET.get('description')
    visible = request.GET.get('visible') == "true"
    attribute_type = request.GET.get('attributeType')
    dealership = DealershipUser.objects.filter(user=request.user).first().dealership
    last_attribute_created = CustomVehicleAttribute.objects.filter(dealership=dealership.pk).order_by('-order_position').first()
    if last_attribute_created is not None:
        last_position = last_attribute_created.order_position
    else:
        last_position = 0
    newAttribute = CustomVehicleAttribute(dealership=dealership, desc=description, visible_inventory=visible, order_position=last_position + 1, attribute_type=attribute_type)
    newAttribute.save()
    if attribute_type == "drop":
        optionString = str(request.GET.get('optionList'))
        optionList = optionString[2:len(optionString)-2].split('","')
        for option in optionList:
            newAttributeOption = CustomVehicleAttributeOptions(attribute=newAttribute, option=option)
            newAttributeOption.save()
    return JsonResponse({'response':'success'})

@login_required(login_url='login')
def delete_vehicle_attribute(request):
    attribute_pk = request.GET.get("attribute_pk")
    attribute = CustomVehicleAttribute.objects.get(pk=attribute_pk)
    attribute.delete()
    return JsonResponse({'response':'success'})

@login_required(login_url='login')
def save_vehicle_attribute(request):
    if request.method == "POST":
        dealership = DealershipUser.objects.filter(user=request.user).first().dealership
        customAttributes = CustomVehicleAttribute.objects.filter(dealership=dealership.pk).all()
        changes = False
        for attribute in customAttributes:
            newAttributeDesc = request.POST.get(f'desc-att-{attribute.pk}')
            newAttributeVisible = request.POST.get(f'visible-att-{attribute.pk}') == "on"
            if newAttributeDesc != attribute.desc and newAttributeDesc is not None:
                attribute.desc = newAttributeDesc
                changes = True
            if newAttributeVisible != attribute.visible_inventory and newAttributeVisible is not None:
                attribute.visible_inventory = newAttributeVisible
                changes = True
            if changes:
                attribute.save()
            changes = False
        new_position = 1
        for field in request.POST:
            if field[0:4] == "desc":
                pk = int(field[9:len(field)])
                customAttribute = CustomVehicleAttribute.objects.get(pk=pk)
                customAttribute.order_position = new_position
                customAttribute.save()
                new_position = new_position + 1

        return redirect('settings')
    else:
        return redirect('settings')

@login_required(login_url='login')
def add_location(request):
    if request.method == "POST":
        form = LocationForm(data=request.POST)
        if form.is_valid():
            form.save()
            print("SAVED")
            return redirect("settings")
        else:
            print("NOT SAVED")
            print(form.errors)
            return redirect("settings")
    else:
        return redirect('settings')