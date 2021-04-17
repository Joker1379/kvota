from django import forms
from .models import Vacancy

E_C = (('-', '-'), ('Начальное общее', 'Начальное общее'), ('Основное общее', 'Основное общее'),
    ('Среднее общее', 'Среднее общее'), ('Среднее профессиональное', 'Среднее профессиональное'),
    ('Высшее образование — бакалавриат', 'Высшее образование — бакалавриат'),
    ('Высшее образование — специалитет/магистратура', 'Высшее образование — специалитет/магистратура'))
M_C = (('-', '-'), ('Пятидневная неделя', 'Пятидневная неделя'), ('Ненормированный рабочий день', 'Ненормированный рабочий день'),
    ('Работа по гибкому графику', 'Работа по гибкому графику'), ('Посменная работа', 'Посменная работа'),
    ('Разделение рабочего дня на части', 'Разделение рабочего дня на части'), ('Дистанционный режим', 'Дистанционный режим'))

class VacancyForm(forms.ModelForm):
    class Meta:
        model = Vacancy
        fields = ('name', 'description', 'education', 'mode', 'city', 'street', 'house', 'email', 'phone')
        labels = {
            'name': 'Наименование вакансии:',
            'description': 'Описание:',
            'education': 'Требуемое образование:',
            'mode': 'Режим работы:',
            'city': 'Город:',
            'street': 'Улица:',
            'house': 'Строение / Расположение офиса:',
            'email': 'Email:',
            'phone': 'Контактный телефон:'}
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control form-control-md'}),
            'description': forms.Textarea(attrs={'class': 'form-control form-control-md'}),
            'education': forms.Select(attrs={'class': 'form-control form-control-md'}, choices=E_C),
            'mode': forms.Select(attrs={'class': 'form-control form-control-md'}, choices=M_C),
            'city': forms.TextInput(attrs={'class': 'form-control form-control-md'}),
            'street': forms.TextInput(attrs={'class': 'form-control form-control-md'}),
            'house': forms.TextInput(attrs={'class': 'form-control form-control-md'}),
            'email': forms.TextInput(attrs={'class': 'form-control form-control-md'}),
            'phone': forms.TextInput(attrs={'class': 'form-control form-control-md'})}

class VacancySearch(forms.Form):
    name = forms.CharField(max_length=50, label='Наименование:', required=False)
    education = forms.CharField(max_length=100, label='Уровень Образования:', required=False)
    mode = forms.CharField(max_length=50, label='Режим Работы:', required=False)
    city = forms.CharField(max_length=50, label='Город:', required=False)
    street = forms.CharField(max_length=50, label='Улица:', required=False)
    name.widget = forms.TextInput(attrs={'class': 'form-control form-control-md'})
    education.widget = forms.Select(attrs={'class': 'form-control form-control-md'}, choices=E_C)
    mode.widget = forms.Select(attrs={'class': 'form-control form-control-md'}, choices=M_C)
    city.widget = forms.TextInput(attrs={'class': 'form-control form-control-md'})
    street.widget = forms.TextInput(attrs={'class': 'form-control form-control-md'})