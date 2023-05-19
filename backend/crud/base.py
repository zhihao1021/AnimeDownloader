from aiosqlmodel import AsyncSession
from config import ENGINE
from models.base import IDBase

from asyncio import create_task, gather
from typing import Any, Generic, Optional, Type, TypeVar, Union

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.exc import IntegrityError
from sqlmodel import select
from sqlmodel.sql.base import Executable
from sqlmodel.sql.expression import Select, SelectOfScalar

ModelType = TypeVar("ModelType", bound=IDBase)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)
SchemaType = TypeVar("SchemaType", bound=BaseModel)

_TSelectParam = TypeVar("_TSelectParam")


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]) -> None:
        self.model = model

    async def get(self, id: int) -> Optional[ModelType]:
        async with AsyncSession(ENGINE) as db_session:
            query_stat = select(self.model).where(self.model.id == id)
            result = await db_session.exec(query_stat)

            return result.first()

    async def get_by_ids(self, ids: list[int]) -> Optional[list[ModelType]]:
        async with AsyncSession(ENGINE) as db_session:
            query_stat = select(self.model).where(self.model.id.in_(ids))
            result = await db_session.exec(query_stat)

            return result.all()

    async def get_range(
        self,
        statement: Union[
            Select[_TSelectParam],
            SelectOfScalar[_TSelectParam],
            Executable[_TSelectParam]
        ],
        start: Optional[int] = None,
        length: Optional[int] = None
    ) -> Optional[list[ModelType]]:
        async with AsyncSession(ENGINE) as db_session:
            query_stat = statement
            query_stat = query_stat.offset(start) if start else query_stat
            query_stat = query_stat.limit(length) if length else query_stat

            result = await db_session.exec(query_stat)
            return result.all()

    async def create(
        self,
        obj: CreateSchemaType,
    ) -> ModelType:
        async with AsyncSession(ENGINE) as db_session:
            obj = self.model.from_orm(obj)

            try:
                db_session.add(obj)
                await db_session.commit()
            except IntegrityError:
                await db_session.rollback()
            await db_session.refresh(obj)
            return obj

    async def create_list(
        self,
        obj_list: list[CreateSchemaType]
    ) -> list[ModelType]:
        async with AsyncSession(ENGINE) as db_session:
            obj_list = list(map(lambda obj: self.model.from_orm(obj), obj_list))

            # try:
            db_session.add_all(obj_list)
            await db_session.commit()
            # except IntegrityError:
                # await db_session.rollback()

            results = await gather(*map(
                db_session.refresh,
                obj_list
            ))
            return results

    async def update(
        self,
        obj: ModelType,
        obj_update: Union[UpdateSchemaType, dict[str, Any], ModelType],
    ) -> ModelType:
        async with AsyncSession(ENGINE) as db_session:
            obj_data = jsonable_encoder(obj)

            if isinstance(obj_update, dict):
                update_data = obj_update
            else:
                update_data = obj_update.dict(
                    exclude_unset=True
                )  # This tells Pydantic to not include the values that were not sent

            for field in set(update_data) & set(obj_data):
                setattr(obj, field, update_data[field])

            db_session.add(obj)
            await db_session.commit()
            await db_session.refresh(obj)
            return obj

    async def delete(
        self,
        id: int,
    ) -> ModelType:
        async with AsyncSession(ENGINE) as db_session:
            obj = await self.get(id)

            await db_session.delete(obj)
            await db_session.commit()

            return obj
