from pydantic import BaseModel, Field
from datetime import datetime

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
