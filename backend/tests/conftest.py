import pytest
from sqlmodel import create_engine
from sqlmodel.pool import StaticPool
from contextlib import contextmanager
from backend.src.main import create_app
from backend.src.services.database import get_session, engine
from backend.src.models.task import Task
from sqlmodel import SQLModel
from fastapi.testclient import TestClient


@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    SQLModel.metadata.create_all(bind=engine)
    with TestingSessionLocal(engine) as session:
        yield session


@pytest.fixture(name="client")
def client_fixture(session):
    def get_session_override():
        return session

    app = create_app()
    app.dependency_overrides[get_session] = get_session_override

    client = TestClient(app)
    yield client

    app.dependency_overrides.clear()


class TestingSessionLocal:
    def __init__(self, engine):
        self.engine = engine

    def __enter__(self):
        self.session = next(get_session())
        # Override the session creation to use our test engine
        return self.session

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.close()


# Create an override for testing
def override_get_session():
    try:
        engine = create_engine(
            "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
        )
        SQLModel.metadata.create_all(bind=engine)
        with next(get_session()) as session:
            yield session
    except Exception:
        pass