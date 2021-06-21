from vacancy.forms import E_C

def rate(v, u):
    r, lv, sv, nv = 0, set(list(v.limits)), list(v.skills), set(v.name.lower().split())
    if (v.group == '-' or u.group == '-' or v.group <= u.group) and (len(lv) == 0 or lv.isdisjoint(set(list(u.limits)))):
        if not nv.isdisjoint(set(u.job_wish.lower().split('!'))): r+=1
        if not nv.isdisjoint(set(u.profession.lower().split('!'))): r+=1
        if not nv.isdisjoint(set(u.experience.lower().split('!'))): r+=1
        for i in sv:
            if i in list(u.skills): r+=1
        if (v.education, v.education) in E_C[:E_C.index((u.education, u.education))+1]: r+=1
        if (u.move == 'Да' and v.apartment == 'Да') or v.mode == 'Дистанционный режим': r+=2
        else:
            if v.city == u.city: r+=1
            if v.street == u.street: r+=1
    return round(r/(6+len(sv)), 2)