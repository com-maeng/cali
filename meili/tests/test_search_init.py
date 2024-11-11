from meili.config import create_documents


def test_create_documents_format() -> None:
    """검색엔진에 정의할 문서를 생성하는 로직을 테스트 합니다."""

    hanjas = ["日 날 일", "月 달 월"]
    documents = create_documents(hanjas)

    assert len(documents) == 10

    # 각 문서의 필드 확인
    for doc in documents:
        assert "id" in doc
        assert "character" in doc
        assert "meaning" in doc
        assert "style" in doc

    # 첫 번째 문서의 데이터 확인
    first_doc = documents[0]
    assert first_doc["character"] == "日 날 일"
    assert first_doc["meaning"] == "날"
    assert first_doc["style"] == "jeonseo"
