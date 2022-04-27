from django.contrib import admin
from django.contrib.auth import get_user_model

from cam_0504.accounts.models import Profile

UserModel = get_user_model()


@admin.register(UserModel)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'is_staff', 'is_superuser',)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('email', 'date_created')
    ordering = ('-date_created',)
    search_fields = ('email',)
