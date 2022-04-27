import django_filters

from cam_0504.main_content.models import Ingredient, Recipe


class IngredientFilter(django_filters.FilterSet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if not self.data.get('name'):
            self.queryset = self.queryset.none()

        self.filters['name'].label = 'Search in ingredients by name'

    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains')

    class Meta:
        model = Ingredient
        fields = ['name']


class RecipeFilter(django_filters.FilterSet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if not self.data.get('name'):
            self.queryset = self.queryset.none()

        self.filters['name'].label = 'Search in recipes by name'

    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains')

    class Meta:
        model = Recipe
        fields = ['name']
