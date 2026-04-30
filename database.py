from sqlalchemy import create_engine,text
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.exc import OperationalError
from fastapi import HTTPException
from dotenv import load_dotenv
import os
import logging

logger = logging.getLogger(__name__)
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

try:
    engine = create_engine(
        DATABASE_URL,
        pool_pre_ping=True,  # Test connections before using them
        pool_recycle=300,    # Recycle connections after 5 minutes
        echo=False           # Set to True for debugging
    )

    # Test the connection
    with engine.connect() as conn:
        logger.info("Database connection successful")

except OperationalError as e:
    logger.error(f"Database connection failed: {e}")
    raise RuntimeError("Unable to connect to database. Please check your DATABASE_URL.")

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        db.execute(text("SELECT 1"))
        yield db
    except OperationalError as e:
        logger.error(f"Database session error: {e}")
        db.rollback()
        raise HTTPException(status_code=503, detail="Database temporarily unavailable")
    except Exception as e:
        logger.error(f"Unexpected database error: {e}")
        db.rollback()
        raise
    finally:
        db.close()