from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from .managers import AutotracksUserManager
class Dealership(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    date_created = models.DateField(auto_now_add=True)

class AutotracksUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = AutotracksUserManager()

    def __str__(self):
        return self.email

class DealershipUser(models.Model):
    dealership = models.ForeignKey(Dealership, on_delete=models.CASCADE)
    user = models.ForeignKey(AutotracksUser, on_delete=models.CASCADE)
    role = models.CharField(max_length=20)
