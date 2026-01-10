# init_db.py
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Note  # Your models here
from datetime import datetime

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./notes.db")

# SQLite engine
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db(drop: bool = False, seed: bool = False):
    #Initialize the database.
    # drop (bool): If True, drop all existing tables first.
    #seed (bool): If True, insert some example seed data.
    
    if drop:
        print("Dropping all tables...")
        Base.metadata.drop_all(bind=engine)

    print("Creating tables...")
    Base.metadata.create_all(bind=engine)

    if seed:
        print("Inserting seed data...")
        db = SessionLocal()
        try:
            notes = [
                Note(title="Buy groceries", content="Milk, Eggs, Bread", done=False, created_at=datetime.now()),
                Note(title="Read book", content="Finish reading Streamlit docs", done=False, created_at=datetime.now()),
                Note(title="Call Alice", content="Discuss project", done=True, created_at=datetime.now()),
            ]
            db.add_all(notes)
            db.commit()
            print(f"{len(notes)} seed notes added.")
        finally:
            db.close()


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Initialize or reset the database.")
    parser.add_argument("--drop", action="store_true", help="Drop existing tables before creating.")
    parser.add_argument("--seed", action="store_true", help="Add seed data after creating tables.")
    args = parser.parse_args()

    # Create DB file if not exists
    if not os.path.exists("notes.db"):
        open("notes.db", "a").close()
        print("Created SQLite database file: notes.db")

    init_db(drop=args.drop, seed=args.seed)
    print("Database initialization complete.")
