"""This class does used rest_framework and Regular expressions."""
import re

from dependency_injector.wiring import inject, Provide
from cali_backend.containers import Container
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from meili.meilisearch_utils import SearchAPI


class SearchView(APIView):

    @inject
    def __init__(
            self, search_api: SearchAPI = Provide[Container.search_api]):
        super().__init__()
        self.search_api = search_api

    q = openapi.Parameter(
        'q', openapi.IN_PATH, description='query', required=True,
        type=openapi.TYPE_STRING)

    s = openapi.Parameter(
        's', openapi.IN_PATH, description='style', required=True,
        type=openapi.TYPE_STRING)

    @swagger_auto_schema(tags=['검색'],
                         manual_parameters=[q, s],
                         responses={200: 'Success'})
    def get(self, request):
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

        pattern = r'^[\u4e00-\u9fff\uac00-\ud7a3\s]+$'
        if not re.match(pattern, query):
            return Response(
                {"error": "검색어가 한문이나 한글이 아닙니다."},
                status=status.HTTP_400_BAD_REQUEST)

        # search request 마다 불필요 작업 발생(documents added), 불필요 작업 제거
        results = self.search_api.search_character(query, style)

        if not results:
            return Response({"error": "document가 구현되어 있지 않거나 없는 데이터입니다."},
                            status=status.HTTP_400_BAD_REQUEST)

        return Response(results, status=status.HTTP_200_OK)
