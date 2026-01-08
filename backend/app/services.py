from sqlalchemy.orm import Session
from typing import List
from app import models, schemas

# Create a note
def create_note(db: Session, note: schemas.NoteCreate) -> models.Note:
    db_note = models.Note(
        title=note.title,
        content=note.content,
        done=note.done,
    )
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return db_note

# Get all notes
def get_notes(db: Session) -> List[models.Note]:
    return db.query(models.Note).order_by(models.Note.created_at.desc()).all()
