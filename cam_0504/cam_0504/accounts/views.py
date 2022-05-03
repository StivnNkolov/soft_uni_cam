from django.contrib.auth import get_user_model, logout
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.views import generic as generic_views
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy

from cam_0504.accounts.forms import UserRegisterForm, UserLogInForm, ProfileEditForm, ChangeUserPasswordForm, \
    ProfileDeleteForm, CustomPasswordResetForm, CustomSetPasswordForm
from cam_0504.accounts.models import Profile
from common.mixins import AccountsAuthenticationPermissionMixin
from common.user_info import get_user_recipes_ingredients_count

UserModel = get_user_model()


class RegisterUserView(SuccessMessageMixin, generic_views.CreateView):
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('index')
    form_class = UserRegisterForm
    success_message = 'Successfully created account!'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('index')
        return super(RegisterUserView, self).dispatch(request, *args, **kwargs)


class LogInView(auth_views.LoginView):
    template_name = 'accounts/log-in.html'
    success_url = reverse_lazy('index')
    form_class = UserLogInForm

    def get_success_url(self):
        if self.success_url:
            return self.success_url
        return super().get_success_url()

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('index')
        return super().dispatch(request, *args, **kwargs)


class ChangeUserPasswordView(AccountsAuthenticationPermissionMixin, auth_views.PasswordChangeView):
    template_name = 'accounts/password_change.html'
    success_url = reverse_lazy('index')
    form_class = ChangeUserPasswordForm

    def form_valid(self, form):
        logout(self.request)
        return super().form_valid(form)


class ProfileDetailsView(AccountsAuthenticationPermissionMixin, generic_views.DetailView):
    template_name = 'accounts/profile_details.html'
    model = Profile
    context_object_name = 'current_profile'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        recipes, ingredients = get_user_recipes_ingredients_count(self.request.user)
        context['recipes_count'] = recipes
        context['ingredients_count'] = ingredients

        return context


class ProfileEditView(AccountsAuthenticationPermissionMixin, generic_views.UpdateView):
    template_name = 'accounts/profile_edit.html'
    model = Profile
    form_class = ProfileEditForm

    def get_success_url(self):
        return reverse_lazy('profile details', kwargs={'pk': self.request.user.id})


class ProfileDeleteView(AccountsAuthenticationPermissionMixin, generic_views.DeleteView):
    template_name = 'accounts/profile_delete.html'
    model = Profile
    form_class = ProfileDeleteForm
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        profile = self.object
        user = profile.user
        logout(self.request)
        profile.delete()
        user.delete()
        return redirect(self.success_url)


class CustomPasswordResetView(auth_views.PasswordResetView):
    template_name = 'accounts/password_reset_form.html'
    form_class = CustomPasswordResetForm


class CustomPasswordResetDoneView(auth_views.PasswordResetDoneView):
    template_name = 'accounts/password_reset_done.html'


class CustomPasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    template_name = 'accounts/password_reset_confirm.html'
    form_class = CustomSetPasswordForm
