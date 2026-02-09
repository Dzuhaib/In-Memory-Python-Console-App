"""Task model for the todo application."""

from datetime import datetime
from enum import Enum
from typing import List, Optional

from sqlalchemy import Column, JSON
from sqlmodel import Field, SQLModel


class Priority(str, Enum):
    """Task priority levels."""
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class Task(SQLModel, table=True):
    """Task entity for the todo application.

    Attributes:
        id: Unique task identifier (auto-generated)
        title: Task description (required, 1-500 characters)
        completed: Whether the task is completed
        priority: Priority level (high/medium/low)
        tags: List of tag strings stored as JSON
        created_at: Timestamp when task was created
        updated_at: Timestamp when task was last modified
    """

    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(min_length=1, max_length=500)
    completed: bool = Field(default=False)
    priority: Priority = Field(default=Priority.MEDIUM)
    tags: List[str] = Field(default_factory=list, sa_column=Column(JSON))
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        use_enum_values = True
