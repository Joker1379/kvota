from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout

def index(request):
    data = {}
    return render(request, 'profile.html', data)

def exit(request):
    data = {}
    logout(request)
    return redirect('/')