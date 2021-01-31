from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Profile

class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', )

class LoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ('username', 'password')

class ProfileForm(forms.ModelForm):
    sex = forms.ChoiceField(choices=(("-", "-"), ("Мужской", "Мужской"), ("Женский", "Женский")), label="Пол")
    education = forms.ChoiceField(
        choices=(("-", "-"), 
        ("Начальное общее", "Начальное общее"), 
        ("Основное общее", "Основное общее"),
        ("Среднее общее", "Среднее общее"),
        ("Среднее профессиональное", "Среднее профессиональное"),
        ("Высшее образование — бакалавриат", "Высшее образование — бакалавриат"),
        ("Высшее образование — специалитет/магистратура", "Высшее образование — специалитет/магистратура"),
        ), label="Образование")
    group = forms.ChoiceField(choices=(("-", "-"), ("1", "1"), ("2", "2"), ('3', '3')), label="Группа инвалидности:")
    move = forms.ChoiceField(choices=(("-", "-"), ("Да", "Да"), ("Нет", "Нет")), label="Готовность переезжать")

    class Meta:
        model = Profile
        fields = ('fio', 'sex', 'age', 'education', 'group', 'city', 'street', 'move', 'phone')
        labels = {
            'fio': 'ФИО',
            'age': 'Возраст',
            'city': 'Город',
            'street': 'Улица',
            'phone': 'Контактный телефон',
        }