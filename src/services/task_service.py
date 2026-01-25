"""Task service providing business logic for todo operations."""

from typing import Dict, List, Optional

from src.models.task import Task, Priority
from src.utils.logger import get_logger

logger = get_logger(__name__)


class TaskService:
    """Service for managing tasks in memory.

    Provides CRUD operations, search, filter, and sort functionality.
    """

    def __init__(self) -> None:
        """Initialize the task service with empty storage."""
        self._tasks: Dict[int, Task] = {}
        self._next_id: int = 1

    def create_task(
        self,
        title: str,
        priority: Priority = Priority.MEDIUM,
        tags: Optional[List[str]] = None
    ) -> Task:
        """Create a new task.

        Args:
            title: Task title (non-empty)
            priority: Task priority level
            tags: Optional list of tags

        Returns:
            The created task

        Raises:
            ValueError: If title is empty
        """
        task = Task(
            id=self._next_id,
            title=title,
            priority=priority,
            tags=tags or []
        )
        self._tasks[task.id] = task
        self._next_id += 1
        logger.info(f"Created task #{task.id}: {task.title}")
        return task

    def get_task(self, task_id: int) -> Optional[Task]:
        """Get a task by ID.

        Args:
            task_id: The task ID

        Returns:
            The task if found, None otherwise
        """
        return self._tasks.get(task_id)

    def list_tasks(self) -> List[Task]:
        """Get all tasks.

        Returns:
            List of all tasks in creation order
        """
        return list(self._tasks.values())

    def update_task(
        self,
        task_id: int,
        title: Optional[str] = None,
        priority: Optional[Priority] = None
    ) -> Optional[Task]:
        """Update a task's title and/or priority.

        Args:
            task_id: The task ID
            title: New title (if provided)
            priority: New priority (if provided)

        Returns:
            The updated task if found, None otherwise

        Raises:
            ValueError: If title is empty
        """
        task = self._tasks.get(task_id)
        if task is None:
            return None

        if title is not None:
            title = title.strip()
            if not title:
                raise ValueError("Title cannot be empty")
            task.title = title

        if priority is not None:
            task.priority = priority

        logger.info(f"Updated task #{task_id}")
        return task

    def delete_task(self, task_id: int) -> Optional[Task]:
        """Delete a task.

        Args:
            task_id: The task ID

        Returns:
            The deleted task if found, None otherwise
        """
        task = self._tasks.pop(task_id, None)
        if task:
            logger.info(f"Deleted task #{task_id}: {task.title}")
        return task

    def complete_task(self, task_id: int) -> Optional[Task]:
        """Mark a task as complete.

        Args:
            task_id: The task ID

        Returns:
            The task if found, None otherwise
        """
        task = self._tasks.get(task_id)
        if task:
            task.completed = True
            logger.info(f"Completed task #{task_id}")
        return task

    def uncomplete_task(self, task_id: int) -> Optional[Task]:
        """Mark a task as incomplete.

        Args:
            task_id: The task ID

        Returns:
            The task if found, None otherwise
        """
        task = self._tasks.get(task_id)
        if task:
            task.completed = False
            logger.info(f"Marked task #{task_id} as incomplete")
        return task

    def add_tag(self, task_id: int, tag: str) -> Optional[Task]:
        """Add a tag to a task.

        Args:
            task_id: The task ID
            tag: Tag to add

        Returns:
            The task if found, None otherwise

        Raises:
            ValueError: If tag is empty
        """
        tag = tag.strip()
        if not tag:
            raise ValueError("Tag cannot be empty")

        task = self._tasks.get(task_id)
        if task and tag not in task.tags:
            task.tags.append(tag)
            logger.info(f"Added tag '{tag}' to task #{task_id}")
        return task

    def remove_tag(self, task_id: int, tag: str) -> Optional[Task]:
        """Remove a tag from a task.

        Args:
            task_id: The task ID
            tag: Tag to remove

        Returns:
            The task if found, None otherwise
        """
        task = self._tasks.get(task_id)
        if task and tag in task.tags:
            task.tags.remove(tag)
            logger.info(f"Removed tag '{tag}' from task #{task_id}")
        return task

    def search_tasks(self, keyword: str) -> List[Task]:
        """Search tasks by keyword (case-insensitive).

        Args:
            keyword: Search term

        Returns:
            List of matching tasks
        """
        if not keyword:
            return self.list_tasks()

        keyword_lower = keyword.lower()
        return [
            task for task in self._tasks.values()
            if keyword_lower in task.title.lower()
        ]

    def filter_tasks(
        self,
        status: Optional[str] = None,
        priority: Optional[Priority] = None,
        tag: Optional[str] = None
    ) -> List[Task]:
        """Filter tasks by criteria (AND logic).

        Args:
            status: "complete" or "incomplete"
            priority: Priority level
            tag: Tag to filter by

        Returns:
            List of matching tasks
        """
        results = self._tasks.values()

        if status is not None:
            is_complete = status.lower() == "complete"
            results = (t for t in results if t.completed == is_complete)

        if priority is not None:
            results = (t for t in results if t.priority == priority)

        if tag is not None:
            results = (t for t in results if tag in t.tags)

        return list(results)

    def sort_tasks(
        self,
        tasks: List[Task],
        sort_by: str = "id"
    ) -> List[Task]:
        """Sort tasks by criteria.

        Args:
            tasks: List of tasks to sort
            sort_by: "priority", "alpha", or "id"

        Returns:
            Sorted list of tasks
        """
        if sort_by == "priority":
            return sorted(tasks, key=lambda t: t.priority.value)
        elif sort_by == "alpha":
            return sorted(tasks, key=lambda t: t.title.lower())
        else:  # Default: by id
            return sorted(tasks, key=lambda t: t.id)
