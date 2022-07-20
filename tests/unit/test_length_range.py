import pytest

from src import LengthRange



def test_length_range_contains():
    assert (1 in LengthRange(1)) is True
    assert (1 in LengthRange(1, max_length=1)) is True
    assert (1 in LengthRange(1, max_length=3)) is True
    assert (1 in LengthRange(2, max_length=5)) is False


def test_length_range_iter():
    for idx, i in enumerate(LengthRange(0, max_length=10)):
        assert idx == i


def test_length_range_one_in_range():
    assert LengthRange(1).one_in_range() == 1
    assert LengthRange(1, max_length=1).one_in_range() == 1
    assert LengthRange(1, 10).one_in_range() in list(range(1, 10))


def test_length_range_invalid_range():
    with pytest.raises(ValueError):
        LengthRange(10, max_length=5)