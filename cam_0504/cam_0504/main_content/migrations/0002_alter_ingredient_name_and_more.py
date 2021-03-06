# Generated by Django 4.0.3 on 2022-04-07 10:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_content', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingredient',
            name='name',
            field=models.CharField(max_length=30, unique=True, verbose_name='Ingredient name'),
        ),
        migrations.AlterField(
            model_name='ingredient',
            name='price_per_type',
            field=models.DecimalField(decimal_places=2, max_digits=6, verbose_name='Price'),
        ),
        migrations.AlterField(
            model_name='ingredient',
            name='type',
            field=models.CharField(choices=[('Kilogram', 'Kilogram'), ('Liter', 'Liter'), ('Piece', 'Piece')], default='Kilogram', max_length=8, verbose_name='For'),
        ),
    ]
