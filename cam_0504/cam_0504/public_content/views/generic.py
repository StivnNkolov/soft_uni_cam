from django.views import generic as generic_views

from cam_0504.public_content.models import PublicRecipe


class HomeView(generic_views.TemplateView):
    # template_name = 'main_content/index.html'
    template_name = 'public_content/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        salads = PublicRecipe.objects.filter(type='salad')
        desserts = PublicRecipe.objects.filter(type='dessert')
        main_dishes = PublicRecipe.objects.filter(type='main dish')

        context['salads'] = salads
        context['desserts'] = desserts
        context['main_dishes'] = main_dishes

        return context
