# Generated by Django 4.0.3 on 2022-04-29 21:10

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_content', '0022_recipe_date_created_alter_ingredient_date_created'),
    ]

    operations = [
        migrations.AlterField(
            model_name='increasepercentage',
            name='percentage',
            field=models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)]),
        ),
    ]
