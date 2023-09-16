from django.shortcuts import render

# Create your views here.

def home(request):
    return render(request, "index.html", {})


def user_signup(request):
    return render(request, "signup.html", {})

def user_login(request):
    return render(request, "user_login.html", {})

def user_logout(request):
    return render(request, "user_login.html")