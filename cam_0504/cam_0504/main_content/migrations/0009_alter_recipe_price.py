# Generated by Django 4.0.3 on 2022-04-08 07:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_content', '0008_alter_recipe_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='price',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=6, null=True),
        ),
    ]
