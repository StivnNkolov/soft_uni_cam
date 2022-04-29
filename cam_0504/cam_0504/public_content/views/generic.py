from django.views import generic as generic_views


class HomeView(generic_views.TemplateView):
    # template_name = 'main_content/index.html'
    template_name = 'public_content/index.html'
