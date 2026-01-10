from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class NoteCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    content: str = Field(..., min_length=1)
    done: bool = False

class NoteResponse(BaseModel):
    id: int
    title: str
    content: str
    done: bool
    created_at: datetime

    class Config:
        orm_mode = True


class NoteUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    content: Optional[str] = Field(None, min_length=1)
    done: Optional[bool] = None


class NoteQueryParams(BaseModel):
    q: Optional[str] = None        # text search
    done: Optional[bool] = None    # filter by done status