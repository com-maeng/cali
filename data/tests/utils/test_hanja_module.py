from data.utils.hanja_module import get_huneums


def test_get_huneum_with_valid_hanja_character():
    huneums = get_huneums('猓')

    assert isinstance(huneums, list)
    assert len(huneums) > 0

    for huneum in huneums:
        assert isinstance(huneum, dict)
        assert len(huneum.keys()) == 2  # 'def', 'kor'

        assert 'def' in huneum.keys()
        assert 'kor' in huneum.keys()

        assert isinstance(huneum['def'], str)
        assert isinstance(huneum['kor'], str)
        assert huneum['def'] != ''
        assert huneum['kor'] != ''


def test_get_huneum_with_invalid_hanja_character():
    huneums_empty_string = get_huneums('')
    huneums_alphabet = get_huneums('A')

    assert isinstance(huneums_empty_string, list)
    assert isinstance(huneums_alphabet, list)

    assert len(huneums_empty_string) == 0
    assert len(huneums_alphabet) == 0
