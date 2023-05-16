from ..base import CURDBase

from aiosqlmodel import AsyncSession
from config import ENGINE
from models.anime import MyselfData
from schemas.anime import MyselfDataCreate, MyselfDataUpdate

from typing import Optional, Type

from sqlmodel import select


class CURDMyselfData(CURDBase[MyselfData, MyselfDataCreate, MyselfDataUpdate]):
    def __init__(self) -> None:
        super().__init__(MyselfData)

    async def get_by_url(
        self,
        url: str
    ) -> Optional[MyselfData]:
        if url is None:
            return None
        async with AsyncSession(ENGINE) as db_session:
            query_stat = select(self.model).where(self.model.url == url)
            result = await db_session.exec(query_stat)

            return result.first()

    async def get_by_tid(
        self,
        tid: str
    ) -> Optional[MyselfData]:
        if tid is None:
            return None
        async with AsyncSession(ENGINE) as db_session:
            query_stat = select(self.model).where(self.model.tid == tid)
            result = await db_session.exec(query_stat)

            return result.first()

    async def get_all_tid(
        self,
        finished: Optional[bool] = None
    ) -> list[str]:
        async with AsyncSession(ENGINE) as db_session:
            if finished is None:
                result = await db_session.exec(select(self.model.tid))
            else:
                result = await db_session.exec(select(self.model.tid).where(self.model.finished == finished))

            return result.all()
