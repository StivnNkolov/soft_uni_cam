# Generated by Django 4.0.3 on 2022-04-07 09:38

import common.validators
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_profile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appuser',
            name='email',
            field=models.EmailField(max_length=254, unique=True, verbose_name='Email'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='age',
            field=models.IntegerField(blank=True, help_text='Enter your age', null=True, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Age'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='city_name',
            field=models.CharField(blank=True, help_text="Enter your city's name", max_length=72, null=True, validators=[common.validators.only_letters_validator, django.core.validators.MinLengthValidator(2)], verbose_name='City'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='first_name',
            field=models.CharField(blank=True, help_text='Enter your first name', max_length=72, null=True, validators=[django.core.validators.MinLengthValidator(2), common.validators.only_letters_validator], verbose_name='First Name'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='last_name',
            field=models.CharField(blank=True, help_text='Enter your last name', max_length=72, null=True, validators=[django.core.validators.MinLengthValidator(2), common.validators.only_letters_validator], verbose_name='Last Name'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='restaurant_name',
            field=models.CharField(blank=True, help_text='Enter the name of your restaurant', max_length=100, null=True, validators=[common.validators.letters_and_numbers_validator, django.core.validators.MinLengthValidator(1)], verbose_name="Restaurant's name"),
        ),
    ]
