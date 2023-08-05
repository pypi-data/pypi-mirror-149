from typing import Any

from district42 import GenericSchema
from district42.types import Schema

from ._substitutor import Substitutor
from ._validator import SubstitutorValidator
from ._version import version

__version__ = version
__all__ = ("substitute", "Substitutor", "SubstitutorValidator",)

_substitutor = Substitutor()


def substitute(schema: GenericSchema, value: Any, **kwargs: Any) -> Any:
    return schema.__accept__(_substitutor, value=value, **kwargs)


Schema.__override__(Schema.__mod__.__name__, substitute)
