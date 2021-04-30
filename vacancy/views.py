from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from users.forms import RegistrationForm, LoginForm
from .forms import VacancySearch
from .models import Vacancy

V_L = ['Требуемое образование', 'Режим работы', 'Город', 'Улица', 'Строение / Расположение офиса', 'Email', 'Контактный телефон']

def index(request):
    data = {}
    if request.method == 'POST':
        if request.POST['action'] == 'registration':
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
        elif request.POST['action'] == 'login':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('/')
        elif request.POST['action'] == 'filter':
            v, vs = list(reversed(Vacancy.objects.all())), []
            for i in v:
                if request.POST.get('name').lower() in i.name.lower() and request.POST.get('city').lower() in i.city.lower() and request.POST.get('street').lower() in i.street.lower():
                    if request.POST.get('education') == '-' or request.POST.get('education') == i.education:
                        if request.POST.get('mode') == '-' or request.POST.get('mode') == i.mode:
                            vs.append(i)
            data['login'] = LoginForm()
            data['registration'] = RegistrationForm()
            data['vsform'] = VacancySearch()
            data['vacancy'] = vs
            data['vlabels'] = V_L
            return render(request, 'vacancy.html', data)
    data['login'] = LoginForm()
    data['registration'] = RegistrationForm()
    data['vsform'] = VacancySearch()
    data['vacancy'] = list(reversed(Vacancy.objects.all()))
    data['vlabels'] = V_L
    return render(request, 'vacancy.html', data)

def delete(request, vid):
    vacancy = Vacancy.objects.get(id = vid)
    vacancy.delete()
    return redirect('/profile/'+str(request.user.id))