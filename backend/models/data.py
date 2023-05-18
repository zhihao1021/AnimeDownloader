from .base import IDBase

from config import NOWTIME

from typing import Optional, Union

from sqlmodel import Column,  JSON, Field as SQLField


class DataBase(IDBase):
    tag: str = SQLField(unique=True, nullable=False)
    update_time: int = SQLField(default_factory=lambda: int(NOWTIME().timestamp()), nullable=False)
    data: Optional[Union[dict, list]] = SQLField(sa_column=Column(JSON()))


class Data(DataBase, table=True):
    __tablename__ = "Data"
