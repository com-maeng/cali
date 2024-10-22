from django.urls import path

from .views import index_search

app_name = 'main'

urlpatterns = [
    path('search', index_search, name='search'),
]
