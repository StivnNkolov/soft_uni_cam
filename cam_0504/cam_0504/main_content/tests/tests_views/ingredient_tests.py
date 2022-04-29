from django import test as django_tests
from django.contrib.auth import get_user_model
from django.urls import reverse

from cam_0504.main_content.models import Ingredient, Recipe, RecipeIngredient
from common.functions_for_tests import ingredient_create, create_user, recipe_create, recipe_ingredient_create

UserModel = get_user_model()


class IngredientMainViewTests(django_tests.TestCase):
    VALID_USER_CREDENTIALS = {
        'email': 'a@a.com',
        'password': '1123qwer'
    }

    def __create_get_response(self):
        return self.client.get(reverse('ingredients main'))

    def test_render_correct_template(self):
        create_user(**self.VALID_USER_CREDENTIALS)

        self.client.login(**self.VALID_USER_CREDENTIALS)
        response = self.__create_get_response()

        self.assertTemplateUsed(response, 'main_content/ingredients_main.html')
        self.assertEqual(200, response.status_code)

    def test_if_user_not_logged_in_redirect(self):
        response = self.__create_get_response()

        self.assertRedirects(response, reverse('log in'))
        self.assertEqual(302, response.status_code)

    def test_view_returns_correct_queryset_for_the_user(self):
        user = create_user(**self.VALID_USER_CREDENTIALS)
        user2 = create_user(**{
            'email': 'b@b.com',
            'password': '1123qwer'
        })

        self.client.login(**self.VALID_USER_CREDENTIALS)
        response = self.__create_get_response()

        ingredient_create('test', 'kilogram', 1, user)
        ingredient_create('test for user 2', 'kilogram', 1, user2)

        expected_ingredients_for_user = Ingredient.objects.filter(user=user)
        self.assertListEqual(list(expected_ingredients_for_user), list(response.context['object_list']))
        self.assertEqual(1, len(list(response.context['object_list'])))

    def test_context_return_the_amount_of_ingredients_for_the_user(self):
        user = create_user(**self.VALID_USER_CREDENTIALS)
        user2 = create_user(**{
            'email': 'b@b.com',
            'password': '1123qwer'
        })

        ingredient_create('test', 'kilogram', 1, user)
        ingredient_create('test for user 2', 'kilogram', 1, user2)

        self.client.login(**self.VALID_USER_CREDENTIALS)
        response = self.__create_get_response()

        expected_ingredients_for_user_count = Ingredient.objects.filter(user=user).count()
        self.assertEqual(expected_ingredients_for_user_count, response.context['ingredients_count'])


class IngredientsListViewTests(django_tests.TestCase):
    VALID_USER_CREDENTIALS = {
        'email': 'a@a.com',
        'password': '1123qwer'
    }

    def __create_get_response(self):
        return self.client.get(reverse('ingredients list'))

    def test_render_correct_template(self):
        create_user(**self.VALID_USER_CREDENTIALS)

        self.client.login(**self.VALID_USER_CREDENTIALS)
        response = self.__create_get_response()

        self.assertTemplateUsed(response, 'main_content/ingredients_list.html')
        self.assertEqual(200, response.status_code)

    def test_if_user_not_logged_in_redirect(self):
        response = self.__create_get_response()

        self.assertRedirects(response, reverse('log in'))
        self.assertEqual(302, response.status_code)

    def test_view_returns_correct_queryset_for_the_user(self):
        user = create_user(**self.VALID_USER_CREDENTIALS)
        user2 = create_user(**{
            'email': 'b@b.com',
            'password': '1123qwer'
        })

        ingredient_create('test', 'kilogram', 1, user)
        ingredient_create('test for user 2', 'kilogram', 1, user2)

        self.client.login(**self.VALID_USER_CREDENTIALS)
        response = self.__create_get_response()

        expected_ingredients_for_user = Ingredient.objects.filter(user=user)
        self.assertListEqual(list(expected_ingredients_for_user), list(response.context['object_list']))


class IngredientCreateViewTests(django_tests.TestCase):
    VALID_USER_CREDENTIALS = {
        'email': 'a@a.com',
        'password': '1123qwer'
    }

    def __create_get_response(self):
        return self.client.get(reverse('ingredient create'))

    def test_render_correct_template(self):
        create_user(**self.VALID_USER_CREDENTIALS)

        self.client.login(**self.VALID_USER_CREDENTIALS)
        response = self.__create_get_response()

        self.assertTemplateUsed(response, 'main_content/ingredient_create.html')
        self.assertEqual(200, response.status_code)

    def test_if_user_not_logged_in_redirect(self):
        response = self.__create_get_response()

        self.assertRedirects(response, reverse('log in'))
        self.assertEqual(302, response.status_code)

    def test_create_ingredient_with_correct_data__create_and_redirect(self):
        user = create_user(**self.VALID_USER_CREDENTIALS)

        self.client.login(**self.VALID_USER_CREDENTIALS)
        response = self.client.post(reverse('ingredient create'),
                                    data={
                                        'name': 'test',
                                        'type': 'Kilogram',
                                        'price_per_type': 1,
                                        'user': user}
                                    )
        ingredient = Ingredient.objects.first()

        self.assertIsNotNone(ingredient)
        self.assertRedirects(response, reverse('ingredients main'))
        self.assertEqual(302, response.status_code)

    def test_create_ingredient_with_bad_data__dont_create(self):
        user = create_user(**self.VALID_USER_CREDENTIALS)

        self.client.login(**self.VALID_USER_CREDENTIALS)
        self.client.post(reverse('ingredient create'),
                         data={
                             'name': 'test',
                             'type': 'pipi',
                             'price_per_type': 1,
                             'user': user}
                         )
        ingredient = Ingredient.objects.first()

        self.assertIsNone(ingredient)


