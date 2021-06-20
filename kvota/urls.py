"""kvota URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from vacancy import views as vv
from cources import views as cv
from users import views as uv

urlpatterns = [
    path('admin/', admin.site.urls),
    path('registration/', uv.registration, name = 'registration'),
    path('login/', uv.login, name = 'login'),
    path('exit/', uv.exit, name = 'logout'),
    path('profile/<int:userid>/<str:category>/<str:item>/', uv.del_item, name = 'delete_speciality'),
    path('profile/<int:userid>/', uv.index, name = 'profile'),
    path('cources/', cv.index, name = 'cources_list'),
    path('ea/<int:vid>/<int:uid>/<int:act>/<str:uv>/', vv.EvalAction, name = 'evaluation_action'),
    path('data/', vv.DataDemo, name = 'generated_data_demonstration'),
    path('users/<int:vid>/<str:mode>/', vv.addu, name = 'users_list_for_vacancy'),
    path('vdelete/<int:vid>/', vv.delete, name = 'delete_vacancy'),
    path('vfavorites/', vv.favorites, name = 'favorites_vacancy_list'),
    path('', vv.index, name = 'vacancy_list')]