"""Unit tests for Task model."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

import pytest
from pydantic import ValidationError

from models.task import Priority, Task


class TestTaskModel:
    """Tests for Task model creation and validation."""

    def test_create_task_with_defaults(self):
        """Test creating a task with default values."""
        task = Task(title="Test task")
        assert task.title == "Test task"
        assert task.completed is False
        assert task.priority == Priority.MEDIUM
        assert task.tags == []

    def test_create_task_with_all_fields(self):
        """Test creating a task with all fields specified."""
        task = Task(
            title="Full task",
            completed=True,
            priority=Priority.HIGH,
            tags=["work", "urgent"],
        )
        assert task.title == "Full task"
        assert task.completed is True
        assert task.priority == Priority.HIGH
        assert task.tags == ["work", "urgent"]

    def test_task_priority_enum(self):
        """Test that priority enum values are correct."""
        assert Priority.HIGH.value == "high"
        assert Priority.MEDIUM.value == "medium"
        assert Priority.LOW.value == "low"

    def test_create_task_with_different_priorities(self):
        """Test creating tasks with different priority levels."""
        high_task = Task(title="High priority", priority=Priority.HIGH)
        medium_task = Task(title="Medium priority", priority=Priority.MEDIUM)
        low_task = Task(title="Low priority", priority=Priority.LOW)

        assert high_task.priority == Priority.HIGH
        assert medium_task.priority == Priority.MEDIUM
        assert low_task.priority == Priority.LOW

    def test_task_with_empty_tags(self):
        """Test that empty tags list is valid."""
        task = Task(title="No tags")
        assert task.tags == []

    def test_task_with_multiple_tags(self):
        """Test task with multiple tags."""
        task = Task(title="Tagged task", tags=["tag1", "tag2", "tag3"])
        assert len(task.tags) == 3
        assert "tag1" in task.tags
        assert "tag2" in task.tags
        assert "tag3" in task.tags

    def test_task_timestamps_auto_set(self):
        """Test that timestamps are automatically set."""
        task = Task(title="Timestamp test")
        assert task.created_at is not None
        assert task.updated_at is not None

    def test_task_title_required(self):
        """Test that title is required."""
        # SQLModel with table=True validates differently - check if model_validate raises
        with pytest.raises(ValidationError):
            Task.model_validate({})

    def test_task_title_min_length(self):
        """Test title minimum length validation."""
        # Empty string should fail validation
        with pytest.raises(ValidationError):
            Task.model_validate({"title": ""})

    def test_task_title_max_length(self):
        """Test title maximum length validation."""
        # Title over 500 chars should fail validation
        long_title = "x" * 501
        with pytest.raises(ValidationError):
            Task.model_validate({"title": long_title})

    def test_task_valid_title_at_limits(self):
        """Test title at boundary lengths."""
        # Single character should work
        task_min = Task(title="x")
        assert task_min.title == "x"

        # 500 characters should work
        task_max = Task(title="x" * 500)
        assert len(task_max.title) == 500
