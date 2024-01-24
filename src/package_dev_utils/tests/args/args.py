import functools
import sys
from collections.abc import Callable
from types import TracebackType
from typing import Any, Protocol, TypeVar, cast
from unittest.mock import patch

T = TypeVar("T", bound=Callable[..., Any])


class StrProtocol(Protocol):
    def __str__(self) -> str:
        ...  # pragma: no cover


class CLIArgs:
    def __init__(self, *args: StrProtocol):
        self.args: tuple[StrProtocol, ...] = args
        self.sys_args_patcher: Any | None = None

    def __call__(self, function: T) -> T:
        @functools.wraps(function)
        def args_wrapper(*func_args: Any, **func_kwargs: Any) -> Any:
            with self:
                return function(*func_args, **func_kwargs)

        return cast(T, args_wrapper)

    def __enter__(self) -> None:
        str_args = (str(arg) for arg in self.args)
        args = [sys.argv[0], *str_args]
        self.sys_args_patcher = patch("sys.argv", args)
        self.sys_args_patcher.__enter__()

    def __exit__(
        self,
        exception_type: type[BaseException] | None,
        exception_value: BaseException | None,
        traceback: TracebackType,
    ) -> None:
        if self.sys_args_patcher is not None:
            self.sys_args_patcher.__exit__(exception_type, exception_value, traceback)
