import sys

from hypothesis import given, strategies
from package_dev_utils.tests.args import cli_args, no_cli_args

text_strategy = strategies.text()
text_list_strategy = strategies.lists(text_strategy)
text_arguments = given(arguments=text_list_strategy)


@no_cli_args
def test_no_cli_args_decorator() -> None:
    verify_no_cli_arguments()


def test_no_cli_args_context_manager() -> None:
    with no_cli_args:
        verify_no_cli_arguments()


@cli_args()
def test_cli_args_decorator() -> None:
    verify_no_cli_arguments()


@text_arguments
def test_cli_args_context_manager(arguments: list[str]) -> None:
    with cli_args(*arguments):
        assert extract_cli_arguments() == arguments


@text_arguments
def test_combined_decorators(arguments: list[str]) -> None:
    with cli_args(*arguments):
        assert extract_cli_arguments() == arguments
    with no_cli_args:
        verify_no_cli_arguments()


@no_cli_args
@text_arguments
def test_decorator_context_manager_combination(arguments: list[str]) -> None:
    verify_no_cli_arguments()
    with cli_args(*arguments):
        assert extract_cli_arguments() == arguments
    verify_no_cli_arguments()


@given(argument=strategies.integers())
def test_string_conversion(argument: int) -> None:
    """
    A lot of packages expect sys.argv values to be strings: e.g. typer, click, ...
    """
    with cli_args(argument):
        for sys_argument in sys.argv:
            assert isinstance(sys_argument, str)


def verify_no_cli_arguments() -> None:
    assert extract_cli_arguments() == []


def extract_cli_arguments() -> list[str]:
    return sys.argv[1:]
