"""This class does used to return to JSON."""
from django.http import JsonResponse

from .meilisearch_utils import Search, make_documents


async def index_search(request):
    """
    request 기반 검색 결과 response

    'q'는 [한자, 훈, 음, 훈 음], 
    's'는 ["jeonseo", "yeseo", "haeseo", "haengseo", "choseo"]
    'q'와 's'를 조합한 검색 결과를 JSON 형식으로 반환합니다.

    Args:
        request: Client 요청

    Raises:
        ValueError: 

    Returns:
        JsonResponse: 검색 결과
    """
    query = request.GET.get("q", "")
    style = request.GET.get("s", "")

    search = Search()
    documents = await make_documents()
    search.doc_settings(documents)

    results = search.search_character(query, style)
    return JsonResponse(results, safe=False,
                        json_dumps_params={'ensure_ascii': False})
