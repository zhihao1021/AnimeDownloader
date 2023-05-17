from enum import Enum, auto


class RequestMethod(str, Enum):
    GET = "get"
    POST = "post"
    HEAD = "head"


class ResultType(int, Enum):
    RAW = auto()
    BYTES = auto()
    SOUP = auto()
    JSON = auto()
    HEADERS = auto()
