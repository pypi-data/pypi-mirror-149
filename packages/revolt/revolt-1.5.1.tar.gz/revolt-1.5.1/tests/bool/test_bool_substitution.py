import pytest
from baby_steps import given, then, when
from district42 import schema
from pytest import raises

from revolt import substitute
from revolt.errors import SubstitutionError


@pytest.mark.parametrize("value", [True, False])
def test_bool_substitution(value: bool):
    with given:
        sch = schema.bool

    with when:
        res = substitute(sch, value)

    with then:
        assert res == schema.bool(value)
        assert res != sch


@pytest.mark.parametrize("value", [True, False])
def test_bool_value_substitution(value: bool):
    with given:
        sch = schema.bool(value)

    with when:
        res = substitute(sch, value)

    with then:
        assert res == sch == schema.bool(value)
        assert id(res) != id(sch)


def test_bool_substitution_invalid_value_error():
    with given:
        sch = schema.bool

    with when, raises(Exception) as exception:
        substitute(sch, None)

    with then:
        assert exception.type is SubstitutionError


@pytest.mark.parametrize("value", [True, False])
def test_bool_substitution_incorrect_value_error(value: bool):
    with given:
        sch = schema.bool(value)

    with when, raises(Exception) as exception:
        substitute(sch, not value)

    with then:
        assert exception.type is SubstitutionError
