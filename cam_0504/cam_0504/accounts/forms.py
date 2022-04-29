from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth import forms as auth_forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Field

from cam_0504.accounts.models import Profile

UserModel = get_user_model()


# TODO some mixin for the helper property. Make em all the same

class UserRegisterForm(auth_forms.UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = UserModel
        fields = ['email', 'password1', 'password2']

    @property
    def helper(self):
        helper = FormHelper()
        helper.form_method = 'POST'
        helper.layout = Layout(

        )
        for field in self.Meta().fields:
            helper.layout.append(
                Field(field, wrapper_class='row')
            )
        helper.layout.append(
            Submit(
                'submit',
                'Submit',
                css_class='btn btn-md btn-secondary',
            )
        )
        helper.field_class = 'col-10 mb-3'
        helper.label_class = 'col-2'
        return helper


class UserLogInForm(auth_forms.AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @property
    def helper(self):
        helper = FormHelper()
        helper.form_method = 'POST'
        helper.layout = Layout(

        )
        for field in self.fields:
            helper.layout.append(
                Field(field, wrapper_class='row')
            )
        helper.layout.append(
            Submit(
                'submit',
                'Log in',
                css_class='btn btn-md btn-secondary',
            ))
        helper.field_class = 'col-10 mb-3'
        helper.label_class = 'col-2'
        return helper


class ProfileEditForm(forms.ModelForm):
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

    @property
    def helper(self):
        helper = FormHelper()
        helper.form_method = 'POST'
        helper.layout = Layout(

        )
        for field in self.Meta().fields:
            helper.layout.append(
                Field(field, wrapper_class='row'),
            )
        helper.layout.append(Submit(
            'submit',
            'Submit',
            css_class='brn btn-md btn-secondary',
        ))
        helper.field_class = 'col-9 mb-3'
        helper.label_class = 'col-3'

        return helper


class ChangeUserPasswordForm(auth_forms.PasswordChangeForm):
    def __init__(self, user, *args, **kwargs):
        super().__init__(user, *args, **kwargs)

    @property
    def helper(self):
        helper = FormHelper()
        helper.form_method = 'POST'
        helper.layout = Layout(

        )
        for field in self.fields:
            helper.layout.append(
                Field(field, wrapper_class='row')
            )
        helper.layout.append(
            Submit(
                'submit',
                'Submit',
                css_class='btn btn-md btn-secondary',

            )
        )
        helper.field_class = 'col-10 mb-3'
        helper.label_class = 'col-2'

        return helper


class ProfileDeleteForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = []


class CustomPasswordResetForm(auth_forms.PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @property
    def helper(self):
        helper = FormHelper()
        helper.form_method = 'POST'
        helper.layout = Layout()
        for field in self.fields:
            helper.layout.append(
                Field(field, wrapper_class='row')
            )
        helper.layout.append(
            Submit(
                'submit',
                'Submit',
                css_class='btn btn-md mt-2 btn-secondary',
            )
        )

        return helper


class CustomSetPasswordForm(auth_forms.SetPasswordForm):
    def __init__(self, user, *args, **kwargs):
        super().__init__(user, *args, **kwargs)

    @property
    def helper(self):
        helper = FormHelper()
        helper.form_method = 'POST'
        helper.layout = Layout()

        for field in self.fields:
            helper.layout.append(
                Field(field, wrapper_class='row')
            )
        helper.layout.append(
            Submit(
                'submit',
                'Submit',
                css_class='btn btn-md mt-3 btn-secondary',
            )
        )

        helper.field_class = 'col-9 mb-3 mt-3'
        helper.label_class = 'col-3 mt-3'
        return helper
