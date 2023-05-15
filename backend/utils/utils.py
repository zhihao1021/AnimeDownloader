from traceback import format_exception as tformat_exception
from sys import version_info


def format_exception(exc: Exception) -> list[str]:
    return tformat_exception(exc.__class__, exc, exc.__traceback__) if version_info.minor < 10 else tformat_exception(exc)


def string_exception(exc: Exception) -> str:
    return "".join(format_exception(exc)).strip()
