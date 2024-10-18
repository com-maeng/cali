from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('redisearch/', include('search_preview.redisearch_app.urls')),
    path('meilisearch/', include('search_preview.meilisearch_app.urls')),
]
