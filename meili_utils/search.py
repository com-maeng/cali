from typing import List

from meili_utils.config import Config


class Search:
    """
    Meilisearch 기반 검색엔진

    실시간 검색 추천과 검색어 기반 필터된 정보를 제공합니다.

    search:
        Description:
            검색 후 s_val 기준으로 필터링된 정보를 반환한다.

    suggest:
        Description:
            사용자 입력 기반 실시간 검색어 추천 최대 5개를 반환한다.
    """

    def __init__(self, config: Config):
        self.config = config

    def search(self, chi: str, s_val: str) -> List[dict]:
        """
        검색된 정보를 반환한다.

        검색어 "chi"과 원하는 오서 중 한개인 "s_val"을 입력받을 경우
        문자 기준으로 검색 후 필터링된 정보를 반환한다.

        Args:
            chi: str [한자, 훈, 음, 훈 음 모두 검색 가능]
            s_val: str [오서 중 한개 검색 ("jeonseo", "yeseo", "haeseo", "haengseo", "choseo")]

        Raises:
            ValueError: 인자가 조건에 맞지 않는 경우

        Returns:
            hits: 검색 조건에 맞는 한자를 반환
        """

        filter_str = f"style = '{s_val}'"
        results = self.config.index.search(
            chi,
            {
                'filter': [filter_str]
            }
        )
        return results

    def suggest(self, chi: str, s_val: str = "") -> List[dict]:
        """
        사용자 입력 기반 실시간 검색어 추천 5개를 반환한다.

        사용자 실시간 입력 "hanja"를 기반으로
        상위 5개의 hits값을 반환한다.

        Args:
            hanja: str [한자, 훈, 음, 훈 음 모두 검색 가능]

        Raises:
            ValueError: 인자가 조건에 맞지 않는 경우

        Returns:
            hits: 검색 조건에 맞는 한자를 반환
        """

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
