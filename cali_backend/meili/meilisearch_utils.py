"""This class does used to type hint."""
import logging
import os
from typing import List
from dotenv import load_dotenv

import meilisearch

LOG_FILE_PATH = os.path.join(os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__))),
    'logs/cali_backend_search.log')

logging.basicConfig(
    filename=LOG_FILE_PATH,
    filemode='a',
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


class SearchInit:
    """
    Meilisearch 초기 설정

    client 및 indexed documents 세팅, filter 정의

    _initialize_index
        Description:
            DI 관련 초기 index 세팅을 하지 못했을 경우를 대비, index 생성

    _doc_settings:
        Description:
            documents, filter 세팅
    """

    def __init__(self):
        load_dotenv()
        self.client = meilisearch.Client(
            'http://' + f'{os.getenv("MEILI_HOST")}:' +
            f'{os.getenv("MEILI_PORT")}', os.getenv("MEILI_MASTER_KEY"))
        self.index = self.client.index("hanja_index")
        self._initialize_index()
        self._doc_settings(make_documents())  # 함수 의존성 낮추는법 ...

    def _initialize_index(self):
        """인덱스가 존재하지 않을 경우 생성"""
        try:
            self.client.get_index("hanja_index")
        except meilisearch.errors.MeilisearchApiError:
            # 인덱스를 새로 생성
            self.client.create_index("hanja_index")

    def _doc_settings(self, documents: List[dict]) -> None:
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
        documents = documents or make_documents()
        logging.info('new documents add...')
        task_info = self.index.add_documents(documents)
        self.index.wait_for_task(task_info.task_uid)
        task_info = self.index.update_filterable_attributes(['style'])
        self.index.wait_for_task(task_info.task_uid)


class SearchAPI:
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

    def __init__(self, c_index):
        self.c_index = c_index

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
            results = self.c_index.search(hanja, {
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
        result = self.c_index.search(
            hanja,
            {
                'filter': [filter_str]
            }
        )
        return result


def make_documents() -> List[dict]:
    # 특정 데이터 기반 documents 제작 후 반환
    # 특정 데이터가 정의되지 않을 동안 리터럴로 값 대입
    # 데이터 추가
    hanjas = ["日 날 일", "月 달 월", "火 불 화"]  # 파라미터로 수정 예정

    logging.info('Create new document data...')
    five_style = ["jeonseo", "yeseo", "haeseo", "haengseo", "choseo"]
    documents = []

    idx = 1
    for hanja in hanjas:
        for s in five_style:
            documents.append({'id': idx, 'character': hanja,
                              'meaning': hanja.split(' ')[1], 'style': s})
            idx += 1

    return documents
