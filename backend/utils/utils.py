from traceback import format_exception as tformat_exception
from sys import version_info

import inspect
from pydantic import BaseModel


def format_exception(exc: Exception) -> list[str]:
    return tformat_exception(exc.__class__, exc, exc.__traceback__) if version_info.minor < 10 else tformat_exception(exc)


def string_exception(exc: Exception) -> str:
    return "".join(format_exception(exc)).strip()


def optional(*fields):
    def dec(_cls):
        for field in fields:
            _cls.__fields__[field].required = False
            if _cls.__fields__[field].default:
                _cls.__fields__[field].default = None
        return _cls

    if fields and inspect.isclass(fields[0]) and issubclass(fields[0], BaseModel):
        cls = fields[0]
        fields = cls.__fields__
        return dec(cls)
    return dec
