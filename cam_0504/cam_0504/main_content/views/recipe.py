from decimal import Decimal

from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import generic as generic_views

from cam_0504.main_content.filters import RecipeFilter
from cam_0504.main_content.forms import RecipeCreateForm, RecipeDeleteForm, RecipePriceIncreasePercentUpdateForm, \
    IngredientCreateForm
from cam_0504.main_content.models import Recipe, IncreasePercentage, Ingredient
from common.calculations import calculate_price_return_in_leva
from common.mixins import AuthenticationRedirectToLoginMixin


class RecipeMainView(AuthenticationRedirectToLoginMixin, generic_views.TemplateView):
    template_name = 'main_content/recipe_main.html'
    model = Recipe

    def get_queryset(self):
        needed_queryset = Recipe.objects.filter(user=self.request.user)
        return needed_queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        recipe_filter = RecipeFilter(self.request.GET, queryset=self.get_queryset())
        recipes_count = self.get_queryset().count()
        found_item = recipe_filter.qs

        context['found_item'] = found_item
        context['recipe_filter'] = recipe_filter
        context['recipes_count'] = recipes_count
        return context


class RecipesListView(AuthenticationRedirectToLoginMixin, generic_views.ListView):
    template_name = 'main_content/recipes_list.html'
    model = Recipe
    paginate_by = 10

    def get_queryset(self):
        needed_queryset = Recipe.objects.filter(user=self.request.user).order_by('date_created')
        return needed_queryset


class RecipeCreateView(AuthenticationRedirectToLoginMixin, generic_views.CreateView):
    template_name = 'main_content/recipe_create.html'
    model = Recipe
    form_class = RecipeCreateForm
    success_url = reverse_lazy('recipes main')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class RecipeDetailsView(AuthenticationRedirectToLoginMixin, generic_views.DetailView):
    template_name = 'main_content/recipe_details.html'
    model = Recipe

    def get(self, request, *args, **kwargs):
        recipe = Recipe.objects.get(id=self.kwargs['pk'])
        self.request.session['recipe'] = recipe.id
        return super().get(request, *args, **kwargs)


class RecipeDeleteView(AuthenticationRedirectToLoginMixin, generic_views.DeleteView):
    template_name = 'main_content/recipe_delete.html'
    model = Recipe
    form_class = RecipeDeleteForm
    success_url = reverse_lazy('recipes main')


def recipe_finalise(request, pk):
    recipe = Recipe.objects.prefetch_related('recipeingredient_set').get(id=pk)
    ingredients = recipe.recipeingredient_set.all()
    recipe_increase_percentage = recipe.increasepercentage.percentage
    price, increased_price = calculate_price_return_in_leva(recipe_increase_percentage, ingredients)
    recipe.price = price
    recipe.increased_price = increased_price
    recipe.save()
    return redirect('recipe details', pk)


class RecipePriceIncreasePercentUpdate(AuthenticationRedirectToLoginMixin, generic_views.UpdateView):
    template_name = 'main_content/recipe_price__increase_percentage_create.html'
    model = IncreasePercentage
    form_class = RecipePriceIncreasePercentUpdateForm

    def get_success_url(self):
        percentage = IncreasePercentage.objects.get(id=self.kwargs['pk'])
        recipe_percentage_id = percentage.recipe.id
        return reverse_lazy('recipe details', kwargs={'pk': recipe_percentage_id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_recipe_id = self.request.session.get('recipe')
        context['current_recipe_id'] = current_recipe_id
        return context


class RecipeAddAsIngredientView(AuthenticationRedirectToLoginMixin, generic_views.CreateView):
    template_name = 'main_content/recipe_add_as_ingredient.html'
    model = Ingredient
    form_class = IngredientCreateForm
    success_url = reverse_lazy('recipes main')

    def get_form(self, form_class=None):
        form = super().get_form(self.form_class)
        recipe = Recipe.objects.get(id=self.kwargs['pk'])
        form.initial = {
            'name': recipe.name,
            'price_per_type': Decimal(recipe.price),
        }
        return form

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


def recipe_delete_all_view(request):
    recipes_for_deletion = Recipe.objects.filter(user=request.user)
    form = RecipeDeleteForm()

    if request.method == 'POST':
        form = RecipeDeleteForm(request.POST)
        if form.is_valid():
            recipes_for_deletion.delete()
            return redirect('recipes main')

    context = {
        'form': form,
    }
    return render(request, 'main_content/recipe_delete_all.html', context)
