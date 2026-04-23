from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from app.models.note import Note
from app.schemas.note import NoteCreate,NoteOut
from app.core.deps import get_current_user
from app.models.task import Task

router = APIRouter(tags=["Notes"])

@router.post("/tasks/{task_id}/notes",response_model=NoteOut)
def add_note(
    task_id: int,
    note: NoteCreate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    task = db.query(Task).filter(
        Task.id == task_id,
        Task.user_id == user.id
    ).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    new_note = Note(task_id=task_id, content=note.content)
    db.add(new_note)
    db.commit()
    db.refresh(new_note)

    return new_note

@router.get("/tasks/{task_id}/notes",response_model=list[NoteOut])
def get_notes(
    task_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    task = db.query(Task).filter(
        Task.id == task_id,
        Task.user_id == user.id
    ).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    return db.query(Note).filter(Note.task_id == task_id).all()