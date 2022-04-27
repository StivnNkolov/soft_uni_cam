# Generated by Django 4.0.3 on 2022-04-10 00:55

import common.validators
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_content', '0016_ingredient_user_recipe_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingredient',
            name='name',
            field=models.CharField(max_length=30, validators=[common.validators.LettersNumbersWhitespacesValidator('(?<![\\s\\W\\D])^([a-zA-Z0-9]+[\\s]?[a-zA-Z0-9]+)+$(?![\\s\\W\\D])'), django.core.validators.MinLengthValidator(2)], verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='name',
            field=models.CharField(max_length=120, validators=[common.validators.LettersNumbersWhitespacesValidator('(?<![\\s\\W\\D])^([a-zA-Z0-9]+[\\s]?[a-zA-Z0-9]+)+$(?![\\s\\W\\D])'), django.core.validators.MinLengthValidator(2)], verbose_name='Recipe name'),
        ),
    ]
