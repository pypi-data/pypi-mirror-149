from baby_steps import given, then, when
from district42 import schema
from pytest import raises

from revolt import substitute
from revolt.errors import SubstitutionError


def test_const_substitution():
    with given:
        const = "banana"
        sch = schema.const(const)

    with when:
        res = substitute(sch, const)

    with then:
        assert res == sch == schema.const(const)
        assert id(res) != id(sch)


def test_const_substitution_incorrect_value_error():
    with given:
        sch = schema.const("banana")

    with when, raises(Exception) as exception:
        substitute(sch, "cucumber")

    with then:
        assert exception.type is SubstitutionError
