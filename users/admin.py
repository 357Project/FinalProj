from django.contrib import admin
from .models import AutotracksUser, Dealership, DealershipUser

# Register your models here.
admin.site.register(AutotracksUser)
admin.site.register(Dealership)
admin.site.register(DealershipUser)
