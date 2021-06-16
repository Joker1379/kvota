from django import forms
from .models import Vacancy, S_C, L_C
from multiselectfield import MultiSelectFormField

E_C = (('-', '-'), ('Начальное общее', 'Начальное общее'), ('Основное общее', 'Основное общее'),
    ('Среднее общее', 'Среднее общее'), ('Среднее профессиональное', 'Среднее профессиональное'),
    ('Высшее образование — бакалавриат', 'Высшее образование — бакалавриат'),
    ('Высшее образование — специалитет/магистратура', 'Высшее образование — специалитет/магистратура'))
M_C = (('-', '-'), ('Пятидневная неделя', 'Пятидневная неделя'), ('Ненормированный рабочий день', 'Ненормированный рабочий день'),
    ('Работа по гибкому графику', 'Работа по гибкому графику'), ('Посменная работа', 'Посменная работа'),
    ('Разделение рабочего дня на части', 'Разделение рабочего дня на части'), ('Дистанционный режим', 'Дистанционный режим'))
G_C = (('-', '-'), ('3', '3'), ('2', '2'), ('1', '1'))
E_F = (E_C[0],)+(('Не требуется', 'Не требуется'),)+E_C[1:]

class VacancyForm(forms.ModelForm):
    class Meta:
        model = Vacancy
        fields = ('name', 'wage', 'description', 'education', 'skills', 'mode', 'group', 'limits', 'city', 'street', 'house', 'email', 'phone')
        labels = {
            'name': 'Наименование вакансии:',
            'wage': 'Предлагаемая зарплата:',
            'description': 'Описание:',
            'education': 'Требуемое образование:',
            'skills': 'Желательные навыки:',
            'mode': 'Режим работы:',
            'group': 'Минимальная допустимая группа инвалидности:',
            'limits': 'Неподходящие физические ограничения:',
            'city': 'Город:',
            'street': 'Улица:',
            'house': 'Строение / Расположение офиса:',
            'email': 'Email:',
            'phone': 'Контактный телефон:'}
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control form-control-md'}),
            'wage': forms.TextInput(attrs={'class': 'form-control form-control-md'}),
            'description': forms.Textarea(attrs={'class': 'form-control form-control-md'}),
            'education': forms.Select(attrs={'class': 'form-control form-control-md'}, choices=E_C),
            'mode': forms.Select(attrs={'class': 'form-control form-control-md'}, choices=M_C),
            'group': forms.Select(attrs={'class': 'form-control form-control-md'}, choices=G_C),
            'city': forms.TextInput(attrs={'class': 'form-control form-control-md'}),
            'street': forms.TextInput(attrs={'class': 'form-control form-control-md'}),
            'house': forms.TextInput(attrs={'class': 'form-control form-control-md'}),
            'email': forms.TextInput(attrs={'class': 'form-control form-control-md'}),
            'phone': forms.TextInput(attrs={'class': 'form-control form-control-md'})}

class VacancySearch(forms.Form):
    name = forms.CharField(max_length=50, label='Наименование:', required=False)
    wage = forms.IntegerField(min_value=0, label='Минимальная зарплата:', required=False)
    education = forms.CharField(max_length=100, label='Уровень образования:', required=False)
    skills = MultiSelectFormField(choices=S_C, label='Желательные навыки:', required=False)
    mode = forms.CharField(max_length=50, label='Режим работы:', required=False)
    group = forms.CharField(max_length=10, label='Допустимая группа инвалидности:', required=False)
    limits = MultiSelectFormField(choices=L_C, label='Допустимые ограничения:', required=False)
    city = forms.CharField(max_length=50, label='Город:', required=False)
    street = forms.CharField(max_length=50, label='Улица:', required=False)
    name.widget = forms.TextInput(attrs={'class': 'form-control form-control-md'})
    wage.widget = forms.NumberInput(attrs={'class': 'form-control form-control-md'})
    education.widget = forms.Select(attrs={'class': 'form-control form-control-md'}, choices=E_F)
    mode.widget = forms.Select(attrs={'class': 'form-control form-control-md'}, choices=M_C)
    group.widget = forms.Select(attrs={'class': 'form-control form-control-md'}, choices=G_C)
    city.widget = forms.TextInput(attrs={'class': 'form-control form-control-md'})
    street.widget = forms.TextInput(attrs={'class': 'form-control form-control-md'})