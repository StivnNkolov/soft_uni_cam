from django.urls import path

from cam_0504.main_content.views.ingredient import IngredientsListView, IngredientCreateView, IngredientEditView, \
    IngredientDeleteView, IngredientMainView, ingredient_delete_all_view
from cam_0504.main_content.views.recipe import RecipesListView, RecipeCreateView, RecipeDetailsView, recipe_finalise, \
    RecipeDeleteView, RecipePriceIncreasePercentUpdate, RecipeAddAsIngredientView, RecipeMainView, \
    recipe_delete_all_view
from cam_0504.main_content.views.recipe_ingredient import RecipeIngredientEditView, \
    recipe_ingredient_delete_view, RecipeIngredientChooseView, RecipeIngredientAddView

urlpatterns = [
    path('ingredients_main/', IngredientMainView.as_view(), name='ingredients main'),
    path('ingredients/list/', IngredientsListView.as_view(), name='ingredients list'),
    path('ingredient/create/', IngredientCreateView.as_view(), name='ingredient create'),
    path('ingredient/edit/<int:pk>/', IngredientEditView.as_view(), name='ingredient edit'),
    path('ingredient/delete/<int:pk>/', IngredientDeleteView.as_view(), name='ingredient delete'),
    path('ingredient/delete/all/', ingredient_delete_all_view, name='ingredient delete all'),

    path('recipe_main/', RecipeMainView.as_view(), name='recipes main'),
    path('recipes/', RecipesListView.as_view(), name='recipes list'),
    path('recipe/create/', RecipeCreateView.as_view(), name='recipe create'),
    path('recipe/details/<int:pk>/', RecipeDetailsView.as_view(), name='recipe details'),
    path('recipe/finalise/<int:pk>/', recipe_finalise, name='recipe finalise'),
    path('recipe/delete/<int:pk>', RecipeDeleteView.as_view(), name='recipe delete'),
    path('recipe/delete/all/', recipe_delete_all_view, name='recipe delete all'),
    path('recipe/price_increase/<int:pk>/', RecipePriceIncreasePercentUpdate.as_view(),
         name='recipe increase price percentage'),
    path('recipe/as_ingredient/<int:pk>/', RecipeAddAsIngredientView.as_view(), name='recipe add as ingredient'),

    path('recipe_ingredient/choose/<int:pk>/', RecipeIngredientChooseView.as_view(), name='recipe ingredient choose'),
    path('recipe_ingredient/create/<int:pk>/', RecipeIngredientAddView.as_view(), name='recipe ingredient create'),
    path('recipe_ingredient/edit/<int:pk>/', RecipeIngredientEditView.as_view(), name='recipe ingredient edit'),
    path('recipe_ingredient/delete/<int:pk>/', recipe_ingredient_delete_view, name='recipe ingredient delete'),
]
