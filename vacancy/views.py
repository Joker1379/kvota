from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from users.forms import RegistrationForm, LoginForm
from .models import Vacancy

def index(request):
    data = {}
    if request.method == 'POST':
        if request.POST["action"] == "registration":
            form = RegistrationForm(request.POST)
            if form.is_valid():
                user = form.save()
                # Так сожраняются дополнительные поля профиля при регистрации:
                # user.refresh_from_db()
                # user.profile.sex = form.cleaned_data.get('sex')
                # user.save()
                raw_password = form.cleaned_data.get('password1')
                user = authenticate(username=user.username, password=raw_password)
                login(request, user)
                return redirect('/')
        else:
            username = request.POST.get("username")
            password = request.POST.get("password")
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('/')
    data["login"] = LoginForm()
    data["registration"] = RegistrationForm()
    data["vacancy"] = list(reversed(Vacancy.objects.all()))
    data["vlabels"] = [
        "Требуемое образование",
        "Режим работы",
        "Город",
        "Улица",
        "Строение / Расположение офиса",
        "Email",
        "Контактный телефон",
    ]
    return render(request, 'vacancy.html', data)

def delete(request, vid):
    vacancy = Vacancy.objects.get(id = vid)
    vacancy.delete()
    return redirect('/profile/'+str(request.user.id))