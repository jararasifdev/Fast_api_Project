from pydantic import BaseModel

class NoteCreate(BaseModel):
    content: str

class NoteOut(BaseModel):
    content: str

    class Config:
        from_attributes = True    