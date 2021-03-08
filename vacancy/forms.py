from django import forms
from .models import Vacancy

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
            'education': forms.Select(attrs={'class': 'form-control form-control-md'},
                choices=(('-', '-'), 
                ('Начальное общее', 'Начальное общее'), 
                ('Основное общее', 'Основное общее'),
                ('Среднее общее', 'Среднее общее'),
                ('Среднее профессиональное', 'Среднее профессиональное'),
                ('Высшее образование — бакалавриат', 'Высшее образование — бакалавриат'),
                ('Высшее образование — специалитет/магистратура', 'Высшее образование — специалитет/магистратура'))),
            'mode': forms.Select(attrs={'class': 'form-control form-control-md'},
                choices=(('-', '-'), 
                ('Пятидневная неделя', 'Пятидневная неделя'), 
                ('Ненормированный рабочий день', 'Ненормированный рабочий день'),
                ('Работа по гибкому графику', 'Работа по гибкому графику'),
                ('Посменная работа', 'Посменная работа'),
                ('Разделение рабочего дня на части', 'Разделение рабочего дня на части'),
                ('Дистанционный режим', 'Дистанционный режим'))),
            'city': forms.TextInput(attrs={'class': 'form-control form-control-md'}),
            'street': forms.TextInput(attrs={'class': 'form-control form-control-md'}),
            'house': forms.TextInput(attrs={'class': 'form-control form-control-md'}),
            'email': forms.TextInput(attrs={'class': 'form-control form-control-md'}),
            'phone': forms.TextInput(attrs={'class': 'form-control form-control-md'})}