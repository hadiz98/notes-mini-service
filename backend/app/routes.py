from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app import services, schemas
from app.database import get_db

router = APIRouter(
    prefix="/notes",
    tags=["notes"]
)

# ---------- GET ALL NOTES ----------
@router.get(
    "",
    response_model=List[schemas.NoteResponse],
    summary="Get all notes",
    description="Retrieve a list of all notes stored in the database. Each note includes its ID, title, content, done status, and creation timestamp."
)
def read_notes(params: schemas.NoteQueryParams = Depends(), db: Session = Depends(get_db)):
    return services.get_notes(db , q= params.q , done = params.done)


# ---------- CREATE NOTE ----------
@router.post(
    "",
    response_model=schemas.NoteResponse,
    status_code=201,
    summary="Create a new note",
    description="Create a new note by providing a title, content, and optional done status (defaults to false)."
)
def create_note(note: schemas.NoteCreate, db: Session = Depends(get_db)):
    return services.create_note(db, note)


# ---------- DELETE NOTE ----------
@router.delete(
    "/{note_id}",
    status_code=204,
    summary="Delete a note",
    description="Delete a note by its ID. Returns 404 if the note does not exist."
)
def delete_note(note_id: int, db: Session = Depends(get_db)):
    deleted = services.delete_note(db, note_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Note not found")
    return


# ---------- UPDATE NOTE ----------
@router.put(
    "/{note_id}",
    response_model=schemas.NoteResponse,
    summary="Update a note",
    description="Partially update a note by its ID. Provide any fields to update (title, content, done). Fields not provided remain unchanged. Returns 404 if the note does not exist."
)
def update_note(note_id: int, note: schemas.NoteUpdate, db: Session = Depends(get_db)):
    updated_note = services.update_note(db, note_id, note)
    if not updated_note:
        raise HTTPException(status_code=404, detail="Note not found")
    return updated_note
