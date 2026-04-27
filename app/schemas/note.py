from pydantic import BaseModel

class NoteCreate(BaseModel):
    content: str

class NoteOut(BaseModel):
    id: int
    content: str
    task_id: int

    class Config:
        from_attributes = True    