from datetime import datetime
from pydantic import BaseModel
from datetime import date

from typing import Optional,List

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    priority: Optional[str] = None
    due_date: Optional[date] = None

class TaskCreate(BaseModel):
    title: str
    description: str
    status: str
    priority: str
    due_date: date

class TaskOut(BaseModel):
    id: int
    title: str
    description: str
    status: str
    priority: str
    due_date: date
    created_at: datetime

    class Config:
        from_attributes = True

class PaginatedTasks(BaseModel):
    page: int
    limit: int
    total_tasks: int
    total_pages: int
    data: List[TaskOut]        