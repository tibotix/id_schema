import pytest


from src import ExactLiteral


def test_exact_literal_one_char_generate():
    literal = ExactLiteral("-")
    assert literal.generate() == "-"


def test_exact_literal_one_char_validate():
    literal = ExactLiteral("-")
    assert literal.validate("-") is True
    assert literal.validate("--") is False
    assert literal.validate("a") is False

def test_exact_literal_one_char_reduce_all_matching():
    literal = ExactLiteral("-")
    assert next(literal.reduce_all_matching("-")) == ""
    assert next(literal.reduce_all_matching("--")) == "-"
    assert next(literal.reduce_all_matching("-a")) == "a"
    with pytest.raises(StopIteration):
        next(literal.reduce_all_matching("a-"))


def test_exact_literal_multi_char_generate():
    literal = ExactLiteral("---")
    assert literal.generate() == "---"


def test_exact_literal_multi_char_validate():
    literal = ExactLiteral("---")
    assert literal.validate("---") is True
    assert literal.validate("--") is False
    assert literal.validate("a--") is False

def test_exact_literal_multi_char_reduce_all_matching():
    literal = ExactLiteral("---")
    assert next(literal.reduce_all_matching("---")) == ""
    assert next(literal.reduce_all_matching("----")) == "-"
    assert next(literal.reduce_all_matching("---a")) == "a"
    assert next(literal.reduce_all_matching("----a")) == "-a"
    with pytest.raises(StopIteration):
        next(literal.reduce_all_matching("--a"))