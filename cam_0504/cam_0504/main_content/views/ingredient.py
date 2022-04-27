from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic as generic_views

from cam_0504.main_content.filters import IngredientFilter
from cam_0504.main_content.forms import IngredientCreateForm, IngredientEditForm, IngredientDeleteForm
from cam_0504.main_content.models import Ingredient, Recipe
from common.mixins import AuthenticationRedirectToLoginMixin


class IngredientMainView(generic_views.TemplateView):
    template_name = 'main_content/ingredients_main.html'
    model = Ingredient

    def get_queryset(self):
        queryset = Ingredient.objects.filter(user=self.request.user)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ingredient_filter = IngredientFilter(self.request.GET, queryset=self.get_queryset())
        ingredients_count = self.get_queryset().count()
        found_item = ingredient_filter.qs

        context['found_item'] = found_item
        context['ingredient_filter'] = ingredient_filter
        context['ingredients_count'] = ingredients_count
        return context


class IngredientsListView(AuthenticationRedirectToLoginMixin, generic_views.ListView):
    template_name = 'main_content/ingredients_list.html'
    model = Ingredient
    paginate_by = 10

    def get_queryset(self):
        queryset = Ingredient.objects.filter(user=self.request.user).order_by('date_created')
        return queryset


class IngredientCreateView(AuthenticationRedirectToLoginMixin, generic_views.CreateView):
    template_name = 'main_content/ingredient_create.html'
    model = Ingredient
    form_class = IngredientCreateForm
    success_url = reverse_lazy('ingredients main')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class IngredientEditView(AuthenticationRedirectToLoginMixin, generic_views.UpdateView):
    template_name = 'main_content/ingredient_edit.html'
    model = Ingredient
    form_class = IngredientEditForm
    success_url = reverse_lazy('ingredients list')


class IngredientDeleteView(AuthenticationRedirectToLoginMixin, generic_views.DeleteView):
    template_name = 'main_content/ingredient_delete.html'
    model = Ingredient
    form_class = IngredientDeleteForm
    success_url = reverse_lazy('ingredients main')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        recipes_containing_this_ingredient = Recipe.objects.filter(recipeingredient__ingredient__name=self.object,
                                                                   user=self.request.user)
        recipes_containing_this_ingredient_count = len(recipes_containing_this_ingredient)

        context['recipes_containing_this_ingredient'] = recipes_containing_this_ingredient
        context['recipes_containing_this_ingredient_count'] = recipes_containing_this_ingredient_count
        return context


def ingredient_delete_all_view(request):
    ingredients_to_delete = Ingredient.objects.filter(user=request.user)
    form = IngredientDeleteForm()

    if request.method == 'POST':
        form = IngredientDeleteForm(request.POST)
        if form.is_valid():
            ingredients_to_delete.delete()
            return redirect('ingredients main')

    context = {
        'form': form,
    }
    return render(request, 'main_content/ingredient_delete_all.html', context)
