import pytest

from src import ExactLiteral, OneOf, RandomGroup


def test_one_of_invalid_components():
    with pytest.raises(TypeError):
        OneOf(components=(
            ExactLiteral("hello"),
            123,
        ))

def test_one_of_component_str_conversion():
    one_of = OneOf(components=(
        "hello",
        "abcd"
    ))
    assert isinstance(one_of.components[0], ExactLiteral) == True


def test_one_of_only_literals():
    one_of = OneOf(components=(
        "gmail.com",
        "webmail.de"
    ))
    assert one_of.generate() in ("gmail.com", "webmail.de")


def test_one_of_weights():
    one_of = OneOf(components=(
        "gmail.com",
        "webmail.de"
    ), weights=(
        1.0,
        0.0
    ))
    assert one_of.generate() == "gmail.com"

def test_one_of_nested():
    one_of = OneOf(components=(
        OneOf(components=(
            "hello",
            "abcd"
        )),
        OneOf(components=(
            "hey",
            "dcba"
        ))
    ))
    assert one_of.generate() in ("hello", "abcd", "hey", "dcba")


def test_one_of_validate():
    one_of = OneOf(components=(
        "hello",
        "abcd"
    ))
    assert one_of.validate("hello") == True
    assert one_of.validate("abcd") == True
    assert one_of.validate("helloabcd") == False
    assert one_of.validate("hell") == False


def test_one_of_nested_validate():
    one_of = OneOf(components=(
        OneOf(components=(
            "hello",
            "abcd"
        )),
        OneOf(components=(
            "hey",
            "dcba"
        ))
    ))
    assert one_of.validate("hello") == True
    assert one_of.validate("abcd") == True
    assert one_of.validate("hey") == True
    assert one_of.validate("dcba") == True
    assert one_of.validate("helloabcd") == False
    assert one_of.validate("abcdhey") == False
    assert one_of.validate("hell") == False
    assert one_of.validate("helloo") == False




