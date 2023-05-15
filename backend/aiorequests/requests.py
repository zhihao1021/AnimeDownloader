from .type import RequestMethod, ResultType

from utils.json import Json
from utils.utils import string_exception

from config import HTTP_CONFIG
from logging import getLogger
from typing import Any, Optional, Union

from aiohttp import ClientTimeout, ClientResponse, ClientSession
from bs4 import BeautifulSoup
from multidict import CIMultiDictProxy

logger = getLogger("http")


def new_client(
    headers: dict[str, str] = HTTP_CONFIG.headers,
    cookies: dict[str, str] = HTTP_CONFIG.cookies,
    timeout: float = HTTP_CONFIG.timeout
):
    return ClientSession(
        headers=headers,
        cookies=cookies,
        conn_timeout=timeout
    )


async def requests(
    url: str,
    client: Optional[ClientSession] = None,
    *,
    method: int = RequestMethod.GET,
    data: Any = None,
    result_type: int = ResultType.BYTES,
    max_redirects: int = 10,
    raise_exception: bool = False,
    ssl: bool = HTTP_CONFIG.ssl,
    headers: Optional[dict[str, str]] = None,
    cookies: Optional[dict[str, str]] = None,
    timeout: Optional[float] = None,
    new_client_headers: dict[str, str] = HTTP_CONFIG.headers,
    new_client_cookies: dict[str, str] = HTTP_CONFIG.cookies,
    new_client_timeout: float = HTTP_CONFIG.timeout,
) -> Optional[Union[bytes, CIMultiDictProxy, ClientResponse, BeautifulSoup, dict, list]]:
    # 檢查Client是否為None
    client_need_close = client == None
    client = client if client else new_client(
        headers=new_client_headers,
        cookies=new_client_cookies,
        timeout=new_client_timeout
    )

    # 檢查是否允許重新導向
    allow_redirects = max_redirects > -1

    try:
        # 設定參數
        kwargs = {
            "url": url,
            "allow_redirects": allow_redirects,
            "max_redirects": max_redirects,
            "ssl": ssl
        }
        if headers:
            kwargs["headers"] = headers
        if cookies:
            kwargs["cookies"] = cookies
        if timeout:
            kwargs["timeout"] = ClientTimeout(connect=timeout)

        # 設定請求方法
        if method == RequestMethod.POST:
            request = client.post
            try:
                data = Json.dumps(data) if type(
                    data) not in (str, bytes) else data
            except:
                pass
            kwargs["data"] = data
        elif method == RequestMethod.HEAD:
            request = client.head
        else:
            request = client.get

        # 發出請求
        result = await request(**kwargs)

        # 回傳
        if result_type == ResultType.RAW:
            return result
        elif result_type == ResultType.BYTES:
            return await result.content.read()
        elif result_type == ResultType.SOUP:
            return BeautifulSoup(
                await result.content.read(),
                features="html.parser",
            )
        elif result_type == ResultType.JSON:
            return await result.json()
        elif result_type == ResultType.HEADERS:
            return result.headers
    except Exception as exc:
        # 紀錄錯誤
        logger.error(string_exception(exc))

        # 回傳錯誤
        if raise_exception:
            raise exc
        return None
    finally:
        if client_need_close:
            await client.close()
