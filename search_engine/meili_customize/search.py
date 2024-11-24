from .config import Config


class Search:
    """Meilisearch 기반 검색엔진

    실시간 사용자 입력 기반 추천 검색 리스트 5개와
    사용자 입력 문자열 기반 검색 정보를 제공합니다.

    search:
        Description:
            사용자가 입력한 문자열 'chi'기준으로 오서 정보를 반환합니다.

    suggest:
        Description:
            사용자가 실시간으로 입력한 문자열 'chi'기반으로 실시간 추천 검색 리스트 5개를 반환합니다.
    """

    def __init__(self, config: Config):
        self.config = config

    def search(self, chi: str) -> list[dict]:
        """사용자가 입력한 문자열 'chi'기준으로 오서 정보를 반환합니다.

        문자열 'chi'기준으로 오서를 포함한 모든 검색 결과를 반환합니다.
        (오서별로 12 건으로 총 60개의 검색 결과로 제한)

        Args:
            chi: str ['한자', '훈', '음', '훈 음' 모두 검색 가능 (예: '月 달 월')]

        Returns:
            hits: 검색 조건에 맞는 한자 문서를 반환
        """

        results = self.config.index.search(
            chi,
            {
                'limit': 60
            }
        )
        return results
