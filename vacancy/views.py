from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from users.forms import RegistrationForm, LoginForm, UserSearch
from .forms import VacancySearch, E_C, G_C
from .models import Vacancy, FavV

V_L = ['Требуемое образование', 'Режим работы', 'Допустимая группа инвалидности', 'Город', 'Улица', 'Строение / Расположение офиса', 'Email', 'Контактный телефон']

def index(request):
    data, V, v, t = {}, [], Vacancy.objects.all(), True
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
            t, e, m = False, request.POST.get('education'), request.POST.get('mode')
            if e == 'Не требуется': e = '-'
            for i in v:
                if request.POST.get('name').lower() in i.name.lower() and request.POST.get('city').lower() in i.city.lower() and request.POST.get('street').lower() in i.street.lower():
                    if request.POST.get('education') == '-' or (i.education, i.education) in E_C[:E_C.index((e, e))+1]:
                        if m == '-' or m == i.mode:
                            if len(FavV.objects.filter(user=request.user, vacancy=i))==1 and FavV.objects.get(user=request.user, vacancy=i).U: V.insert(0, (i, True))
                            else: V.insert(0, (i, False))
    if t:
        if request.user.is_authenticated:
            for i in v:
                if len(FavV.objects.filter(user=request.user, vacancy=i))==1 and FavV.objects.get(user=request.user, vacancy=i).U: V.insert(0, (i, True))
                else: V.insert(0, (i, False))
        else:
            for i in v: V.insert(0, (i, False))
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

def fv(request, vid, uid, act, uv):
    v, u, U = Vacancy.objects.get(id=vid), User.objects.get(id=uid).profile, User.objects.get(id=uid)
    x = FavV.objects.filter(user=U, vacancy=v)
    if act == 1:
        if len(x)==0:
            r, lv, sv, nv = 0, str(v.limits).replace(';', '').lower(), str(v.skills).replace(';', '').lower(), v.name.lower().split()
            '''if v.group != '-' and u.group != '-' and v.group > u.group:
                fv = FavV.objects.create(user=request.user, vacancy=Vacancy.objects.get(id=vid), U=True, rate=0, note="Неподходящая группа инвалидности")
            elif not set(lv.split(', ')).isdisjoint(set(str(u.limits).replace(';', '').lower().split(', '))):
                fv = FavV.objects.create(user=request.user, vacancy=Vacancy.objects.get(id=vid), U=True, rate=0, note="Неподходящие физические ограничения")'''
            if (v.group == '-' or u.group == '-' or v.group <= u.group) and (bool(set(lv.split(', '))) or set(lv.split(', ')).isdisjoint(set(str(u.limits).replace(';', '').lower().split(', ')))):
                if not set(nv).isdisjoint(set(u.job_wish.lower().split('!'))): r+=1
                if not set(nv).isdisjoint(set(u.profession.lower().split('!'))): r+=1
                if not set(nv).isdisjoint(set(u.experience.lower().split('!'))): r+=1
                if sv == '': r+=1
                else:
                    for i in sv.split(', '):
                        if not set([i]).isdisjoint(set(str(u.skills).replace(';', '').lower().split(', '))): r+=1
                if (v.education, v.education) in E_C[:E_C.index((u.education, u.education))+1]: r+=1
                if u.move == 'Да' or v.city == '': r+=2
                else:
                    if v.city == u.city: r+=1
                    if v.street == u.street: r+=1
            if uv=='u': res = FavV.objects.create(user=U, vacancy=v, U=True, rate=round(r/(6+len(sv.split(', '))), 2))
            else: res = FavV.objects.create(user=U, vacancy=v, V=True, rate=round(r/(6+len(sv.split(', '))), 2))
        elif uv=='u': x.update(U=True)
        else: x.update(V=True)
    else:
        if uv=='u': x.update(U=False)
        else: x.update(V=False)
        if not x[0].U and not x[0].V: x[0].delete()
    return redirect('/')

def favorite(request):
    data, V, v = {}, [], Vacancy.objects.all()
    for i in v:
        if len(FavV.objects.filter(user=request.user, vacancy=i))==1 and FavV.objects.get(user=request.user, vacancy=i).U: V.insert(0, (i, True))
    data['filter'] = VacancySearch()
    data['vacancy'] = V
    data['vlabels'] = V_L
    return render(request, 'vacancy.html', data)

def addu(request, vid, mode):
    data, U, u, v, t = {}, [], User.objects.all(), Vacancy.objects.get(id=vid), True
    if request.method == 'POST':
        if request.POST['action'] == 'filter':
            t, e, m, g = False, request.POST.get('education'), request.POST.get('move'), request.POST.get('group')
            for i in u:
                if request.POST.get('name').lower() in i.profile.fio.lower() and request.POST.get('city').lower() in i.profile.city.lower():
                    if g == '-' or (i.profile.group, i.profile.group) in G_C[:G_C.index((g, g))+1]:
                        if (e, e) in E_C[:E_C.index((i.profile.education, i.profile.education))+1]:
                            if m == '-' or m == i.profile.move:
                                if len(FavV.objects.filter(user=i, vacancy=v))==1 and FavV.objects.get(user=i, vacancy=v).V: U.insert(0, (i, True))
                                else: U.insert(0, (i, False))
    if t:
        for i in u:
            if len(FavV.objects.filter(user=i, vacancy=v))==1 and FavV.objects.get(user=i, vacancy=v).V: U.insert(0, (i, True))
            elif mode != 'chosen': U.insert(0, (i, False))
    data['filter'] = UserSearch()
    data['users'] = U
    data['vid'] = vid
    return render(request, 'usersearch.html', data)

def uni(request):
    data, recs = {}, FavV.objects.all()
    data['items'] = list(reversed(recs))
    data['vlabels'] = V_L
    return render(request, 'unidata.html', data)