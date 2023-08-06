import inspect
import warnings
from pydoc import locate
from typing import (
    Any,
    Callable,
    Dict,
    Mapping,
    Optional,
    Sequence,
    Tuple,
    Type,
    TypeVar,
    get_origin,
)

from typeguard import check_type

import smartparams.utils.string as strutil
from smartparams.exceptions import (
    ArgumentTypeError,
    MissingArgument,
    MissingArgumentValue,
    ObjectNotCallableError,
    ObjectNotFoundError,
    UnexpectedArgument,
)

_T = TypeVar('_T')


def parse_object(
    dictionary: Dict[str, Any],
    keyword: str,
) -> Tuple[Dict[str, Any], str, Optional[str]]:
    kwargs = dictionary.copy()
    name = kwargs.pop(keyword)
    name, _, option = name.partition(strutil.OBJECT_SEPARATOR)
    return kwargs, name, option


def import_callable(
    name: str,
    trace: str,
) -> Callable:
    obj = locate(name)
    if obj is None:
        raise ObjectNotFoundError(name, trace)
    if not callable(obj):
        raise ObjectNotCallableError(name, trace)
    return obj


def get_name(obj: Any) -> str:
    try:
        return obj.__qualname__
    except AttributeError:
        return obj.__class__.__qualname__


def get_return_type(callable_: Callable[..., _T]) -> Type[_T]:
    if inspect.isclass(callable_):
        return callable_

    annotation = inspect.signature(callable_).return_annotation
    return Any if annotation is inspect.Parameter.empty else annotation


def get_type_hints(signature: inspect.Signature) -> Dict[str, Any]:
    type_hints: Dict[str, Any] = {}
    for name, param in signature.parameters.items():
        if param.annotation is not inspect.Parameter.empty:
            param_type = param.annotation
        elif param.default is not inspect.Parameter.empty and param.default is not None:
            param_type = get_origin(param.default) or type(param.default)
        else:
            param_type = Any

        if param.kind == inspect.Parameter.VAR_POSITIONAL:
            type_hints[name] = Tuple[param_type, ...]  # type: ignore
        elif param.kind == inspect.Parameter.VAR_KEYWORD:
            type_hints[name] = Dict[str, param_type]  # type: ignore
        else:
            type_hints[name] = param_type

    return type_hints


def check_overrides(
    params: Dict[str, Any],
    kwargs: Dict[str, Any],
    trace: str,
    raise_error: bool,
) -> None:
    if overrides := set(params).intersection(kwargs):
        exc = UnexpectedArgument(trace, overrides)
        if raise_error:
            raise exc
        warnings.warn(exc.message)


def check_missings(
    kwargs: Dict[str, Any],
    missing_value: str,
    trace: str,
    raise_error: bool,
) -> None:
    for name, value in kwargs.items():
        if isinstance(value, str) and value.endswith(missing_value):
            exc = MissingArgumentValue(trace, name)
            if raise_error:
                raise exc
            warnings.warn(exc.message)


def check_typings(
    callable_: Callable,
    args: Tuple[Any, ...],
    kwargs: Dict[str, Any],
    trace: str,
    raise_error: bool,
) -> None:
    if callable_ is dict:
        return None

    signature = inspect.signature(callable_)
    try:
        arguments = signature.bind(*args, **kwargs).arguments
    except TypeError as e:
        raise MissingArgument(trace, " ".join(e.args))

    for name, expected_type in get_type_hints(signature).items():
        if name in arguments:
            try:
                check_type(
                    argname=f"{trace}'s argument '{name}'",
                    value=arguments[name],
                    expected_type=expected_type,
                )
            except TypeError as e:
                exc = ArgumentTypeError(" ".join(e.args))
                if raise_error:
                    raise exc
                warnings.warn(exc.message)


def convert_to_primitives(
    obj: Any,
    unknown_type: str,
) -> Any:
    if isinstance(obj, (bool, int, float, str, type(None))):
        return obj

    if isinstance(obj, Mapping):
        return {
            convert_to_primitives(k, unknown_type): convert_to_primitives(v, unknown_type)
            for k, v in obj.items()
        }

    if isinstance(obj, Sequence):
        return [convert_to_primitives(item, unknown_type) for item in obj]

    return unknown_type
