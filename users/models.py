import datetime
from django.db import models
from django.contrib.auth.models import User
from multiselectfield import MultiSelectField
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.core.cache import cache 
from vacancy.models import S_C, L_C, FavV, Vacancy
from modules.DataEvaluation import rate

# Number of seconds of inactivity before a user is marked offline:
USER_ONLINE_TIMEOUT = 100

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    fio = models.CharField(max_length=100, blank=True, default='-')
    sex = models.CharField(max_length=30, blank=True, default='-')
    age = models.PositiveSmallIntegerField(blank=True, default=0)
    education = models.CharField(max_length=100, blank=True, default='-')
    group = models.CharField(max_length=100, blank=True, default='-')
    city = models.CharField(max_length=50, blank=True, default='-')
    street = models.CharField(max_length=50, blank=True, default='-')
    move = models.CharField(max_length=10, blank=True, default='-')
    phone = models.CharField(max_length=20, blank=True, default='-')
    job_wish = models.CharField(max_length=300, blank=True, default='')
    profession = models.CharField(max_length=300, blank=True, default='')
    experience = models.CharField(max_length=300, blank=True, default='')
    skills = MultiSelectField(choices=S_C, blank=True)
    limits = MultiSelectField(choices=L_C, blank=True)
    def s_list(self): return str(self.skills).split(',')[:3]
    def l_list(self): return str(self.limits).split(',')[:3]
    def last_seen(self): return cache.get('seen_'+self.user.username)
    def online(self):
        if self.last_seen():
            now = datetime.datetime.now()
            if now > self.last_seen() + datetime.timedelta(seconds=USER_ONLINE_TIMEOUT): return False
            else: return True
        else: return False

@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created: Profile.objects.create(user=instance)
    instance.profile.save()

@receiver(post_save, sender=Profile)
def user_data_update(sender, instance, created, **kwargs):
    for i in FavV.objects.filter(user=instance.user):
        i.rate = rate(i.vacancy, i.user.profile)
        i.save()

@receiver(post_save, sender=Vacancy)
def vacancy_data_update(sender, instance, created, **kwargs):
    for i in FavV.objects.filter(vacancy=instance):
        i.rate = rate(i.vacancy, i.user.profile)
        i.save()