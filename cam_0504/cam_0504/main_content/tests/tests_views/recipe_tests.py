from django.contrib.auth import get_user_model
from django import test as django_tests
from django.urls import reverse

from cam_0504.main_content.models import Recipe, Ingredient, IncreasePercentage
from common.functions_for_tests import create_user, recipe_create

UserModel = get_user_model()


class RecipeMainViewTests(django_tests.TestCase):
    VALID_USER_CREDENTIALS = {
        'email': 'a@a.com',
        'password': '1123qwer'
    }

    VALID_USER_CREDENTIALS_2 = {
        'email': 'b@b.com',
        'password': '1123qwer'
    }

    def __create_get_response(self):
        return self.client.get(reverse('recipes main'))

    def test_render_correct_template(self):
        create_user(**self.VALID_USER_CREDENTIALS)

        self.client.login(**self.VALID_USER_CREDENTIALS)
        response = self.__create_get_response()

        self.assertTemplateUsed(response, 'main_content/recipe_main.html')

    def test_if_user_not_logged_in_redirect(self):
        response = self.client.post(reverse('recipes main'))

        self.assertRedirects(response, reverse('log in'))
        self.assertEqual(302, response.status_code)

    def test_if_recipe_context_return_the_amount_of_recipes_for_the_user(self):
        user_1 = create_user(**self.VALID_USER_CREDENTIALS)
        user_2 = create_user(**self.VALID_USER_CREDENTIALS_2)

        recipe_create('test', user_1)
        recipe_create('test2', user_1)
        recipe_create('test', user_2)

        self.client.post(reverse('recipes main'))
        recipes_count_for_user_1 = Recipe.objects.filter(user=user_1).count()

        self.assertEqual(2, recipes_count_for_user_1)


class RecipeListViewTests(django_tests.TestCase):
    VALID_USER_CREDENTIALS = {
        'email': 'a@a.com',
        'password': '1123qwer'
    }

    VALID_USER_CREDENTIALS_2 = {
        'email': 'b@b.com',
        'password': '1123qwer'
    }

    def test_render_correct_template(self):
        create_user(**self.VALID_USER_CREDENTIALS)

        self.client.login(**self.VALID_USER_CREDENTIALS)
        response = self.client.get(reverse('recipes list'))

        self.assertTemplateUsed(response, 'main_content/recipes_list.html')

    def test_if_user_not_logged_in_redirect(self):
        response = self.client.post(reverse('recipes list'))

        self.assertRedirects(response, reverse('log in'))
        self.assertEqual(302, response.status_code)

    def test_context_return_the_recipes_for_the_logged_in_user(self):
        user_1 = create_user(**self.VALID_USER_CREDENTIALS)
        user_2 = create_user(**self.VALID_USER_CREDENTIALS_2)

        recipe_create('test1', user_1)
        recipe_create('test2', user_1)
        recipe_create('test1', user_2)

        self.client.login(**self.VALID_USER_CREDENTIALS)
        response = self.client.get(reverse('recipes list'))
        expected_recipes_for_user = Recipe.objects.filter(user=user_1)

        self.assertListEqual(list(expected_recipes_for_user), list(response.context['object_list']))


class RecipeCreateViewTests(django_tests.TestCase):
    VALID_USER_CREDENTIALS = {
        'email': 'a@a.com',
        'password': '1123qwer'
    }

    VALID_USER_CREDENTIALS_2 = {
        'email': 'b@b.com',
        'password': '1123qwer'
    }

    def test_if_user_not_logged_in_redirect(self):
        response = self.client.post(reverse('recipe create'))

        self.assertRedirects(response, reverse('log in'))
        self.assertEqual(302, response.status_code)

    def test_when_recipe_is_created__recipe_ingredient_is_also_created(self):
        user = create_user(**self.VALID_USER_CREDENTIALS)
        recipe_data = {
            'name': 'test',
            'user': user,
        }

        self.client.login(**self.VALID_USER_CREDENTIALS)
        self.client.post(reverse('recipe create'), data=recipe_data)

        increase_percentage = IncreasePercentage.objects.first()

        self.assertIsNotNone(increase_percentage)


class RecipeDetailViewTests(django_tests.TestCase):
    VALID_USER_CREDENTIALS = {
        'email': 'a@a.com',
        'password': '1123qwer'
    }

    def test_if_user_not_logged_in_redirect(self):
        user = create_user(**self.VALID_USER_CREDENTIALS)
        recipe = recipe_create('test1', user)
        response = self.client.get(reverse('recipe details', kwargs={'pk': recipe.pk}))
        self.assertRedirects(response, reverse('log in'))
        self.assertEqual(302, response.status_code)

    def test_if_session_contains_recipe(self):
        user = create_user(**self.VALID_USER_CREDENTIALS)
        self.client.login(**{'email': 'a@a.com', 'password': '1123qwer'})
        self.client.post(reverse('recipe create'), data={'name': 'test', 'user': user})
        recipe = Recipe.objects.first()
        self.client.get(reverse('recipe details', kwargs={'pk': recipe.pk}))
        self.assertIsNotNone(self.client.session.get('recipe'))
        self.assertEqual(recipe.id, self.client.session.get('recipe'))


