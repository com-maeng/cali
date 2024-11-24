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
            'estimatedTotalHits': 5,
            'hits': [
                {'id': 10, 'character': '火 불 화', 'style': 'jeonseo'},
                {'id': 11, 'character': '火 불 화', 'style': 'yeseo'},
                {'id': 12, 'character': '火 불 화', 'style': 'haeseo'},
                {'id': 13, 'character': '火 불 화', 'style': 'haengseo'},
                {'id': 14, 'character': '火 불 화', 'style': 'choseo'},
            ],
            'limit': 20, 'offset': 0, 'processingTimeMs': 0, 'query': '불'}

        self.mock_index.search.return_value = mock_results
        result = self.search_instance.search('불')

        # 검색 결과가 잘 나오는지 확인
        self.assertEqual(result, mock_results)

        # index.search() 메서드의 인자값으로 아래와 같이 요청이 되었는지 확인
        self.mock_index.search.assert_called_once_with(
            '불', {'limit': 60})
