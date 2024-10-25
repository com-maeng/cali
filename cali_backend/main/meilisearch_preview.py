"""This class does used to type hint."""
from typing import List

import meilisearch


class Search:
    """
    Meilisearch 기반 검색엔진

    index와 documents를 정의하고,
    실시간 검색 추천과 검색어 기반 필터된 정보를 제공합니다.

    doc_settings
        Description:
            Meilisearch 초기 index값 세팅

    suggestions:
        Description:
            사용자 입력 기반 실시간 검색어 추천 5개를 반환한다.

    search_character:
        Description:
            검색된 정보를 반환한다.
    """
    client = meilisearch.Client('http://search-server-m:7700')
    index = client.index("hanja_index")

    def doc_settings(self, documents: List[dict]):
        """
        Meilisearch 초기 index값 세팅

        서비스로 제공할 검색어 리스트 "documents"를 index에 추가하고,
        검색어에 필요한 filter의 field값을 업데이트한다.

        Args:
            documents: List[dict] [검색어 리스트]

        Raises:
            ValueError: 인자가 조건에 맞지 않는 경우

        Returns:
            None
        """
        self.index.add_documents(documents)

        self.index.update_filterable_attributes([
            'style'
        ])

    def suggestions(self, hanja: str = "") -> List[str]:
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
        if hanja:
            results = self.index.search(hanja, {
                'limit': 5
            })
            suggestions = [hit['character'] for hit in results['hits']]
        else:
            suggestions = []
        return suggestions

    def search_character(
            self, hanja: str = "", s_value: str = "jeonseo") -> List[str]:
        """
        검색된 정보를 반환한다.

        검색어 "hanja"과 원하는 오서 중 한개인 "s_value"을 입력받을 경우
        문자 기준으로 검색 후 필터링된 정보를 반환한다.

        Args:
            hanja: str [한자, 훈, 음, 훈 음 모두 검색 가능]
            s_value: str [오서 중 한개 검색 ("jeonseo", "yeseo", "haeseo", "haengseo", "choseo")]

        Raises:
            ValueError: 인자가 조건에 맞지 않는 경우

        Returns:
            hits: 검색 조건에 맞는 한자를 반환
        """
        filter_str = f"style = '{s_value}'"
        result = self.index.search(
            hanja,
            {
                'filter': [filter_str]
            }
        )
        return result


# 데이터 추가
documents = [
    {'id': 1, 'character': '日 날 일1', 'meaning': '날 일 1', 'style': 'jeonseo'},
    {'id': 2, 'character': '日 날 일2', 'meaning': '날 일 2', 'style': 'yeseo'},
    {'id': 3, 'character': '日 날 일3', 'meaning': '날 일 3', 'style': 'haeseo'},
    {'id': 4, 'character': '日 날 일4', 'meaning': '날 일 4', 'style': 'haengseo'},
    {'id': 5, 'character': '日 날 일5', 'meaning': '날 일 5', 'style': 'choseo'},
    {'id': 6, 'character': '月 달 월1', 'meaning': '달 월 1', 'style': 'jeonseo'},
    {'id': 7, 'character': '月 달 월2', 'meaning': '달 월 2', 'style': 'yeseo'},
    {'id': 8, 'character': '月 달 월3', 'meaning': '달 월 3', 'style': 'haeseo'},
    {'id': 9, 'character': '月 달 월4', 'meaning': '달 월 4', 'style': 'haengseo'},
    {'id': 10, 'character': '月 달 월5', 'meaning': '달 월 5', 'style': 'choseo'},
    {'id': 11, 'character': '火 불 화1', 'meaning': '불 화 1', 'style': 'jeonseo'},
    {'id': 12, 'character': '火 불 화2', 'meaning': '불 화 2', 'style': 'yeseo'},
    {'id': 13, 'character': '火 불 화3', 'meaning': '불 화 3', 'style': 'haeseo'},
    {'id': 14, 'character': '火 불 화4', 'meaning': '불 화 4', 'style': 'haengseo'},
    {'id': 15, 'character': '火 불 화5', 'meaning': '불 화 5', 'style': 'choseo'},
]