class IngredientEditViewTests(django_tests.TestCase):
    VALID_USER_CREDENTIALS = {
        'email': 'a@a.com',
        'password': '1123qwer'
    }

    def test_render_correct_template(self):
        user = create_user(**self.VALID_USER_CREDENTIALS)
        ingredient = ingredient_create('test', 'kilogram', 1, user)

        self.client.login(**self.VALID_USER_CREDENTIALS)
        response = self.client.get(reverse('ingredient edit', kwargs={'pk': ingredient.pk}))

        self.assertTemplateUsed(response, 'main_content/ingredient_edit.html')
        self.assertEqual(200, response.status_code)

    def test_if_user_not_logged_in_redirect(self):
        user = create_user(**self.VALID_USER_CREDENTIALS)

        ingredient = ingredient_create('test', 'kilogram', 1, user)
        response = self.client.get(reverse('ingredient edit', kwargs={'pk': ingredient.pk}))

        self.assertRedirects(response, reverse('log in'))
        self.assertEqual(302, response.status_code)


class IngredientDeleteViewTests(django_tests.TestCase):
    VALID_USER_CREDENTIALS = {
        'email': 'a@a.com',
        'password': '1123qwer'
    }

    def test_render_correct_template(self):
        user = create_user(**self.VALID_USER_CREDENTIALS)

        ingredient = ingredient_create('test', 'kilogram', 1, user)
        self.client.login(**self.VALID_USER_CREDENTIALS)
        response = self.client.get(reverse('ingredient delete', kwargs={'pk': ingredient.pk}))

        self.assertTemplateUsed(response, 'main_content/ingredient_delete.html')
        self.assertEqual(200, response.status_code)

    def test_if_user_not_logged_in_redirect(self):
        user = create_user(**self.VALID_USER_CREDENTIALS)

        ingredient = ingredient_create('test', 'kilogram', 1, user)
        response = self.client.get(reverse('ingredient delete', kwargs={'pk': ingredient.pk}))

        self.assertRedirects(response, reverse('log in'))
        self.assertEqual(302, response.status_code)

    def test_context_return_the_recipes_that_contains_this_ingredient(self):
        user = create_user(**self.VALID_USER_CREDENTIALS)
        user_2 = create_user(**{'email': 'v@v.com', 'password': '1123qwe'})

        ingredient = ingredient_create('test', 'kilogram', 1, user)
        ingredient_create('test2', 'kilogram', 1, user)
        recipe = recipe_create('test recipe', user)
        recipe_create('test recipe', user_2)
        recipe_ingredient_create(recipe, ingredient)

        self.client.login(**self.VALID_USER_CREDENTIALS)
        response = self.client.get(reverse('ingredient delete', kwargs={'pk': ingredient.pk}))

        expected_recipes = Recipe.objects.filter(recipeingredient__ingredient__name=ingredient, user=user)
        expected_recipes_count = expected_recipes.count()

        self.assertListEqual(list(expected_recipes), list(response.context['recipes_containing_this_ingredient']))
        self.assertEqual(expected_recipes_count, response.context['recipes_containing_this_ingredient_count'])


class IngredientsDeleteAllTests(django_tests.TestCase):
    VALID_USER_CREDENTIALS = {
        'email': 'a@a.com',
        'password': '1123qwer'
    }

    def test_render_correct_template(self):
        create_user(**self.VALID_USER_CREDENTIALS)

        self.client.login(**self.VALID_USER_CREDENTIALS)
        response = self.client.get(reverse('ingredient delete all'))

        self.assertTemplateUsed(response, 'main_content/ingredient_delete_all.html')
        self.assertEqual(200, response.status_code)

    def test_if_user_not_logged_in_redirect(self):
        response = self.client.get(reverse('ingredient delete all'))

        self.assertEqual(302, response.status_code)

    def test_delete_all__deletes_all_ingredients_for_the_user(self):
        user = create_user(**self.VALID_USER_CREDENTIALS)
        user2 = create_user(**{'email': 'b@a.com', 'password': '1123qwer'})
        ingredient_create('test', 'kilogram', 1, user)
        ingredient_create('test for user 2', 'kilogram', 1, user2)
        ingredient_for_user_one = Ingredient.objects.get(user=user)
        ingredient_for_user_two = Ingredient.objects.get(user=user2)

        self.assertIsNotNone(ingredient_for_user_one)
        self.assertIsNotNone(ingredient_for_user_two)

        self.client.login(**self.VALID_USER_CREDENTIALS)
        response = self.client.post(reverse('ingredient delete all'))

        self.assertListEqual([], list(Ingredient.objects.filter(user=user)))
        self.assertIsNotNone(Ingredient.objects.get(user=user2))
        self.assertEqual(302, response.status_code)
