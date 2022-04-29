from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth import forms as auth_forms


from cam_0504.accounts.models import Profile
from common.mixins import CrispyFormHelperCustomMixin, CrispyFormHelperBuildinMixin

UserModel = get_user_model()


class UserRegisterForm(CrispyFormHelperCustomMixin, auth_forms.UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = UserModel
        fields = ['email', 'password1', 'password2']


class UserLogInForm(CrispyFormHelperBuildinMixin, auth_forms.AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class ProfileEditForm(CrispyFormHelperCustomMixin, forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'age', 'city_name', 'email', 'restaurant_name']
        labels = {
            'first_name': 'First Name:',
            'last_name': 'Last Name:',
            'age': 'Age:',
            'city_name': 'City:',
            'email': 'Email:',
            'restaurant_name': "Restaurant's name:"
        }
        widgets = {
            'age': forms.NumberInput(
                attrs={
                    'min': 0,
                },
            ),
        }


class ChangeUserPasswordForm(CrispyFormHelperBuildinMixin, auth_forms.PasswordChangeForm):
    def __init__(self, user, *args, **kwargs):
        super().__init__(user, *args, **kwargs)


class ProfileDeleteForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = []


class CustomPasswordResetForm(CrispyFormHelperBuildinMixin, auth_forms.PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class CustomSetPasswordForm(CrispyFormHelperCustomMixin, auth_forms.SetPasswordForm):
    def __init__(self, user, *args, **kwargs):
        super().__init__(user, *args, **kwargs)
