from django.contrib import admin
from django.urls import path, include, re_path

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Cali",
        default_version='0.0.1',
        description="Cali-project API 문서",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="-"),  # 부가정보
        license=openapi.License(name="mit"),  # 부가정보
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    re_path(
        r'swagger(?P<format>\.json|\.yaml)', schema_view.without_ui(
            cache_timeout=0),
        name='schema-json'),
    path(
        r'swagger', schema_view.with_ui('swagger', cache_timeout=0),
        name='schema-swagger-ui'),
    path(
        r'redoc', schema_view.with_ui('redoc', cache_timeout=0),
        name='schema-redoc-v1'),
    path('admin/', admin.site.urls),
    path('', include('main.urls')),]
