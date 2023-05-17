from aiorequests import new_client, requests, ResultType
from config import HTTP_CONFIG, NOWTIME
from crud.anime import CRUDMyselfData
from models.anime import MyselfData, MyselfVideo
from utils import Json, string_exception

from datetime import datetime, timedelta
from logging import getLogger
from re import search
from typing import Optional

from aiohttp import ClientSession


crud_myself_data = CRUDMyselfData()


async def get_m3u8_url(
    tid: str,
    vid: str,
    client: Optional[ClientSession] = None,
) -> Optional[str]:
    client_need_close = client is None
    client = client if client else new_client()

    try:
        ws = await client.ws_connect(
            url="wss://v.myself-bbs.com/ws",
            origin="https://v.myself-bbs.com",
            ssl=HTTP_CONFIG.ssl,
        )

        data = {
            "tid": tid,
            "vid": vid,
            "id": ""
        } if vid.isdigit() else {
            "tid": "",
            "vid": "",
            "id": vid
        }
        await ws.send_json(data, dumps=Json.dumps)

        result = await ws.receive_json(
            loads=Json.loads,
            timeout=HTTP_CONFIG.timeout
        )
        return f"https://{result['video']}"
    except Exception as exc:
        logger = getLogger("http")
        logger.error(string_exception(exc))

        return None
    finally:
        if client_need_close:
            await client.close()


class Myself:
    @staticmethod
    async def get(
        url: str,
        update: Optional[bool] = None,
        client: Optional[ClientSession] = None,
    ) -> Optional[MyselfData]:
        url = url.strip()
        if not url.startswith("https://myself-bbs.com"):
            return None

        origin_data = await crud_myself_data.get_by_url(url)

        if update == None:
            if origin_data is None:
                update = True
            elif origin_data.finished:
                update = False
            else:
                update_date = datetime.fromtimestamp(origin_data.update_date)
                update = update_date - NOWTIME(False) > timedelta(days=1)

        if update:
            soup = await requests(
                url=url,
                client=client,
                result_type=ResultType.SOUP,
            )

            info_text = tuple(map(
                lambda tag: tag.text.split(": ", 1)[1].strip(),
                soup.select("div.info_info li")
            ))
            update_data = {
                "url": url,
                "tid": search("(?<=/thread-)\d+", url).group(),
                "name": soup.select_one("meta[name='keywords']")["content"],
                "anime_type": info_text[0],
                "premiere_date": info_text[1],
                "episode_num": info_text[2],
                "author": info_text[3],
                "official_web": info_text[4],
                "remarks": info_text[5],
                "intro": soup.select_one("#info_introduction_text").text,
                "image_path": soup.select_one("div.info_img_box img")["src"],
                "video_list": [
                    {
                        "name": tag.select_one("li>a").text,
                        "vid": tag.select_one("a[data-href*='myself-bbs']")["data-href"].rsplit("/", 1)[-1].strip()
                    }
                    for tag in soup.select("ul.main_list li:has(ul a[data-href*='myself-bbs'])")
                ],
                "update_date": NOWTIME().timestamp(),
                "finished": soup.select_one("div.z>a[href='forum-113-1.html']") is not None
            }

            if origin_data:
                result = await crud_myself_data.update(origin_data, update_date)
            else:
                new_data = MyselfData(**update_data)
                result = await crud_myself_data.create(new_data)

        return result
    
    @staticmethod
    async def get_weekly_update():
        pass