import functools
import sys
import typing
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
        exception: BaseException | None,
        traceback: TracebackType,
    ) -> bool:
        sys_args_patcher = typing.cast(Any, self.sys_args_patcher)
        exception_handled = sys_args_patcher.__exit__(
            exception_type, exception, traceback
        )
        return typing.cast(bool, exception_handled)
