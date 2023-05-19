from utils import Json

from datetime import datetime, timedelta, timezone
from os.path import isfile

from pydantic import BaseModel
from sqlalchemy.ext.asyncio import create_async_engine


class WebConfig(BaseModel):
    host: str = "0.0.0.0"
    port: int = 8080


class SQLAlchemyConfig(BaseModel):
    url: str = "sqlite+aiosqlite:///data.db"
    check_same_thread: bool = False


class HttpConfig(BaseModel):
    headers: dict[str, str] = {
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36 OPR/98.0.0.0"
    }
    cookies: dict[str, str] = {}
    timeout: float = 10.0
    ssl: bool = True


if isfile("config.json"):
    config = Json.load_nowait("config.json")
else:
    config = {
        "web": {
            "host": "0.0.0.0",
            "port": 8080
        },
        "logging": {

        },
        "sqlalchemy": {
            "url": "sqlite+aiosqlite:///data.db",
            "check_same_thread": False,
        },
        "http": {
            "headers": {
                "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36 OPR/98.0.0.0",
            },
            "cookies": {},
            "timeout": 10,
            "ssl": True,
        },
        "timezone": 8,
    }
    Json.dump_nowait("config.json", config)

WEB_CONFIG = WebConfig(**config.get("web", {}))
SQLALCHEMY_CONFIG = SQLAlchemyConfig(**config.get("sqlalchemy", {}))
HTTP_CONFIG = HttpConfig(**config.get("http", {}))

ENGINE = create_async_engine(
    SQLALCHEMY_CONFIG.url,
    connect_args={
        "check_same_thread": SQLALCHEMY_CONFIG.check_same_thread,
    },
)

TIMEZONE = timezone(timedelta(hours=config.get("timezone", 8)))


# def NOWTIME(timezone: bool = True) -> datetime:
#     return datetime.now(TIMEZONE if timezone else None)
