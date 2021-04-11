from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    path('', default_view, name='default'),
    path('login/', login_view, name='login'),
    path('login-user', login_user, name='login-user'),
    path('logout/', logout_user, name='logout'),
    path('forgot-password/', forgot_password, name='forgot-password'),
]