from .config import Config


class Search:
    """Meilisearch 기반 검색엔진

    실시간 사용자 입력 기반 추천 검색 리스트 5개와
    사용자 입력 문자열 기반 검색 정보를 제공합니다.

    search:
        Description:
            사용자가 입력한 문자열 'chi'와 's_val' 기준으로 필터링된 정보를 반환합니다.

    suggest:
        Description:
            사용자가 실시간으로 입력한 문자열 'chi'기반으로 실시간 추천 검색 리스트 5개를 반환합니다.
    """

    def __init__(self, config: Config):
        self.config = config
        self.five_style = ['jeonseo', 'yeseo', 'haeseo', 'haengseo', 'choseo']

    def search(self, chi: str, s_val: str = 'jeonseo') -> list[dict]:
        """사용자가 입력한 문자열 'chi'와 's_val' 기준으로 필터링된 정보를 반환합니다.

        문자열 'chi'와 원하는 오서 중 한개인 's_val'을 매개변수로 입력받을 경우
        필터링된 검색 정보를 반환합니다.

        Args:
            chi: str ['한자', '훈', '음', '훈 음' 모두 검색 가능 (예: '月 달 월')]
            s_val: str [오서('jeonseo', 'yeseo', 'haeseo', 'haengseo', 'choseo') 중 한개를 입력하며, 기본값은 'jeonseo'입니다.]

        Raises:
            ValueError: 인자가 조건에 맞지 않는 경우

        Returns:
            hits: 검색 조건에 맞는 한자 문서를 반환
        """

        if s_val not in self.five_style:
            raise Exception(
                '오서("jeonseo", "yeseo", "haeseo", "haengseo", "choseo") 중 한개를 입력해주세요.')
        if not chi and isinstance(chi, str):
            raise Exception('알맞은 검색어로 검색해주세요.')

        filter_str = f'style = "{s_val}"'
        results = self.config.index.search(
            chi,
            {
                'filter': [filter_str]
            }
        )
        return results

    def suggest(self, chi: str, s_val: str = 'jeonseo') -> list[dict]:
        """사용자가 실시간으로 입력한 문자열 'chi'기반으로 실시간 추천 검색 리스트 5개를 반환합니다.

        사용자가 문자열을 입력할 경우, 입력한 문자(or문자열)이 실시간으로 매개변수 'chi'로 요청하여,
        상위 5개의 hits값을 반환합니다.

        Args:
            chi: str ['한자', '훈', '음', '훈 음' 모두 검색 가능 (예: '月 달 월')]
            s_val: str [오서('jeonseo', 'yeseo', 'haeseo', 'haengseo', 'choseo') 중 한개를 입력하며, 기본값은 'jeonseo'입니다.]

        Raises:
            ValueError: 인자가 조건에 맞지 않는 경우

        Returns:
            hits: 검색 조건에 맞는 한자 리스트를 반환
        """

        if s_val not in self.five_style:
            raise Exception(
                '오서("jeonseo", "yeseo", "haeseo", "haengseo", "choseo") 중 한개를 입력해주세요.')
        if not chi and isinstance(chi, str):
            raise Exception('알맞은 검색어로 검색해주세요.')

        filter_str = f"style = '{s_val}'"
        results = self.config.index.search(
            chi,
            {
                'filter': [filter_str],
                'limit': 5
            }
        )
        suggestions = [hit['character'] for hit in results['hits']]
        return suggestions
