from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('primera_app.urls')),
    path('taller/', include('app_gestion_taller.urls')),
]
