"""이미지 전처리, OCR, 크롭 등의 이미지 처리 기능이 정의된 모듈입니다."""


import pytesseract
from PIL import Image


def preprocess_image_to_ocr(image: Image) -> Image:
    """이미지 OCR의 성능 향상을 위해 이미지를 전처리합니다.

    TODO: 현재는 입력값을 그대로 반환하는 로직이며, 향후 실제 전처리 로직이 추가될 예정입니다.

    Args:
        image: 전처리할 이미지입니다.

    Returns:
        전처리된 이미지를 반환합니다.
    """

    return image


def recognize_optical_character(image: Image, lang: str) -> str:
    """원본 이미지를 전처리하고 Tesseract를 활용해 OCR 하여 인식된 문자를 반환합니다.

    Args:
        image: 전처리하고 문자를 인식할 이미지입니다.
        lang: Tesseract에서 사용할 언어 모델입니다.

    Returns:
        이미지에서 식별된 문자와 그 좌표값이 포함된 문자열입니다.
        문자열의 예시는 다음과 같습니다.

        '''
        e 334 126 349 144 0
        r 351 126 379 144 0
        t 388 126 397 149 0
        '''

        문자는 개행문자를 기준으로 구분되며, 각 문자의 정보는 아래와 같이 구성됩니다.
        '문자, left, bottom, right, top, page_num'
    """

    preprocessed_image = preprocess_image_to_ocr(image)
    boxes = pytesseract.image_to_boxes(preprocessed_image, lang=lang)

    return boxes


def convert_box_coords_from_tesseract_to_pil(
    image: Image,
    coords: list[int]
) -> list[int]:
    """Tesseract 형식의 box 좌표값을 PIL 형식으로 변환합니다.

    left, right 값은 두 형식 모두 동일하지만, bottom(upper), top(lower) 값은 서로 반대입니다.
    - Tesseract: left bottom right top
    - PIL: left upper right lower

    image의 높이값을 활용하여 값이 서로 호환되도록 변형합니다.

    Args:
        image: 이미지의 높이값을 참고하는 데 활용됩니다.
        coords: Box 좌표값이 저장된 리스트입니다.

    Retruns:
        PIL 형식의 box 좌표값으로, [left, upper, right, lower] 으로 구성됩니다.
    """

    left, bottom, right, top = coords
    upper, lower = image.size[1] - bottom, image.size[1] - top

    return [left, upper, right, lower]
