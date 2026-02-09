"""Task model and Priority enum for the todo application."""

from dataclasses import dataclass, field
from enum import IntEnum
from typing import List


class Priority(IntEnum):
    """Task priority levels with natural ordering for sorting."""
    HIGH = 1
    MEDIUM = 2
    LOW = 3

    @classmethod
    def from_string(cls, value: str) -> "Priority":
        """Convert string to Priority enum.

        Args:
            value: Priority string (case-insensitive)

        Returns:
            Priority enum value

        Raises:
            ValueError: If value is not a valid priority
        """
        value_upper = value.upper().strip()
        if value_upper == "HIGH":
            return cls.HIGH
        elif value_upper == "MEDIUM":
            return cls.MEDIUM
        elif value_upper == "LOW":
            return cls.LOW
        else:
            raise ValueError(
                f"Invalid priority: '{value}'. Must be high, medium, or low."
            )

    def __str__(self) -> str:
        """Return lowercase string representation."""
        return self.name.lower()


@dataclass
class Task:
    """Represents a todo task.

    Attributes:
        id: Unique sequential identifier
        title: Task description (non-empty)
        completed: Whether the task is done
        priority: Task importance level
        tags: List of category labels
    """
    id: int
    title: str
    completed: bool = False
    priority: Priority = Priority.MEDIUM
    tags: List[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        """Validate task fields after initialization."""
        # Validate title
        if not isinstance(self.title, str):
            raise ValueError("Title must be a string")

        self.title = self.title.strip()
        if not self.title:
            raise ValueError("Title cannot be empty")

        # Validate id
        if not isinstance(self.id, int) or self.id < 1:
            raise ValueError("ID must be a positive integer")

        # Validate priority
        if not isinstance(self.priority, Priority):
            raise ValueError("Priority must be a Priority enum value")

        # Validate and clean tags
        if not isinstance(self.tags, list):
            raise ValueError("Tags must be a list")

        cleaned_tags = []
        for tag in self.tags:
            if not isinstance(tag, str):
                raise ValueError("Each tag must be a string")
            tag = tag.strip()
            if tag and tag not in cleaned_tags:  # Non-empty and unique
                cleaned_tags.append(tag)
        self.tags = cleaned_tags
