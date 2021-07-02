import json
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from .forms import LoginForm, RegistrationForm, ProfileForm, ERR
from vacancy.models import Vacancy
from vacancy.forms import VacancyForm
from vacancy.views import V_L

def index(request, userid):
    data, user = {}, User.objects.get(id = userid)
    if request.method == 'POST':
        if request.POST['action'] == 'info':
            form = ProfileForm(request.POST, instance=request.user.profile)
            form.save()
        elif request.POST['action'] == 'wish':
            user.profile.job_wish = user.profile.job_wish + request.POST['input'] + '!'
            user.save()
        elif request.POST['action'] == 'profession':
            user.profile.profession = user.profile.profession + request.POST['input'] + '!'
            user.save()
        elif request.POST['action'] == 'experience':
            user.profile.experience = user.profile.experience + request.POST['input'] + '!'
            user.save()
        elif request.POST['action'] == 'limits':
            user.profile.limits = user.profile.limits + request.POST['input'] + '!'
            user.save()
        elif request.POST['action'] == 'add_vacancy':
            form = VacancyForm(request.POST)
            vacancy = form.save(commit=False)
            vacancy.user = request.user
            vacancy.save()
        elif request.POST['action'].split('!')[0] == 'red_vacancy':
            vacancy = Vacancy.objects.get(id=int(request.POST['action'].split('!')[1]))
            form = VacancyForm(request.POST, instance=vacancy)
            form.save()
    data['uobj'] = user
    data['profile'] = ProfileForm(instance=user.profile)
    data['wish'] = user.profile.job_wish.split('!')
    data['profession'] = user.profile.profession.split('!')
    data['experience'] = user.profile.experience.split('!')
    data['vform'] = VacancyForm()
    data['vacancy'] = list(reversed(Vacancy.objects.filter(user = user)))
    data['vlabels'] = V_L
    data['login'] = LoginForm()
    data['registration'] = RegistrationForm()
    return render(request, 'profile.html', data)

def del_item(request, userid, category, item):
    user = User.objects.get(id = userid)
    if category == 'wish':
        s = user.profile.job_wish
        user.profile.job_wish = s[0:s.find(item)]+s[s.find(item)+len(item)+1:]
    if category == 'profession':
        s = user.profile.profession
        user.profile.profession = s[0:s.find(item)]+s[s.find(item)+len(item)+1:]
    if category == 'experience':
        s = user.profile.experience
        user.profile.experience = s[0:s.find(item)]+s[s.find(item)+len(item)+1:]
    user.save()
    return redirect('/profile/'+str(userid))

def Registration(request):
    form = RegistrationForm(request.POST)
    t = 1 if form.is_valid() else 0
    s, r, l = str(form.errors), '<br><ul class="errorlist">', request.POST['username']
    if len(l) < 4: t, r = 0, r+'<li>'+'<strong>Логин</strong> слишком короткий (минимум <strong>4</strong> символа);'+'</li>'
    if not l.isalnum(): t, r = 0, r+'<li>'+'<strong>Логин</strong> может включать в себя только <strong>буквы</strong> или <strong>цифры</strong>;'+'</li>'
    for i in ERR:
        if i[0] in s: r+='<li>'+i[1]+'</li>'
    if t == 1:
        user = form.save()
        # Так сожраняются дополнительные поля профиля при регистрации:
        # user.refresh_from_db()
        # user.profile.sex = form.cleaned_data.get('sex')
        # user.save()
        raw_password = form.cleaned_data.get('password1')
        user = authenticate(username=user.username, password=raw_password)
        login(request, user)
    if r == '<br><ul class="errorlist">': r = ''
    return HttpResponse(json.dumps({'v': t, 'errors': r}))

def Login(request):
    user = authenticate(username=request.POST.get('username'), password=request.POST.get('password'))
    if user:
        login(request, user)
        return HttpResponse(json.dumps({'v': 1, 'errors': ''}))
    else:
        r, l = '<br><ul class="errorlist">', request.POST['username']
        if len(User.objects.filter(username=l)) == 1: r+='<li>'+'Неправильное сочетание <strong>логина</strong> и <strong>пароля</strong>;'+'</li>'
        else: r+='<li>'+'Пользователя с указанным <strong>логином</strong> не существует;'+'</li>'
        return HttpResponse(json.dumps({'v': 0, 'errors': r}))

def exit(request):
    logout(request)
    return redirect('/')