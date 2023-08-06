import inspect
import warnings
from typing import Callable, Dict, Mapping, Optional, Sequence, Union

import smartparams.utils.string as strutil
import smartparams.utils.typing as typeutil


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

    def __call__(
        self,
        classes: Union[
            Sequence[Union[str, Callable]],
            Mapping[str, str],
            Mapping[Callable, str],
            Mapping[Union[str, Callable], str],
        ],
        prefix: str = '',
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
        if isinstance(classes, Sequence):
            self._register_classes(
                classes=classes,
                prefix=prefix,
                force=force,
            )
        elif isinstance(classes, Mapping):
            self._register_aliases(
                aliases=classes,
                prefix=prefix,
                force=force,
            )
        else:
            raise TypeError(f"Register classes type '{type(classes)}' is not supported.")

    def reset(self) -> None:
        """Removes all registered classes and aliases."""
        self._aliases.clear()
        self._origins.clear()

    def _register_classes(
        self,
        classes: Sequence[Union[str, Callable]],
        prefix: str = '',
        force: Optional[bool] = None,
    ) -> None:
        self._register_aliases(
            aliases={c: c if isinstance(c, str) else typeutil.get_name(c) for c in classes},
            prefix=prefix,
            force=force,
        )

    def _register_aliases(
        self,
        aliases: Union[
            Mapping[str, str],
            Mapping[Callable, str],
            Mapping[Union[str, Callable], str],
        ],
        prefix: str = '',
        force: Optional[bool] = None,
    ) -> None:
        for origin, alias in aliases.items():
            origin = origin if isinstance(origin, str) else inspect.formatannotation(origin)
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
