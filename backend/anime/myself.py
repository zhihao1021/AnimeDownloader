from aiorequests import new_client, requests, ResultType
from config import HTTP_CONFIG, NOWTIME
from crud import CRUDData
from crud.anime import CRUDMyselfData
from models import Data
from models.anime import MyselfData, MyselfVideo
from utils import Json, string_exception

from datetime import datetime, timedelta
from fastapi.encoders import jsonable_encoder
from logging import getLogger
from re import search, sub
from typing import Optional

from aiohttp import ClientSession


crud_data = CRUDData()
crud_myself_data = CRUDMyselfData()


UPDATE_TIME_DELTA = timedelta(days=1)


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

        if update is None:
            if origin_data is None:
                update = True
            elif origin_data.finished:
                update = False
            else:
                update_time = datetime.fromtimestamp(origin_data.update_time)
                update = NOWTIME(False) - update_time > UPDATE_TIME_DELTA

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
                "update_time": int(NOWTIME().timestamp()),
                "finished": soup.select_one("div.z>a[href='forum-113-1.html']") is not None
            }

            if origin_data:
                result = await crud_myself_data.update(origin_data, update_data)
            else:
                new_data = MyselfData(**update_data)
                result = await crud_myself_data.create(new_data)
        else:
            result = origin_data

        return result

    @staticmethod
    async def get_weekly_update(
        update: Optional[bool] = None,
        client: Optional[ClientSession] = None,
    ) -> list[list[tuple[MyselfData, str]]]:
        origin_data = await crud_data.get_by_tag("MyselfWeeklyUpdate")

        if update is None:
            if origin_data is None:
                update = True
            else:
                update_time = datetime.fromtimestamp(origin_data.update_time)
                update = NOWTIME(False) - update_time > UPDATE_TIME_DELTA

        if update:
            soup = await requests(
                url="https://myself-bbs.com/portal.php",
                client=client,
                result_type=ResultType.SOUP
            )

            week_data = [
                [
                    (
                        MyselfData(
                            url=(
                                url := f"https://myself-bbs.com/{a_tag['href']}"),
                            tid=search("(?<=/thread-)\d+", url).group(),
                            name=a_tag.text.strip()
                        ),
                        sub("[\n\t]+", "", span_tag.text),
                    )
                    for a_tag, span_tag in zip(
                        week_tag.select("li>a"),
                        week_tag.select("li>span")
                    )
                ]
                for week_tag in soup.select("#tabSuCvYn .move-span")
            ]
            model_data = jsonable_encoder(week_data)
            result = week_data

            if origin_data:
                await crud_data.update(
                    origin_data,
                    {
                        "data": model_data
                    }
                )
            else:
                new_data = Data(
                    tag="MyselfWeeklyUpdate",
                    data=model_data
                )
                await crud_data.create(new_data)
        else:
            data = origin_data.data if origin_data else []
            result = list(map(
                lambda week_day: list(map(
                    lambda anime_tuple: (
                        MyselfData(**anime_tuple[0]),
                        anime_tuple[1],
                    ),
                    week_day
                )),
                data
            ))

        return result

    @staticmethod
    async def get_yearly_data(
        update: Optional[bool] = None,
        client: Optional[ClientSession] = None,
    ) -> dict[str, list[MyselfData]]:
        origin_data = await crud_data.get_by_tag("MyselfYearlyUpdate")

        if update is None:
            if origin_data is None:
                update = True
            else:
                update_time = datetime.fromtimestamp(origin_data.update_time)
                update = NOWTIME(False) - update_time > UPDATE_TIME_DELTA

        if update:
            soup = await requests(
                url="https://myself-bbs.com/portal.php?mod=topic&topicid=8",
                client=client,
                result_type=ResultType.SOUP
            )

            year_data = {
                sub("[^\d]+", "", season_tag.select_one(".title").text): [
                    MyselfData(
                        url=(
                            url := f"https://myself-bbs.com/{a_tag['href']}"),
                        tid=search("(?<=/thread-)\d+", url).group(),
                        name=a_tag.text.strip()
                    )
                    for a_tag in season_tag.select("a")
                ]
                for season_tag in soup.select(".frame-tab.cl .block")
            }

            model_data = jsonable_encoder(year_data)
            result = year_data

            if origin_data:
                await crud_data.update(
                    origin_data,
                    {
                        "data": model_data
                    }
                )
            else:
                new_data = Data(
                    tag="MyselfYearlyUpdate",
                    data=model_data
                )
                await crud_data.create(new_data)
        else:
            data = origin_data.data if origin_data else {}
            result = {
                key: [
                    MyselfData(**value)
                    for value in values
                ]
                for key, values in data.items()
            }

        return result
