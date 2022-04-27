from django.views import generic as generic_views

from cam_0504.public_content.helper import create_recipe_ingredients
from cam_0504.public_content.models import Product, PublicRecipe, PublicRecipeIngredient


class MeasurementsView(generic_views.TemplateView):
    template_name = 'public_content/measurements.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        products = Product.objects.all()
        context['products'] = products

        return context


class PublicRecipeDetailsView(generic_views.DetailView):
    template_name = 'public_content/recipe_details.html'
    model = PublicRecipe

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ingredients = PublicRecipeIngredient.objects.filter(recipe_id=self.object.id)
        finalised_ingredients = create_recipe_ingredients(ingredients)
        context['ingredients'] = finalised_ingredients
        return context
