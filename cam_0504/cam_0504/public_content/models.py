from django.core.validators import MinLengthValidator, MinValueValidator
from django.db import models

from common.validators import LettersNumbersWhitespacesValidator


class Product(models.Model):
    NAME_MAX_LENGTH = 300
    NAME_MIN_LENGTH = 2

    REGEX_PATTERN = '(?<![\s\W\D])^([a-zA-Z0-9]+[\s]?[a-zA-Z0-9]+)+$(?![\s\W\D])'

    MEASURES_MIN_VALUE = 1

    name = models.CharField(
        max_length=NAME_MAX_LENGTH,
        validators=[
            LettersNumbersWhitespacesValidator(REGEX_PATTERN),
            MinLengthValidator(NAME_MIN_LENGTH),
        ]
    )

    tea_cup_in_grams = models.IntegerField(
        blank=True,
        null=True,
        validators=[
            MinValueValidator(MEASURES_MIN_VALUE),
        ]
    )
    coffee_cup_in_grams = models.IntegerField(
        blank=True,
        null=True,
        validators=[
            MinValueValidator(MEASURES_MIN_VALUE),
        ]
    )
    tablespoon_in_grams = models.IntegerField(
        blank=True,
        null=True,
        validators=[
            MinValueValidator(MEASURES_MIN_VALUE),
        ]
    )
    tea_spoon_in_grams = models.IntegerField(
        blank=True,
        null=True,
        validators=[
            MinValueValidator(MEASURES_MIN_VALUE),
        ]
    )

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name


class PublicRecipe(models.Model):
    name = models.CharField(
        max_length=300,
    )
    preparation = models.TextField(

    )
    type = models.CharField(
        max_length=300,
        choices=(
            ('dessert', 'Dessert'),
            ('salad', 'Salad'),
            ('main dish', 'Main dish'),
        )
    )

    description = models.TextField(

    )

    def __str__(self):
        return self.name


class PublicRecipeIngredient(models.Model):
    name = models.CharField(
        max_length=300,
    )
    amount = models.IntegerField(

    )

    recipe = models.ForeignKey(
        PublicRecipe,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.name
