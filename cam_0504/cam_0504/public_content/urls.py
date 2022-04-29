from django.urls import path

from cam_0504.public_content.views.generic import HomeView
from cam_0504.public_content.views.public_content_views import MeasurementsView

urlpatterns = [
    path('', HomeView.as_view(), name='index'),
    path('measurements/', MeasurementsView.as_view(), name='measurements'),
]
