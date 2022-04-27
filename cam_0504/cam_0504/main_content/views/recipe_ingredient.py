from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import generic as generic_views

from cam_0504.main_content.filters import IngredientFilter
from cam_0504.main_content.forms import RecipeIngredientCreateForm, RecipeIngredientEditForm
from cam_0504.main_content.models import RecipeIngredient, Recipe, Ingredient
from common.mixins import AuthenticationRedirectToLoginMixin


class RecipeIngredientChooseView(AuthenticationRedirectToLoginMixin, generic_views.ListView):
    template_name = 'main_content/recipe_ingredient_choose.html'
    model = Ingredient

    def get_queryset(self):
        ingredients = Ingredient.objects.filter(user=self.request.user)
        return ingredients

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)

        recipe = Recipe.objects.get(id=self.kwargs['pk'])
        self.request.session['recipe'] = recipe.id
        ingredient_filter = IngredientFilter(self.request.GET, queryset=self.get_queryset())
        found_item = ingredient_filter.qs

        context['current_recipe'] = recipe
        context['found_item'] = found_item
        context['ingredient_filter'] = ingredient_filter

        return context


class RecipeIngredientAddView(AuthenticationRedirectToLoginMixin, generic_views.CreateView):
    template_name = 'main_content/recipe_ingredient_add.html'
    model = RecipeIngredient
    form_class = RecipeIngredientCreateForm

    def get_queryset(self):
        ingredients = Ingredient.objects.get(id=self.kwargs['pk'])
        return ingredients

    def get_form(self, form_class=None):
        form = super().get_form(self.form_class)
        ingredient_queryset = Ingredient.objects.filter(id=self.kwargs['pk'])
        form.initial = {
            'ingredient': ingredient_queryset[0],
        }
        form.fields['ingredient'].queryset = ingredient_queryset
        return form

    def form_valid(self, form):
        recipe_id = self.request.session.get('recipe')
        recipe = Recipe.objects.get(id=recipe_id)
        recipe_ingredient = RecipeIngredient.objects.create(
            recipe=recipe,
            ingredient=form.cleaned_data['ingredient'],
            amount=form.cleaned_data['amount'],
        )
        recipe_ingredient.save()
        return redirect('recipe details', recipe.id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        recipe_id = self.request.session.get('recipe')
        context['current_recipe_id'] = recipe_id
        return context


class RecipeIngredientEditView(AuthenticationRedirectToLoginMixin, generic_views.UpdateView):
    template_name = 'main_content/recipe_ingr_edit.html'
    model = RecipeIngredient
    form_class = RecipeIngredientEditForm

    def get_success_url(self):
        recipe_id = Recipe.objects.get(recipeingredient=self.object).id
        return reverse_lazy('recipe details', kwargs={'pk': recipe_id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        recipe_id = Recipe.objects.get(recipeingredient=self.object).id

        context['current_recipe_id'] = recipe_id
        return context


def recipe_ingredient_delete_view(request, pk):
    recipe_ingredient = RecipeIngredient.objects.get(id=pk)
    recipe = recipe_ingredient.recipe
    recipe_ingredient.delete()
    return redirect('recipe details', recipe.id)
