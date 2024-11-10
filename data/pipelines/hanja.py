"""한자 데이터 파이프라인의 구현체인 HanjaDataPipeline이 정의된 모듈입니다."""


import logging
from typing import NoReturn

from PIL import Image

from dtos import Artwork
from dtos import Hanja
from utils.image_module import recognize_optical_character, crop_image_to_box
from utils.hanja_module import get_huneum


class HanjaDataPipeline:
    """작품 이미지에서 한자 데이터를 추출하여 적재하는 파이프라인입니다."""

    def __init__(self, artworks: list[Artwork]) -> None:
        self.artworks = artworks
        self.hanjas = []  # list[Hanja]
        self.tesseract_lang = 'chi_tra+chi_tra_vert+chi_sim+chi_sim_vert'

    def activate_pipeline(self) -> NoReturn:
        """한자 데이터 파이프라인을 가동하기 위한 트리거 API입니다.

        API가 호출되면 아래 작업들이 순차적으로 실행됩니다.
        1. 인스턴스 변수 `artworks`를 순회합니다.
        2. 원소의 작품 이미지 리스트 `image_stream`을 순회합니다.
        3. Hanja 인스턴스를 생성하여 하기 4, 5번의 정보를 담습니다.
        4. 이미지를 전처리 한 후 OCR 모듈을 호출하여 한자 문자를 인식합니다.
        5. 인식된 한자를 '훈음'으로 라벨링합니다.
        6. Hanja 인스턴스를 파이프라인의 인스턴스 변수인 `hanjas`에 추가합니다.
        7. `artworks`의 순회가 끝나면 `hanjas` 리스트를 순회합니다.
        8. 원소의 이미지와 메티데이터를 GCS 버킷에 적재합니다.
        9. 원소의 '훈음' 데이터를 Meilisearch에 적재합니다.

        Args:
            API 호출 시 지정할 수 있는 매개변수가 없습니다.

        Returns:
            API 호출 후 반환되는 값이 없습니다.
        """

        logging.info('Activate HanjaDataPipeline...')

        for artwork in self.artworks:
            for image_stream in artwork.image_streams:
                image = Image.open(image_stream)
                boxes = recognize_optical_character(image, self.tesseract_lang)

                for box in boxes.splitlines():
                    hanja_character, left, bottom, right, top, _ = box.split()
                    coords = list(map(int, [left, bottom, right, top]))

                    box_image = crop_image_to_box(image, coords)
                    huneum = get_huneum(hanja_character)

                    self.hanjas.append(Hanja(
                        hanja_character=hanja_character,
                        huneum=huneum,
                        image=box_image,
                        from_artwork=artwork.artwork_name,
                        from_artist=artwork.artist_name
                    ))

        # TODO: 로직 구현 (Upload hanjas to GCS, Meilisearch)
