import unittest
from unittest.mock import patch, Mock

from search_engine.meili_customize.search import Search


class TestSearchMock(unittest.TestCase):

    @patch('search_engine.meili_customize.config.Config')
    def setUp(self, MockConfig):
        """메일리서치 API 통신을 임의의 가짜(Mock)로 대체합니다."""
        self.mock_config = MockConfig()
        self.mock_index = Mock()
        self.mock_config.index = self.mock_index
        self.search_instance = Search(self.mock_config)

    def test_search(self):
        """검색 테스트"""
        mock_results = {
            'estimatedTotalHits': 1,
            'hits': [{'id': 12, 'character': '火 불 화', 'style': 'yeseo'}],
            'limit': 20, 'offset': 0, 'processingTimeMs': 0, 'query': '불'}

        self.mock_index.search.return_value = mock_results
        result = self.search_instance.search('불', 'yeseo')

        # 검색 결과가 잘 나오는지 확인
        self.assertEqual(result, mock_results)

        # index.search() 메서드의 인자값으로 아래와 같이 요청이 되었는지 확인
        self.mock_index.search.assert_called_once_with(
            '불', {'filter': ['style = "yeseo"']})

    def test_suggest(self):
        """추천 검색어 리스트 테스트"""
        mock_suggestions = {
            'hits': [
                {
                    'id': 7,
                    'character': '月 달 월',
                    'style': 'yeseo'
                },
                {
                    'id': 2,
                    'character': '日 날 일',
                    'style': 'yeseo'
                }
            ],
            'query': '달',
            'processingTimeMs': 367,
            'limit': 5,
            'offset': 0,
            'estimatedTotalHits': 2
        }
        self.mock_index.search.return_value = mock_suggestions

        suggestions = self.search_instance.suggest('달', 'yeseo')
        expected_suggestions = ['月 달 월', '日 날 일']

        # 문자('달') 기반으로 추천 리스트 확인
        self.assertEqual(suggestions, expected_suggestions)

        # index.search() 메서드의 인자값으로 아래와 같이 요청이 되었는지 확인
        self.mock_index.search.assert_called_once_with(
            '달', {'filter': ["style = 'yeseo'"], 'limit': 5})
