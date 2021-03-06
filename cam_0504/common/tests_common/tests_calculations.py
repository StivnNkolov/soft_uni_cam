from django import test as django_tests
from django.contrib.auth import get_user_model

from cam_0504.main_content.models import Ingredient, Recipe, RecipeIngredient, IncreasePercentage
from common.calculations import get_price_in_stotinki, get_price_for_one_unit, increase_value_by_percent, \
    calculate_price_return_in_leva
from common.functions_for_tests import create_user, ingredient_create, recipe_create, recipe_ingredient_create, \
    increase_percentage_create

UserModel = get_user_model()


class CalculationsTests(django_tests.TestCase):
    VALID_USER_DATA = {
        'email': 'a@a.com',
        'password': '1123qwer',
    }

    TEST_RECIPE_NAME = 'test recipe'

    def test_get_price_in_stotinki_returns_the_actual_amount(self):
        amount_in_leva = 1.23
        expected_amount_in_stotinki = 123

        returned_amount = get_price_in_stotinki(amount_in_leva)

        self.assertEqual(expected_amount_in_stotinki, returned_amount)

    def test_get_price_for_one_unit__if_type_of_food_is_Piece__return_the_value_in_leva_but_in_stotinki(self):
        price_in_leva = 1
        type_of_food = 'Piece'

        expected_return_value = 100

        return_amount = get_price_for_one_unit(type_of_food, price_in_leva)

        self.assertEqual(expected_return_value, return_amount)

    def test_get_price_for_one_unit__if_type_of_food_is_Kilogram__return_the_value_for_one_unit(self):
        price_in_leva = 1
        type_of_food = 'Kilogram'

        expected_return_value = 0.1

        return_amount = get_price_for_one_unit(type_of_food, price_in_leva)

        self.assertEqual(expected_return_value, return_amount)

    def test_get_price_for_one_unit__if_type_of_food_is_Liter__return_the_value_for_one_unit(self):
        price_in_leva = 1
        type_of_food = 'Liter'

        expected_return_value = 0.1

        return_amount = get_price_for_one_unit(type_of_food, price_in_leva)

        self.assertEqual(expected_return_value, return_amount)

    def test_increase_value_by_percent__with_0_percentage_increase__return_the_initial_value(self):
        initial_value = 100
        increase_percentage = 0

        expected_return_value = 100

        return_amount = increase_value_by_percent(initial_value, increase_percentage)

        self.assertEqual(expected_return_value, return_amount)

    def test_increase_value_by_percent__with_percentage_different_than_0__return_the_increased_value(self):
        initial_value = 100
        increase_percentage = 100

        expected_return_value = 200

        return_amount = increase_value_by_percent(initial_value, increase_percentage)

        self.assertEqual(expected_return_value, return_amount)

    def test_calculate_price__without_added_ingredients__return_zero_as_end_price(self):
        increase_percentage = 0
        ingredients = []

        expected_return_value = 0

        end_price, _ = calculate_price_return_in_leva(increase_percentage, ingredients)

        self.assertEqual(expected_return_value, end_price)

    def test_calculate_price__without_added_ingredients__return_zero_as_increased_end_price(self):
        increase_percentage = 0
        ingredients = []

        expected_return_value = 0

        _, increased_end_price = calculate_price_return_in_leva(increase_percentage, ingredients)

        self.assertEqual(expected_return_value, increased_end_price)

    def test_calculate_price__with_added_ingredients___return_the_right_amount_(self):
        user = create_user(**self.VALID_USER_DATA)

        ingredient = ingredient_create('test', 'Kilogram', 1, user)
        ingredient2 = ingredient_create('test1', 'Liter', 1, user)

        recipe = recipe_create(self.TEST_RECIPE_NAME, user)

        recipe_ingredient_create(recipe, ingredient, 100)
        recipe_ingredient_create(recipe, ingredient2, 100)

        increase_percentage = increase_percentage_create(recipe, 0)

        all_ingredients = RecipeIngredient.objects.all()

        expected_return_value = 0.20

        end_price, _ = calculate_price_return_in_leva(increase_percentage.percentage, all_ingredients)

        self.assertEqual(expected_return_value, end_price)

    def test_calculate_price__with_added_ingredients_without_added_increase_percentage__return_the_same_end_price(self):
        user = create_user(**self.VALID_USER_DATA)

        ingredient = ingredient_create('test', 'Kilogram', '1', user)

        recipe = recipe_create(self.TEST_RECIPE_NAME, user)

        recipe_ingredient_create(recipe, ingredient, 100)

        increase_percentage = increase_percentage_create(recipe, 0)

        all_ingredients = RecipeIngredient.objects.all()

        expected_return_value = 0.10

        _, increased_end_price = calculate_price_return_in_leva(increase_percentage.percentage, all_ingredients)

        self.assertEqual(expected_return_value, increased_end_price)

    def test_calculate_price__with_added_ingredients_with_added_increase_percentage__return_different_values(self):
        user = create_user(**self.VALID_USER_DATA)

        ingredient = ingredient_create('test', 'Kilogram', 1, user)
        ingredient2 = ingredient_create('test2', 'Liter', 1, user)

        recipe = recipe_create(self.TEST_RECIPE_NAME, user)

        recipe_ingredient_create(recipe, ingredient, 100)
        recipe_ingredient_create(recipe, ingredient2, 100)

        increase_percentage = increase_percentage_create(recipe, 100)

        all_ingredients = RecipeIngredient.objects.all()

        expected_end_value = 0.20
        expected_increased_end_value = 0.40

        end_price, increased_end_price = calculate_price_return_in_leva(increase_percentage.percentage, all_ingredients)

        self.assertEqual(end_price, expected_end_value)
        self.assertEqual(expected_increased_end_value, increased_end_price)

    def test_calculate_price__without_added_ingredients_with_added_increase_percentage__return_0(self):
        increase_percentage = 100
        ingredients = []

        expected_return_value = 0.0

        end_price, increased_end_price = calculate_price_return_in_leva(increase_percentage, ingredients)

        self.assertEqual(expected_return_value, end_price)
        self.assertEqual(expected_return_value, increased_end_price)

    def test_calculate_price__with_added_ingredients_of_type_Piece__return_expected_value(self):
        user = create_user(**self.VALID_USER_DATA)

        ingredient = ingredient_create('test', 'Piece', 1, user)

        recipe = recipe_create(self.TEST_RECIPE_NAME, user)

        recipe_ingredient_create(recipe, ingredient, 1)

        increase_percentage = increase_percentage_create(recipe, 0)

        all_ingredients = RecipeIngredient.objects.all()

        expected_return_value = 1

        end_value, _ = calculate_price_return_in_leva(increase_percentage.percentage, all_ingredients)

        self.assertEqual(expected_return_value, end_value)

    def test_calculate_price__with_added_ingredients_of_all_types_and_added_increase_percentage__return_expected_value(
            self):
        user = create_user(**self.VALID_USER_DATA)

        ingredient = ingredient_create('test', 'Kilogram', 1, user)
        ingredient2 = ingredient_create('test2', 'Piece', 1, user)

        recipe = recipe_create(self.TEST_RECIPE_NAME, user)

        recipe_ingredient_create(recipe, ingredient, 100)
        recipe_ingredient_create(recipe, ingredient2, 1)

        increase_percentage = increase_percentage_create(recipe, 100)

        all_ingredients = RecipeIngredient.objects.all()

        expected_end_value = 1.1
        expected_increased_end_value = 2.2

        end_price, increased_end_price = calculate_price_return_in_leva(increase_percentage.percentage, all_ingredients)
        self.assertEqual(expected_end_value, end_price)
        self.assertEqual(expected_increased_end_value, increased_end_price)
