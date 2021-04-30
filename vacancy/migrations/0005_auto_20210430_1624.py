# Generated by Django 3.1.2 on 2021-04-30 06:24

from django.db import migrations
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('vacancy', '0004_auto_20210430_1623'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vacancy',
            name='limits',
            field=multiselectfield.db.fields.MultiSelectField(blank=True, choices=[('Ограничение 1;', 'Ограничение 1;'), ('Ограничение 2;', 'Ограничение 2;'), ('Ограничение 3;', 'Ограничение 3;')], max_length=44),
        ),
        migrations.AlterField(
            model_name='vacancy',
            name='skills',
            field=multiselectfield.db.fields.MultiSelectField(blank=True, choices=[('Умение Работать в Команде;', 'Умение Работать в Команде;'), ('git;', 'git;'), ('Проведение Уроков;', 'Проведение Уроков;')], max_length=50),
        ),
    ]
