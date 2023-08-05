# revolt

[![Codecov](https://img.shields.io/codecov/c/github/nikitanovosibirsk/revolt/master.svg?style=flat-square)](https://codecov.io/gh/nikitanovosibirsk/revolt)
[![PyPI](https://img.shields.io/pypi/v/revolt.svg?style=flat-square)](https://pypi.python.org/pypi/revolt/)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/revolt?style=flat-square)](https://pypi.python.org/pypi/revolt/)
[![Python Version](https://img.shields.io/pypi/pyversions/revolt.svg?style=flat-square)](https://pypi.python.org/pypi/revolt/)

Value substitutor for [district42](https://github.com/nikitanovosibirsk/district42) schema

## Installation

```sh
pip3 install revolt
```

## Usage

```python
from district42 import schema
from revolt import substitute

UserSchema = schema.dict({
    "id": schema.int,
    "name": schema.str | schema.none,
    "id_deleted": schema.bool,
})

substituted = substitute(UserSchema, {"id": 1, "name": "Bob"})

# syntax sugar
substituted = UserSchema % {"id": 1, "name": "Bob"}
```

## Documentation

* [Documentation](#documentation)
  * [Custom Types](#custom-types)
    * [1. Declare Schema](#1-declare-schema)
    * [2. Register Substitutor](#2-register-substitutor)
    * [3. Register Representor](#3-register-representor)
    * [4. Use](#4-use)

### Custom Types

#### 1. Declare Schema

```python
from typing import Any
from uuid import UUID
from district42 import Props, SchemaVisitor, SchemaVisitorReturnType as ReturnType
from district42.types import Schema
from niltype import Nilable


class UUIDProps(Props):
    @property
    def value(self) -> Nilable[UUID]:
        return self.get("value")


class UUIDSchema(Schema[UUIDProps]):
    def __accept__(self, visitor: SchemaVisitor[ReturnType], **kwargs: Any) -> ReturnType:
        return visitor.visit_uuid(self, **kwargs)

    def __call__(self, /, value: UUID) -> "UUIDSchema":
        return self.__class__(self.props.update(value=value))
```

#### 2. Register Substitutor

```python
from typing import Any
from uuid import UUID
from niltype import Nil
from revolt import Substitutor


class UUIDSubstitutor(Substitutor, extend=True):
    def visit_uuid(self, schema: UUIDSchema, *, value: Any = Nil, **kwargs: Any) -> UUIDSchema:
        assert isinstance(value, UUID) and schema.props.value is Nil

        return schema.__class__(schema.props.update(value=value))
```

#### 3. Register Representor

```python
from typing import Any
from district42.representor import Representor
from niltype import Nil


class UUIDRepresentor(Representor, extend=True):
    def visit_uuid(self, schema: UUIDSchema, *, indent: int = 0, **kwargs: Any) -> str:
        r = f"{self._name}.uuid"

        if schema.props.value is not Nil:
            r += f"({schema.props.value!r})"

        return r
```

#### 4. Use

```python
from uuid import uuid4
from district42 import register_type, schema

register_type("uuid", UUIDSchema)

print(schema.uuid % uuid4())
# schema.uuid(UUID('8289806e-4f61-45a1-993b-1aa1b289735b'))
```

Full code available here: [district42_exp_types/uuid](https://github.com/nikitanovosibirsk/district42-exp-types/tree/master/district42_exp_types/uuid)
