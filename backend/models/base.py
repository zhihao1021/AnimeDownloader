from typing import Optional

from sqlmodel import Field as SQLField, SQLModel


class IDBase(SQLModel):
    id: Optional[int] = SQLField(
        None, primary_key=True, unique=True, description="ID")
