import pytest
from utils.encode_string import encode_string


@pytest.mark.parametrize("emojize", [True, False])
def test_string_is_encoded_correctly__regular_word(emojize):
    assert encode_string(string="hello", emojize=emojize) == "hello"


@pytest.mark.parametrize(
    "params",
    [
        ("😎", True, "😎"),
        ("😎", False, ":smiling_face_with_sunglasses:"),
        (":smiling_face_with_sunglasses:", False, ":smiling_face_with_sunglasses:"),
        (":smiling_face_with_sunglasses:", True, "😎"),
    ],
)
def test_string_is_encoded_correctly__emoji(params):
    assert encode_string(string=params[0], emojize=params[1]) == params[2]
