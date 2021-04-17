from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Profile

E_C = (('-', '-'), ('Начальное общее', 'Начальное общее'), ('Основное общее', 'Основное общее'),
    ('Среднее общее', 'Среднее общее'), ('Среднее профессиональное', 'Среднее профессиональное'),
    ('Высшее образование — бакалавриат', 'Высшее образование — бакалавриат'),
    ('Высшее образование — специалитет/магистратура', 'Высшее образование — специалитет/магистратура'))

class RegistrationForm(UserCreationForm):
    password1 = forms.CharField(label="Пароль:", widget=forms.PasswordInput(attrs={'class':'form-control form-control-md', 'type':'password'}))
    password2 = forms.CharField(label="Повторите Пароль:", widget=forms.PasswordInput(attrs={'class':'form-control form-control-md', 'type':'password'}))
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')
        labels = {'username': 'Логин:'}
        widgets = {'username': forms.TextInput(attrs={'class': 'form-control form-control-md'})}

class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Логин:", widget=forms.TextInput(attrs={'class': 'form-control form-control-md'}))
    password = forms.CharField(label="Пароль:", widget=forms.PasswordInput(attrs={'class':'form-control form-control-md', 'type':'password'}))
    class Meta:
        model = User
        fields = ('username', 'password')

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('fio', 'sex', 'age', 'education', 'group', 'city', 'street', 'move', 'phone')
        labels = {
            'fio': 'ФИО:',
            'sex': 'Пол:',
            'age': 'Возраст:',
            'education': 'Образование:',
            'group': 'Группа инвалидности:',
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
            'group': forms.Select(attrs={'class': 'form-control form-control-md'},
                choices=(('-', '-'), ('1', '1'), ('2', '2'), ('3', '3'))),
            'city': forms.TextInput(attrs={'class': 'form-control form-control-md'}),
            'street': forms.TextInput(attrs={'class': 'form-control form-control-md'}),
            'move': forms.Select(attrs={'class': 'form-control form-control-md'},
                choices=(('-', '-'), ('Да', 'Да'), ('Нет', 'Нет'))),
            'phone': forms.TextInput(attrs={'class': 'form-control form-control-md'})}