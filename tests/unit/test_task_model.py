"""Unit tests for Task model."""

import pytest

from src.models.task import Task, Priority


class TestPriority:
    """Tests for Priority enum."""

    def test_priority_values(self):
        """Test priority enum values for sorting order."""
        assert Priority.HIGH.value == 1
        assert Priority.MEDIUM.value == 2
        assert Priority.LOW.value == 3

    def test_priority_from_string_valid(self):
        """Test converting valid strings to Priority."""
        assert Priority.from_string("high") == Priority.HIGH
        assert Priority.from_string("HIGH") == Priority.HIGH
        assert Priority.from_string("medium") == Priority.MEDIUM
        assert Priority.from_string("low") == Priority.LOW
        assert Priority.from_string("  LOW  ") == Priority.LOW

    def test_priority_from_string_invalid(self):
        """Test that invalid strings raise ValueError."""
        with pytest.raises(ValueError, match="Invalid priority"):
            Priority.from_string("urgent")

        with pytest.raises(ValueError, match="Invalid priority"):
            Priority.from_string("")

    def test_priority_str(self):
        """Test string representation of Priority."""
        assert str(Priority.HIGH) == "high"
        assert str(Priority.MEDIUM) == "medium"
        assert str(Priority.LOW) == "low"


class TestTask:
    """Tests for Task dataclass."""

    def test_task_creation_minimal(self):
        """Test creating a task with minimal arguments."""
        task = Task(id=1, title="Buy groceries")

        assert task.id == 1
        assert task.title == "Buy groceries"
        assert task.completed is False
        assert task.priority == Priority.MEDIUM
        assert task.tags == []

    def test_task_creation_full(self):
        """Test creating a task with all arguments."""
        task = Task(
            id=1,
            title="Important task",
            completed=True,
            priority=Priority.HIGH,
            tags=["work", "urgent"]
        )

        assert task.id == 1
        assert task.title == "Important task"
        assert task.completed is True
        assert task.priority == Priority.HIGH
        assert task.tags == ["work", "urgent"]

    def test_task_title_whitespace_stripped(self):
        """Test that title whitespace is stripped."""
        task = Task(id=1, title="  Buy groceries  ")
        assert task.title == "Buy groceries"

    def test_task_empty_title_raises(self):
        """Test that empty title raises ValueError."""
        with pytest.raises(ValueError, match="Title cannot be empty"):
            Task(id=1, title="")

        with pytest.raises(ValueError, match="Title cannot be empty"):
            Task(id=1, title="   ")

    def test_task_invalid_id_raises(self):
        """Test that invalid ID raises ValueError."""
        with pytest.raises(ValueError, match="ID must be a positive integer"):
            Task(id=0, title="Test")

        with pytest.raises(ValueError, match="ID must be a positive integer"):
            Task(id=-1, title="Test")

    def test_task_tags_cleaned(self):
        """Test that tags are cleaned and deduplicated."""
        task = Task(id=1, title="Test", tags=["  work  ", "home", "work"])

        assert task.tags == ["work", "home"]

    def test_task_empty_tags_filtered(self):
        """Test that empty tags are filtered out."""
        task = Task(id=1, title="Test", tags=["work", "", "  ", "home"])

        assert task.tags == ["work", "home"]
