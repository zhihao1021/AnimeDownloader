from aiohttp import ClientSession
from asyncio import run
from time import time
from orjson import dumps, loads
from bs4 import BeautifulSoup
"""
{"tid":"","vid":"","id":"AgADDggAAtx3aVU"}
"""


async def main():
    async with ClientSession(
        headers={
            "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36 OPR/98.0.0.0"}
    ) as client:
        res = await client.get(
            "https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&cad=rja&uact=8&ved=2ahUKEwjEwMmamvv-AhXC4GEKHZiMDcsQjBB6BAgZEAE&url=https%3A%2F%2Fmyself-bbs.com%2Fthread-49466-1-1.html",
            allow_redirects=True,
        )
        # soup =
        print(res)
        print(res.headers)

run(main())
