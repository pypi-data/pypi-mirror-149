import inspect
import warnings
from typing import Any, Callable, Dict, Optional, Tuple, Union

import smartparams.utils.string as strutil
import smartparams.utils.typing as typeutil
from smartparams.utils.enums import Option


class SmartRegister:
    def __init__(self) -> None:
        self._aliases: Dict[str, str] = dict()
        self._origins: Dict[str, str] = dict()

    @property
    def aliases(self) -> Dict[str, str]:
        return self._aliases.copy()

    @property
    def origins(self) -> Dict[str, str]:
        return self._origins.copy()

    def reset(self) -> None:
        """Removes all registered classes and aliases."""
        self._aliases.clear()
        self._origins.clear()

    def __call__(
        self,
        *classes: Union[str, Callable, Tuple[Union[str, Callable], str]],
        prefix: str = '',
        option: Optional[str] = None,
        force: Optional[bool] = None,
    ) -> None:
        """Registers given classes with aliases.

        Args:
            classes: Classes (with aliases) to register.
            prefix: Prefix added to alias of class.
            force: Whether to allow override of existing classes and aliases.

        Notes:
            Use mapping to register a class with a custom alias (class -> alias).

        """
        for origin, alias in dict(self._create_alias(c) for c in classes).items():
            if isinstance(origin, str):
                origin = origin
            elif callable(origin):
                origin = inspect.formatannotation(origin)
                if option:
                    option = option.upper()
                    if option not in Option.keys():
                        raise ValueError(
                            f"Option {option} is not supported. "
                            f"Available: {', '.join(Option.keys())}."
                        )
                    origin = strutil.join_objects(origin, Option[option])
            else:
                raise TypeError(f"Origin have to be a string or callable instead of {type(alias)}.")

            if not isinstance(alias, str):
                raise TypeError(f"Alias have to be a string instead of {type(alias)}.")

            alias = strutil.join_keys(prefix, alias)

            if origin in self._aliases:
                message = f"Origin '{origin}' has been overridden."
                if force is False:
                    raise ValueError(message)
                elif force is None:
                    warnings.warn(message)
                self._origins.pop(self._aliases.pop(origin))

            if alias in self._origins:
                message = f"Alias '{alias}' has been overridden."
                if force is False:
                    raise ValueError(message)
                elif force is None:
                    warnings.warn(message)
                self._aliases.pop(self._origins.pop(alias))

            self._aliases[origin] = alias
            self._origins[alias] = origin

    @staticmethod
    def _create_alias(obj: Any) -> Tuple[Union[str, Callable], str]:
        if isinstance(obj, str):
            return obj, obj
        if isinstance(obj, tuple):
            if len(obj) != 2:
                raise ValueError("A tuple must consist of 2 elements (class, alias).")
            return obj  # type: ignore
        return obj, typeutil.get_name(obj)
