from django.contrib.auth import get_user_model

from cam_0504.main_content.models import Ingredient, Recipe, RecipeIngredient, IncreasePercentage

UserModel = get_user_model()


def ingredient_create(name, ingredient_type, price, user):
    return Ingredient.objects.create(
        name=name,
        type=ingredient_type,
        price_per_type=price,
        user=user
    )


def recipe_create(name, user):
    return Recipe.objects.create(
        name=name,
        user=user
    )


def create_user(**credentials):
    return UserModel.objects.create_user(**credentials)


def recipe_ingredient_create(recipe, ingredient, amount=1):
    return RecipeIngredient.objects.create(
        recipe=recipe,
        ingredient=ingredient,
        amount=amount,
    )


def increase_percentage_create(recipe, percentage):
    return IncreasePercentage.objects.create(
        recipe=recipe,
        percentage=percentage
    )
