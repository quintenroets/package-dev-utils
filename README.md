# Package Dev Utils
[![PyPI version](https://badge.fury.io/py/package-dev-utils.svg)](https://badge.fury.io/py/package-dev-utils)
![Python version](https://img.shields.io/badge/python-3.10+-brightgreen)
![Operating system](https://img.shields.io/badge/os-linux%20%7c%20macOS%20%7c%20windows-brightgreen)
![Coverage](https://img.shields.io/badge/coverage-100%25-brightgreen)

## Usage
```python
from package_dev_utils.tests.args import cli_args


@cli_args("--debug")
def test_debugging() -> None:
    ...


def test_authentication() -> None:
    token = extract_token()
    with cli_args("--token", token):
        ...
```
## Installation
```shell
pip install package-dev-utils
```
