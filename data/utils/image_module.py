import io

import pytesseract
from PIL import Image


def preprocess_image_to_ocr(image: io.BytesIO) -> io.BytesIO:
    # 이미지 OCR을 위한 전처리 작업이 추가될 예정입니다.

    return image


def recognize_optical_character(image_stream: io.BytesIO, lang: str) -> str:
    preprocessed_image = preprocess_image_to_ocr(
        image_stream['image_stream'])
    boxes = pytesseract.image_to_boxes(preprocessed_image, lang=lang)

    return boxes


def cut_image_using_coords(image_stream: io.BytesIO, coords: list[str]) -> io.BytesIO:
    image = Image.open(image_stream)

    left, bottom, right, top = map(int, coords)
    upper, lower = image.size[1] - bottom, image.size[1] - top

    return image.crop(left, upper, right, lower)
