from ..base import IDBase

from typing import Optional

from pydantic import BaseModel
from sqlmodel import Column, Field as SQLField, JSON


class MyselfVideo(BaseModel):
    name: str
    vid: str


class MyselfDataBase(IDBase):
    url: str = SQLField(title="網址", unique=True, nullable=False)
    tid: str = SQLField(title="TID", unique=True, nullable=False)
    name: Optional[str] = SQLField(None, title="名稱", nullable=True)
    anime_type: Optional[str] = SQLField(None, title="類別", nullable=True)
    premiere_date: Optional[str] = SQLField(None, title="播出日期", nullable=True)
    episode_num: Optional[str] = SQLField(None, title="集數", nullable=True)
    author: Optional[str] = SQLField(None, title="作者", nullable=True)
    official_web: Optional[str] = SQLField(None, title="官網", nullable=True)
    remarks: Optional[str] = SQLField(None, title="備註", nullable=True)
    intro: Optional[str] = SQLField(None, title="介紹", nullable=True)
    image_path: Optional[str] = SQLField(None, title="封面圖片網址", nullable=True)
    video_list: list[dict[str, str]] = SQLField(
        [], title="資料列表", sa_column=Column(JSON()))
    update_date: int = SQLField(0, title="資料更新日期", nullable=False)
    finished: bool = SQLField(False, title="是否已完結")


class MyselfData(MyselfDataBase, table=True):
    __tablename__ = "MyselfData"
