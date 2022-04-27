from django.contrib import admin

from cam_0504.main_content.models import Ingredient, Recipe, RecipeIngredient, IncreasePercentage


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'price_per_type', 'user',)
    ordering = ('user', 'name',)
    list_filter = ('user',)
    list_per_page = 20


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'user',)
    ordering = ('user', 'name',)
    list_filter = ('user',)
    list_per_page = 20


@admin.register(RecipeIngredient)
class RecipeIngredientAdmin(admin.ModelAdmin):
    list_display = ('ingredient', 'recipe',)
    ordering = ('ingredient', 'recipe',)
    list_per_page = 20


@admin.register(IncreasePercentage)
class IncreasePercentageAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'percentage',)
    ordering = ('percentage',)
    list_per_page = 20
