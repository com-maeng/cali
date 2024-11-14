from search_engine.meili_customize.config import create_documents, hanja_preprocessor


def test_create_documents_format() -> None:
    """검색엔진에 정의할 문서를 생성하는 로직을 테스트 합니다."""

    hanjas = ['日 날 일', '月 달 월']
    documents = create_documents(hanjas)

    assert len(documents) == 10

    # 각 문서의 필드 확인
    for doc in documents:
        assert 'id' in doc
        assert 'character' in doc
        assert 'meaning' in doc
        assert 'style' in doc

    # 첫 번째 문서의 데이터 확인
    first_doc = documents[0]
    assert first_doc['character'] == '日 날 일'
    assert first_doc['meaning'] == '날'
    assert first_doc['style'] == 'jeonseo'


def test_hanja_data_preprocessor() -> None:
    """hanjaDic Json 파일 전처리하는 로직을 테스트 합니다."""

    hanja_json = ['仮 거짓 가', '伽 절 가']
    data = hanja_preprocessor()
    data = data[:2]

    assert len(data) == 2
    assert hanja_json == data

    # 리스트 요소값인 문자열의 '한자, 훈, 음'이 맞는지 확인
    for data_value, json_value in zip(data, hanja_json):
        data_hanja, data_hun, data_eum = data_value.split(' ')
        json_hanja, json_hun, json_eum = json_value.split(' ')

        assert data_hanja == json_hanja
        assert data_hun == json_hun
        assert data_eum == json_eum
