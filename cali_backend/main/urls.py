from django.urls import path

from .views import SearchView

app_name = 'main'

urlpatterns = [
    path('search', SearchView.as_view(), name='search'),
]
