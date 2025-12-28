from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

# HA add-ons persist data in the /data directory
DATA_DIR = os.environ.get("DATA_DIR", "/data")
os.makedirs(DATA_DIR, exist_ok=True)

# SQLite database
DATABASE_URL = f"sqlite:///{DATA_DIR}/storage.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# SQLAlchemy model base class
Base = declarative_base()

# Dependency to get a database session
def get_db():
    """Dependency for FastAPI routes to get a db session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()