from django.db import models
from django.contrib.auth.models import User
from multiselectfield import MultiSelectField

S_C= (('Умение Работать в Команде;', 'Умение Работать в Команде;'), ('git;', 'git;'), ('Проведение Уроков;', 'Проведение Уроков;'))
L_C=(('Ограничение 1;', 'Ограничение 1;'), ('Ограничение 2;', 'Ограничение 2;'), ('Ограничение 3;', 'Ограничение 3;'))

class Vacancy(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    date = models.DateField(auto_now_add=True)
    name = models.CharField(max_length=50)
    description = models.TextField()
    education = models.CharField(max_length=100)
    mode = models.CharField(max_length=50)
    city = models.CharField(max_length=50, blank=True)
    street = models.CharField(max_length=50, blank=True)
    house = models.CharField(max_length=50, blank=True)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    #New:
    group = models.CharField(max_length=100, blank=True, default='')
    skills = MultiSelectField(choices=S_C, blank=True)
    limits = MultiSelectField(choices=L_C, blank=True)

class FavV(models.Model):
    date = models.DateField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    vacancy = models.ForeignKey(Vacancy, on_delete = models.CASCADE)
    V = models.BooleanField(default=False)
    U = models.BooleanField(default=False)
    rate = models.FloatField()
    note = models.CharField(max_length=50, blank=True)