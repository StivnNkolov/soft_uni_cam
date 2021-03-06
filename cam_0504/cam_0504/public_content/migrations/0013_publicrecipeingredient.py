# Generated by Django 4.0.3 on 2022-04-22 11:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('public_content', '0012_remove_publicrecipe_ingredients'),
    ]

    operations = [
        migrations.CreateModel(
            name='PublicRecipeIngredient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=300)),
                ('amount', models.IntegerField()),
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='public_content.publicrecipe')),
            ],
        ),
    ]
