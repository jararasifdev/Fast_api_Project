from pydantic import BaseModel
from datetime import date

class TaskCreate(BaseModel):
    title: str
    description: str
    status: str
    priority: str
    due_date: date
    created_at:date

class TaskOut(BaseModel):
    id: int
    title: str
    status: str

    class Config:
        from_attributes = True