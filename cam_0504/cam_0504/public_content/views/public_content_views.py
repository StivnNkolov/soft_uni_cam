from django.views import generic as generic_views

from cam_0504.public_content.models import Product


class MeasurementsView(generic_views.TemplateView):
    template_name = 'public_content/measurements.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        products = Product.objects.all()
        context['products'] = products

        return context
