"""데이터 파이프라인에서 활용되는 DTO가 정의된 모듈입니다."""


import io
from dataclasses import dataclass

from PIL import Image


@dataclass
class Artwork:
    """작품 데이터를 담는 DTO입니다."""

    row_num: int
    artist_name: str
    artwork_name: str
    drive_url: str
    image_streams: list[dict[str, str | io.BytesIO]]


@dataclass
class Hanja:
    """작품에서 추출된 한자 데이터를 담는 DTO입니다."""

    hanja_character: str
    huneums: list[dict[str, str]]  # [{'def': '꾸짖을', 'kor': '갈'}]
    image: Image
    from_artwork: str
    from_artist: str
