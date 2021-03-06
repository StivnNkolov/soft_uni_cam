# Generated by Django 4.0.3 on 2022-04-18 20:13

import common.validators
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('public_content', '0008_alter_product_coffee_cup_in_grams_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ('name',)},
        ),
        migrations.AlterField(
            model_name='product',
            name='coffee_cup_in_grams',
            field=models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(1)]),
        ),
        migrations.AlterField(
            model_name='product',
            name='name',
            field=models.CharField(max_length=300, validators=[common.validators.LettersNumbersWhitespacesValidator('(?<![\\s\\W\\D])^([a-zA-Z0-9]+[\\s]?[a-zA-Z0-9]+)+$(?![\\s\\W\\D])'), django.core.validators.MinLengthValidator(2)]),
        ),
        migrations.AlterField(
            model_name='product',
            name='tablespoon_in_grams',
            field=models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(1)]),
        ),
        migrations.AlterField(
            model_name='product',
            name='tea_cup_in_grams',
            field=models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(1)]),
        ),
        migrations.AlterField(
            model_name='product',
            name='tea_spoon_in_grams',
            field=models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(1)]),
        ),
    ]
