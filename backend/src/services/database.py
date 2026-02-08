from sqlmodel import create_engine, Session
from typing import Generator, Optional
from contextlib import contextmanager
from ..config.settings import settings


def get_database_url() -> str:
    """Get the database URL with proper dialect for psycopg3"""
    url = settings.database_url
    # Use postgresql+psycopg dialect for psycopg3 compatibility
    if url.startswith("postgresql://"):
        url = url.replace("postgresql://", "postgresql+psycopg://", 1)
    return url

# Lazy engine creation
_engine: Optional[object] = None


def get_engine():
    """Get or create the database engine (lazy initialization)"""
    global _engine
    if _engine is None:
        _engine = create_engine(
            get_database_url(),
            echo=False,  # Set to True to see SQL queries in logs
            pool_size=3,
            max_overflow=5,
            pool_pre_ping=True,  # Verify connections before use
            pool_recycle=300,    # Recycle connections after 5 minutes
            connect_args={
                "connect_timeout": 30,  # Connection timeout in seconds
            }
        )
    return _engine


# Backward compatibility
@property
def engine():
    return get_engine()


def get_session() -> Generator[Session, None, None]:
    """
    Get a database session for dependency injection
    """
    with Session(get_engine()) as session:
        yield session


@contextmanager
def get_db_session():
    """
    Context manager for database sessions
    """
    session = Session(get_engine())
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def create_db_and_tables():
    """
    Create database tables - call this on startup
    """
    from ..models.task import Task
    from ..models.user import User
    from sqlmodel import SQLModel

    # Create all tables
    SQLModel.metadata.create_all(get_engine())
    print("Database tables created successfully!")

    SQLModel.metadata.create_all(engine)