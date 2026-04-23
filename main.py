from fastapi import FastAPI
from database import Base, engine

from app.routers import auth, tasks, tags, notes

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Task & Notes Manager API")

app.include_router(auth.router)
app.include_router(tasks.router)
app.include_router(tags.router)
app.include_router(notes.router)