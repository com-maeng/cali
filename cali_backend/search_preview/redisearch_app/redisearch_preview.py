from typing import List

from redis import Redis
from redisearch import Client, TextField

# Redis 및 RediSearch 클라이언트 초기화
redis_client: Redis = Redis(host='search-server', port=6379)
search_client: Client = Client("hanja_index", conn=redis_client)

# 인덱스 생성
try:
    search_client.create_index([
        TextField("character", weight=5.0),
        TextField("meaning")
    ])
except:
    print("Index already exists")

# 한자 예시 데이터 추가 (1번만)
# 데이터 추가 시 한글과 한자를 함께 저장
search_client.add_document("doc1", character="日 날 일", meaning="날 일")
search_client.add_document("doc2", character="月 달 월", meaning="달 월")
search_client.add_document("doc3", character="火 불 화", meaning="불 화")


def search_character(query: str) -> List[str]:
    # 예시: 쿼리 문자열을 사용하여 검색
    try:
        result = search_client.search(f"@character:*{query}*")
        return [{"character": doc.character, "meaning": doc.meaning} for doc in result.docs]
    except Exception as e:
        print("Search Error:", e)
        return []


if '__name__' == '__main__':
    # 예제 사용
    results = search_character("날")
    for result in results:
        print(f"Character: {result['character']}, Meaning: {result['meaning']}")
