from django.urls import path
from .views import index_search

app_name = 'redisearch_app'

urlpatterns = [
    path('', index_search, name='search'),
]
