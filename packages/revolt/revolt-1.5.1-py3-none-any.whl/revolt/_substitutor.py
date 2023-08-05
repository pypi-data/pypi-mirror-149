from typing import Any, Dict, List, Optional, cast

from district42 import SchemaVisitor, from_native
from district42.types import (
    AnySchema,
    BoolSchema,
    BytesSchema,
    ConstSchema,
    DictSchema,
    FloatSchema,
    GenericSchema,
    GenericTypeAliasSchema,
    IntSchema,
    ListSchema,
    NoneSchema,
    StrSchema,
    TypeAliasPropsType,
)
from district42.utils import is_ellipsis
from niltype import Nil
from valera import Formatter, Validator

from ._validator import SubstitutorValidator
from .errors import SubstitutionError, make_substitution_error

__all__ = ("Substitutor",)


class Substitutor(SchemaVisitor[GenericSchema]):
    def __init__(self, validator: Optional[Validator] = None,
                 formatter: Optional[Formatter] = None) -> None:
        self._validator = validator or SubstitutorValidator()
        self._formatter = formatter or Formatter()

    def _from_native(self, value: Any) -> GenericSchema:
        try:
            return from_native(value)
        except ValueError:
            raise SubstitutionError(f"Can't convert {value!r} to schema")

    def visit_none(self, schema: NoneSchema, *, value: Any = Nil, **kwargs: Any) -> NoneSchema:
        result = schema.__accept__(self._validator, value=value)
        if result.has_errors():
            raise make_substitution_error(result, self._formatter)
        return schema.__class__(schema.props)

    def visit_bool(self, schema: BoolSchema, *, value: Any = Nil, **kwargs: Any) -> BoolSchema:
        result = schema.__accept__(self._validator, value=value)
        if result.has_errors():
            raise make_substitution_error(result, self._formatter)
        return schema.__class__(schema.props.update(value=value))

    def visit_int(self, schema: IntSchema, *, value: Any = Nil, **kwargs: Any) -> IntSchema:
        result = schema.__accept__(self._validator, value=value)
        if result.has_errors():
            raise make_substitution_error(result, self._formatter)
        return schema.__class__(schema.props.update(value=value))

    def visit_float(self, schema: FloatSchema, *, value: Any = Nil, **kwargs: Any) -> FloatSchema:
        result = schema.__accept__(self._validator, value=value)
        if result.has_errors():
            raise make_substitution_error(result, self._formatter)
        return schema.__class__(schema.props.update(value=value))

    def visit_str(self, schema: StrSchema, *, value: Any = Nil, **kwargs: Any) -> StrSchema:
        result = schema.__accept__(self._validator, value=value)
        if result.has_errors():
            raise make_substitution_error(result, self._formatter)
        return schema.__class__(schema.props.update(value=value))

    def _substitute_elements(self,
                             value: List[Any],
                             elements: List[GenericSchema],
                             start: int = 0,
                             **kwargs: Any) -> List[GenericSchema]:
        substituted = []
        for index, element_schema in enumerate(elements):
            real_index = start + index
            if real_index >= len(value):
                raise SubstitutionError(f"Index {real_index} out of range")
            res = element_schema.__accept__(self, value=value[real_index], **kwargs)
            substituted.append(res)

        for i in range(start + len(substituted), len(value)):
            substituted.insert(i, self._from_native(value[i]))

        for i in range(start):
            substituted.insert(i, self._from_native(value[i]))

        return substituted

    def visit_list(self, schema: ListSchema, *, value: Any = Nil, **kwargs: Any) -> ListSchema:
        result = schema.__accept__(self._validator, value=value)
        if result.has_errors():
            raise make_substitution_error(result, self._formatter)

        if len(value) > 0 and all(is_ellipsis(x) for x in value):
            raise SubstitutionError("Can't substitute all ...")

        if (schema.props.elements is Nil) and (schema.props.type is Nil):
            elements = []
            for val in value:
                element = val if is_ellipsis(val) else self._from_native(val)
                elements.append(element)
            return schema.__class__(schema.props.update(elements=elements))

        if schema.props.type is not Nil:
            elements = []
            for val in value:
                if is_ellipsis(val):
                    element = val
                else:
                    element = schema.props.type.__accept__(self, value=val, **kwargs)
                elements.append(element)
            return schema.__class__(schema.props.update(elements=elements, type=Nil))

        elements = cast(List[GenericSchema], schema.props.elements)
        if ... in value:
            raise SubstitutionError("Can't substitute ...")

        # body
        if (len(elements) > 2) and is_ellipsis(elements[0]) and is_ellipsis(elements[-1]):
            for index, val in enumerate(value):
                try:
                    substituted = self._substitute_elements(value, elements[1:-1], index, **kwargs)
                except SubstitutionError:
                    pass
                else:
                    return schema.__class__(schema.props.update(elements=substituted))

        # head
        if (len(elements) >= 2) and is_ellipsis(elements[-1]):
            substituted = self._substitute_elements(value, elements[:-1], **kwargs)
            return schema.__class__(schema.props.update(elements=substituted))

        # tail
        if (len(elements) >= 1) and is_ellipsis(elements[0]):
            elements = elements[1:]
            index = max(0, len(value) - len(elements))
            substituted = self._substitute_elements(value, elements, index, **kwargs)
            return schema.__class__(schema.props.update(elements=substituted))

        substituted = self._substitute_elements(value, elements, **kwargs)
        return schema.__class__(schema.props.update(elements=substituted))

    def visit_dict(self, schema: DictSchema, *, value: Any = Nil, **kwargs: Any) -> DictSchema:
        result = schema.__accept__(self._validator, value=value)
        if result.has_errors():
            raise make_substitution_error(result, self._formatter)

        if ... in value:
            raise SubstitutionError("Can't substitute ...")

        keys: Dict[Any, Any] = {}
        if schema.props.keys is Nil or (len(schema.props.keys) == 1 and ... in schema.props.keys):
            for key, val in value.items():
                keys[key] = (self._from_native(val), False)
            if (schema.props.keys is not Nil) and (... in schema.props.keys):
                keys[...] = (..., False)
        else:
            for key, (val, is_optional) in schema.props.keys.items():
                if key in value:
                    keys[key] = (val.__accept__(self, value=value[key], **kwargs), False)
                else:
                    keys[key] = (val, is_optional)
            for key, val in value.items():
                if key not in schema.props.keys:
                    raise SubstitutionError(f"Unknown key {key!r}")

        return schema.__class__(schema.props.update(keys=keys))

    def visit_any(self, schema: AnySchema, *, value: Any = Nil, **kwargs: Any) -> AnySchema:
        result = schema.__accept__(self._validator, value=value)
        if result.has_errors():
            raise make_substitution_error(result, self._formatter)

        types = []
        if schema.props.types is Nil:
            types.append(self._from_native(value))
        else:
            for sch_type in schema.props.types:
                try:
                    substituted = sch_type.__accept__(self, value=value, **kwargs)
                except SubstitutionError:
                    pass
                else:
                    types.append(substituted)
        return schema.__class__(schema.props.update(types=tuple(types)))

    def visit_const(self, schema: ConstSchema, *, value: Any = Nil, **kwargs: Any) -> Any:
        result = schema.__accept__(self._validator, value=value)
        if result.has_errors():
            raise make_substitution_error(result, self._formatter)
        return schema.__class__(schema.props.update(value=value))

    def visit_bytes(self, schema: BytesSchema, *, value: Any = Nil, **kwargs: Any) -> BytesSchema:
        result = schema.__accept__(self._validator, value=value)
        if result.has_errors():
            raise make_substitution_error(result, self._formatter)
        return schema.__class__(schema.props.update(value=value))

    def visit_type_alias(self, schema: GenericTypeAliasSchema[TypeAliasPropsType], *,
                         value: Any = Nil,
                         **kwargs: Any) -> GenericTypeAliasSchema[TypeAliasPropsType]:
        substituted = schema.props.type.__accept__(self, value=value, **kwargs)
        return schema.__class__(schema.props.update(type=substituted))
