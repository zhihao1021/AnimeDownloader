from .base import IDBase

from datetime import datetime
from enum import auto, Enum
from typing import Optional

from sqlmodel import Column, DATETIME, Enum as SQLEnum, Field as SQLField


class DownloadStatus(int, Enum):
    NONE = auto()
    DOWNLOADING = auto()
    DOWNLOADED = auto()
    CANCEL = auto()
    FAILED = auto()


class DownloadDataBase(IDBase):
    vid: str = SQLField(title="該集ID", description="網站代號-ID-集次",
                        unique=True, nullable=False)
    aid: str = SQLField(title="該部動畫ID", description="網站代號-ID", nullable=False)
    episode: str = SQLField(title="集次", description="動畫集次", nullable=False)
    download_status: DownloadStatus = SQLField(
        DownloadStatus.NONE, title="下載狀態", description="當前下載狀態", sa_column=Column(SQLEnum(DownloadStatus)), nullable=False)
    download_path: Optional[str] = SQLField(
        None, title="下載位置", description="動畫下載位置", nullable=True)
    download_time: datetime = SQLField(
        None, title="下載時間", description="動畫下載時間", nullable=True, sa_column=(DATETIME()))


class DownloadData(DownloadDataBase, table=True):
    __tablename__ = "DownloadData"
