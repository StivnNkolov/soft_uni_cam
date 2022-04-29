from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit
from django.shortcuts import redirect


class AuthenticationRedirectToLoginMixin:

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('log in')
        return super().dispatch(request, *args, **kwargs)


class CrispyFormHelperMixin:
    @property
    def helper(self):
        helper = FormHelper()
        helper.form_method = 'POST'
        helper.layout = Layout(

        )
        for field in self.Meta().fields:
            helper.layout.append(
                Field(field, )
            )
        helper.layout.append(
            Submit(
                'submit',
                'Save',
                css_class='btn btn-md mt-2 btn-secondary',
            )
        )
        helper.field_class = 'mb-3'
        helper.label_class = 'mb-3'

        return helper


class CrispyFormHelperCustomMixin:
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
            css_class='btn btn-md btn-secondary',
        ))
        helper.field_class = 'col-9 mb-3'
        helper.label_class = 'col-3'

        return helper


class CrispyFormHelperBuildinMixin:
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
