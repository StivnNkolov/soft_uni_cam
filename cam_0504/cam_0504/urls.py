from django.contrib import admin
from django.urls import path, include

admin.site.site_header = 'Cook and Math admin panel'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('account/', include('cam_0504.accounts.urls')),
    path('', include('cam_0504.main_content.urls')),
    path('', include('cam_0504.public_content.urls'))
]
