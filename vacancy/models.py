from django.db import models
from django.contrib.auth.models import User

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