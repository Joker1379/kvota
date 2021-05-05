from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from .forms import ProfileForm
from vacancy.models import Vacancy
from vacancy.forms import VacancyForm
from vacancy.views import V_L

def index(request, userid):
    data = {}
    user = User.objects.get(id = userid)
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
            print(request.POST)
            vacancy = Vacancy.objects.get(id=int(request.POST['action'].split('!')[1]))
            form = VacancyForm(request.POST, instance=vacancy)
            form.save()
        return redirect('/profile/'+str(userid))
    data['uobj'] = user
    data['profile'] = ProfileForm(instance=user.profile)
    data['wish'] = user.profile.job_wish.split('!')
    data['profession'] = user.profile.profession.split('!')
    data['experience'] = user.profile.experience.split('!')
    data['vform'] = VacancyForm()
    data['vacancy'] = list(reversed(Vacancy.objects.filter(user = user)))
    data['vlabels'] = V_L
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

def exit(request):
    logout(request)
    return redirect('/')