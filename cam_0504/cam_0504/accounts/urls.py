from django.contrib.auth import views as auth_views
from django.urls import path

from cam_0504.accounts.views import RegisterUserView, LogInView, ChangeUserPasswordView, ProfileDetailsView, \
    ProfileEditView, ProfileDeleteView, CustomPasswordResetView, CustomPasswordResetDoneView, \
    CustomPasswordResetConfirmView

urlpatterns = [
    path('register/', RegisterUserView.as_view(), name='register'),
    path('log-in/', LogInView.as_view(), name='log in'),
    path('log-out/', auth_views.LogoutView.as_view(), name='logout'),
    path('change_password/<int:pk>/', ChangeUserPasswordView.as_view(), name='change password'),

    path('profile/details/<int:pk>/', ProfileDetailsView.as_view(), name='profile details'),
    path('profile/edit/<int:pk>/', ProfileEditView.as_view(), name='profile edit'),
    path('profile/delete/<int:pk>/', ProfileDeleteView.as_view(), name='profile delete'),

    # path('password_reset/', auth_views.PasswordResetView.as_view(template_name='accounts/password_reset_form.html'),
    #      name='password_reset'),
    path('password_reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', CustomPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/',
         auth_views.PasswordResetCompleteView.as_view(template_name='accounts/password_reset_complete.html'),
         name='password_reset_complete'),

]
