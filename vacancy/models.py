from django.db import models
from django.contrib.auth.models import User
from multiselectfield import MultiSelectField

S_C= (('Умение Работать в Команде;', 'Умение Работать в Команде;'), ('git;', 'git;'), ('Проведение Уроков;', 'Проведение Уроков;'))
L_C=(('Речевые ограничения;', 'Речевые ограничения;'), ('Слабый слух;', 'Слабый слух;'), ('Нарушенная координация;', 'Нарушенная координация;'))

class Vacancy(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    date = models.DateField(auto_now_add=True)
    name = models.CharField(max_length=50)
    wage = models.PositiveIntegerField(default=0)
    description = models.TextField()
    education = models.CharField(max_length=100)
    mode = models.CharField(max_length=50)
    city = models.CharField(max_length=50, blank=True)
    street = models.CharField(max_length=50, blank=True)
    house = models.CharField(max_length=50, blank=True)
    apartment = models.CharField(max_length=10, blank=True)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    group = models.CharField(max_length=10, blank=True, default='')
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