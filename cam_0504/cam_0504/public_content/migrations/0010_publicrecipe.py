# Generated by Django 4.0.3 on 2022-04-18 20:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('public_content', '0009_alter_product_options_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='PublicRecipe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=300)),
                ('ingredients', models.TextField()),
                ('preparation', models.TextField()),
                ('type', models.CharField(choices=[('dessert', 'Dessert'), ('salad', 'Salad'), ('main dish', 'Main dish')], max_length=300)),
            ],
        ),
    ]
