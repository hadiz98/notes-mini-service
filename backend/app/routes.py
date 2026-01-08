from fastapi import APIRouter, Depends, HTTPException
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


# Delete a note
@router.delete("/{note_id}", status_code=204)
def delete_note(note_id: int, db: Session = Depends(get_db)):
    deleted = services.delete_note(db, note_id)
    if not deleted:
        raise HTTPException(status_code=404 , detail="Note not found")
    

@router.put("/{note_id}", response_model=schemas.NoteResponse)
def update_note_route(note_id: int, note: schemas.NoteUpdate, db: Session = Depends(get_db)):
    updated_note = services.update_note(db, note_id, note)
    if not updated_note:
        raise HTTPException(status_code=404, detail="Note not found")
    return updated_note