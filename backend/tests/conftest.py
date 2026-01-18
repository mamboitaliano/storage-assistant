import pytest, os, sys
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

# Ensure backend package is on path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.database import Base, get_db
from app.models import Floor, Room
from app.main import app

# shared in-memory SQLite test engine with FK support
engine = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

@event.listens_for(engine, "connect")
def _set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def db_session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture(scope="function")
def client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


# Floor fixture ----------------------------------------------------------------
@pytest.fixture(scope="function")
def floor(db_session):
    f = Floor(name="Test Floor", floor_number=1)
    db_session.add(f)
    db_session.commit()
    return f

# Room fixture ----------------------------------------------------------------
@pytest.fixture(scope="function")
def room(db_session, floor):
    room = Room(name="Test room", floor_id=floor.id)
    db_session.add(room)
    db_session.commit()
    return room
