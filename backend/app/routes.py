from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app import services, schemas
from app.database import get_db

router = APIRouter(
    prefix="/notes",
    tags=["notes"]
)

# GET all notes
@router.get("", response_model=List[schemas.NoteResponse])
def read_notes(db: Session = Depends(get_db)):
    return services.get_notes(db)

# CREATE a new note
@router.post("", response_model=schemas.NoteResponse, status_code=201)
def create_note(note: schemas.NoteCreate, db: Session = Depends(get_db)):
    return services.create_note(db, note)
