from pydantic import BaseModel

class TagCreate(BaseModel):
    name: str

class TagOut(BaseModel):
    name: str

    class Config:
        from_attributes = True    