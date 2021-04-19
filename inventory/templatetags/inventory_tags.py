from django import template
from inventory.models import CustomVehicleAttributeOptions, CustomVehicleAttribute, VehicleType, StringVehicleAttribute, IntegerVehicleAttribute, CurrencyVehicleAttribute, DateTimeVehicleAttribute, VehicleAttribute

register = template.Library()

def get_attribute_choices(attribute):
    choices = CustomVehicleAttributeOptions.objects.filter(attribute=attribute.pk).all()
    return choices

def is_dropdown(attribute, attribute_pk):
    pk = int(attribute_pk)
    attribute = CustomVehicleAttribute.objects.get(pk=pk)
    return attribute.attribute_type == "drop"

def is_integer(attribute, attribute_pk):
    pk = int(attribute_pk)
    attribute = CustomVehicleAttribute.objects.get(pk=pk)
    return attribute.attribute_type == "int"

def is_currency(attribute, attribute_pk):
    pk = int(attribute_pk)
    attribute = CustomVehicleAttribute.objects.get(pk=pk)
    return attribute.attribute_type == "cur"

def is_date_time(attribute, attribute_pk):
    pk = int(attribute_pk)
    attribute = CustomVehicleAttribute.objects.get(pk=pk)
    return attribute.attribute_type == "date"

def is_visible(attribute, attribute_pk):
    attribute_type = VehicleType.objects.select_related().filter(vehicle_attribute=attribute).first()
    return attribute_type.custom_attribute.visible_inventory

def return_attribute_value(attribute, attribute_pk):
    attribute_type = VehicleType.objects.select_related().filter(vehicle_attribute=attribute_pk).first()
    if attribute_type.custom_attribute.attribute_type == "str" or attribute_type.custom_attribute.attribute_type == "drop":
        # query StringVehicleAttribute
        return StringVehicleAttribute.objects.filter(vehicle_attribute=attribute_pk).first().string_value
    elif attribute_type.custom_attribute.attribute_type == "int":
        # query IntegerVehicleAttribute
        return IntegerVehicleAttribute.objects.filter(vehicle_attribute=attribute_pk).first().integer_value
    elif attribute_type.custom_attribute.attribute_type == "cur":
        # query CurrencyVehicleAttribute
        return CurrencyVehicleAttribute.objects.filter(vehicle_attribute=attribute_pk).first().decimal_value
    elif attribute_type.custom_attribute.attribute_type == "date":
        # query DateTimeVehicleAttribute
        return DateTimeVehicleAttribute.objects.filter(vehicle_attribute=attribute_pk).first().date_time_value
    else:
        return null

def attribute_list(vehicle, vehicle_pk):
    vehicle_attributes = VehicleType.objects.select_related('vehicle_attribute', 'custom_attribute').filter(vehicle_attribute__vehicle=vehicle).order_by('custom_attribute__order_position')
    attributes = []
    for vehicle in vehicle_attributes:
        attributes.append(vehicle.vehicle_attribute)
    return attributes


register.filter('get_choices', get_attribute_choices)
register.filter('is_dropdown', is_dropdown)
register.filter('is_integer', is_integer)
register.filter('is_currency', is_currency)
register.filter('is_date_time', is_date_time)
register.filter('is_visible', is_visible)
register.filter('return_attribute_value', return_attribute_value)
register.filter('attribute_list', attribute_list)