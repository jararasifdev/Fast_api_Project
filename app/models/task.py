from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
from app.models.task_tag import task_tags

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    description = Column(String)
    status = Column(String)
    priority = Column(String)
    due_date = Column(Date)
    created_at= Column(Date)
    user_id = Column(Integer, ForeignKey("users.id"))

    notes = relationship("Note", back_populates="task", cascade="all, delete")
    tags = relationship("Tag", secondary=task_tags, back_populates="tasks")
    user = relationship("User", back_populates="tasks")
