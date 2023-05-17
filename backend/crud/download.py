from .base import CRUDBase

from aiosqlmodel import AsyncSession
from config import ENGINE
from models import DownloadData
from schemas import DownloadDataCreate, DownloadDataUpdate

from typing import Optional

from sqlmodel import select


class CRUDDownloadData(CRUDBase[DownloadData, DownloadDataCreate, DownloadDataUpdate]):
    def __init__(self) -> None:
        super().__init__(DownloadData)

    async def get_by_vid(
        self,
        vid: str
    ) -> Optional[DownloadData]:
        if vid is None:
            return None
        async with AsyncSession(ENGINE) as db_session:
            query_stat = select(self.model).where(self.model.vid == vid)
            result = await db_session.exec(query_stat)

            return result.first()

    async def get_by_aid(
        self,
        aid: str
    ) -> list[DownloadData]:
        if aid is None:
            return []
        async with AsyncSession(ENGINE) as db_session:
            query_stat = select(self.model).where(self.model.aid == aid)
            result = await db_session.exec(query_stat)

            return result.all()

    async def get_by_download_status(
        self,
        download_status: int
    ) -> list[DownloadData]:
        if download_status is None:
            return []
        async with AsyncSession(ENGINE) as db_session:
            query_stat = select(self.model).where(
                self.model.download_status == download_status)
            result = await db_session.exec(query_stat)

            return result.all()
