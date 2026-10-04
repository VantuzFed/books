from datetime import datetime
from pydantic import BaseModel, ConfigDict


class BookBase(BaseModel):
    title: str
    author: str
    description: str | None = None


class BookCreate(BookBase):
    pass


class BookUpdate(BaseModel):
    title: str | None = None
    author: str | None = None
    description: str | None = None


class BookResponse(BookBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
