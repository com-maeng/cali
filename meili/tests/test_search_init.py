from meili.config import Config, create_documents


def test_add_documents() -> None:
    """문서 초기값 테스트"""

    docs = [
        {
            "id": 1,
            "character": "日 날 일",
            "meaning": "날",
            "style": "jeonseo"
        },
        {
            "id": 2,
            "character": "日 날 일",
            "meaning": "날",
            "style": "yeseo"
        },
        {
            "id": 3,
            "character": "日 날 일",
            "meaning": "날",
            "style": "haeseo"
        },
        {
            "id": 4,
            "character": "日 날 일",
            "meaning": "날",
            "style": "haengseo"
        },
        {
            "id": 5,
            "character": "日 날 일",
            "meaning": "날",
            "style": "choseo"
        },
        {
            "id": 6,
            "character": "月 달 월",
            "meaning": "달",
            "style": "jeonseo"
        },
        {
            "id": 7,
            "character": "月 달 월",
            "meaning": "달",
            "style": "yeseo"
        },
        {
            "id": 8,
            "character": "月 달 월",
            "meaning": "달",
            "style": "haeseo"
        },
        {
            "id": 9,
            "character": "月 달 월",
            "meaning": "달",
            "style": "haengseo"
        },
        {
            "id": 10,
            "character": "月 달 월",
            "meaning": "달",
            "style": "choseo"
        },
        {
            "id": 11,
            "character": "火 불 화",
            "meaning": "불",
            "style": "jeonseo"
        },
        {
            "id": 12,
            "character": "火 불 화",
            "meaning": "불",
            "style": "yeseo"
        },
        {
            "id": 13,
            "character": "火 불 화",
            "meaning": "불",
            "style": "haeseo"
        },
        {
            "id": 14,
            "character": "火 불 화",
            "meaning": "불",
            "style": "haengseo"
        },
        {
            "id": 15,
            "character": "火 불 화",
            "meaning": "불",
            "style": "choseo"
        }
    ]

    conf = Config()

    hanjas = ["日 날 일", "月 달 월", "火 불 화"]

    docs = create_documents(hanjas)
    conf.add_docs(docs)
    result = conf.index.get_documents()
    result_dicts = [doc.__dict__['_Document__doc'] for doc in result.results]
    assert result_dicts == docs
