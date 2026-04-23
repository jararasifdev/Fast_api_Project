from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Note(Base):
    __tablename__ = "notes"

    id = Column(Integer, primary_key=True)
    content = Column(String)
    task_id = Column(Integer, ForeignKey("tasks.id"))

    task = relationship("Task", back_populates="notes")