class RecipeDeleteViewTests(django_tests.TestCase):
    VALID_USER_CREDENTIALS = {
        'email': 'a@a.com',
        'password': '1123qwer'
    }

    def test_if_user_not_logged_in_redirect(self):
        user = create_user(**self.VALID_USER_CREDENTIALS)
        recipe = recipe_create('test1', user)

        response = self.client.get(reverse('recipe delete', kwargs={'pk': recipe.pk}))

        self.assertRedirects(response, reverse('log in'))
        self.assertEqual(302, response.status_code)

    def test_if_recipe_deleted__increase_percentage_is_also_deleted(self):
        user = create_user(**self.VALID_USER_CREDENTIALS)

        self.client.login(**{'email': 'a@a.com', 'password': '1123qwer'})
        self.client.post(reverse('recipe create'), data={'name': 'test', 'user': user})

        recipe = Recipe.objects.first()
        increase_percentage = IncreasePercentage.objects.first()
        self.assertIsNotNone(recipe)
        self.assertIsNotNone(increase_percentage)

        self.client.post(reverse('recipe delete', kwargs={'pk': recipe.pk}))
        self.assertIsNone(Recipe.objects.first())
        self.assertIsNone(IncreasePercentage.objects.first())


class RecipePriceIncreasePercentUpdateTests(django_tests.TestCase):
    VALID_USER_CREDENTIALS = {
        'email': 'a@a.com',
        'password': '1123qwer'
    }

    def test_if_user_not_logged_in_redirect(self):
        response = self.client.get(reverse('recipe increase price percentage', kwargs={'pk': 1}))
        self.assertRedirects(response, reverse('log in'))
        self.assertEqual(302, response.status_code)

    def test_when_updated_redirect_to_exact_recipe_details_view(self):
        user = create_user(**self.VALID_USER_CREDENTIALS)
        self.client.login(**{'email': 'a@a.com', 'password': '1123qwer'})
        self.client.post(reverse('recipe create'), data={'name': 'test', 'user': user})
        recipe = Recipe.objects.first()
        increase_percentage = IncreasePercentage.objects.first()
        response = self.client.post(reverse('recipe increase price percentage', kwargs={'pk': recipe.pk}),
                                    data={'percentage': 20})
        self.assertEqual(302, response.status_code)
        self.assertRedirects(response, reverse('recipe details', kwargs={'pk': recipe.pk}))


class RecipeAddAsIngredientTests(django_tests.TestCase):
    VALID_USER_CREDENTIALS = {
        'email': 'a@a.com',
        'password': '1123qwer'
    }

    def test_if_user_not_logged_in_redirect(self):
        user = create_user(**self.VALID_USER_CREDENTIALS)
        recipe = recipe_create('test1', user)
        response = self.client.get(reverse('recipe add as ingredient', kwargs={'pk': recipe.pk}))
        self.assertRedirects(response, reverse('log in'))
        self.assertEqual(302, response.status_code)

    def test_if_actually_recipe_is_added_as_ingredient(self):
        user = create_user(**self.VALID_USER_CREDENTIALS)
        recipe = recipe_create('test1', user)

        ingredients = Ingredient.objects.all()
        self.assertListEqual([], list(ingredients))
        data = {
            'name': recipe.name,
            'type': 'Kilogram',
            'price_per_type': recipe.price,
            'user': user
        }

        self.client.login(**{'email': 'a@a.com', 'password': '1123qwer'})
        self.client.post(reverse('recipe add as ingredient', kwargs={'pk': recipe.pk}), data=data)
        ingredients_after_addition = Ingredient.objects.all()
        self.assertEqual(1, len(list(ingredients_after_addition)))


class RecipeDeleteAllViewTests(django_tests.TestCase):
    VALID_USER_CREDENTIALS = {
        'email': 'a@a.com',
        'password': '1123qwer'
    }

    VALID_USER_CREDENTIALS_2 = {
        'email': 'b@b.com',
        'password': '1123qwer'
    }

    def test_view_render_correct_template(self):
        UserModel.objects.create_user(
            **self.VALID_USER_CREDENTIALS
        )
        self.client.login(**self.VALID_USER_CREDENTIALS)

        response = self.client.get(reverse('recipe delete all'))

        self.assertTemplateUsed(response, 'main_content/recipe_delete_all.html')

    def test_view_delete_all_recipes_for_the_user_that_is_logged_in_and_redirect(self):
        user = create_user(**self.VALID_USER_CREDENTIALS)

        user2 = create_user(**self.VALID_USER_CREDENTIALS_2)
        recipe_create('test', user)
        recipe_create('test2', user)
        recipe_create('test3', user2)

        initial_recipes_for_user = Recipe.objects.filter(user=user)
        initial_recipes_for_user2 = Recipe.objects.filter(user=user2)

        self.assertEqual(2, len(initial_recipes_for_user))
        self.assertEqual(1, len(initial_recipes_for_user2))

        self.client.login(**self.VALID_USER_CREDENTIALS)
        response = self.client.post(reverse('recipe delete all'))
        recipes_after_deletion_user = Recipe.objects.filter(user=user)
        recipes_after_deletion_user2 = Recipe.objects.filter(user=user2)

        self.assertEqual(0, len(recipes_after_deletion_user))
        self.assertEqual(1, len(recipes_after_deletion_user2))
        self.assertEqual(302, response.status_code)
        self.assertRedirects(response, reverse('recipes main'))
