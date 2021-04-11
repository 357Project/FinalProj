from django.shortcuts import render, redirect
from .models import AutotracksUser
from django.contrib.auth import authenticate, login, logout


# Create your views here.
def default_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    else:
        return redirect('landing')

def login_view(request):
    return render(request, 'authentication/basic/login.html')

def login_user(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    else:
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            return redirect('login')

def logout_user(request):
    logout(request)
    return redirect('landing')

def forgot_password(request):
    return redirect('landing')
