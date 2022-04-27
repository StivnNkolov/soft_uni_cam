from django.contrib import admin

from cam_0504.public_content.models import Product, PublicRecipe, PublicRecipeIngredient


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'tea_cup_in_grams', 'coffee_cup_in_grams', 'tablespoon_in_grams', 'tea_spoon_in_grams',)
    list_filter = ('tea_cup_in_grams', 'name',)
    search_fields = ('name', )
    ordering = ('name', )
    search_help_text = 'Search by name'
    list_per_page = 20


@admin.register(PublicRecipe)
class PublicRecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'type',)


@admin.register(PublicRecipeIngredient)
class PublicRecipeIngredientAdmin(admin.ModelAdmin):
    pass
