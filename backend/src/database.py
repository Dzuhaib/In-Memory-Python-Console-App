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
    """Add any missing columns to existing tables.

    SQLModel's create_all only creates new tables, it won't alter existing ones.
    This handles schema evolution for columns added in later phases.
    """
    from sqlalchemy import text, inspect

    try:
        inspector = inspect(db_engine)
        if "task" in inspector.get_table_names():
            columns = {col["name"] for col in inspector.get_columns("task")}
            with db_engine.begin() as conn:
                if "completed" not in columns:
                    print("Migration: Adding 'completed' column to task table", file=sys.stderr)
                    conn.execute(text("ALTER TABLE task ADD COLUMN completed BOOLEAN DEFAULT FALSE"))
                if "tags" not in columns:
                    print("Migration: Adding 'tags' column to task table", file=sys.stderr)
                    conn.execute(text("ALTER TABLE task ADD COLUMN tags JSON DEFAULT '[]'"))
                if "created_at" not in columns:
                    print("Migration: Adding 'created_at' column to task table", file=sys.stderr)
                    conn.execute(text("ALTER TABLE task ADD COLUMN created_at TIMESTAMP DEFAULT NOW()"))
                if "updated_at" not in columns:
                    print("Migration: Adding 'updated_at' column to task table", file=sys.stderr)
                    conn.execute(text("ALTER TABLE task ADD COLUMN updated_at TIMESTAMP DEFAULT NOW()"))
            print("Migrations complete", file=sys.stderr)
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
