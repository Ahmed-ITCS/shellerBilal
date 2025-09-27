from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView,SpectacularSwaggerView
from rest_framework.schemas import get_schema_view


schema_view = get_schema_view(
    title="Munji Management API",
    description="API for managing Munji purchases, production, expenses, and global settings",
    version="1.0.0"
)
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('munji_app.urls')),

    # OpenAPI schema
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),  # always up-to-date

    # ReDoc UI (works in Django 5.x without templates)
    path('redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    path('swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]
