"""Database connection and session management."""

import sys
from typing import Generator

from sqlmodel import Session, SQLModel, create_engine

from config import settings


def get_database_url() -> str:
    """Get and normalize database URL.

    Railway/Heroku use postgres:// but SQLAlchemy requires postgresql://
    """
    url = settings.database_url
    if url.startswith("postgres://"):
        url = url.replace("postgres://", "postgresql://", 1)
    return url


def create_db_engine():
    """Create database engine with proper configuration."""
    db_url = get_database_url()

    connect_args = {}
    if db_url.startswith("sqlite"):
        connect_args = {"check_same_thread": False}

    # For PostgreSQL, add connection pool settings for production
    pool_settings = {}
    if db_url.startswith("postgresql"):
        pool_settings = {
            "pool_size": 5,
            "max_overflow": 10,
            "pool_pre_ping": True,  # Verify connections before use
        }

    return create_engine(
        db_url,
        echo=settings.log_level == "DEBUG",
        connect_args=connect_args,
        **pool_settings,
    )


# Create engine - will be initialized on first import
engine = None


def get_engine():
    """Get or create database engine."""
    global engine
    if engine is None:
        engine = create_db_engine()
    return engine


def run_migrations(db_engine) -> None:
    """Ensure the task table matches the current model schema.

    The table may have been created in Phase 1 with a different schema
    (e.g. 'is_complete' instead of 'completed'). If the schema doesn't
    match, drop and recreate the table.
    """
    from sqlalchemy import text, inspect

    try:
        inspector = inspect(db_engine)
        if "task" in inspector.get_table_names():
            columns = {col["name"] for col in inspector.get_columns("task")}
            expected = {"id", "title", "completed", "priority", "tags", "created_at", "updated_at"}

            # If schema doesn't match (e.g. has 'is_complete' from Phase 1), recreate
            if "is_complete" in columns or not expected.issubset(columns):
                print("Migration: Table schema mismatch detected, recreating task table", file=sys.stderr)
                with db_engine.begin() as conn:
                    conn.execute(text("DROP TABLE IF EXISTS task CASCADE"))
                print("Migration: Old task table dropped, will be recreated by create_all", file=sys.stderr)
            else:
                print("Migration: Task table schema is up to date", file=sys.stderr)
    except Exception as e:
        print(f"Migration warning: {e}", file=sys.stderr)


def create_db_and_tables() -> None:
    """Create all database tables and run migrations.

    Call this function on application startup to ensure
    all SQLModel tables exist in the database.
    """
    try:
        db_engine = get_engine()
        run_migrations(db_engine)
        SQLModel.metadata.create_all(db_engine)
    except Exception as e:
        print(f"ERROR: Failed to create database tables: {e}", file=sys.stderr)
        raise


def get_session() -> Generator[Session, None, None]:
    """Get a database session.

    Yields a SQLModel Session that automatically handles
    commit/rollback on context exit.

    Yields:
        Session: Database session for executing queries
    """
    db_engine = get_engine()
    with Session(db_engine) as session:
        yield session
