from django import test as django_tests
from django.contrib.auth import get_user_model
from django.urls import reverse, reverse_lazy

from cam_0504.accounts.models import Profile
from cam_0504.main_content.models import Recipe, Ingredient

UserModel = get_user_model()


class RegisterViewTests(django_tests.TestCase):

    def test_render_correct_template(self):
        response = self.client.get(reverse('register'))
        self.assertTemplateUsed(response, 'accounts/register.html')

    def test_when_user_is_logged_in__redirect_to_index(self):
        user = UserModel.objects.create(
            email='a@a.com',
        )
        user.set_password('1123qwer')
        user.save()

        user_credentials = {
            'email': 'a@a.com',
            'password': '1123qwer'
        }
        self.client.login(**user_credentials)
        response = self.client.get(reverse('register'))

        self.assertEqual(302, response.status_code)
        self.assertRedirects(response, reverse('index'))

    def test_when_all_credentials_valid_expects_to_create_user_and_profile(self):
        valid_user_credentials = {
            'email': 'a@a.com',
            'password1': '1123qwer',
            'password2': '1123qwer',
        }
        self.client.post(reverse('register'), data=valid_user_credentials)
        user = UserModel.objects.get(email='a@a.com')
        profile = Profile.objects.get(user=user)

        self.assertIsNotNone(user)
        self.assertIsNotNone(profile)


class LogInViewTests(django_tests.TestCase):
    VALID_USER_CREDENTIALS = {
        'email': 'a@a.com',
        'password': '1123qwer'
    }

    def test_render_correct_template(self):
        response = self.client.get(reverse('log in'))
        self.assertTemplateUsed(response, 'accounts/log-in.html')

    def test_when_user_is_logged_in__redirect_to_index(self):
        user = UserModel.objects.create(
            email='a@a.com',
        )
        user.set_password('1123qwer')
        user.save()

        user_credentials = {
            'email': 'a@a.com',
            'password': '1123qwer'
        }
        self.client.login(**user_credentials)
        response = self.client.get(reverse('log in'))

        self.assertEqual(302, response.status_code)
        self.assertRedirects(response, reverse('index'))


