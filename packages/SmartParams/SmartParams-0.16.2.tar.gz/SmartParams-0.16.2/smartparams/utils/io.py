import json
from pathlib import Path
from pprint import pformat
from typing import Any, Dict

import yaml

_YAML_SUFFIXES = ('yaml', 'yml', '.yaml', '.yml')
_JSON_SUFFIXES = ('json', '.json')
_DICT_SUFFIXES = ('dict',)


def load_data(path: Path) -> Dict[str, Any]:
    if not path.is_file():
        raise FileNotFoundError(f"File '{path}' does not exist.")

    if not path.suffix:
        raise ValueError(f"File '{path}' has no extension.")
    elif path.suffix in _YAML_SUFFIXES:
        with path.open() as stream:
            dictionary = yaml.safe_load(stream)
    elif path.suffix in _JSON_SUFFIXES:
        with path.open() as stream:
            dictionary = json.load(stream)
    else:
        raise ValueError(f"File extension '{path.suffix}' is not supported.")

    if isinstance(dictionary, dict):
        return dictionary
    if dictionary is None:
        return dict()
    raise ValueError(f"File '{path}' does not contain a dictionary.")


def format_data(
    data: Any,
    fmt: str,
) -> str:
    if fmt in _YAML_SUFFIXES:
        return yaml.safe_dump(
            data=data,
            sort_keys=False,
        )

    if fmt in _JSON_SUFFIXES:
        return json.dumps(
            obj=data,
            indent=2,
            sort_keys=False,
            default=str,
        )

    if fmt in _DICT_SUFFIXES:
        return pformat(
            object=data,
            sort_dicts=False,
        )

    raise ValueError(f"Format '{fmt}' is not supported.")


def print_data(
    data: Any,
    fmt: str,
) -> None:
    print(format_data(data=data, fmt=fmt))


def save_data(
    data: Dict[str, Any],
    path: Path,
) -> None:
    if not path.suffix:
        raise ValueError(f"File '{path}' has no extension.")

    if path.suffix in _YAML_SUFFIXES:
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open('w') as stream:
            yaml.safe_dump(
                data=data,
                stream=stream,
                sort_keys=False,
            )
    elif path.suffix in _JSON_SUFFIXES:
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open('w') as stream:
            json.dump(
                obj=data,
                fp=stream,
                indent=2,
                sort_keys=False,
                default=str,
            )
    else:
        raise ValueError(f"File extension '{path.suffix}' is not supported.")
