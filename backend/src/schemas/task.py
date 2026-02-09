"""Pydantic schemas for task API requests and responses."""

from typing import List, Optional

from pydantic import BaseModel, Field

from models.task import Priority


class CreateTaskRequest(BaseModel):
    """Schema for creating a new task."""

    title: str = Field(min_length=1, max_length=500, description="Task description")
    priority: Priority = Field(default=Priority.MEDIUM, description="Priority level")
    tags: List[str] = Field(default_factory=list, description="Initial tags")


class UpdateTaskRequest(BaseModel):
    """Schema for updating an existing task."""

    title: Optional[str] = Field(
        default=None, min_length=1, max_length=500, description="New task description"
    )
    priority: Optional[Priority] = Field(default=None, description="New priority level")


class AddTagRequest(BaseModel):
    """Schema for adding a tag to a task."""

    tag: str = Field(min_length=1, max_length=50, description="Tag to add")
