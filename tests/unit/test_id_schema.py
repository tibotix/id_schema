import pytest
import string

from src import OneOf, RandomGroup, IDSchema, ExactLiteral
from src.components.random_group import LengthRange

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
            RandomGroup(alphabet=string.punctuation+string.ascii_letters, length=LengthRange(0,30)),
            RandomGroup(alphabet=string.punctuation+string.ascii_letters, length=LengthRange(0,30)),
        )),
        RandomGroup(alphabet=string.punctuation+string.ascii_letters, length=LengthRange(0,30)),
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
        RandomGroup(alphabet=string.punctuation+string.ascii_letters, length=LengthRange(0,30)),
    )


class ManyComponentsSchema(IDSchema):
    Components = tuple(ExactLiteral("a") for _ in range(500))


class RecursionLimitSchema(IDSchema):
    Components = tuple(ExactLiteral("a") for _ in range(2000))

class DoSSchema(IDSchema):
    Components = (
        RandomGroup(alphabet="a", length=LengthRange(1, 1000)),
        RandomGroup(alphabet="a", length=LengthRange(1, 1000))
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

def test_empty_schema_validate_empty():
    assert EmptySchema.validate("") is True
    assert EmptySchema.validate("abcd") is False

def test_single_schema_validate():
    assert SingleSchema.validate("abcd") is True
    assert SingleSchema.validate("abce") is False

def test_simple_schema_validate():
    assert SimpleSchema.validate("abcd") is True
    assert SimpleSchema.validate("abce") is False

def test_complex_schema_validate():
    for _ in range(100):
        assert ComplexSchema.validate(ComplexSchema.generate_one()) is True

def test_many_components_limit_schema_validate():
    assert ManyComponentsSchema.validate(ManyComponentsSchema.generate_one()) is True
    assert ManyComponentsSchema.validate(ManyComponentsSchema.generate_one(), iterative=False) is True

def test_recursion_limit_schema_validate():
    assert RecursionLimitSchema.validate(RecursionLimitSchema.generate_one()) is True
    with pytest.raises(ValueError):
        RecursionLimitSchema.validate(RecursionLimitSchema.generate_one(), iterative=False)

def test_dos_schema_validate():
    assert DoSSchema.validate("a"*100 + "a", iterative=True) is True
    with pytest.raises(RuntimeError):
        assert DoSSchema.validate("a"*1500 + "b", iterative=False) is True
    with pytest.raises(RuntimeError):
        assert DoSSchema.validate("a"*1500 + "b", iterative=True) is True


simple_schema = SimpleSchema.generate_one()
complex_schema = ComplexSchema.generate_one()
many_components_schema = ManyComponentsSchema.generate_one()

def test_simple_id_schema_validate_recursive_benchmark(benchmark):
    assert benchmark(SimpleSchema.validate, simple_schema, iterative=False) is True

def test_simple_id_schema_validate_iterative_benchmark(benchmark):
    assert benchmark(SimpleSchema.validate, simple_schema, iterative=True) is True

def test_many_components_id_schema_validate_recursive_benchmark(benchmark):
    assert benchmark(ManyComponentsSchema.validate, many_components_schema, iterative=False) is True

def test_many_components_id_schema_validate_iterative_benchmark(benchmark):
    assert benchmark(ManyComponentsSchema.validate, many_components_schema, iterative=True) is True

def test_complex_id_schema_validate_recursive_benchmark(benchmark):
    assert benchmark(ComplexSchema.validate, complex_schema, iterative=False) is True

def test_complex_id_schema_validate_iterative_benchmark(benchmark):
    assert benchmark(ComplexSchema.validate, complex_schema, iterative=True) is True
