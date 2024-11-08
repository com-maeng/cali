import logging
import os
from typing import List
from dotenv import load_dotenv

import meilisearch
import meilisearch.errors


class Config:
    """
    Meilisearch 초기 설정

    client 및 indexed documents 설정, filter 정의

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
            "http://localhost:7700", os.getenv("MEILI_MASTER_KEY"))
        self.index = self.client.index("chi")
        self._initialize_index()

    def _initialize_index(self):
        """인덱스가 존재하지 않을 경우 생성"""
        try:
            self.client.get_index("chi")
        except meilisearch.errors.MeilisearchApiError:
            task_info = self.client.create_index("chi")
            self.index.wait_for_task(task_info.task_uid)

    def add_docs(self, documents: List[dict]) -> None:
        """
        검색엔진을 위한 색인된 문서값 정의

        서비스로 제공할 검색어 리스트 "documents"를 index에 추가합니다.

        Args:
            documents: List[dict] [검색어 리스트]

        Raises:
            ValueError: 인자가 조건에 맞지 않는 경우

        Returns:
            None
        """

        self.index.add_documents(documents)

    def add_filter(self) -> None:
        """
        구체적인 검색을 위한 필터링 정의

        검색어에 필요한 filter의 field값을 업데이트한다.

        Args:
            None

        Raises:
            ValueError: 문서가 정의되지 않을 경우

        Returns:
            None
        """

        task_info = self.index.update_filterable_attributes(['style'])
        self.index.wait_for_task(task_info.task_uid)


# 메일리서치 모듈에서 제거할 예정 메인 작업 리포 이슈 #17
def create_documents(hanjas: List[str] = []) -> List[dict]:
    """
        메일리서치 문서 생성

        문자열[한자, 훈, 음] 리스트를 매개변수로 넣으면 각각 오서에 맞게 문서를 생성합니다.

        Args:
            hanjas: List[str] [문자열[한자, 훈, 음] 리스트]

        Raises:
            ValueError: 문자열 리스트를 넣지 않았을 경우

        Returns:
            List[dict] ["id", "character", "meaning", "style"]를 담은 리스트(문서)를 반환
        """

    five_style = ["jeonseo", "yeseo", "haeseo", "haengseo", "choseo"]

    documents = []

    idx = 1
    for hanja in hanjas:
        for s in five_style:
            documents.append({"id": idx, "character": hanja,
                              'meaning': hanja.split(' ')[1], "style": s})
            idx += 1

    return documents
