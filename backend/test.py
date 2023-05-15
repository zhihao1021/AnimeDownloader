from aiohttp import ClientSession
from asyncio import run
from time import time

URL = "https://nazuna.v.anime1.me/1247/1.mp4"
HEADER = {
    # "accept": "*/*",
    # "accept-language": "zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7",
    # "range": "bytes=0-",
    # "sec-ch-ua": "\"Chromium\";v=\"112\", \"Not_A Brand\";v=\"24\", \"Opera\";v=\"98\"",
    # "sec-ch-ua-mobile": "?0",
    # "sec-ch-ua-platform": "\"Linux\"",
    # "sec-fetch-dest": "video",
    # "sec-fetch-mode": "no-cors",
    # "sec-fetch-site": "same-site",
    "Referer": "https://anime1.me/",
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36 OPR/98.0.0.0"
    # "Referrer-Policy": "strict-origin-when-cross-origin"
}
COOKIES = {
    "e": 1684154637,
    "p": "eyJpc3MiOiJhbmltZTEubWUiLCJleHAiOjE2ODQxNTQ2MzcwMDAsImlhdCI6MTY4NDEyNjQyNzAwMCwic3ViIjoiLzEyNTkvMS5tcDQifQ",
    "h": "9j015PspQODQ_tjnDAdqhA",
}


async def main():
    async with ClientSession() as client:
        res = await client.post(
            "https://v.anime1.me/api",
            headers={
                # "accept": "*/*",
                # "accept-language": "zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7",
                # "cache-control": "no-cache",
                "content-type": "application/x-www-form-urlencoded",
                # "pragma": "no-cache",
                # "sec-ch-ua": "\"Chromium\";v=\"112\", \"Not_A Brand\";v=\"24\", \"Opera\";v=\"98\"",
                # "sec-ch-ua-mobile": "?0",
                # "sec-ch-ua-platform": "\"Linux\"",
                # "sec-fetch-dest": "empty",
                # "sec-fetch-mode": "cors",
                # "sec-fetch-site": "same-site",
                # "cookie": "_gid=GA1.2.1945647740.1684128639; _ga=GA1.1.446982096.1684128639; _ga_1QW4P0C598=GS1.1.1684126411.1.1.1684128652.43.0.0",
                # "Referer": "https://anime1.me/",
                # "origin": "https://anime1.me/",
                # "Referrer-Policy": "strict-origin-when-cross-origin",
                "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36 OPR/98.0.0.0",
            },
            # data=data,
            data="d=%7B%22c%22%3A%221247%22%2C%22e%22%3A%221%22%2C%22t%22%3A1684128579%2C%22p%22%3A0%2C%22s%22%3A%2285a90724f60c99940a11000ce8f6b66b%22%7D"
        )
        print(res.status, res.cookies)
        res = await client.head(URL, headers=HEADER)
        print(res.status)

run(main())
