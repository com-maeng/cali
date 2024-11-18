"""한자 문자를 처리하는 다양한 API들이 정의된 모듈입니다."""


import json


HANJA_DIC_JSON_FILE = 'data/utils/hanjaDic.json'


def get_huneums(hanja_character: str) -> list[dict[str, str]]:
    """입력된 한자 문자의 훈음을 식별하여 반환합니다.

    Args:
        hanja_character: 훈음을 식별할 한자 문자입니다.

    Returns:
        입력값으로 들어온 한자 문자의 훈음을 str 타입으로 반환합니다.
        식별된(대응되는) 훈음이 없을 경우 빈 리스트를 반환합니다.
    """

    with open(HANJA_DIC_JSON_FILE, 'r', encoding='utf8') as f:
        hanja_dic = json.load(f)

    if hanja_character in hanja_dic.keys():
        return hanja_dic[hanja_character]

    return []
