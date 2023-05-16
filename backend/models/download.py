from .base import IDBase

from typing import Optional

from sqlmodel import Field as SQLField


class DownloadStatus:
    NONE = 0
    DOWNLOADING = 1
    DOWNLOADED = 2
    CANCEL = 3
    FAILED = 4


class DownloadDataBase(IDBase):
    vid: str = SQLField(title="該集ID", description="網站代號-ID-集次",
                        unique=True, nullable=False)
    aid: str = SQLField(title="該部動畫ID", description="網站代號-ID", nullable=False)
    episode: str = SQLField(title="集次", description="動畫集次", nullable=False)
    download_status: int - \
        SQLField(0, title="下載狀態", description="當前下載狀態",
                 ge=0, le=4, nullable=False)
    download_path: Optional[str] = SQLField(
        None, title="下載位置", description="動畫下載位置", nullable=True)
    download_timestamp: int = SQLField(
        0, title="下載時間", description="動畫下載時間", nullable=False)


class DownloadData(DownloadDataBase, table=True):
    __tablename__ = "DownloadData"
