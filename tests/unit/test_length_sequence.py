import pytest

from src import LengthSequence

def test_length_sequence_contains():
    assert (1 in LengthSequence(1)) is True
    assert (1 in LengthSequence(1,2)) is True
    assert (2 in LengthSequence(1,5)) is False

def test_length_sequence_parse_length():
    x = LengthSequence(1,2,3)
    x = LengthSequence((1,2,3))
    x = LengthSequence((1,2,3), 2, 3)
    with pytest.raises(ValueError):
        LengthSequence()
    with pytest.raises(TypeError):
        LengthSequence(None)

def test_length_sequence_iter():
    for idx, i in enumerate(LengthSequence(0, 5, 10, 15)):
        assert idx*5 == i

def test_length_sequence_one_in_range():
    assert LengthSequence(1).one_in_range() == 1
    assert LengthSequence(1,2,3).one_in_range() in (1,2,3)
    assert LengthSequence(1, 5, 9, 14, 22).one_in_range() in (1, 5, 9, 14, 22)
