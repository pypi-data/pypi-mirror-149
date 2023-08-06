from typing import Set


class ConfigurationError(Exception):
    def __init__(
        self,
        message: str = '',
    ) -> None:
        self.message = message
        super().__init__(self.message)


class DummyError(ConfigurationError):
    pass


class MissingArgument(ConfigurationError):
    def __init__(
        self,
        trace: str,
        message: str,
    ) -> None:
        self.trace = trace
        super().__init__(f"The '{trace}' has {message}.")


class MissingArgumentValue(ConfigurationError):
    def __init__(
        self,
        trace: str,
        value_name: str,
    ) -> None:
        self.trace = trace
        self.value_name = value_name
        super().__init__(f"Missing {trace}'s argument '{value_name}' value.")


class ArgumentTypeError(ConfigurationError):
    def __init__(
        self,
        message: str,
    ) -> None:
        super().__init__(f"The {message}.")


class ArgumentParserError(ConfigurationError):
    def __init__(
        self,
        param: str,
    ) -> None:
        self.param = param
        super().__init__(f"Param '{param}' has not assigned value. Use {param}=... .")


class UnexpectedArgument(ConfigurationError):
    def __init__(
        self,
        trace: str,
        overrides: Set[str],
    ) -> None:
        self.trace = trace
        self.overrides = overrides
        super().__init__(f"Override {trace}'s arguments {overrides}.")


class MissingPath(ConfigurationError):
    def __init__(self) -> None:
        super().__init__("Cannot dump params if path is not specified.")


class ObjectNotFoundError(ConfigurationError):
    def __init__(
        self,
        name: str,
        trace: str,
    ) -> None:
        self.name = name
        self.trace = trace
        super().__init__(f"Object '{name}' in '{trace}' does not exist.")


class ObjectNotRegistered(ConfigurationError):
    def __init__(
        self,
        name: str,
        trace: str,
    ) -> None:
        self.name = name
        self.trace = trace
        super().__init__(f"Object '{name}' in '{trace}' is not registered.")


class UnexpectedTypeOptionArguments(ConfigurationError):
    def __init__(
        self,
        trace: str,
    ) -> None:
        self.trace = trace
        super().__init__(f"Cannot specify any arguments for {trace}'s type.")


class ObjectInvalidOptionError(ConfigurationError):
    def __init__(
        self,
        option: str,
        trace: str,
    ) -> None:
        self.option = option
        self.trace = trace
        super().__init__(f"Option '{option}' in '{trace}' is not supported.")


class ObjectNotCallableError(ConfigurationError):
    def __init__(
        self,
        name: str,
        trace: str,
    ) -> None:
        self.name = name
        self.trace = trace
        super().__init__(f"Object '{name}' in '{trace}' is not callable.")
