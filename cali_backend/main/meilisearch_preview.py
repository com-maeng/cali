"""This class does used to type hint."""
from typing import List

import meilisearch

client = meilisearch.Client('http://search-server-m:7700')

index = client.index("hanja_index")

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
index.add_documents(documents)

index.update_filterable_attributes([
    'style'
])


def search_character(hanja: str = "", s_value: str = "jeonseo") -> List[str]:
    """
    검색된 데이터를 반환한다.

    검색어 "string"과 원하는 오서 중 한개인 "style"을 입력받을 경우
    문자 기준으로 검색 후 필터링된 데이터를 반환한다.

    Args:
        string: str [한자, 훈, 음, 훈 음 모두 검색 가능]
        style: str [오서 중 한개 검색 ("jeonseo", "yeseo", "haeseo", "haengseo", "choseo")]

    Raises:
        ValueError: 인자가 조건에 맞지 않는 경우

    Returns:
        hits: 검색 조건에 맞는 한자를 반환
    """
    print(hanja, s_value, type(hanja), type(s_value), flush=True)
    try:
        filter_str = f"style = '{s_value}'"

        result = index.search(
            hanja,
            {
                'filter': [filter_str]
            }
        )
        return result
    except Exception as e:
        print("Search Error:", e, flush=True)
        return []
