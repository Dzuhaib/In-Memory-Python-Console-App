"""Task model for the todo application."""

# Task T005: Add RecurrenceRule enum to backend/src/models/task.py
# Task T006: Add 4 nullable fields (due_at, remind_at, recurrence_rule, recurrence_interval) to Task model

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


class RecurrenceRule(str, Enum):
    """Task recurrence patterns."""
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    EVERY_N_DAYS = "every_N_days"


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
        due_at: Optional due date for the task
        remind_at: Optional reminder time (must be <= due_at if both set)
        recurrence_rule: Optional recurrence pattern
        recurrence_interval: Optional custom interval in days (for every_N_days rule)
    """

    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(min_length=1, max_length=500)
    completed: bool = Field(default=False)
    priority: Priority = Field(default=Priority.MEDIUM)
    tags: List[str] = Field(default_factory=list, sa_column=Column(JSON))
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Phase 5 extensions (T006)
    due_at: Optional[datetime] = Field(default=None)
    remind_at: Optional[datetime] = Field(default=None)
    recurrence_rule: Optional[RecurrenceRule] = Field(default=None)
    recurrence_interval: Optional[int] = Field(default=None)

    class Config:
        use_enum_values = True
