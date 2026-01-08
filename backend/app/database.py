from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Base

DATABASE_URL = "sqlite:///./notes.db"

# SQLite specification: check_same_thread=False
engine = create_engine(
    DATABASE_URL
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


def init_db() -> None:
    # Create all tables in the database
    Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        # Return database as yield , only used when needed!
        yield db
    finally:
        db.close()
