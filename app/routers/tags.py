from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from app.models.tag import Tag
from app.schemas.tag import TagCreate, TagOut

router = APIRouter(prefix="/tags", tags=["Tags"])


@router.post("/", response_model=TagOut)
def create_tag(
    tag: TagCreate, 
    db: Session = Depends(get_db)):

    new_tag = Tag(name=tag.name)
    db.add(new_tag)
    db.commit()
    db.refresh(new_tag) 
    return new_tag


@router.get("/", response_model=list[TagOut])
def get_tags(
    db: Session = Depends(get_db)):
    return db.query(Tag).all()