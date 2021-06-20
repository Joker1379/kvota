from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Profile
from multiselectfield import MultiSelectFormField
from vacancy.forms import E_C, G_C
from vacancy.models import S_C, L_C

ERR = (
    ('A user with that username already exists.', 'Пользователь с таким <strong>логином</strong> уже существует;'),
    ('This password is too short. It must contain at least 8 characters.', '<strong>Пароль</strong> слишком короткий (минимум <strong>8</strong> символов);'),
    ('This password is too common.', '<strong>Пароль</strong> слишком простой;'),
    ('This password is entirely numeric.', '<strong>Пароль</strong> не должен состоять из одних цифр;'),
    ('The two password fields didn’t match.', 'Указанные <strong>пароли</strong> не совпадают;'),
    ('The password is too similar to the username.', '<strong>Логин</strong> и <strong>пароль</strong> слишком схожи;'),)

class RegistrationForm(UserCreationForm):
    username = forms.CharField(label="Логин:", widget=forms.TextInput(attrs={'class': 'form-control form-control-md'}))
    password1 = forms.CharField(label="Пароль:", widget=forms.PasswordInput(attrs={'class':'form-control form-control-md', 'type':'password'}))
    password2 = forms.CharField(label="Повторите Пароль:", widget=forms.PasswordInput(attrs={'class':'form-control form-control-md', 'type':'password'}))
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')

class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Логин:", widget=forms.TextInput(attrs={'class': 'form-control form-control-md'}))
    password = forms.CharField(label="Пароль:", widget=forms.PasswordInput(attrs={'class':'form-control form-control-md', 'type':'password'}))
    class Meta:
        model = User
        fields = ('username', 'password')

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('fio', 'sex', 'age', 'education', 'skills', 'group', 'limits', 'city', 'street', 'move', 'phone')
        labels = {
            'fio': 'ФИО:',
            'sex': 'Пол:',
            'age': 'Возраст:',
            'education': 'Образование:',
            'skills': 'Навыки:',
            'group': 'Группа инвалидности:',
            'limits': 'Физические ограничения:',
            'city': 'Город:',
            'street': 'Улица:',
            'move': 'Готовность переезжать:',
            'phone': 'Контактный телефон:'}
        widgets = {
            'fio': forms.TextInput(attrs={'class': 'form-control form-control-md'}),
            'sex': forms.Select(attrs={'class': 'form-control form-control-md'},
                choices=(('-', '-'), ('Мужской', 'Мужской'), ('Женский', 'Женский'))),
            'age': forms.TextInput(attrs={'class': 'form-control form-control-md'}),
            'education': forms.Select(attrs={'class': 'form-control form-control-md'}, choices=E_C),
            'group': forms.Select(attrs={'class': 'form-control form-control-md'}, choices=G_C),
            'city': forms.TextInput(attrs={'class': 'form-control form-control-md'}),
            'street': forms.TextInput(attrs={'class': 'form-control form-control-md'}),
            'move': forms.Select(attrs={'class': 'form-control form-control-md'},
                choices=(('-', '-'), ('Да', 'Да'), ('Нет', 'Нет'))),
            'phone': forms.TextInput(attrs={'class': 'form-control form-control-md'})}

class UserSearch(forms.Form):
    name = forms.CharField(max_length=50, label='ФИО:', required=False)
    education = forms.CharField(max_length=100, label='Уровень образования:', required=False)
    skills = MultiSelectFormField(choices=S_C, label='Желательные навыки:', required=False)
    group = forms.CharField(max_length=50, label='Допустимая группа инвалидности:', required=False)
    limits = MultiSelectFormField(choices=L_C, label='Недопустимые ограничения:', required=False)
    city = forms.CharField(max_length=50, label='Город:', required=False)
    move = forms.CharField(max_length=10, label='Готовность переезжать:', required=False)
    name.widget = forms.TextInput(attrs={'class': 'form-control form-control-md'})
    education.widget = forms.Select(attrs={'class': 'form-control form-control-md'}, choices=E_C)
    group.widget = forms.Select(attrs={'class': 'form-control form-control-md'}, choices=G_C)
    city.widget = forms.TextInput(attrs={'class': 'form-control form-control-md'})
    move.widget = forms.Select(attrs={'class': 'form-control form-control-md'},
        choices=(('-', '-'), ('Да', 'Да'), ('Нет', 'Нет')))