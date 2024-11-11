import os
from dotenv import load_dotenv

import meilisearch
import meilisearch.errors


class Config:
    """Meilisearch 초기 설정 클래스

    Meilisearch client 및 index를 설정합니다.
    추가로 검색엔진에 사용할 정의된 문서를 추가하고,
    검색 시 필터링 할 필드값을 설정합니다.

    _initialize_index
        Description:
            객체 생성 시 index 설정을 하지 못했을 경우, index 설정

    add_docs:
        Description:
            documents 설정

    add_filter:
        Description:
            filter 설정
    """

    def __init__(self):
        load_dotenv()
        self.client = meilisearch.Client(
            'http://localhost:7700', os.getenv('MEILI_MASTER_KEY'))
        self.index = self.client.index('chi')
        self._initialize_index()

    def _initialize_index(self):
        """인덱스가 존재하지 않을 경우 생성"""

        try:
            self.client.get_index('chi')
        except meilisearch.errors.MeilisearchApiError:
            task_info = self.client.create_index('chi')
            self.index.wait_for_task(task_info.task_uid)

    def add_docs(self, documents: list[dict]) -> None:
        """검색엔진의 색인된 문서를 추가 및 정의

        검색 리스트 'documents'를 Meilisearch index에 추가합니다.

        Args:
            documents: list[dict] [검색어 리스트로 dict형의 키값은 'id', 'character', 'meaning', 'style' 입니다.]

        Raises:
            ValueError: 인자가 조건에 맞지 않는 경우

        Returns:
            None
        """

        task_info = self.index.add_documents(documents)
        self.index.wait_for_task(task_info.task_uid)

    def add_filter(self) -> None:
        """구체적인 검색을 위한 필터링 정의

        검색어에 필요한 filter의 field값을 정의합니다.
        field값은 'documents' 리스트의 dict형 키값을 기반으로 정의합니다.

        Args:
            None

        Raises:
            ValueError: 문서가 정의되지 않을 경우

        Returns:
            None
        """

        task_info = self.index.update_filterable_attributes(['style'])
        self.index.wait_for_task(task_info.task_uid)


def create_documents(hanjas: list[str]) -> list[dict]:
    """메일리서치 문서 생성

        문자열('한자 훈 음') 리스트를 매개변수로 넣으면 오서를 기준으로 각각 문서를 생성합니다.

        Args:
            hanjas: List[str] [문자열('한자 훈 음') 리스트] (예: '月 달 월')

        Raises:
            ValueError: 문자열 리스트를 넣지 않았을 경우

        Returns:
            List[dict] ('id', 'character', 'meaning', 'style')키값을 담은 리스트를 반환
        """

    five_style = ['jeonseo', 'yeseo', 'haeseo', 'haengseo', 'choseo']
    documents = []
    doc_id = 0

    for hanja in hanjas:
        for s in five_style:
            documents.append({'id': doc_id, 'character': hanja,
                              'meaning': hanja.split(' ')[1], 'style': s})
            doc_id += 1

    if not documents:
        raise Exception(
            '형식에 맞는 문자열 리스트를 넣어주세요.\nList[str] [문자열("한자 훈 음") 리스트] (예: "月 달 월")')
    return documents
