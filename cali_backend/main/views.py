"""This class does used to return to JSON."""
from django.http import JsonResponse

from adrf.views import APIView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .meilisearch_utils import Search, make_documents


class SearchView(APIView):

    q = openapi.Parameter(
        'q', openapi.IN_PATH, description='query', required=True,
        type=openapi.TYPE_STRING)

    s = openapi.Parameter(
        's', openapi.IN_PATH, description='style', required=True,
        type=openapi.TYPE_STRING)

    @swagger_auto_schema(tags=['검색'],
                         manual_parameters=[q, s],
                         responses={200: 'Success'})
    async def get(self, request):
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
        return JsonResponse(results, status=200)
