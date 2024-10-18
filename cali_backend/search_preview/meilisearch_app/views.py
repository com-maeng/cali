from django.http import JsonResponse

from .meilisearch_preview import search_character
# from .models import Post

# Create your views here.
def index_search(request):
    query = request.GET.get("q", "")
    results = search_character(query) # => <Queryset for Post>
    return JsonResponse(results, safe=False, json_dumps_params={'ensure_ascii': False})
