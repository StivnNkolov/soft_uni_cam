from django import test as django_tests
from django.contrib.auth import get_user_model

from cam_0504.accounts.models import Profile

UserModel = get_user_model()


class SignalTests(django_tests.TestCase):
    def test_when_user_created__create_profile(self):
        UserModel.objects.create_user(
            email='a@a.com',
            password='1123qwer',
        )

        profile = Profile.objects.first()

        self.assertIsNotNone(profile)
