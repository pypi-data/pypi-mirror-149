from enum import Enum
from typing import Tuple, cast


class StrEnum(str, Enum):
    @classmethod
    def keys(cls) -> Tuple[str, ...]:
        return tuple(cast(Enum, item).name for item in cls)

    @classmethod
    def values(cls) -> Tuple[str, ...]:
        return tuple(cast(Enum, item).value for item in cls)


class Option(StrEnum):
    SMART = 'Smart'
    TYPE = 'Type'


class Print(StrEnum):
    PARAMS = 'params'
    DICT = 'dict'
    KEYS = 'keys'
