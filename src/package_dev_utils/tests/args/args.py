import functools
from collections.abc import Callable
from types import TracebackType
from typing import Any, TypeVar
from unittest.mock import patch

T = TypeVar("T")


class CLIArgs:
    def __init__(self, *args: str):
        self.args: tuple[str, ...] = args
        self.sys_args_patcher: Any | None = None

    def __call__(self, function: Callable[..., T]) -> Callable[..., T]:
        @functools.wraps(function)
        def args_wrapper(*func_args: Any, **func_kwargs: Any) -> T:
            with self:
                return function(*func_args, **func_kwargs)

        return args_wrapper

    def __enter__(self) -> None:
        args = list(self.args)
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
