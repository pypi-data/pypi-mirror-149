from enum import Enum
from typing import Tuple, cast


class Option(str, Enum):
    SMART = 'Smart'
    TYPE = 'Type'


class Print(str, Enum):
    PARAMS = 'params'
    DICT = 'dict'
    KEYS = 'keys'

    @classmethod
    def values(cls) -> Tuple[str, ...]:
        return tuple(cast(Enum, item).value for item in cls)
