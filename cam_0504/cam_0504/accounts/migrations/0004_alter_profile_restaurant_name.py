# Generated by Django 4.0.3 on 2022-04-09 20:08

import common.validators
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_alter_appuser_email_alter_profile_age_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='restaurant_name',
            field=models.CharField(blank=True, help_text='Enter the name of your restaurant', max_length=100, null=True, validators=[common.validators.LettersNumbersWhitespacesValidator('(?<![\\s\\W\\D])^([a-zA-Z0-9]+[\\s]?[a-zA-Z0-9]+)+$(?![\\s\\W\\D])'), django.core.validators.MinLengthValidator(1)], verbose_name="Restaurant's name"),
        ),
    ]
