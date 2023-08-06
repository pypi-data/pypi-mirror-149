from typing import Any

from terality._terality import global_client


def set_option(pat: str, value: Any) -> None:
    global_client().set_pandas_option(pat, value)


def get_option(pat: str) -> Any:
    return global_client().get_pandas_option(pat)
