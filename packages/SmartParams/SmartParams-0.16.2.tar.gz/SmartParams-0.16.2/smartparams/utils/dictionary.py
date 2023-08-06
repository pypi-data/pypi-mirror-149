from typing import Any, Dict, List, Tuple

import smartparams.utils.string as strutil


def flatten_keys(
    obj: Any,
    _prefix: str = '',
) -> List[str]:
    if not isinstance(obj, dict) or (not obj and _prefix):
        return [_prefix]

    keys = []
    for k, v in obj.items():
        keys.extend(flatten_keys(v, strutil.join_keys(_prefix, k)))

    return keys


def find_nested(
    dictionary: Dict[str, Any],
    key: str,
    create_mode: bool = False,
    set_mode: bool = False,
    required: bool = False,
) -> Tuple[Dict[str, Any], str]:
    *nested_keys, last_key = key.split(strutil.KEY_SEPARATOR)

    key_list = list()
    for k in nested_keys:
        key_list.append(k)
        if k not in dictionary:
            if create_mode:
                dictionary[k] = dict()
            else:
                key_trace = strutil.KEY_SEPARATOR.join(key_list)
                raise KeyError(f"Param '{key_trace}' is not in dictionary.")

        if not isinstance(dictionary[k], dict):
            if set_mode:
                dictionary[k] = dict()
            else:
                key_trace = strutil.KEY_SEPARATOR.join(key_list)
                raise ValueError(f"Param '{key_trace}' is not dictionary.")

        dictionary = dictionary[k]

    if required and last_key not in dictionary:
        key_list.append(last_key)
        key_trace = strutil.KEY_SEPARATOR.join(key_list)
        raise KeyError(f"Param '{key_trace}' is not in dictionary.")

    return dictionary, last_key


def check_key_is_in(
    key: str,
    dictionary: Dict[str, Any],
) -> bool:
    key, _, sub_key = key.partition(strutil.KEY_SEPARATOR)
    if key not in dictionary:
        return False

    if not sub_key:
        return True

    dictionary = dictionary[key]

    if not isinstance(dictionary, dict):
        return True

    return check_key_is_in(
        key=sub_key,
        dictionary=dictionary,
    )


def normalize(
    dictionary: Dict,
    trace: str = '',
) -> Dict:
    normalized_dictionary: Dict = {}
    for key, value in dictionary.items():
        if isinstance(key, str):
            key, _, sub_key = key.partition(strutil.KEY_SEPARATOR)
            if sub_key:
                value = {sub_key: value}

            current_trace = strutil.join_keys(trace, key)

            if isinstance(value, dict):
                value = normalize(
                    dictionary=value,
                    trace=current_trace,
                )

            if key in normalized_dictionary:
                value = merge(
                    a=normalized_dictionary[key],
                    b=value,
                    trace=current_trace,
                )

        normalized_dictionary[key] = value

    return normalized_dictionary


def merge(
    a: Any,
    b: Any,
    trace: str = '',
) -> Any:
    if isinstance(a, dict) and isinstance(b, dict):
        dictionary = {}
        intersection = set(a).intersection(b)
        for key in set(a).union(b):
            if key in intersection:
                dictionary[key] = merge(
                    a=a[key],
                    b=b[key],
                    trace=strutil.join_keys(trace, key),
                )
            else:
                dictionary[key] = a.get(key, b.get(key))

        return dictionary

    raise ValueError(f"Cannot merge params with key: '{trace}'.")
