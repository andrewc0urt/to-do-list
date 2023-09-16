from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import logout

# Create your views here.

def home(request):
    return render(request, "index.html", {})


def user_signup(request):
    return render(request, "signup.html", {})

def user_login(request):
    return render(request, "user_login.html", {})

def user_logout(request):
    logout(request)
    messages.info(request, "You've successfully logged out. Have a great day!")
    return redirect('user_login')