from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class RegistrationForm(UserCreationForm):
    # Подобным образом можно добавить любое поле из профиля в форму:
    sex = forms.ChoiceField(choices=((1, "Мужской"), (2, "Женский")))

    class Meta:
        model = User
        fields = ('username', 'sex', 'password1', 'password2', )

class LoginForm(forms.Form):
    Email = forms.EmailField()
    Password = forms.CharField(max_length=20, label="Пароль")