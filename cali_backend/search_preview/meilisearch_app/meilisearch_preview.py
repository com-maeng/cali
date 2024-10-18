from typing import List

import meilisearch

client = meilisearch.Client('http://search-server-m:7700')

# index = client.index("movies")

# # 데이터 추가
# documents = [
#     { 'id': 1, 'title': 'Carol', 'genres': ['Romance', 'Drama'] },
#     { 'id': 2, 'title': 'Wonder Woman', 'genres': ['Action', 'Adventure'] },
#     { 'id': 3, 'title': 'Life of Pi', 'genres': ['Adventure', 'Drama'] },
#     { 'id': 4, 'title': 'Mad Max: Fury Road', 'genres': ['Adventure', 'Science Fiction'] },
#     { 'id': 5, 'title': 'Moana', 'genres': ['Fantasy', 'Action']},
#     { 'id': 6, 'title': 'Philadelphia', 'genres': ['Drama'] },
# ]
index = client.index("hanja_index")

# 데이터 추가
documents = [
    { 'id': 1, 'character': '日 날 일', 'meaning': '날 일' },
    { 'id': 2, 'character': '月 달 월', 'meaning': '달 월' },
    { 'id': 3, 'character': '火 불 화', 'meaning': '불 화' },
]
index.add_documents(documents)

def search_character(query: str) -> List[str]:
    # 예시: 쿼리 문자열을 사용하여 검색
    try:
        result = index.search(query)
        return result
    except Exception as e:
        print("Search Error:", e)
        return []

if __name__ == '__main__':
    # 검색 요청
    search_results = index.search('불')
    print(search_results)
