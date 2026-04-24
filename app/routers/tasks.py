from fastapi import APIRouter, Depends, HTTPException,Query
from sqlalchemy.orm import Session
from database import get_db
from app.models.task import Task
from app.schemas.task import TaskCreate,TaskOut,TaskUpdate,PaginatedTasks
from app.core.deps import get_current_user
import math

router = APIRouter(prefix="/tasks", tags=["Tasks"])

@router.post("/",response_model=TaskOut)
def create_task(
    task:TaskCreate, db:Session =Depends(get_db),user = Depends(get_current_user)
):
    new_task = Task(**task.dict(), user_id=user.id)
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task

@router.get("/{id}",response_model=TaskOut)
def get_task(
    id: int,
    db: Session = Depends(get_db), 
    user=Depends(get_current_user)):

    task = db.query(Task).filter(
        Task.id == id, Task.user_id == user.id
        ).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    return task

@router.put("/{id}", response_model=TaskOut)
def update_task(
    id: int,
    task: TaskUpdate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    db_task = db.query(Task).filter(
        Task.id == id,
        Task.user_id == user.id
    ).first()

    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")

    update_data = task.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_task, key, value)

    db.commit()
    db.refresh(db_task)

    return db_task

@router.delete("/{id}")
def delete_task(
    id: int, 
    db: Session = Depends(get_db), 
    user=Depends(get_current_user)):

    task = db.query(Task).filter(
        Task.id == id, Task.user_id == user.id
        ).first()

    if not task:
        raise HTTPException(404, "Task not found")

    db.delete(task)
    db.commit()
    return {"msg": "Task Deleted Succesfully"}    


@router.get("/",response_model=PaginatedTasks)
def get_tasks(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    status: str = None,
    priority: str = None,
    search: str = None,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    query = db.query(Task).filter(Task.user_id == user.id)

    if status:
        query = query.filter(Task.status == status)
    if priority:
        query = query.filter(Task.priority == priority)
    if search:
        query = query.filter(Task.title.contains(search))

    total = query.count()
    offset = (page - 1) * limit

    tasks = query.offset(offset).limit(limit).all()

    return {
        "page": page,
        "limit": limit,
        "total_tasks": total,
        "total_pages": math.ceil(total / limit) if limit else 1,
        "data": tasks
    }