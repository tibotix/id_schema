import pytest
import string

from src import RandomGroup, IDSchema, ExactLiteral

class SimpleSchema(IDSchema):
    Components = (
        ExactLiteral("a"),
        ExactLiteral("bc"),
        ExactLiteral("d")
    )

class ComplexSchema(IDSchema):
    Components = (
        RandomGroup(alphabet=string.punctuation+string.ascii_letters, length=(0,30)),
        RandomGroup(alphabet=string.punctuation+string.ascii_letters, length=(0,30)),
        ExactLiteral("-"),
        RandomGroup(alphabet="abcd", length=4),
        ExactLiteral("abcd"),
        RandomGroup(alphabet="abcd", length=2),
        ExactLiteral("a"),
        RandomGroup(alphabet="abcd", length=2),
        RandomGroup(alphabet=string.punctuation+string.ascii_letters, length=(0,30)),
    )


def test_id_schema_generate_one():
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
    assert SimpleSchema.validate("abcd") is True
    assert SimpleSchema.validate("abce") is False
    for _ in range(100):
        assert ComplexSchema.validate(ComplexSchema.generate_one()) is True


