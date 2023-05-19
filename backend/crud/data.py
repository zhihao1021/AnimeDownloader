from models.data import Data
from .base import CRUDBase

from aiosqlmodel import AsyncSession
from config import ENGINE
from models import Data
from schemas import DataCreate, DataUpdate

from typing import Any, Optional, Union

from sqlmodel import select


class CRUDData(CRUDBase[Data, DataCreate, DataUpdate]):
    def __init__(self) -> None:
        super().__init__(Data)

    async def get_by_tag(
        self,
        tag: str
    ) -> Optional[Data]:
        if tag is None:
            return None
        async with AsyncSession(ENGINE) as db_session:
            query_stat = select(self.model).where(self.model.tag == tag)
            result = await db_session.exec(query_stat)
            

            return result.first()
