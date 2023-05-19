from .base import IDBase

from datetime import datetime
from typing import Optional, Union

from sqlmodel import Column, DATETIME, JSON, Field as SQLField


class DataBase(IDBase):
    tag: str = SQLField(unique=True, nullable=False)
    update_time: datetime = SQLField(default_factory=datetime.utcnow, nullable=False, sa_column=Column(
        DATETIME(), onupdate=datetime.utcnow))
    data: Optional[Union[dict, list]] = SQLField(sa_column=Column(JSON()))


class Data(DataBase, table=True):
    __tablename__ = "Data"
