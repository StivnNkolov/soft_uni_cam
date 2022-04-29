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

