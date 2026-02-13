"""Pydantic schemas for task API requests and responses."""

# Task T007: Update CreateTaskRequest with new fields
# Task T008: Update UpdateTaskRequest with new fields
# Task T009: Add Pydantic model validators
# Task T040: Define TaskEvent Pydantic model

from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field, field_validator, model_validator

from models.task import Priority, RecurrenceRule


class CreateTaskRequest(BaseModel):
    """Schema for creating a new task."""

    title: str = Field(min_length=1, max_length=500, description="Task description")
    priority: Priority = Field(default=Priority.MEDIUM, description="Priority level")
    tags: List[str] = Field(default_factory=list, description="Initial tags")

    # Phase 5 extensions (T007)
    due_at: Optional[datetime] = Field(default=None, description="Optional due date")
    remind_at: Optional[datetime] = Field(default=None, description="Optional reminder time")
    recurrence_rule: Optional[RecurrenceRule] = Field(default=None, description="Optional recurrence pattern")
    recurrence_interval: Optional[int] = Field(default=None, description="Custom interval for every_N_days rule")

    @model_validator(mode='after')
    def validate_dates_and_recurrence(self):
        """Validate date and recurrence constraints (T009)."""
        now = datetime.utcnow()

        # Validate remind_at <= due_at when both are set
        if self.remind_at and self.due_at:
            if self.remind_at > self.due_at:
                raise ValueError("remind_at must be <= due_at when both are set")

        # Validate recurrence_interval >= 1 when rule is every_N_days
        if self.recurrence_rule == RecurrenceRule.EVERY_N_DAYS:
            if not self.recurrence_interval or self.recurrence_interval < 1:
                raise ValueError("recurrence_interval must be >= 1 when recurrence_rule is every_N_days")

        # Validate remind_at is in the future at creation
        if self.remind_at and self.remind_at <= now:
            raise ValueError("remind_at must be in the future")

        return self


class UpdateTaskRequest(BaseModel):
    """Schema for updating an existing task."""

    title: Optional[str] = Field(
        default=None, min_length=1, max_length=500, description="New task description"
    )
    priority: Optional[Priority] = Field(default=None, description="New priority level")

    # Phase 5 extensions (T008)
    due_at: Optional[datetime] = Field(default=None, description="New due date")
    remind_at: Optional[datetime] = Field(default=None, description="New reminder time")
    recurrence_rule: Optional[RecurrenceRule] = Field(default=None, description="New recurrence pattern")
    recurrence_interval: Optional[int] = Field(default=None, description="New custom interval")

    @model_validator(mode='after')
    def validate_dates_and_recurrence(self):
        """Validate date and recurrence constraints (T009)."""
        now = datetime.utcnow()

        # Validate remind_at <= due_at when both are set
        if self.remind_at and self.due_at:
            if self.remind_at > self.due_at:
                raise ValueError("remind_at must be <= due_at when both are set")

        # Validate recurrence_interval >= 1 when rule is every_N_days
        if self.recurrence_rule == RecurrenceRule.EVERY_N_DAYS:
            if not self.recurrence_interval or self.recurrence_interval < 1:
                raise ValueError("recurrence_interval must be >= 1 when recurrence_rule is every_N_days")

        # Validate remind_at is in the future when updating
        if self.remind_at and self.remind_at <= now:
            raise ValueError("remind_at must be in the future")

        return self


class AddTagRequest(BaseModel):
    """Schema for adding a tag to a task."""

    tag: str = Field(min_length=1, max_length=50, description="Tag to add")


class TaskEvent(BaseModel):
    """Schema for task events published to Kafka via Dapr Pub/Sub.

    Task T040: TaskEvent model with event_id UUID, event_type, task_id,
    task_snapshot dict, actor str, timestamp datetime, metadata optional dict.
    """

    event_id: str = Field(description="Unique event identifier (UUID)")
    event_type: str = Field(
        description="Event type: task.created, task.updated, task.completed, task.deleted, reminder.due"
    )
    task_id: int = Field(description="Task identifier")
    task_snapshot: Dict[str, Any] = Field(description="Full task state at the time of the event")
    actor: str = Field(description="Who triggered the event: user or system")
    timestamp: datetime = Field(description="When the event occurred (ISO 8601)")
    metadata: Optional[Dict[str, Any]] = Field(default=None, description="Additional context")
