import pytest
import string

from src import OneOf, RandomGroup, IDSchema, ExactLiteral

class EmptySchema(IDSchema):
    Components = []


class SingleSchema(IDSchema):
    Components = (
        ExactLiteral("abcd"),
    )

class SimpleSchema(IDSchema):
    Components = (
        ExactLiteral("a"),
        ExactLiteral("bc"),
        ExactLiteral("d")
    )

class ComplexSchema(IDSchema):
    Components = (
        OneOf(components=(
            RandomGroup(alphabet=string.punctuation+string.ascii_letters, length=(0,30)),
            RandomGroup(alphabet=string.punctuation+string.ascii_letters, length=(0,30)),
        )),
        RandomGroup(alphabet=string.punctuation+string.ascii_letters, length=(0,30)),
        ExactLiteral("-"),
        RandomGroup(alphabet="abcd", length=4),
        ExactLiteral("abcd"),
        RandomGroup(alphabet="abcd", length=2),
        ExactLiteral("a"),
        OneOf(components=(
            "a",
            "b",
            "c",
        )),
        RandomGroup(alphabet="abcd", length=2),
        RandomGroup(alphabet=string.punctuation+string.ascii_letters, length=(0,30)),
    )


def test_id_schema_generate_one():
    assert EmptySchema.generate_one() == ""
    assert SingleSchema.generate_one() == "abcd"
    assert SimpleSchema.generate_one() == "abcd"

def test_id_schema_generate_n():
    l = SimpleSchema.generate_n(2)
    assert len(l) == 2
    assert l[0] == "abcd"
    assert l[1] == "abcd"


def test_id_schema_generate_n_unique():
    l = SimpleSchema.generate_n_unique(1)
    assert len(l) == 1
    assert l[0] == "abcd"

    with pytest.raises(RuntimeError):
        SimpleSchema.generate_n_unique(2)


def test_id_schema_validate():
    assert SingleSchema.validate("abcd") is True
    assert SingleSchema.validate("abce") is False
    assert SimpleSchema.validate("abcd") is True
    assert SimpleSchema.validate("abce") is False
    for _ in range(100):
        assert ComplexSchema.validate(ComplexSchema.generate_one()) is True


def test_id_schema_validate_empty():
    assert EmptySchema.validate("") is True
    assert EmptySchema.validate("abcd") is False