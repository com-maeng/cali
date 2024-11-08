import unittest
from unittest.mock import patch, Mock

from meili.search import Search
from meili.config import create_documents


class TestSearchMock(unittest.TestCase):

    @patch('meili.config.Config')
    def setUp(self, MockConfig):
        """메일리서치 API 통신을 임의의 가짜로 대체합니다."""
        self.mock_config = MockConfig()
        self.mock_index = Mock()
        self.mock_config.index = self.mock_index
        self.search_instance = Search(self.mock_config)

    def test_search(self):
        """검색 테스트"""
        mock_results = {'estimatedTotalHits': 1,
                        'hits': [{'character': '火 불 화', 'id': 12, 'meaning': '불', 'style': 'yeseo'}],
                        'limit': 20,
                        'offset': 0,
                        'processingTimeMs': 0,
                        'query': '불'}

        self.mock_index.search.return_value = mock_results
        result = self.search_instance.search("불", "yeseo")

        self.assertEqual(result, mock_results)
        self.mock_index.search.assert_called_once_with(
            "불", {'filter': ["style = 'yeseo'"]})

    def test_suggest(self):
        """추천 검색어 테스트"""
        mock_suggestions = {
            "hits": [
                {
                    "id": 7,
                    "character": "月 달 월",
                    "meaning": "달",
                    "style": "yeseo"
                },
                {
                    "id": 2,
                    "character": "日 날 일",
                    "meaning": "날",
                    "style": "yeseo"
                }
            ],
            "query": "달",
            "processingTimeMs": 367,
            "limit": 5,
            "offset": 0,
            "estimatedTotalHits": 2
        }
        self.mock_index.search.return_value = mock_suggestions

        suggestions = self.search_instance.suggest("달", "yeseo")
        expected_suggestions = ['月 달 월', '日 날 일']

        self.assertEqual(suggestions, expected_suggestions)
        self.mock_index.search.assert_called_once_with(
            "달", {'filter': ["style = 'yeseo'"], 'limit': 5})


class TestCreateDocuments(unittest.TestCase):

    def test_create_documents_format(self):
        hanjas = ["日 날 일", "月 달 월"]
        documents = create_documents(hanjas)

        self.assertEqual(len(documents), 10)

        # 각 문서의 필드 확인
        for doc in documents:
            self.assertIn("id", doc)
            self.assertIn("character", doc)
            self.assertIn("meaning", doc)
            self.assertIn("style", doc)

        # 첫 번째 문서의 데이터 확인
        first_doc = documents[0]
        self.assertEqual(first_doc["character"], "日 날 일")
        self.assertEqual(first_doc["meaning"], "날")
        self.assertEqual(first_doc["style"], "jeonseo")


if __name__ == "__main__":
    unittest.main()
