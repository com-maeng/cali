from django.urls import path
from .views import index_search

app_name = 'meilisearch_app'

urlpatterns = [
    path('', index_search, name='m_search'),
]
