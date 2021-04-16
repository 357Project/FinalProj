from django.forms import ModelForm
from inventory.models import Location

# Create the form class.
class LocationForm(ModelForm):
    class Meta:
        model = Location
        fields = ['dealership', 'name', 'address', 'city', 'province', 'postal_code', 'description']