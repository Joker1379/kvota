from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from users.forms import RegistrationForm, LoginForm, UserSearch
from modules.DataEvaluation import rate
from .forms import VacancySearch, E_C, G_C
from .models import Vacancy, FavV

V_L = ['Требуемое образование', 'Режим работы', 'Допустимая группа инвалидности', 'Город', 'Улица', 'Строение / Расположение офиса', 'Предоставление жилья', 'Email', 'Контактный телефон']

def index(request):
    data, V, v = {}, [], Vacancy.objects.all()
    if request.method == 'POST':
        if request.POST['action'] == 'filter':
            e, m, s, l, w = request.POST.get('education'), request.POST.get('mode'), set(request.POST.getlist('skills')), set(request.POST.getlist('limits')), request.POST.get('wage')
            if e == 'Не требуется': e = '-'
            if w == '': w = 0
            for i in v:
                if request.POST.get('name').lower() in i.name.lower() and request.POST.get('city').lower() in i.city.lower() and request.POST.get('street').lower() in i.street.lower():
                    if request.POST.get('education') == '-' or (i.education, i.education) in E_C[:E_C.index((e, e))+1]:
                        if (m == '-' or m == i.mode) and (request.POST.get('group') == '-' or request.POST.get('group') >= i.group):
                            if s.issubset(set(list(i.skills))) and l.isdisjoint(set(list(i.limits))) and i.wage >= int(w):
                                if request.POST.get('apartment') == '-' or request.POST.get('apartment') == i.apartment:
                                    if request.user.is_authenticated and len(FavV.objects.filter(user=request.user, vacancy=i))==1 and FavV.objects.get(user=request.user, vacancy=i).U: V.insert(0, (i, True))
                                    else: V.insert(0, (i, False))
        elif request.POST['action'] == 'suitable':
            u = request.user.profile
            for i in v:
                if (i.education, i.education) in E_C[:E_C.index((u.education, u.education))+1]:
                    if (u.group == '-' or u.group >= i.group) and set(list(u.limits)).isdisjoint(set(list(i.limits))):
                        if u.city == '' or u.city.lower() in i.city.lower() or (u.move == 'Да' and i.apartment == 'Да') or i.mode == 'Дистанционный режим':
                            if len(FavV.objects.filter(user=request.user, vacancy=i))==1 and FavV.objects.get(user=request.user, vacancy=i).U: V.insert(0, (i, True))
                            else: V.insert(0, (i, False))
        elif request.POST['action'] == 'search':
            sd = request.POST['search'].lower()
            for i in v:
                f = True
                for j in sd.split():
                    if not (j in i.name.lower() or j in i.description.lower() or j in str(i.wage)): f = False
                if f:
                    if request.user.is_authenticated and len(FavV.objects.filter(user=request.user, vacancy=i))==1 and FavV.objects.get(user=request.user, vacancy=i).U: V.insert(0, (i, True))
                    else: V.insert(0, (i, False))
    else:
        for i in v:
            if request.user.is_authenticated and len(FavV.objects.filter(user=request.user, vacancy=i))==1 and FavV.objects.get(user=request.user, vacancy=i).U: V.insert(0, (i, True))
            else: V.insert(0, (i, False))
    data['login'] = LoginForm()
    data['registration'] = RegistrationForm()
    data['filter'] = VacancySearch()
    data['vacancy'] = V
    data['vlabels'] = V_L
    return render(request, 'vacancy.html', data)

def delete(request, vid):
    vacancy = Vacancy.objects.get(id = vid)
    vacancy.delete()
    return redirect('/profile/'+str(request.user.id))

def favorites(request):
    data, V, v = {}, [], Vacancy.objects.all()
    for i in v:
        if len(FavV.objects.filter(user=request.user, vacancy=i))==1 and FavV.objects.get(user=request.user, vacancy=i).U: V.insert(0, (i, True))
    data['filter'] = VacancySearch()
    data['vacancy'] = V
    data['vlabels'] = V_L
    return render(request, 'vacancy.html', data)

def addu(request, vid, mode):
    data, U, u, v, t, s, l = {}, [], User.objects.all(), Vacancy.objects.get(id=vid), True, set(request.POST.getlist('skills')), set(request.POST.getlist('limits'))
    if request.method == 'POST':
        if request.POST['action'] == 'filter':
            e, m, g = request.POST.get('education'), request.POST.get('move'), request.POST.get('group')
            for i in u:
                if request.POST.get('name').lower() in i.profile.fio.lower() and request.POST.get('city').lower() in i.profile.city.lower():
                    if g == '-' or (i.profile.group, i.profile.group) in G_C[:G_C.index((g, g))+1]:
                        if (e, e) in E_C[:E_C.index((i.profile.education, i.profile.education))+1]:
                            if (m == '-' or m == i.profile.move) and s.issubset(set(list(i.profile.skills))) and l.isdisjoint(set(list(i.profile.limits))):
                                if len(FavV.objects.filter(user=i, vacancy=v))==1 and FavV.objects.get(user=i, vacancy=v).V: U.insert(0, (i, True))
                                else: U.insert(0, (i, False))
        elif request.POST['action'] == 'suitable':
            for i in u:
                if (v.education, v.education) in E_C[:E_C.index((i.profile.education, i.profile.education))+1]:
                    if (i.profile.group == '-' or i.profile.group >= v.group) and set(list(v.limits)).isdisjoint(set(list(i.profile.limits))):
                        if v.city == '' or i.profile.city.lower() in v.city.lower() or (i.profile.move == 'Да' and v.apartment == 'Да') or v.mode == 'Дистанционный режим':
                            if len(FavV.objects.filter(user=i, vacancy=v))==1 and FavV.objects.get(user=i, vacancy=v).V: U.insert(0, (i, True))
                            else: U.insert(0, (i, False))
        elif request.POST['action'] == 'search':
            sd = request.POST['search'].lower()
            for i in u:
                if sd in i.username.lower() or sd in i.profile.fio.lower():
                    if len(FavV.objects.filter(user=i, vacancy=v))==1 and FavV.objects.get(user=i, vacancy=v).V: U.insert(0, (i, True))
                    else: U.insert(0, (i, False))
    else:
        for i in u:
            if len(FavV.objects.filter(user=i, vacancy=v))==1 and FavV.objects.get(user=i, vacancy=v).V: U.insert(0, (i, True))
            elif mode != 'chosen': U.insert(0, (i, False))
    data['filter'] = UserSearch()
    data['users'] = U
    data['vid'] = vid
    return render(request, 'usersearch.html', data)

def EvalAction(request, vid, uid, act, uv):
    v, u, U = Vacancy.objects.get(id=vid), User.objects.get(id=uid).profile, User.objects.get(id=uid)
    x = FavV.objects.filter(user=U, vacancy=v)
    if act == 1:
        if len(x)==0:
            if uv=='u': res = FavV.objects.create(user=U, vacancy=v, U=True, rate=rate(v, u))
            else: res = FavV.objects.create(user=U, vacancy=v, V=True, rate=rate(v, u))
        elif uv=='u': x.update(U=True)
        else: x.update(V=True)
    else:
        if uv=='u': x.update(U=False)
        else: x.update(V=False)
        if not x[0].U and not x[0].V: x[0].delete()
    return HttpResponse()

def DataDemo(request):
    data, recs = {}, FavV.objects.all()
    data['items'] = list(reversed(recs))
    data['vlabels'] = V_L
    return render(request, 'datadisplay.html', data)