class ProfileDetailsViewTests(django_tests.TestCase):
    VALID_USER_CREDENTIALS = {
        'email': 'a@a.com',
        'password': '1123qwer'
    }

    @staticmethod
    def __create_recipe(name, user):
        recipe = Recipe.objects.create(
            name=name,
            user=user,
        )
        return recipe

    @staticmethod
    def __create_ingredient(name, product_type, price, user):
        ingredient = Ingredient.objects.create(
            name=name,
            type=product_type,
            price_per_type=price,
            user=user
        )
        return ingredient

    @staticmethod
    def __create_user(**credentials):
        return UserModel.objects.create_user(**credentials)

    def test_when_user_not_logged_in_redirect_to_log_in(self):
        UserModel.objects.create_user(
            email='a@a.com',
            password='1123qwer',
        )
        response = self.client.get(reverse('profile details', kwargs={'pk': 2}))
        self.assertEqual(302, response.status_code)
        self.assertRedirects(response, reverse('log in'))

    def test_when_open_with_not_existing_profile__return_404(self):
        UserModel.objects.create_user(
            email='a@a.com',
            password='1123qwer',
        )

        self.client.login(**{'email': 'a@a.com', 'password': '1123qwer'})

        response = self.client.get(reverse('profile details', kwargs={'pk': 2}))
        self.assertEqual(404, response.status_code)

    def test_render_correct_template(self):
        user = UserModel.objects.create_user(**self.VALID_USER_CREDENTIALS)
        self.client.login(**self.VALID_USER_CREDENTIALS)
        response = self.client.get(reverse('profile details', kwargs={'pk': user.pk}))
        self.assertTemplateUsed(response, 'accounts/profile_details.html')

    def test_when_user_have_1_recipe_and_1_ingredient__expect_both_to_return_1(self):
        user = self.__create_user(**self.VALID_USER_CREDENTIALS)

        self.__create_recipe('test', user)
        self.__create_ingredient('test', 'Kilogram', 1, user)

        expected_recipes_count = 1
        expected_ingredients_count = 1

        self.client.login(**self.VALID_USER_CREDENTIALS)
        response = self.client.get(reverse('profile details', kwargs={'pk': user.pk}))
        self.assertEqual(expected_recipes_count, response.context['recipes_count'])
        self.assertEqual(expected_ingredients_count, response.context['ingredients_count'])

    def test_when_user_have_0_recipe_and_0_ingredient__expect_both_to_return_0(self):
        user = self.__create_user(**self.VALID_USER_CREDENTIALS)

        expected_recipes_count = 0
        expected_ingredients_count = 0

        self.client.login(**self.VALID_USER_CREDENTIALS)
        response = self.client.get(reverse('profile details', kwargs={'pk': user.pk}))
        self.assertEqual(expected_recipes_count, response.context['recipes_count'])
        self.assertEqual(expected_ingredients_count, response.context['ingredients_count'])

    def test_when_user_have_2_recipe_and_0_ingredient__expect_recipes_to_return_2_ingredients_0(self):
        user = self.__create_user(**self.VALID_USER_CREDENTIALS)

        self.__create_recipe('test', user)
        self.__create_recipe('test1', user)

        expected_recipes_count = 2
        expected_ingredients_count = 0

        self.client.login(**self.VALID_USER_CREDENTIALS)
        response = self.client.get(reverse('profile details', kwargs={'pk': user.pk}))
        self.assertEqual(expected_recipes_count, response.context['recipes_count'])
        self.assertEqual(expected_ingredients_count, response.context['ingredients_count'])

    def test_context_return_recipes_ingredients_for_the_logged_user(self):
        user1 = self.__create_user(**self.VALID_USER_CREDENTIALS)
        user2 = self.__create_user(**{'email': 'b@b.com', 'password': '1123qwer'})

        self.__create_ingredient('test', 'Kilogram', 1, user1)

        self.__create_recipe('test user2', user2)
        self.__create_recipe('test2 user2', user2)

        expected_recipes_count_for_user1 = 0
        expected_ingredients_count_for_user1 = 1

        expected_recipes_count_for_user2 = 2

        self.client.login(**self.VALID_USER_CREDENTIALS)
        response = self.client.get(reverse('profile details', kwargs={'pk': user1.pk}))

        self.assertEqual(expected_recipes_count_for_user1, response.context['recipes_count'])
        self.assertEqual(expected_ingredients_count_for_user1, response.context['ingredients_count'])

        self.client.login(**{'email': 'b@b.com', 'password': '1123qwer'})
        response2 = self.client.get(reverse('profile details', kwargs={'pk': user2.pk}))
        self.assertEqual(expected_recipes_count_for_user2, response2.context['recipes_count'])

    def test_if_user_not_logged_in_redirect_to_log_in_view(self):
        response = self.client.get(reverse('profile details', kwargs={'pk': 1}))
        self.assertEqual(302, response.status_code)
        self.assertRedirects(response, reverse('log in'))


class ProfileEditViewTests(django_tests.TestCase):
    VALID_USER_CREDENTIALS = {
        'email': 'a@a.com',
        'password': '1123qwer'
    }

    def test_render_correct_template(self):
        user = UserModel.objects.create_user(**self.VALID_USER_CREDENTIALS)
        self.client.login(**self.VALID_USER_CREDENTIALS)
        response = self.client.get(reverse('profile details', kwargs={'pk': user.pk}))
        self.assertTemplateUsed(response, 'accounts/profile_details.html')

    def test_when_profile_edited__saves_the_changes_for_the_profile(self):
        user = UserModel.objects.create_user(
            email='a@a.com',
            password='1123qwer',
        )

        profile = Profile.objects.first()
        self.assertIsNotNone(profile)
        self.assertIsNone(profile.first_name)
        self.client.login(**{'email': 'a@a.com', 'password': '1123qwer'})
        self.client.post(reverse('profile edit', kwargs={'pk': profile.pk}), data={'first_name': 'Stivun'})
        profile_after_response = Profile.objects.first()
        self.assertEqual('Stivun', profile_after_response.first_name)

    def test_when_profile_edited_redirected_to_profile_details(self):
        user = UserModel.objects.create_user(
            email='a@a.com',
            password='1123qwer',
        )
        self.client.login(**{'email': 'a@a.com', 'password': '1123qwer'})
        response = self.client.post(reverse('profile edit', kwargs={'pk': user.pk}), data={'first_name': 'Stivun'})

        self.assertEqual(302, response.status_code)
        self.assertRedirects(response, reverse('profile details', kwargs={'pk': user.pk}))

    def test_when_user_is_not_logged_in_redirect_to_log_in(self):
        user = UserModel.objects.create_user(
            email='a@a.com',
            password='1123qwer',
        )

        response = self.client.get(reverse('profile edit', kwargs={'pk': user.pk}))

        self.assertEqual(302, response.status_code)
        self.assertRedirects(response, reverse_lazy('log in'))
