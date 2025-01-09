import os
import json
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
            'http://localhost:7700',
            os.getenv('MEILI_MASTER_KEY')
        )
        self.index = self.client.index('hanja')
        self._initialize_index()

    def _initialize_index(self):
        """인덱스가 존재하지 않을 경우 생성"""

        self.client.create_index(
            'hanja',
            {'primaryKey': 'hanja_id'}
        )

    def add_docs(self, documents: list[dict]) -> None:
        """검색엔진의 색인된 문서를 추가 및 정의

        검색 리스트 'documents'를 Meilisearch index에 추가합니다.

        Args:
            documents: list[dict] [검색어 리스트로 dict형의 키값은 'id', 'character', 'style' 입니다.]

        Raises:
            ValueError: 인자가 조건에 맞지 않는 경우

        Returns:
            None
        """

        try:
            task_info = self.index.add_documents(documents)
            self.index.wait_for_task(task_info.task_uid)
        except Exception as e:
            print(f'검색엔진 문서 추가에 문제가 생겼습니다.\n\n{e}', flush=True)


def create_documents(hanjas: list[str]) -> list[dict]:
    """메일리서치 문서 생성

    문자열('한자 훈 음') 리스트를 매개변수로 넣으면 오서를 기준으로 각각 문서를 생성합니다.

    Args:
        hanjas: List[str] [문자열('한자 훈 음') 리스트] (예: '月 달 월')

    Raises:
        ValueError: 문자열 리스트를 넣지 않았을 경우

    Returns:
        List[dict] ('id', 'character', 'style')키값을 담은 리스트를 반환
    """

    documents = []

    try:
        hanja_id = 1
        for hanja in hanjas:
            documents.append({
                'hanja_id': hanja_id,
                'hanja_hun_eum': hanja
            })
            hanja_id += 1
    except Exception as e:
        print(f'문서 생성에 문제가 생겼습니다.\n\n{e}', flush=True)
        documents = []

    return documents


def hanja_preprocessor() -> list[str]:
    """메일리서치 문서 생성에 활용할 데이터 전처리

    hanjaDict.json 파일을 읽어 들여, 메일리서치 문서 생성 함수인 create_documents 인자값에 맞는
    문자열('한자 훈 음') 리스트로 전처리 후 반환합니다.

    Args:
        None: 인자값이 필요하지 않습니다.

    Returns:
        List[str] [문자열('한자 훈 음') 리스트를 반환합니다.] (예: '月 달 월')
    """

    try:
        with open('/cali/search_engine/hanjaDic.json', 'r', encoding='utf-8') as file:
            data = json.load(file)

        new_data = []
        for hanja_character, huneums in data.items():
            for huneum in huneums:
                hanja_hun_eum = ' '.join([
                    hanja_character,
                    huneum['def'],
                    huneum['kor']]
                )
                new_data.append(hanja_hun_eum)
    except FileNotFoundError as e:
        print(f'hanjaDic.json 파일을 찾지 못했습니다.\n\n{e}', flush=True)
        new_data = []
    except Exception as e:
        print(f'한자 데이터 전처리에 문제가 생겼습니다.\n\n{e}', flush=True)
        new_data = []

    return new_data
