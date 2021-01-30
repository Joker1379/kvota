from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User

def index(request, userid):
    data = {}
    data["uobj"] = User.objects.get(id = userid)
    return render(request, 'profile.html', data)

def exit(request):
    data = {}
    logout(request)
    return redirect('/')