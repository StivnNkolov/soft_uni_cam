# Generated by Django 4.0.3 on 2022-04-18 19:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('public_content', '0005_product'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='measure_unit',
        ),
        migrations.DeleteModel(
            name='MeasureUnit',
        ),
        migrations.DeleteModel(
            name='Product',
        ),
    ]
