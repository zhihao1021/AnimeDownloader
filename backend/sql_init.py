from config import ENGINE

from os import getenv

from sqlmodel import SQLModel

import models
import models.anime


async def sql_init():
    DEBUG = getenv("DEBUG", "False").lower() == "true"
    async with ENGINE.begin() as conn:
        if DEBUG:
            await conn.run_sync(SQLModel.metadata.drop_all)
        await conn.run_sync(SQLModel.metadata.create_all)
