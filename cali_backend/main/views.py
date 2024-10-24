"""This class does used to return to JSON."""
from django.http import JsonResponse

from .meilisearch_preview import search_character


def index_search(request):
    """
    원점에서 출발한 물체의 착륙 지점을 계산한다.

    XY 평면 (0,0) 좌표에서 X축 기준 angle 방향과
    velocity 값의 속력으로 출발한 물체가, -Y축 방향
    중력 가속도 g 하에 얼마의 x 값에서 y=0에 도달할 지 계산하는 함수.

    Args:
        velocity: 물체의 초기 속력 (0 < velocity)
        angle: 물체의 초기 이동 방향 (0 < angle < 180, degree)
        g_constant: 중력 가속도 (0 < g_constant)

    Raises:
        ValueError: 인자가 조건에 맞지 않는 경우

    Returns:
        landing_position: 물체의 y 좌표가 0에 도달했을 시점에서의 x 좌표
    """
    query = request.GET.get("q", "")
    style = request.GET.get("s", "")
    print(f'{query}, {style}', flush=True)
    results = search_character(query, style)
    return JsonResponse(results, safe=False,
                        json_dumps_params={'ensure_ascii': False})
