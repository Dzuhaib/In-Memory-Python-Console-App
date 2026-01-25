"""Database connection and session management."""

from typing import Generator

from sqlmodel import Session, SQLModel, create_engine

from config import settings

# Create engine with appropriate settings based on database type
connect_args = {}
if settings.database_url.startswith("sqlite"):
    # SQLite needs this for use with FastAPI's async workers
    connect_args = {"check_same_thread": False}

engine = create_engine(
    settings.database_url,
    echo=settings.log_level == "DEBUG",
    connect_args=connect_args,
)


def create_db_and_tables() -> None:
    """Create all database tables.

    Call this function on application startup to ensure
    all SQLModel tables exist in the database.
    """
    SQLModel.metadata.create_all(engine)


def get_session() -> Generator[Session, None, None]:
    """Get a database session.

    Yields a SQLModel Session that automatically handles
    commit/rollback on context exit.

    Yields:
        Session: Database session for executing queries
    """
    with Session(engine) as session:
        yield session
