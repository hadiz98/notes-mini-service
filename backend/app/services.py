from sqlalchemy.orm import Session
from typing import List, Optional
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

# Delete a note
def delete_note(db: Session, note_id: int) -> bool:
    db_note = db.query(models.Note).filter(models.Note.id == note_id).first()
    if not db_note:
        return False
    db.delete(db_note)
    db.commit()
    return True

# Update a note
def update_note(db: Session, note_id: int, note_update: schemas.NoteUpdate) -> Optional[models.Note]:
    db_note = db.query(models.Note).filter(models.Note.id == note_id).first()
    if not db_note:
        return None  # note not found

    # Update only provided fields
    if note_update.title is not None:
        db_note.title = note_update.title
    if note_update.content is not None:
        db_note.content = note_update.content
    if note_update.done is not None:
        db_note.done = note_update.done

    db.commit()
    db.refresh(db_note)
    return db_note
