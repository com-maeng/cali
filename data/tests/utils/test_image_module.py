"""이미지 처리 모듈 'data.utils.image_module'을 테스트 하는 모듈입니다."""


import PIL
from PIL import Image

from data.utils.image_module import preprocess_image_to_ocr
from data.utils.image_module import recognize_optical_character


def get_test_image(characters: bool = True) -> Image:
    """테스트 이미지를 불러오는 메서드입니다.

    Args:
        charactres: 식별할 문자가 존재하는 이미지와 빈 이미지 중 어떤 것을 사용할지 결정하는 값입니다.

    Returns:
        불러온 이미지를 Image 타입으로 반환합니다.
    """

    if characters:
        image_file_path = 'data/tests/utils/images/test_image.webp'
    else:
        image_file_path = 'data/tests/utils/images/test_image_without_characters.webp'

    return Image.open(image_file_path)


def test_preprocess_image_to_ocr():
    """이미지 OCR 전처리용 메서드를 테스트합니다."""

    test_image = get_test_image()
    preprocessed_image = preprocess_image_to_ocr(test_image)

    assert isinstance(preprocessed_image,
                      PIL.Image.Image), '전처리된 이미지의 타입이 잘못되었습니다.'
    assert preprocessed_image.width > 0, '전처리된 이미지의 width 값이 잘못되었습니다.'
    assert preprocessed_image.height > 0, '전처리된 이미지의 height 값이 잘못되었습니다.'


def test_preprocess_image_to_ocr_without_characters():
    """이미지 OCR 전처리용 메서드를 식별할 문자가 없는 빈 이미지로 테스트합니다."""

    test_image = get_test_image(characters=False)
    preprocessed_image = preprocess_image_to_ocr(test_image)

    assert isinstance(preprocessed_image,
                      PIL.Image.Image), '전처리된 이미지의 타입이 잘못되었습니다.'
    assert preprocessed_image.width > 0, '전처리된 이미지의 width 값이 잘못되었습니다.'
    assert preprocessed_image.height > 0, '전처리된 이미지의 height 값이 잘못되었습니다.'


def test_recognize_optical_character_with_chi_models():
    """이미지 OCR 메서드를 Tesseract 한자 언어 모델을 활용해 테스트합니다."""

    test_image = get_test_image()
    lang = 'chi_sim+chi_sim_vert+chi_tra+chi_tra_vert'

    boxes = recognize_optical_character(test_image, lang=lang)

    assert isinstance(boxes, str), '인식된 문자들의 정보를 담는 값의 타입이 잘못되었습니다.'

    for box in boxes.splitlines():
        c, l, b, r, t, _ = box.split()

        assert isinstance(c, str), '인식된 문자의 타입이 잘못되었습니다.'
        assert l.isdigit(), 'Box의 left 좌표값이 잘못되었습니다.'
        assert b.isdigit(), 'Box의 bottom 좌표값이 잘못되었습니다.'
        assert r.isdigit(), 'Box의 right 좌표값이 잘못되었습니다.'
        assert t.isdigit(), 'Box의 top 좌표값이 잘못되었습니다.'


def test_recognize_optical_character_with_chi_models_without_characters():
    """이미지 OCR 메서드를 Tesseract 한자 언어 모델과 빈 이미지를 활용해 테스트합니다."""

    test_image = get_test_image(characters=False)
    lang = 'chi_sim+chi_sim_vert+chi_tra+chi_tra_vert'

    boxes = recognize_optical_character(test_image, lang=lang)

    assert isinstance(boxes, str), '인식된 문자들의 정보를 담는 값의 타입이 잘못되었습니다.'
    assert boxes == '', '잘못된 문자 인식이 이루어졌습니다.'
