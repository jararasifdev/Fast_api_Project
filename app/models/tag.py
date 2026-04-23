from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from database import Base
from app.models.task_tag import task_tags

class Tag(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True)
    name = Column(String)

    tasks = relationship("Task", secondary=task_tags, back_populates="tags")