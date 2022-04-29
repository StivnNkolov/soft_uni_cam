from django import test as django_tests
from django.contrib.auth import get_user_model

from cam_0504.main_content.models import Recipe, Ingredient
from common.functions_for_tests import create_user, recipe_create, ingredient_create
from common.user_info import get_user_recipes_ingredients_count

UserModel = get_user_model()


class UserInfoTests(django_tests.TestCase):
    VALID_USER_DATA = {
        'email': 'a@a.com',
        'password': '1123qwer',
    }

    RECIPE_NAME = 'test'
    INGREDIENT_NAME = 'test'
    INGREDIENT_TYPE = 'Kilogram'
    INGREDIENT_PRICE = 1

    def test_get_user_recipes_ingredients_count__with_1_recipe_return_1(self):
        user = create_user(**self.VALID_USER_DATA)

        recipe_create(self.RECIPE_NAME, user)

        expected_amount = 1

        recipes_count, _ = get_user_recipes_ingredients_count(user)

        self.assertEqual(expected_amount, recipes_count)

    def test_get_user_recipes_ingredients_count__with_0_recipes_return_0(self):
        user = create_user(**self.VALID_USER_DATA)

        expected_amount = 0

        recipes_count, _ = get_user_recipes_ingredients_count(user)

        self.assertEqual(expected_amount, recipes_count)

    def test_get_user_recipes_ingredients_count__with_1_ingredient_return_1(self):
        user = create_user(**self.VALID_USER_DATA)

        ingredient_create(self.INGREDIENT_NAME, self.INGREDIENT_TYPE, self.INGREDIENT_PRICE, user)

        expected_amount = 1

        _, ingredient_count = get_user_recipes_ingredients_count(user)

        self.assertEqual(expected_amount, ingredient_count)

    def test_get_user_recipes_ingredients_count__with_0_ingredients_return_0(self):
        user = create_user(**self.VALID_USER_DATA)

        expected_amount = 0

        _, ingredients_count = get_user_recipes_ingredients_count(user)

        self.assertEqual(expected_amount, ingredients_count)

    def test_get_user_recipes_ingredients_count__with_1_ingredient_1_recipe__return_1_and_1(self):
        user = create_user(**self.VALID_USER_DATA)

        recipe_create(self.RECIPE_NAME, user)
        ingredient_create(self.INGREDIENT_NAME, self.INGREDIENT_TYPE, self.INGREDIENT_PRICE, user)

        expected_return_value = (1, 1)

        self.assertEqual(expected_return_value, get_user_recipes_ingredients_count(user))
