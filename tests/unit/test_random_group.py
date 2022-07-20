import pytest

from src import RandomGroup, LengthRange


def test_random_group_invalid_alphabet_type():
    with pytest.raises(TypeError):
        RandomGroup(alphabet=["abcd", "efgh"])
    with pytest.raises(TypeError):
        RandomGroup(alphabet=123)

def test_random_group_invalid_alphabet_value():
    with pytest.raises(ValueError):
        RandomGroup(alphabet="aab")


def test_random_group_single_alphabet_generate():
    assert RandomGroup(alphabet="a", length=1).generate() == "a"
    assert RandomGroup(alphabet="a", length=3).generate() == "aaa"


def test_random_group_default_length():
    assert len(RandomGroup(alphabet="ab").generate()) == 2
    assert len(RandomGroup(alphabet="abcd").generate()) == 4

def test_random_group_generate_single_length():
    group = RandomGroup(alphabet="abcd", length=1).generate()
    assert len(group) == 1
    assert group in "abcd"

def test_random_group_generate_multi_length():
    group = RandomGroup(alphabet="abcd", length=4).generate()
    assert len(group) == 4
    for char in group:
        assert char in "abcd"

def test_random_group_generate_length_range():
    group = RandomGroup(alphabet="abcd", length=(1,2)).generate()
    assert len(group) in (1,2)
    group = RandomGroup(alphabet="abcd", length=LengthRange(1, 2)).generate()
    assert len(group) in (1,2)


def test_random_group_weights_generate():
    for _ in range(10):
        group = RandomGroup(alphabet="abcd", length=2, weights=[1, 0, 0 ,0]).generate()
        assert group == "aa"

def test_random_group_unique_generate():
    group = RandomGroup(alphabet="ab", unique=True).generate() 
    assert group in ("ab", "ba")


def test_random_group_unique_generate_fail():
    with pytest.raises(ValueError):
        RandomGroup(alphabet="ab", length=5, unique=True).generate()


def test_random_group_validate_non_unique():
    assert RandomGroup(alphabet="abcd").validate("abcd") is True
    assert RandomGroup(alphabet="abcd").validate("aaaa") is True
    assert RandomGroup(alphabet="abcd", length=8).validate("abcd") is False
    assert RandomGroup(alphabet="a", length=4).validate("aaaa") is True

def test_random_group_validate_unique():
    assert RandomGroup(alphabet="abcd", unique=True).validate("abcd") is True
    assert RandomGroup(alphabet="abcd", unique=True).validate("aaaa") is False


def test_random_group_validate_length_range():
    assert RandomGroup(alphabet="abcd", length=(1,3)).validate("a") is True
    assert RandomGroup(alphabet="abcd", length=(1,3)).validate("aa") is True
    assert RandomGroup(alphabet="abcd", length=(1,3)).validate("abc") is True
    assert RandomGroup(alphabet="abcd", length=(1,3)).validate("abcd") is False
    assert RandomGroup(alphabet="abcd", length=(1,3)).validate("") is False


def test_random_group_reduce_all_matching_non_unique():
    assert next(RandomGroup(alphabet="abcd", length=2).reduce_all_matching("ddab")) == "ab"
    with pytest.raises(StopIteration):
        next(RandomGroup(alphabet="abcd", length=2).reduce_all_matching("edab"))

def test_random_group_reduce_all_matching_unique():
    assert next(RandomGroup(alphabet="abcd", length=2, unique=True).reduce_all_matching("daab")) == "ab"
    with pytest.raises(StopIteration):
        next(RandomGroup(alphabet="abcd", length=2, unique=True).reduce_all_matching("ddab"))