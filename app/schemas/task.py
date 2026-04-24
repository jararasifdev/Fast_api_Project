from datetime import datetime
from pydantic import BaseModel,Field
from datetime import date

from typing import Optional,List


from enum import Enum

class StatusEnum(str, Enum):
    todo = "todo"
    in_progress = "in_progress"
    done = "done"

class PriorityEnum(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"

class TaskUpdate(BaseModel):
    title: str = Field(min_length=1,max_length=200)
    description: str = Field(min_length=1)
    status: Optional[StatusEnum] = None
    priority: Optional[PriorityEnum] = None
    due_date: Optional[date] = None

class TaskCreate(BaseModel):
    title: str = Field(min_length=1,max_length=200)
    description: str = Field(min_length=1)
    status: StatusEnum 
    priority: PriorityEnum
    due_date: date

class TaskOut(BaseModel):
    id: int
    title: str
    description: str
    status: Optional[StatusEnum] = None
    priority: Optional[PriorityEnum]=None
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