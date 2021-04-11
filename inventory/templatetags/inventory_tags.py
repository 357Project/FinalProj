from django import template
from inventory.models import CustomVehicleAttributeOptions, CustomVehicleAttribute

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

register.filter('get_choices', get_attribute_choices)
register.filter('is_dropdown', is_dropdown)
register.filter('is_integer', is_integer)
register.filter('is_currency', is_currency)
register.filter('is_date_time', is_date_time)